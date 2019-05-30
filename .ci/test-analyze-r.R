
library(R6)

# test package stored in integration_tests/test-packages
TEST_PACKAGE <- "testpkguno"
TESTING_DIR <- tempdir()
ANALYZE_SCRIPT <- file.path(
    getwd(), "doppel", "bin", "analyze.R"
)

TEST_VALUES <- list(
    "pkg" = TEST_PACKAGE,
    "output_dir" = TESTING_DIR,
    "kwargs_string" = "~~KWARGS~~",
    "constructor_string" = "~~CONSTRUCTOR~~"
)

# override argparse:::Parser
MockParser <- R6::R6Class(
    "MockParser",
    public = list(
        initialize = function(...){
            return(invisible(NULL))
        },
        parse_args = function(...){
            print("returning mocked values")
            return(TEST_VALUES)
        },
        add_argument = function(...){
            return(invisible(NULL))
        }
    )
)

utils::assignInNamespace(
    x = "Parser"
    , value = MockParser
    , ns = "argparse"
)

x <- tryCatch({
   sys.source(
       ANALYZE_SCRIPT
       , envir = .GlobalEnv
   )
}, error = function(e){
    return(NULL)
})

.analyze(
    args = argparse::ArgumentParser()$parse_args()
)
