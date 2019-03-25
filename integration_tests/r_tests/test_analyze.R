
# integration tests on doppel-describe commandline entrypoint
# (targeting an R package)
library(jsonlite)
library(testthat)

# Set up test data
PACKAGE_NAME <- 'testpkguno'
TEST_DATA_DIR <- tools::file_path_as_absolute("../../test_data")

# TL;DR R doesn't care about your bash PATH so finding conda stuff is
# hard. Passing in the direct path to doppel-describe through the environment
DOPPEL_DESCRIBE_LOC <- Sys.getenv("DOPPEL_DESCRIBE_LOC")
if (DOPPEL_DESCRIBE_LOC == ""){
    stop("You did not set environment variable DOPPEL_DESCRIBE_LOC")
}

cmd <- paste0(
    DOPPEL_DESCRIBE_LOC,
    " --language r -p ",
    PACKAGE_NAME,
    " --data-dir ",
    TEST_DATA_DIR
)

exit_code <- system(
    command = cmd
    , wait = TRUE
)

if (exit_code != 0){
    stop("Running doppel-describe failed")
}

OUTPUT_FILE <- paste0("r_", PACKAGE_NAME, ".json")
PATH_TO_OUTPUT_FILE <- file.path(
    TEST_DATA_DIR
    , OUTPUT_FILE
)

RESULT_JSON <- jsonlite::fromJSON(
    PATH_TO_OUTPUT_FILE
    , simplifyVector = TRUE
)

# Small function to take a super long string formatted
# similar to a Python docstring and strip all the whitespace
# generated
.docstring <- function(txt){
    txt <- gsub('\n', '', txt)
    txt <- gsub('\\s+', ' ', txt)
    txt <- trimws(txt)
    return(txt)
}


# Tests that check that basic truths about the
# JSON file produced by doppel-describe remain
# true.
context("Basic contract")

test_that("The JSON file produce by doppel-describe should have only the expected top-level dictionary keys", {

    expect_named(
        RESULT_JSON
        , c("name", "language", "functions", "classes")
        , ignore.order = TRUE
        , ignore.case = FALSE
    )
    expect_equal(length(RESULT_JSON), 4)

})

test_that("'name' should be a string", {
    expect_is(RESULT_JSON[["name"]], "character")
})

test_that("'language' should be 'r'", {
    expect_equal(RESULT_JSON[["language"]], "r")
})

txt <- .docstring(
    "
    'functions' should be a dictionary key by function name. Each
    function should have a dictionary keyed by 'args' where 'args'
    holds an array of strings.

    Nothing other than 'args' should be included in the function
    interface.
    "
)

test_that(txt, {

    func_block <- RESULT_JSON[["functions"]]

    func_names <- names(func_block)
    for (func_name in func_names){
        func_interface <- func_block[[func_name]]

        expect_named(
            func_interface
            , "args"
            , ignore.order = TRUE
            , ignore.case = FALSE
        )

        args <- func_interface[["args"]]
        if (length(args) > 0){
            expect_true(is.character(args))
        }
    }

})

txt <- .docstring(
    "
    'classes' should be a dictionary keyed
    by class name. Each of those classes should
    have a single section called 'public_methods'.
    Each method should have a dictionary keyed
    by 'args' where 'args' holds an array of strings.

    Nothing other than 'args' should be included in the
    method interface and nothing other than 'public_methods'
    should be included in the class interface.
    "
)
test_that(txt, {

    class_block <- RESULT_JSON[['classes']]

    class_names <- names(class_block)
    for (class_name in class_names){
        class_interface <- class_block[[class_name]]

        expect_named(
            class_interface
            , "public_methods"
            , ignore.order = TRUE
            , ignore.case = FALSE
        )

        method_names <- names(class_interface[["public_methods"]])

        for (method_name in method_names){
            method_interface <- class_interface[["public_methods"]][[method_name]]
            args <- method_interface[["args"]]
            if (length(args) > 0){
                expect_true(is.character(args))
            }
        }
    }

})

context("function block")

txt <- .docstring(
    "
    Exported functions should all be found,
    even if decorators are used on them.

    No other stuff should end up in 'functions'.
    "
)
test_that(txt, {

    func_block <- RESULT_JSON[['functions']]

    expect_named(
        func_block
        , c("function_a", "function_b", "function_c")
        , ignore.order = TRUE
        , ignore.case = FALSE
    )

})

test_that("Functions without arguments should get an 'args' dictionary with an empty list", {
    expect_is(
        RESULT_JSON[['functions']][['function_a']][['args']]
        , 'list'
    )

    expect_equal(
        RESULT_JSON[['functions']][['function_a']][['args']]
        , list()
    )
})

test_that("Functions with a mix of actual keyword args and '...' should have correct signature", {
    expect_equal(
        RESULT_JSON[['functions']][['function_b']]
        , list(
            'args' = c('x', 'y', '~~KWARGS~~')
        )
    )
})

test_that("Functions with only '...' should have the correct signature", {
    expect_equal(
        RESULT_JSON[['functions']][['function_c']]
        , list(
            'args' = c('~~KWARGS~~')
        )
    )
})

context("class block")

test_that("Exported classes should all be found", {
    expect_named(
        RESULT_JSON[['classes']]
        , c('ClassA', 'ClassB', 'ClassC', 'ClassD')
        , ignore.order = TRUE
        , ignore.case = FALSE
    )
})

txt <- .docstring(
    "
    Public class methods of all exported classes
    should be found.

    No other stuff should end up underneath classes
    within 'classes'.
    "
)
test_that(txt, {

    class_block <- RESULT_JSON[["classes"]]

    expected_methods <- c(
        '~~CONSTRUCTOR~~',
        'anarchy',
        'banarchy',
        'canarchy'
    )

    expect_named(
        RESULT_JSON[["classes"]][["ClassA"]][["public_methods"]]
        , expected_methods
        , ignore.order = TRUE
        , ignore.case = FALSE
    )
})


txt <- .docstring(
    "
    Public methods documented in the API of exported
    classes should include methods which are defined
    by a parent object and not overwritten by the
    child.

    No other stuff should end up underneath classes
    within 'classes'.
    "
)
test_that(txt, {

    class_block <- RESULT_JSON[["classes"]]

    expected_methods <- c(
        '~~CONSTRUCTOR~~',
        'anarchy',
        'banarchy',
        'canarchy',
        'hello_there'
    )

    expect_named(
        RESULT_JSON[["classes"]][["ClassB"]][["public_methods"]]
        , expected_methods
        , ignore.order = TRUE
        , ignore.case = FALSE
    )

})

txt <- .docstring(
    "
    Class methods should be correctly found and
    documented alongside other public methods in
    a class
    "
)
test_that(txt, {
    expect_named(
        RESULT_JSON[["classes"]][["ClassC"]][["public_methods"]]
        , c("~~CONSTRUCTOR~~", "from_string")
        , ignore.order = TRUE
        , ignore.case = FALSE
    )
})

txt <- .docstring(
    "
    Class methods inherited from a parent class should be correctly found
    and documented alongside other public methods in a class
    "
)
test_that(txt, {
    testthat::skip("This test does not apply to R6 classes. You cannot inherit class methods in R6.")
})

test_that("analyze.R should ignore R6-specific public methods like print()", {
    expect_named(
        RESULT_JSON[["classes"]][["ClassD"]][["public_methods"]]
        , c("~~CONSTRUCTOR~~")
        , ignore.order = TRUE
        , ignore.case = FALSE
    )
})
