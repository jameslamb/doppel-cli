
#' @name SomeClass
#' @title SomeClass
#' @description SomeClass
#' @importFrom R6 R6Class
#' @export
SomeClass <- R6::R6Class(
    "SomeClass",
    public = list(
        initialize = function(){
            return(invisible(NULL))
        },
        some_method = function(x){
            return(x + 5)
        }
    )
)
