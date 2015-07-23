Hey David.  I really like your project!  You've written some very nice (and sufficiently complicated) code!

Here are a specific things I noticed when looking through your repo:
* We talked about it Sunday, but using UNION ALL to combine multiple queries from different tables.  The key here is that each query must return the same number of columns.  Since it literally just puts each successive query result below the first, make sure your columns line up (it will not do this for you; you must do it manually).  So if you have the columns "name", "address", "phone number" in the first result set, you need to have the columns "name", "address", "phone number", in that order, in the second result set.  Unfortunately, since it only requires the two result sets to have the same number of columns, it would return a result if they are not in correct order.  This would be technically okay, but practically incorrect.  The format looks like this:
```SQL 
SELECT <column_1>, <column_2>, ..., <column_n>
FROM table_1
WHERE <conditions>
UNION ALL
SELECT <column_1>, <column_2>, ..., <column_n>
FROM table_2
WHERE <conditions>
UNION ALL
SELECT <column_1>, <column_2>, ..., <column_n>
FROM table_3
WHERE <conditions>
```
* In a few of the files (DAT4_library: ```class connect_DB```: function ```connect```, for example), I notice you import libraries right before you use them within the function itself.  The convention is to import all libraries used at the top of the file (I like to write them in order of appearance).  While some of this is convention, there is also some logic to it.  By writing the ```import``` in a function, you are importing the library every time you call that function.  While it will probably work, it's extra overhead that is uncessary, especially for functions that are called often.  If you import these files at the top of your code, they'll be loaded for use whenever you call the library functions within your self defined function.
* We talked about things you do for prediction, like predicting whether a loan is approved or not and what factors most play into that approvial process.
* I like your plots, very nice.

I don't have much else to add at the moment.  It's a good project.  As usual, feel free to Slack me if you have any questions about anything!