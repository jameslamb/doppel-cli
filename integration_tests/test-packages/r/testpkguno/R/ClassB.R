
#' @title ClassB
#' @name ClassB
#' @description This is ClassB
#' @importFrom R6 R6Class
#' @export
ClassB <- R6::R6Class(
    classname = "ClassB",
    inherit = ClassA,

    public = list(

        initialize = function(...) {
            return(invisible(NULL))
        },

        # Overwriting one method from ClassA to
        # test that ordering of inheritance is
        # respected
        banarchy = function(nonsense = TRUE) {
            return(nonsense)
        },

        hello_there = function(greeting) {
            return(invisible(NULL))
        }

    )
)

# Adding an internal class to be sure tests catch
# these suddenly getting picked up by analyze.py
.SomeInternalClass <- R6::R6Class(
    classname = "SomeInternalClass",
    public = list(
        x = NULL,
        initialize = function(x) {
            self[["x"]] <- x
            return(invisible(NULL))
        }
    )
)
