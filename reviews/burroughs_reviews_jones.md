Hey Kerry.  I really like your project and the write up!  Very well put together and informative, particarly the codebook part.

Here are some suggestions:
* Have you tried using different sets of features in the models? 
* I noticed that some of the features are inherently correlated, such as free throws made per game, free throw attemps per game, and free throw percentage.  The correlation between these three thigns might affect the outcome of certain models.  
* You mention missing values in certain columns and how you handled some of them.  Have you tried more advanced imputation methods to replace the missing values?  You can do the more straightforward ones like replacing a missing value with the mean or median for that column.  You can also try the mean or median for that column segemented by another attribute, such as player type.  You can also try things like "knn" imputation where you can take the mean, median, or the exact value of the players closest to the player with a missing value.
* I think you should try other models (as you've mentioned), but that intelligent feature selection might get you a little further in predictive accuracy.

Overall, great job!