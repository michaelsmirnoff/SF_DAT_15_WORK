import csv
import glob
import pandas as pd
import numpy as np
import scipy.spatial.distance as dist
import matplotlib.pyplot as plt
import os
from numpy import mean
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split

# building a data set only using the first driver's data
path ='..\dat4\drivers_data'
allFolders = glob.glob("1")
drive_list = []
prob_list = []
submission = pd.DataFrame()
overall = pd.DataFrame()
combination = pd.DataFrame()
for folder in allFolders:
    print folder
    allFiles = glob.glob(folder+"/*.csv")
    dist_sumlist = []
    mph_maxlist = []
    mph_avglist = []
    drive_number = []
    probs = []
    # create summary stats (drive length and max speed) for each drive
    for file in allFiles:
        print file
        with open(file, 'rU') as f:
            header = next(csv.reader(f))
            data = [row for row in csv.reader(f)]
            drive = pd.DataFrame(data, columns=header)
            dist_list = []
            mph_list = []
            # measuring the distance between rows and using time (one second per row) to measure speed
            for i in range(len(data)-1):
                start = np.array([float(data[i][0]), float(data[i][1])])
                end = np.array([float(data[i+1][0]), float(data[i+1][1])])
                dst = dist.euclidean(start, end) / 1609.34
                dist_list.append(dst)
                mph = dst*60*60
                mph_list.append(mph)
        # pulling out the total distance and max mph for each trip
        dist_sumlist.append(round(sum(dist_list),2))
        mph_maxlist.append(round(max(mph_list),0))
        mph_avglist.append(round(np.mean(mph_list),2))
        file_number = file.split('.')
        drive_number.append(file_number[0].replace('/','_'))
    # building a data frame using these new lists
    frame = pd.DataFrame()
    '''
    Feature 1
    '''
    # total drive distance
    frame['eucDist'] = pd.Series(dist_sumlist)
    dist_mean = round(float(frame.eucDist.mean(axis=0)),0)
    dist_stan_dev = np.std(frame.eucDist)
    dist_zscore = (frame.eucDist - dist_mean) / dist_stan_dev
    frame['eucDist_zScore'] = np.where(dist_zscore > 4, 0, dist_zscore)
    # plot average trip length zscore
    frame.eucDist_zScore.plot(kind='line', title='Driving Distances')
    plt.show()
    
    '''
    Feature 2
    '''
    # drive avg speed
    frame['mph_avg'] = mph_avglist
    avgmph_mean = round(float(frame.mph_avg.mean(axis=0)),0)
    avgmph_stan_dev = np.std(frame.mph_avg)
    avgmph_zscore = (frame.mph_avg - avgmph_mean) / avgmph_stan_dev
    frame['avgmph_zScore'] = np.where(avgmph_zscore > 4, 0, avgmph_zscore)
    # plot max speed zscore
    frame.avgmph_zScore.plot(kind='line', title='Driving Average Speeds')
    plt.show()
    
    '''
    Feature 3
    '''
    # drive max speed
    frame['max_mph'] = mph_maxlist
    mph_mean = round(float(frame.max_mph.mean(axis=0)),0)
    mph_stan_dev = np.std(frame.max_mph)
    mph_zscore = (frame.max_mph - mph_mean) / mph_stan_dev
    frame['mph_zScore'] = np.where(mph_zscore > 1, 0, mph_zscore)
    # plot max speed zscore
    frame.mph_zScore.plot(kind='line', title='Driving Max Speeds')
    plt.show()

    frame['driver_1'] = 1
    feature_df = pd.DataFrame(frame, columns=['eucDist_zScore','avgmph_zScore','mph_zScore','driver_1'])

'''
Pulling the next folder in
'''
allFolders = glob.glob("2")
for folder in allFolders:
    print folder
    allFiles = glob.glob(folder+"/*.csv")
    dist_sumlist = []
    mph_maxlist = []
    mph_avglist = []
    drive_number = []
    probs = []
    # create summary stats (drive length and max speed) for each drive
    for file in allFiles:
        print file
        with open(file, 'rU') as f:
            header = next(csv.reader(f))
            data = [row for row in csv.reader(f)]
            drive = pd.DataFrame(data, columns=header)
            dist_list = []
            mph_list = []
            # measuring the distance between rows and using time (one second per row) to measure speed
            for i in range(len(data)-1):
                start = np.array([float(data[i][0]), float(data[i][1])])
                end = np.array([float(data[i+1][0]), float(data[i+1][1])])
                dst = dist.euclidean(start, end) / 1609.34
                dist_list.append(dst)
                mph = dst*60*60
                mph_list.append(mph)
        # pulling out the total distance and max mph for each trip
        dist_sumlist.append(round(sum(dist_list),2))
        mph_maxlist.append(round(max(mph_list),0))
        mph_avglist.append(round(np.mean(mph_list),2))
        file_number = file.split('.')
        drive_number.append(file_number[0].replace('/','_'))
    # building a data frame using these new lists
    frame = pd.DataFrame()
    
    '''
    Feature 1
    '''
    # total drive distance
    frame['eucDist'] = pd.Series(dist_sumlist)
    dist_mean = round(float(frame.eucDist.mean(axis=0)),0)
    dist_stan_dev = np.std(frame.eucDist)
    dist_zscore = (frame.eucDist - dist_mean) / dist_stan_dev
    frame['eucDist_zScore'] = dist_zscore
    # plot average trip length zscore
    frame.eucDist_zScore.plot(kind='line', title='Driving Distances')
    plt.show()
    
    '''
    Feature 2
    '''
    # drive avg speed
    frame['mph_avg'] = mph_avglist
    avgmph_mean = round(float(frame.mph_avg.mean(axis=0)),0)
    avgmph_stan_dev = np.std(frame.mph_avg)
    avgmph_zscore = (frame.mph_avg - avgmph_mean) / avgmph_stan_dev
    frame['avgmph_zScore'] = avgmph_zscore
    # plot max speed zscore
    frame.avgmph_zScore.plot(kind='line', title='Driving Average Speeds')
    plt.show()
    
    '''
    Feature 3
    '''
    # drive max speed
    frame['max_mph'] = mph_maxlist
    mph_mean = round(float(frame.max_mph.mean(axis=0)),0)
    mph_stan_dev = np.std(frame.max_mph)
    mph_zscore = (frame.max_mph - mph_mean) / mph_stan_dev
    frame['mph_zScore'] = mph_zscore
    # plot max speed zscore
    frame.mph_zScore.plot(kind='line', title='Driving Max Speeds')
    plt.show()
    
    frame['driver_1'] = 0

    feature2_df = pd.DataFrame(frame, columns=['eucDist_zScore','avgmph_zScore','mph_zScore','driver_1'])


'''
Combining the two folders' data to create training data
'''
combination = pd.concat([feature_df,feature2_df], axis=0)

combination.hist()
plt.show()

# # Performing Logistic Regression on two driver data
X = combination[['eucDist_zScore','avgmph_zScore','mph_zScore']]
y = combination.driver_1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1)

train = pd.DataFrame(data=X_train, columns=['eucDist_zScore','avgmph_zScore','mph_zScore'])
train['driver_1'] = y_train
test = pd.DataFrame(data=X_test, columns=['eucDist_zScore','avgmph_zScore','mph_zScore'])
test['driver_1'] = y_test

# Create a histogram of all variables
train.hist()

train_nd = combination[combination.driver_1 == 0]
train_d = combination[combination.driver_1 == 1]

plt.figure()
plt.scatter(train_nd.eucDist_zScore, train_nd.avgmph_zScore, alpha = .5, marker='+', c= 'b')

plt.scatter(train_d.eucDist_zScore, train_d.avgmph_zScore, marker='o', 
            edgecolors = 'r', facecolors = 'none')
plt.ylim([0,5]); plt.xlim([0, 5])
plt.legend( ('yes', 'no'), loc='upper right')

# 1 - Run a logistic regression on the balance variable
driver = LogisticRegression()
driver.fit(X_train, y_train)
B1 = driver.coef_[0][0]
B0 = driver.intercept_[0]
np.exp(B1)

x = np.linspace(test.eucDist_zScore.min(), test.eucDist_zScore.max(),500)
beta = [B0,B1]

y = np.exp(beta[0] + beta[1]*x) / (1 + np.exp(beta[0] + beta[1]*x))
odds = np.exp(beta[0] + beta[1]*x)
log_odds = beta[0] + beta[1]*x

plt.figure(figsize=(7, 8))
plt.subplot(311)
plt.plot(x, y, 'r', linewidth=2)
plt.ylabel('Probability')
plt.text(500, 0.7, r'$\frac{e^{\beta_o + \beta_1x}}{1+e^{\beta_o + \beta_1x}}$', fontsize=25)
plt.show()

x = np.linspace(test.eucDist_zScore.min(), test.eucDist_zScore.max(),5)
beta = [B0,B1]

y = np.exp(beta[0] + beta[1]*x) / (1 + np.exp(beta[0] + beta[1]*x))
odds = np.exp(beta[0] + beta[1]*x)
log_odds = beta[0] + beta[1]*x

plt.figure(figsize=(7, 8))
plt.subplot(311)
plt.plot(x, y, 'r', linewidth=2)
plt.ylabel('Probability')
plt.text(500, 0.7, r'$\frac{e^{\beta_o + \beta_1x}}{1+e^{\beta_o + \beta_1x}}$', fontsize=25)

plt.subplot(312)
plt.plot(x, odds, 'k', linewidth=2)
plt.ylabel('Odds')
plt.text(500, 10, r'$e^{\beta_o + \beta_1x}$', fontsize=20)

plt.subplot(313)
plt.plot(x, log_odds, 'c', linewidth=2)
plt.ylabel('Log(Odds)')
plt.xlabel('x')
plt.text(500, 1, r'$\beta_o + \beta_1x$', fontsize=15)


#Create predictions using the driver model on the test set
test['prob'] = driver.predict(test[['eucDist_zScore','avgmph_zScore','mph_zScore']])

# Accuracy
accuracy = sum(test.prob == test.driver_1) / float(len(test.driver_1))

# Specificity
test_nd = test[test.driver_1 == 0]
specificity = sum(test_nd.prob == test_nd.driver_1) / float(len(test_nd.driver_1))

# Sensitivity
test_d = test[test.driver_1 == 1]
sensitivity = sum(test_d.prob == test_d.driver_1) / float(len(test_d.driver_1))

# Classification accuracy compare to the not-driver rate
null = 1 - sum(combination.driver_1) / float(len(combination.driver_1))

# # Getting initial prob values for each drive for initial submission

# import scipy.stats as st
# prob = 1 - st.norm.cdf(mph_zscore)
# probs.append(prob)


# submissions = os.lisdir(wd)
# f = open('master.csv', 'a')
# for submission in submissions:
#     f.write(submission)

# # Formatting the data for submission

frame['prob'] = driver.predict(frame[['eucDist_zScore','avgmph_zScore','mph_zScore']])
frame['driver_trip'] = drive_number
submission = pd.concat([frame.driver_trip,frame.prob], axis=1)
overall = pd.concat([overall, submission], axis=0)
final_overall = overall.set_index('driver_trip')
final_overall.to_csv("submission.csv")

