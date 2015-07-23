Hey JB.  Great job!  
* I really like the file organization here.  This is an underrated but essential skill to have as your projects grow larger and larger.
* Also, on that note, _AWESOME_ data model!  I really like the visualization there.  
* With regards to dropping the rows that had missing values, you should think about imputing new values there.  This could be that you replace the missing value with the mean of that column.  For instance, if the "age" column is missing a value for a particular row, you could replace the missing values with the mean age for that entire column.  You could also use the median, a max, min, etc.  There are a lot of different ideas on how to replace missing values.  We can talk more about it in person some time, though this covers the major idea.
* You mentioned using logistic regression first and then multiple linear regression.  I think you meant this, but just to be clear,
    * Logistic regression is a classification method.  It is used to predict a '1' or '0'.  It predicts something either works or doesn't work, yes or no, etc...
    * Linear regression is a regression method.  It is used to predict a continuous range of values.  You could try to predict income (a continuous range of values), number of widgets produced, number of students that take a class, etc.
    * You can have a multiple logistic regression or a multiple linear regression, one predicts classes, one predicts a range of continuous values.
* The data munging scripts are all really good too.

Great job with everything.  Let me know if you need any help when it comes to constructing the models.  Feel free to Slcak me anytime.