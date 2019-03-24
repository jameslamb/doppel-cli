
#' @title ClassB
#' @name ClassB
#' @description This is ClassB
#' @importFrom R6 R6Class
#' @export
ClassB <- R6::R6Class(
    classname = "ClassB",

    public = list(

        initialize = function(...){
            return(invisible(NULL))
        }

    )
)

ClassB$from_string <- function(the_string){
    return(ClassB$new(the_string))
}
