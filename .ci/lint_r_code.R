
library(argparse)
library(lintr)

parser <- argparse::ArgumentParser()
parser$add_argument(
    "--file"
    , type = "character"
    , help = "Single .R file to lint"
)
args <- parser$parse_args()

FILE_TO_LINT <- args[["file"]]

LINTERS_TO_USE <-list(
    "unused" = lintr::object_usage_linter
    , "open_curly" = lintr::open_curly_linter
    , "closed_curly" = lintr::closed_curly_linter
    , "T_F" = lintr::T_and_F_symbol_linter
    , "tabz" = lintr::no_tab_linter
    , "paths" = lintr::nonportable_path_linter
    , "spaces" = lintr::infix_spaces_linter
    , "trailing_blank" = lintr::trailing_blank_lines_linter
    , "trailing_white" = lintr::trailing_whitespace_linter
)

result <- lintr::lint(
    filename = FILE_TO_LINT
    , linters = LINTERS_TO_USE
    , cache = FALSE
)

cat(sprintf(
    "Found %i linting errors in %s\n"
    , length(result)
    , FILE_TO_LINT
))

if (length(result) > 0){
    cat("\n")
    print(result)
}

quit(save = "no", status = length(result))
