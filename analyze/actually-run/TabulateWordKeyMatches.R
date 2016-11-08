

#########################
##Tabulate Co-Occurances
#########################

#Try to tabulate by tweet, then sum
system.time({
  
  no_cores <- detectCores() - 1
  cl <- makeCluster(no_cores)
  registerDoParallel(cl)
  
  wordsel <- make.names(gsub('@', 'AT', gsub('#', 'HSH', words)))
  
  out <- foreach(id=wordsdf$id_str[1:5000]) %dopar%{
    
    keys_bin <- keysdf[keysdf$id_str==id, keys$V1]
    words_bin <- wordsdf[wordsdf$id_str==id, wordsel]
    sapply(words_bin, '&', keys_bin)
    
  }
  
  tabulation <- Reduce('+', out)
  
  colnames(tabulation) <- wordsel
  rownames(tabulation) <- keys$V1
  
  #Get margin totals too!
  
  stopCluster(cl)
  
})


jointCount <- function(vec1, vec2){
  
}


#Try to mergeDfs, then tabulate all
system.time({
  
  no_cores <- detectCores() - 1
  cl <- makeCluster(no_cores)
  registerDoParallel(cl)
  
  wordsel <- make.names(gsub('@', 'AT', gsub('#', 'HSH', words)))
  
  mergedf <- merge(keysdf, wordsdf, by='id_str')
  
  out <- foreach(id=wordsdf$id_str[1:50]) %dopar%{
    
    keys_bin <- keysdf[keysdf$id_str==id, keys$V1]
    words_bin <- wordsdf[wordsdf$id_str==id, wordsel]
    sapply(words_bin, '&', keys_bin)
    
  }
  
  stopCluster(cl)
  
})