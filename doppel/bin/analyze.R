#!/usr/bin/env Rscript

library(argparse)
library(futile.logger)
library(jsonlite)
library(R6)

parser <- argparse::ArgumentParser()
parser$add_argument(
    "--pkg"
    , type = "character"
    , help = "Name of the R package to test"
)
parser$add_argument(
   "--output_dir"
   , type = "character"
   , default = getwd()
   , help = "Path to write files to"
)
parser$add_argument(
   "--kwargs-string"
   , type = "character"
   , help = "String value to replace **kwarg"
)

# Grab args (store in constants for easier debugging)
args <- parser$parse_args()
PKG_NAME <- args[["pkg"]]
OUT_DIR <- args[["output_dir"]]
KWARGS_STRING <- args[["kwargs_string"]]
LANGUAGE <- 'r'

# lil helper
.log_info <- function(msg){
    futile.logger::flog.info(msg)
    return(invisible(NULL))
}

# grab just the exported objects
.log_info(sprintf("Loading up namespace for package %s", PKG_NAME))
pkg_env <- loadNamespace(PKG_NAME)
export_names <- names(pkg_env[[".__NAMESPACE__."]][["exports"]])
.log_info(sprintf("Found %i exported objects", length(export_names)))

# Set up skeleton thing
# TODO: handle stuff that isn't just functions or R6 classes
# TODO: figure out how to handle S3Methods
# TODO: figure out and document how to handle Python magic methods
out <- list(
    "name" = paste0(PKG_NAME, ' [r]')
    , "language" = 'r'
    , "functions" = list()
    , "classes" = list()
)

for (obj_name in export_names){
    obj <- get(obj_name, envir = pkg_env)

    if (is.function(obj)){
        out[["functions"]][[obj_name]] <- list(
            "args" = gsub(
                "\\.\\.\\."
                , KWARGS_STRING
                , names(formals(obj))
            )
        )
        next
    }

    if (R6::is.R6Class(obj)){
        out[["classes"]][[obj_name]] <- list()
        next
    }
}

# jsonlite treates mpty, unnamed lists as arrays, we want to write empty dicts
for (obj_type in c("functions", "classes")){
    if (identical(out[[obj_type]], list())){
        lst <- list()
        names(lst) <- character(0)
        out[[obj_type]] <- lst
    }
}

# write it out
out_file <- file.path(OUT_DIR, sprintf("%s_%s.json", LANGUAGE, PKG_NAME))
.log_info(sprintf("Writing output to %s", out_file))
write(x = jsonlite::toJSON(out, auto_unbox = TRUE), file = out_file, append = FALSE)
.log_info("Done analyzing this package.")
