###General
* Explaining code block functions was well done and made code sections of the iPython notebook understandable on a conceptual level
* Making use of in-line comments would help make the code easier to read and understand on a line by line level
* Using += on strings was really cool to see.

###Introduction
* What are the highlights of the controversy surrounding the use of patents as a measure of innovation?
* What other measures have been or can be used?

###Data Cleaning
* Explanations of why some steps were taken would be helpful.
    For example: Why did you strip the first three charaters in order to extrat the classification category title?
* Filter patent data to only include names of firms from Crunchbase will increase the relevance of data exploration.

###Data Exploration
* Noting any take-aways with comments in the data exploration phase would help build a project narrative and give insight into what you think are important aspects in the data
heads and tails show that the patents data set is fairly skewed toward large tech firms
* I am unsure what the axes are on the graph on line 37 in the iPython notebook
* Visualize distribution of funding amounts, funding amonts by type (round) of funding
    Which types of funding are more common?
    Which types of funding provide more funds?
    Are certain types of funding more common for different industries?
* Is there a normal progression through funding types for startups? For example, does seed funding precede series a, b, c?
* From my limited experience, it seems that companies receive increasing amounts of funding as they progress through funding rounds. I believe this is a self-selection issue
as non-viable products fail (or fail to attract investors) and drop out of funding rounds.
* Grouping funding by type of funding or startup industry and then running .describe() would be a good way to show if funding amount is consistent by industry type or industry sector.

###Analysis
* In addition to running a linear regression, it may be informative to do a classification model to see what underlying factors predict funding/no funding.
* If a classifier is useful in predicting if a startup will get funding, then removing entries with no funding and running the linear regression on only those firms that were
funded may provide more insight into what investors value.
* Seeing that debt financing was the second most frequent type of funding is interesting because it has the implication that there is operational revenue from the business
(or a believe that revenue will be coming shortly).