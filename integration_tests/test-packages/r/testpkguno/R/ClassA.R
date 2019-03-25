
#' @title ClassA
#' @name ClassA
#' @description This is ClassA
#' @importFrom R6 R6Class
#' @export
ClassA <- R6::R6Class(
    classname = "ClassA",
    public = list(

        story1 = TRUE,
        story2 = 5,
        story3 = "hello",

        initialize = function(x, y, z){
            return(invisible(NULL))
        },

        anarchy = function(...){
            return(invisible(NULL))
        },

        banarchy = function(thing_1, thing_2, yes){
            return(invisible(NULL))
        },

        canarchy = function(x, y, ...){
            return(invisible(NULL))
        }
    ),

    active = list(

        number_four = function(){
            return(4)
        }

    ),

    private = list(

        acclimate = function(...){
            return(invisible(NULL))
        },

        backlimate = function(stuff = TRUE, ...){
            return(invisible(NULL))
        },

        secret1 = TRUE,
        secret2 = 5,
        secret3 = "hello"

    )
)
