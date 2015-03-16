# [Kaggle: Using Telemetric Driving Data to Build Driver Profiles](https://www.kaggle.com/c/axa-driver-telematics-analysis)
# *Frank Ix*

## Problem Statement and Hypothesis

Kaggle provided data for 3612 drivers: 200 files, each representing one drive. Drives were measured by plotting x and y coordinates each second of the trip. However, this geo-data was stripped of all mapping characteristics: the trips were rotated randomly on between 0 and 360 degrees, short chunks of trips were randomly taken out, and entirely random trips were included into a driver's folder. This prevents competitors from trip matching, i.e. figuring out a driver's actual location and normal trips, and requires focusing on more basic features such as speed and overall distance.

The basic requirement of the competition was to predict the random drives inserted into each driver's folder by building a profile for that driver and seeing which drives do not fit into that profile. My hypothesis was that basic features should produce a small number of outliers for each driver, and those outliers likely to be the random drives inserted into driver files.

## Data Overview

While the data was provided by the competition and outside data iwas not allowed, the data set was very large. As stated, it contained data for 3612 drivers (each in its own folder) and 200 drives per driver. Building a generalizeable model for all drivers will be challenging, as will processing all of this modeling work for each driver.

## Pre-processing Steps

The pre-processing steps took more time for me to complete than the rest of my processing steps combined.These steps including creating loops to go through each folder, and each file within those folders, to create my features and run models for each driver. I then had to combine this data into a master data file for submission.

## Data Exploration and Feature Creation

After doing the pre-processing work, I was then able to explore the data and experiment with feature creation. I started by creating a *Total Trip Distance* feature (EucDistance) to get a basic understanding of the trip profiles for Driver 1. This was derived by looping through each second of the trip to find the distance between each second's location and summing the distances over the whole trip. I used standard devations to derive z-scores for this feature to normalize the data, and the data looked like what I expected: some long trips, some short trips, but no major outliers or things to further to investigate. I used these trip distances to create two more features: *Average Speed per Trip* (in MPH), and *Max Speed per Trip* (in MPH). Using z-scores for these features provided more interesting characteristics: for many drivers, there were trip instances with Max Speeds over 1000mph. Initially, this was an exciting discovery as I thought I had uncovered the key to finding random trips, but it seemed that these actually represented errors in the drivers' GPS units, and they should be treated as such in the data. I wasn't sure whether to keep these outliers in, or to wash them out, because in theory the GPS errors could be telling as to who was driving (someone different that doesn't know how to work the unit), or where they were driving (somewhere out of the GPS's range), and that my be evidence for a fake driver still. In the end, I decided to take out the outliers by replacing there values with a z-score of 0. Deleting the outliers altogether would have screwed up my submission file.

By reading the forums on Kaggle, I could tell that many competitors were using between 50-200 advanced features, but I decided to stick with the three I created as a starting point, and then would add additional features in if I had time.

## Modeling Process

My first step was to create initial probablities using z-scores from my features to submit a first file to complete the process from beginning to end. For example, if the *Total Trip Distance* z-score was 6, the probability for whether that was Driver 1 was near 0. This would be used for my score for my submission after looping through all files and folders. However, while this process helped me towards completing a submission file, it took me a long time and could still not complete the process.

After a week or two of working on completing the full process, I switched gears back towards building a more suitable model. As my data was unlabeled but required predictions, my initial inclination was to use K-Means clustering for each driver to find clusters of typical drives and potential outliers. After building this model for Driver 1, it became clear that the process of building generalizable code to calculate unique clusters for 3612 drivers would be both difficult and computationally expensive.

In order to use more simple models to create predicted values, I would need labeled data. To do this, I  created dataframes with features for each driver and the next driver in the loop, with an additional column "Driver_1", which was given a 1 if it was Driver 1 (or the main driver being analyzed), and a 0 if it wasn't (i.e. it was the next driver in the loop). Using and 80/20 train-test split, I was then able to predict values for that individual driver, for each driver in the loop.


## Challenges and Successes

This competition was both frusterating and rewarding. When I signed up to do a Kaggle, it was mostly because I knew the data collection process would be simple, and the modeling problem would be complex and interesting. However, I underestimated how much data manipulation would be required to get the data in the right format to analyze it, and then a different format to submit it. This ended up taking up way more of my time than I expected. Given how complicated this was, I was also surprised that there wasn't more discussion of these challenges on the Kaggle forums, but there wasn't. While this, at times, was frusterating, it also provided me a crash course in using python for data manipulation, and in data structures, all of which will be useful for me going forward.

Given that I had less time than I would have liked to explore the final data with different models, I also found the modeling to be a challenge. Creating training data was especially difficult and I never really fully understood how my structure was helping me predict driver values (maybe it wasn't). I would have like to have tried Niave Bayes and Random Forest/Decision Trees (and possibly an ensemble of all three) had I had time and was able to submit each model for accuracy scores.

## Next Steps

My final step is to finalize my run of my logistic model and submit it before the Kaggle deadline to see what my score is. I believe that my score will fall between 60-80%, making it a very average model based on other people's log model scores. After the competition is closed, I plan to review winning strategies on the forums to better understand people's approach to tackling this complext problem. I also plan to continue competing in Kaggle competitions- I'm sure that no matter how experienced you are as a data scientist, these competitions force you to learn a lot of new things every time you compete in them. Also, now that class is over, I'm sure that my skills may atrophy unless I continue to use python and stay current with different modeling options and techniques.

## Conclusions and key learnings

While in some sense I feel like I failed the Kaggle competition by not being able to submit and review submissions earlier, I still learned a massive amount about python, data structures, and modeling techniques. One of the major breakthroughs for me was that even though my data was unlabeled initially, that did not mean that all modeling techniques were not options to me. Understanding that I could break through the basic guidelines of model evaluation if necessary was a novel concept that will serve me well moving forward. Choosing one model over another will not catapult me to the top of a Kaggle leaderboard; instead, understanding and manipulating my data is key to building better models.