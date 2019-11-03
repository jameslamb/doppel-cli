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
parser$add_argument(
   "--constructor-string"
   , type = "character"
   , help = "String value to replace the constructor in the list of class public methods"
)

# Grab args (store in constants for easier debugging)
args <- parser$parse_args()

# Wrap the entire pipeline in a function so it can be tested
.analyze <- function(args) {

    PKG_NAME <- args[["pkg"]]
    OUT_DIR <- args[["output_dir"]]
    KWARGS_STRING <- args[["kwargs_string"]]
    CONSTRUCTOR_STRING <- args[["constructor_string"]]

    LANGUAGE <- "r"
    R6_SPECIAL_METHODS_TO_EXCLUDE <- c(
        "clone",
        "print"
    )
    R6_CONSTRUCTOR_NAME <- "initialize"
    R6_CLASS_METHODS <- c(
        "clone_method",
        "debug",
        "get_inherit",
        "has_private",
        "is_locked",
        "lock",
        "new",
        "set",
        "undebug",
        "unlock"
    )

    # lil helper
    .log_info <- function(msg) {
        futile.logger::flog.info(msg)
        return(invisible(NULL))
    }


    # Get all public methods (handling inheritance)
    .get_r6_public_methods <- function(obj) {

        if (is.null(obj)) {
            return(list())
        }

        # Be sure the children can override their parents!
        # Looping like this means we'll REPLACE keys (since R
        # lists don't guarantee key uniqueness)
        public_methods <- .get_r6_public_methods(
            obj$get_inherit()
        )

        these_methods <- obj$public_methods
        for (method_name in names(these_methods)) {
            public_methods[[method_name]] <- these_methods[[method_name]]
        }

        return(public_methods)
    }

    # grab just the exported objects
    .log_info(sprintf("Loading up namespace for package %s", PKG_NAME))
    pkg_env <- loadNamespace(PKG_NAME)
    export_names <- names(pkg_env[[".__NAMESPACE__."]][["exports"]])
    .log_info(sprintf("Found %i exported objects", length(export_names)))

    # Set up skeleton thing
    out <- list(
        "name" = paste0(PKG_NAME, " [r]")
        , "language" = "r"
        , "functions" = list()
        , "classes" = list()
    )

    for (obj_name in export_names) {

        obj <- get(obj_name, envir = pkg_env)

        if (is.function(obj)) {
            out[["functions"]][[obj_name]] <- list(
                "args" = as.list(
                    gsub(
                        "\\.\\.\\."
                        , KWARGS_STRING
                        , names(formals(obj))
                    )
                )
            )
            next
        }

        if (R6::is.R6Class(obj)) {

            out[["classes"]][[obj_name]] <- list()
            out[["classes"]][[obj_name]][["public_methods"]] <- list()

            public_methods <- .get_r6_public_methods(obj)

            # Drop R6-specific public methods like "clone"
            methods_to_keep <- base::setdiff(
                names(public_methods)
                , R6_SPECIAL_METHODS_TO_EXCLUDE
            )
            public_methods <- public_methods[methods_to_keep]

            # If the R6 constructor ('initialize') isn't defined, an empty
            # one won't show up in the list of public methods. Need to
            # add it here to be explicit
            if (! R6_CONSTRUCTOR_NAME %in% names(public_methods)) {
                public_methods[[R6_CONSTRUCTOR_NAME]] <- function() {NULL}

                # Calling this is an annoying hack to get
                # covr to treat this if statement as covered
                public_methods[[R6_CONSTRUCTOR_NAME]]()
            }

            for (i in seq_len(length(public_methods))) {

                pm <- public_methods[[i]]
                method_name <- names(public_methods)[[i]]
                if (method_name == R6_CONSTRUCTOR_NAME) {
                    method_name <- CONSTRUCTOR_STRING
                }

                # Grab ordered list of arguments
                method_args <- suppressWarnings({
                    names(formals(pm))
                })

                if (is.null(method_args)) {
                    method_args <- list()
                }

                out[["classes"]][[obj_name]][["public_methods"]][[method_name]] <- list(
                    "args" = as.list(
                        gsub(
                            "\\.\\.\\."
                            , KWARGS_STRING
                            , method_args
                        )
                    )
                )
            }

            # Check for class methods. For now, these are just treated as
            # "public methods"
            class_methods <- Filter(
                f = function(o) {is.function(o)}
                , x = eapply(obj, function(x) {x})
            )

            # Drop class methods that ship with R6
            non_default_class_methods <- base::setdiff(
                names(class_methods)
                , R6_CLASS_METHODS
            )

            if (length(non_default_class_methods) == 0L) {
                .log_info(sprintf(
                    "No class methods found in class '%s'"
                    , obj_name
                ))
            } else {

                for (method in non_default_class_methods) {
                    # Grab ordered list of arguments
                    method_args <- suppressWarnings({
                        names(formals(get(method, obj)))
                    })

                    if (is.null(method_args)) {
                        method_args <- list()
                    }

                    out[["classes"]][[obj_name]][["public_methods"]][[method]] <- list(
                        "args" = as.list(method_args)
                    )
                }
            }
            next
        }
    }

    # jsonlite treats empty, unnamed lists as arrays, we want to write empty dicts
    for (obj_type in c("functions", "classes")) {
        if (identical(out[[obj_type]], list())) {
            lst <- list()
            names(lst) <- character(0L)
            out[[obj_type]] <- lst
        }
    }

    # write it out
    out_file <- file.path(OUT_DIR, sprintf("%s_%s.json", LANGUAGE, PKG_NAME))
    .log_info(sprintf("Writing output to %s", out_file))
    write(
        x = jsonlite::toJSON(out, auto_unbox = TRUE)
        , file = out_file
        , append = FALSE
    )
    .log_info("Done analyzing this package.")
}

.analyze(args)
