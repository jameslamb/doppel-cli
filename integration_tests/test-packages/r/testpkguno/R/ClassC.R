
#' @title ClassC
#' @name ClassC
#' @description This is ClassC
#' @importFrom R6 R6Class
#' @export
ClassC <- R6::R6Class(
    classname = "ClassC",
    public = list(
        initialize = function(...){
            return(invisible(NULL))
        }
    )
)

ClassC$from_string <- function(the_string){
    return(ClassC$new(the_string))
}
