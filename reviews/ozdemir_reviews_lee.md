## Ozdemir Reviews Lee
### Sinan Ozdemir

#### Preliminary thoughts
I think this is a very intereting idea. Obviously predicting stock movement is in an of itself is interesting but training a model based on visual data makes it even more so.

####Predictors
I am having trouble understanding the exact predictors you are using that you are "Generating" from the visual image. Are you using the price itself at all or purely visual predictors. It might be beneficial to list out the exact predictors, such as I am looking at slope of the graph, height of the graph, second derivative, etc, etc


####Suggestions
1. I might look into a multi procesing loop that preforms that long for loop (in line 170) of your code to make it run a bit faster.
2. As far as the space issue that we discussed in class, storing image data like this is inherently space ineffeicent.. so perhaps just storing the predictors and metrics might be an option?
3. opencv has many options for dealing with images, perhaps you can look at percentages of colors, hues as a predictor? There is also contour detection that might help quantify the images in the image.

As always, please feel free to reach out if you have any questions.