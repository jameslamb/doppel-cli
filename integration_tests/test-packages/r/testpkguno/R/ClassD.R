
#' @title ClassD
#' @name ClassD
#' @description This is ClassD
#' @importFrom R6 R6Class
#' @export
ClassD <- R6::R6Class(
    classname = "ClassD",
    inherit = ClassC,
    public = list(
        #' @field x x
        x = NULL,

        #' @description create a ClassD
        #' @param x x
        initialize = function(x) {
            self[["x"]] <- x
            return(invisible(NULL))
        },

        #' @description print a ClassD instance
        print = function() {
            return(invisible(NULL))
        }
    )
)

# You can't do inheritance of class methods in R6, so
# have to do this here (it's inherited in the Python package)
ClassD$from_string <- function(the_string) {
    return(ClassD$new(the_string))
}
