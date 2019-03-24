
# Lint all R files in
# a directory and all it's sub-directories

library(argparse)
library(lintr)

parser <- argparse::ArgumentParser()
parser$add_argument(
    "--source-dir"
    , type = "character"
    , help = "Fully-qualified directory to search for R files"
)
args <- parser$parse_args()

SOURCE_DIR <- args[["source_dir"]]

FILES_TO_LINT <- list.files(
    path = SOURCE_DIR
    , pattern = "\\.r$"
    , all.files = TRUE
    , ignore.case = TRUE
    , full.names = TRUE
    , recursive = TRUE
    , include.dirs = FALSE
)

LINTERS_TO_USE <- list(
    "unused" = lintr::object_usage_linter
    , "open_curly" = lintr::open_curly_linter
    , "closed_curly" = lintr::closed_curly_linter
    , "tabz" = lintr::no_tab_linter
    , "spaces" = lintr::infix_spaces_linter
    , "trailing_blank" = lintr::trailing_blank_lines_linter
    , "trailing_white" = lintr::trailing_whitespace_linter
)

cat(sprintf("Found %i R files to lint\n", length(FILES_TO_LINT)))

results <- c()

for (r_file in FILES_TO_LINT){

    this_result <- lintr::lint(
        filename = r_file
        , linters = LINTERS_TO_USE
        , cache = FALSE
    )

    cat(sprintf(
        "Found %i linting errors in %s\n"
        , length(this_result)
        , r_file
    ))

    results <- c(results, this_result)

}

issues_found <- length(results)

if (issues_found > 0){
    cat("\n")
    print(results)
}

quit(save = "no", status = issues_found)
