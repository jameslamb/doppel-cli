
library(argparse)
library(R6)

# test package stored in integration_tests/test-packages
TEST_PACKAGES <- c(
    "testpkguno"
    , "testpkgdos"
)
TESTING_DIR <- tempdir()
ANALYZE_SCRIPT <- file.path(
    getwd(), "doppel", "bin", "analyze.R"
)

for (TEST_PACKAGE in TEST_PACKAGES) {

    # override argparse:::Parser
    MockParser <- R6::R6Class(
        "MockParser",
        public = list(
            initialize = function(...) {
                return(invisible(NULL))
            },
            parse_args = function(..., verbose = FALSE) {
                print("returning mocked values")
                out <- list(
                    "pkg" = TEST_PACKAGE
                    , "output_dir" = TESTING_DIR
                    , "kwargs_string" = "~~KWARGS~~"
                    , "constructor_string" = "~~CONSTRUCTOR~~"
                    , "verbose" = verbose
                )
                return(out)
            },
            add_argument = function(...) {
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
    }, error = function(e) {
        print(e)
        return(NULL)
    })

    .analyze(
        args = argparse::ArgumentParser()$parse_args(verbose = TRUE)
    )
    .analyze(
        args = argparse::ArgumentParser()$parse_args(verbose = FALSE)
    )
}
