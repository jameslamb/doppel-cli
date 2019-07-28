
parser <- argparse::ArgumentParser()
parser$add_argument(
    "--source-dir"
    , type = "character"
    , help = "Full path to source code of doppel-cli"
)
parser$add_argument(
    "--fail-under"
    , type = "integer"
    , help = "Integer from 0 to 100 indicating the minimum allowable code coverage"
)

# Grab args (store in constants for easier debugging)
args <- parser$parse_args()
SOURCE_DIR <- args[["source_dir"]]
FAIL_UNDER <- args[["fail_under"]]

SOURCE_FILE <- c(
    file.path(SOURCE_DIR, "doppel", "bin", "analyze.R")
)
TEST_FILE <- c(
    file.path(SOURCE_DIR, ".ci", "test-analyze-r.R")
)

# I don't know why, but calling this source before covr
# does _something_ to warm the environment in a way that
# makes the coverage magic work. This means the code in the
# analyze script gets run three times but whatever, it works.
sys.source(
    TEST_FILE
    , envir = .GlobalEnv
)

coverage <- covr::file_coverage(
    source_files = SOURCE_FILE
    , test_files = TEST_FILE
)

print(coverage)

total_coverage <- covr::percent_coverage(coverage)
print(paste0("Total coverage: ", round(total_coverage, 2), "%"))

# covr::report(coverage, 'coverage.html')

if (total_coverage < FAIL_UNDER){
    print("Coverage below threshold. Failing.")
    quit(save = "no", status = 1)
}

print("Done testing coverage of analyze.R")
