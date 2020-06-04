
#' @name SomeClass
#' @title SomeClass
#' @description SomeClass
#' @importFrom R6 R6Class
#' @export
SomeClass <- R6::R6Class(
    "SomeClass",
    public = list(

        #' @description create a SomeClass
        initialize = function() {
            return(invisible(NULL))
        },

        #' @description gr8 code
        #' @param x x
        some_method = function(x) {
            return(x + 5L)
        }
    )
)
