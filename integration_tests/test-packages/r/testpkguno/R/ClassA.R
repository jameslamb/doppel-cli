
#' @title ClassA
#' @name ClassA
#' @description This is ClassA
#' @importFrom R6 R6Class
#' @export
ClassA <- R6::R6Class(
    classname = "ClassA",
    public = list(

        #' @field story1 a story
        story1 = TRUE,

        #' @field story2 another story
        story2 = 5.0,

        #' @field story3 the third story
        story3 = "hello",

        #' @description create a ClassA
        #' @param x x
        #' @param y y
        #' @param z z
        initialize = function(x, y, z) {
            return(invisible(NULL))
        },

        #' @description anarchy
        #' @param ... dotz
        anarchy = function(...) {
            return(invisible(NULL))
        },

        #' @description banarchy
        #' @param thing_1 thing_1
        #' @param thing_2 thing_2
        #' @param yes yes
        banarchy = function(thing_1, thing_2, yes) {
            return(invisible(NULL))
        },

        #' @description canarchy
        #' @param x x
        #' @param y y
        #' @param ... dotz
        canarchy = function(x, y, ...) {
            return(invisible(NULL))
        }
    ),

    active = list(

        #' @field number_four the fourth number
        number_four = function() {
            return(4L)
        }

    ),

    private = list(

        acclimate = function(...) {
            return(invisible(NULL))
        },

        backlimate = function(stuff = TRUE, ...) {
            return(invisible(NULL))
        },

        secret1 = TRUE,
        secret2 = 5.0,
        secret3 = "hello"

    )
)
