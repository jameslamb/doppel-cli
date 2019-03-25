
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
