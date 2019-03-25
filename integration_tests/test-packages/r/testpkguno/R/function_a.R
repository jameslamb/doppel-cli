
# Adding an internal function to be sure tests catch
# these suddenly getting picked up by analyze.R
.add_5 <- function(n){
    return(n + 5)
}

#' @name function_a
#' @title function_a
#' @description function_a
#' @export
function_a <- function(){
    return(rnorm(1))
}
