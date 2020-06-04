
#' @title ClassE
#' @name ClassE
#' @description This is ClassE, a class whose constructor
#'              has no keyword arguments and which has a
#'              class method with no keyword args
#' @importFrom R6 R6Class
#' @export
ClassE <- R6::R6Class(
    classname = "ClassE",
    public = list(
        #' @description create a ClassE
        initialize = function() {
            return(invisible(NULL))
        }
    )
)

ClassE$from_string <- function() {
    return(ClassE$new())
}
