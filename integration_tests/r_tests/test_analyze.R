
# integration tests on doppel-describe commandline entrypoint
# (targeting an R package)
library(jsonlite)
library(testthat)

# details that will always be true of doppel-describe output
TOP_LEVEL_KEYS <- c("name", "language", "functions", "classes")
NUM_TOP_LEVEL_KEYS <- length(TOP_LEVEL_KEYS)

# Set up test data
TEST_PACKAGES <- c(
    'testpkguno'
    , 'testpkgdos'
)
TEST_DATA_DIR <- tools::file_path_as_absolute("../../test_data")

# TL;DR R doesn't care about your bash PATH so finding conda stuff is
# hard. Passing in the direct path to doppel-describe through the environment
DOPPEL_DESCRIBE_LOC <- Sys.getenv("DOPPEL_DESCRIBE_LOC")
if (DOPPEL_DESCRIBE_LOC == ""){
    stop("You did not set environment variable DOPPEL_DESCRIBE_LOC")
}

.run_doppel_describe <- function(package_name, doppel_describe_loc, test_data_dir){

    cmd <- paste0(
        doppel_describe_loc,
        " --language r -p ",
        package_name,
        " --data-dir ",
        test_data_dir
    )

    exit_code <- system(
        command = cmd
        , wait = TRUE
    )

    if (exit_code != 0){
        stop("Running doppel-describe failed")
    }

    OUTPUT_FILE <- paste0("r_", package_name, ".json")
    PATH_TO_OUTPUT_FILE <- file.path(
        test_data_dir
        , OUTPUT_FILE
    )

    # Read in the raw JSON produced by doppel-describe. Using
    # paste0() here to make sure these tests don't care about
    # whether that code pretty-prints the JSON it produces
    raw_json <- paste0(
        readLines(PATH_TO_OUTPUT_FILE)
        , collapse = ""
    )
    result_json <- jsonlite::fromJSON(
        raw_json
        , simplifyVector = TRUE
    )

    return(list(
        "raw" = raw_json
        , "parsed" = result_json
    ))
}

RESULTS <- list()
for (pkg_name in TEST_PACKAGES){
    RESULTS[[pkg_name]] <- .run_doppel_describe(
        package_name = pkg_name
        , doppel_describe_loc = DOPPEL_DESCRIBE_LOC
        , test_data_dir = TEST_DATA_DIR
    )
}

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
        RESULTS[["testpkguno"]][["parsed"]]
        , EXPECTED_TOP_LEVEL_KEYS
        , ignore.order = TRUE
        , ignore.case = FALSE
    )
    expect_equal(length(RESULTS[["testpkguno"]][["parsed"]]), NUM_TOP_LEVEL_KEYS)

})

test_that("'name' should be a string", {
    expect_is(RESULTS[["testpkguno"]][["parsed"]][["name"]], "character")
})

test_that("'language' should be 'r'", {
    expect_equal(RESULTS[["testpkguno"]][["parsed"]][["language"]], "r")
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

    func_block <- RESULTS[["testpkguno"]][["parsed"]][["functions"]]

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

    class_block <- RESULTS[["testpkguno"]][["parsed"]][['classes']]

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

    func_block <- RESULTS[["testpkguno"]][["parsed"]][['functions']]

    expect_named(
        func_block
        , c("function_a", "function_b", "function_c")
        , ignore.order = TRUE
        , ignore.case = FALSE
    )

})

test_that("Functions without arguments should get an 'args' dictionary with an empty list", {
    expect_is(
        RESULTS[["testpkguno"]][["parsed"]][['functions']][['function_a']][['args']]
        , 'list'
    )

    expect_equal(
        RESULTS[["testpkguno"]][["parsed"]][['functions']][['function_a']][['args']]
        , list()
    )
})

test_that("Functions with a mix of actual keyword args and '...' should have correct signature", {
    expect_equal(
        RESULTS[["testpkguno"]][["parsed"]][['functions']][['function_b']]
        , list(
            'args' = c('x', 'y', '~~KWARGS~~')
        )
    )
})

test_that("Functions with only '...' should have the correct signature", {
    expect_equal(
        RESULTS[["testpkguno"]][["parsed"]][['functions']][['function_c']]
        , list(
            'args' = c('~~KWARGS~~')
        )
    )
})

context("class block")

test_that("Exported classes should all be found", {
    expect_named(
        RESULTS[["testpkguno"]][["parsed"]][['classes']]
        , c('ClassA', 'ClassB', 'ClassC', 'ClassD', 'ClassE', 'ClassF')
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

    class_block <- RESULTS[["testpkguno"]][["parsed"]][["classes"]]

    expected_methods <- c(
        '~~CONSTRUCTOR~~',
        'anarchy',
        'banarchy',
        'canarchy'
    )

    expect_named(
        RESULTS[["testpkguno"]][["parsed"]][["classes"]][["ClassA"]][["public_methods"]]
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

    class_block <- RESULTS[["testpkguno"]][["parsed"]][["classes"]]

    expected_methods <- c(
        '~~CONSTRUCTOR~~',
        'anarchy',
        'banarchy',
        'canarchy',
        'hello_there'
    )

    expect_named(
        RESULTS[["testpkguno"]][["parsed"]][["classes"]][["ClassB"]][["public_methods"]]
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
        RESULTS[["testpkguno"]][["parsed"]][["classes"]][["ClassC"]][["public_methods"]]
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
        RESULTS[["testpkguno"]][["parsed"]][["classes"]][["ClassD"]][["public_methods"]]
        , c("~~CONSTRUCTOR~~", "from_string")
        , ignore.order = TRUE
        , ignore.case = FALSE
    )
})

test_that("Classes with constructors that have no keyword args should be serialized correctly", {
    expect_named(
        RESULTS[["testpkguno"]][["parsed"]][["classes"]][["ClassE"]][["public_methods"]]
        , c("~~CONSTRUCTOR~~", "from_string")
        , ignore.order = TRUE
        , ignore.case = FALSE
    )
    expect_is(RESULTS[["testpkguno"]][["parsed"]][["classes"]][["ClassE"]][["public_methods"]][["~~CONSTRUCTOR~~"]][["args"]], "list")
    expect_is(RESULTS[["testpkguno"]][["parsed"]][["classes"]][["ClassE"]][["public_methods"]][["from_string"]][["args"]], "list")

    # test that things with no kwargs produce "args": [], not "args": {}
    expect_true(isTRUE(
        grepl('.+"ClassE".+~~CONSTRUCTOR~~.+"args"\\:\\[\\]', RESULTS[["testpkguno"]][["raw"]])
    ))
    expect_true(isTRUE(
        grepl('.+"from_string".+~~CONSTRUCTOR~~.+"args"\\:\\[\\]', RESULTS[["testpkguno"]][["raw"]])
    ))
})

test_that("Totally empty classes should still have their constructors documented", {
    expect_named(
        RESULTS[["testpkguno"]][["parsed"]][["classes"]][["ClassF"]][["public_methods"]]
        , c("~~CONSTRUCTOR~~")
        , ignore.order = TRUE
        , ignore.case = FALSE
    )
    expect_named(
        RESULTS[["testpkguno"]][["parsed"]][["classes"]][["ClassF"]][["public_methods"]][["~~CONSTRUCTOR~~"]]
        , c("args")
        , ignore.order = TRUE
        , ignore.case = FALSE
    )
})

context("function-only packages")

test_that("The JSON file produce by doppel-describe should have only the expected top-level dictionary keys", {

    expect_named(
        RESULTS[["testpkgdos"]][["parsed"]]
        , EXPECTED_TOP_LEVEL_KEYS
        , ignore.order = TRUE
        , ignore.case = FALSE
    )
    expect_equal(length(RESULTS[["testpkguno"]][["parsed"]]), NUM_TOP_LEVEL_KEYS)

})
