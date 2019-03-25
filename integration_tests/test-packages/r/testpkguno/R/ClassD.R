
#' @title ClassD
#' @name ClassD
#' @description This is ClassD
#' @importFrom R6 R6Class
#' @export
ClassD <- R6::R6Class(
    classname = "ClassD",
    inherit = ClassC,
    public = list(
        x = NULL,
        initialize = function(x){
            self[["x"]] <- x
            return(invisible(NULL))
        },
        print = function(){
            return(invisible(NULL))
        }
    )
)

# You can't do inheritance of class methods in R6, so
# have to do this here (it's inherited in the Python package)
ClassD$from_string <- function(the_string){
    return(ClassD$new(the_string))
}
