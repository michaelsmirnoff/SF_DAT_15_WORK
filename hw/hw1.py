'''
Move this code into your OWN SF_DAT_15_WORK repo

Please complete each question using 100% python code

If you have any questions, ask a peer or one of the instructors!

When you are done, add, commit, and push up to your repo

This is due 7/1/2015
'''
#Author:Nick Smirnov

import pandas as pd
# pd.set_option('max_colwidth', 50)
# set this if you need to

pk_file = 'C:\Users\Nick\Desktop\GA\SF_DAT_15\hw\data\police-killings.csv'
killings = pd.read_csv(pk_file)
killings.head()
killings.columns
# 1. Make the following changed to column names:
# lawenforcementagency -> agency
# raceethnicity        -> race
killings.rename(columns={'lawenforcementagency':'agency', 'raceethnicity':'race'}, inplace=True)

# 2. Show the count of missing values in each column
killings.isnull().sum()


# 3. replace each null value in the dataframe with the string "Unknown"
killings.fillna(value='Unknown', inplace=True)   


# 4. How many killings were there so far in 2015?
killings[killings.year==2015].year.count()

# 5. Of all killings, how many were male and how many female?
killings.groupby('gender').gender.count()

# 6. How many killings were of unarmed people?
killings[killings.armed == 'No'].armed.count()

# 7. What percentage of all killings were unarmed?
unarmed = killings[killings.armed == 'No'].armed.count()
total = killings.armed.count()
percentage = float(unarmed) / float(total) * 100

# 8. What are the 5 states with the most killings?
killings.groupby('state').state.count().nlargest(5)

# 9. Show a value counts of deaths for each race
killings.groupby('race').race.count()

# 10. Display a histogram of ages of all killings

killings.groupby('age').age.plot(kind='hist', stacked=True)

# 11. Show 6 histograms of ages by race

killings.groupby('race').age.plot(kind='hist', stacked=False)

# 12. What is the average age of death by race?
killings.groupby('race').age.mean()

# 13. Show a bar chart with counts of deaths every month
killings.groupby('month').month.count().plot(kind='bar')

###################
### Less Morbid ###
###################

m_file = 'C:\Users\Nick\Desktop\GA\SF_DAT_15\hw\data\college-majors.csv'
majors = pd.read_csv(m_file)
majors.head()
majors.columns
# 1. Delete the columns (employed_full_time_year_round, major_code)
del majors['Major_code']
del majors['Employed_full_time_year_round']
# 2. Show the cout of missing values in each column
majors.isnull().sum()

# 3. What are the top 10 highest paying majors?
majors.sort_index(by='P75th', ascending=False).Major.head(10)

# 4. Plot the data from the last question in a bar chart, include proper title, and labels!
#import matplotlib.pyplot as plt

top10 = majors.sort_index(by='P75th', ascending=False).head(10)
top10.plot(x='Major', y='P75th', kind='bar')

'''plt.xlabel("Major")                          # set the x axis label
plt.ylabel("Salary")         # set the y axis label
plt.title("Top 10 Highest Paying majors")  # set the title
plt.plot(top10.Major, top10.P75th) 
'''

# 5. What is the average median salary for each major category?
majors.groupby('Major_category').Median.mean()

# 6. Show only the top 5 paying major categories
majors.groupby('Major_category').Median.mean().nlargest(5)

# 7. Plot a histogram of the distribution of median salaries

majors.groupby('Major').Median.mean().plot(kind='hist')

# 8. Plot a histogram of the distribution of median salaries by major category

majors.groupby('Major_category').Median.mean().plot(kind='hist')

# 9. What are the top 10 most UNemployed majors?
# What are the unemployment rates?
majors.columns
majors.sort_index(by='Unemployed', ascending=False).head(5)

# 10. What are the top 10 most UNemployed majors CATEGORIES? Use the mean for each category
# What are the unemployment rates?
majors.groupby('Major_category').Unemployed.mean().nlargest(10)

# 11. the total and employed column refer to the people that were surveyed.
# Create a new column showing the emlpoyment rate of the people surveyed for each major
# call it "sample_employment_rate"
# Example the first row has total: 128148 and employed: 90245. it's 
# sample_employment_rate should be 90245.0 / 128148.0 = .7042
majors['sample_employment_rate'] = [(m.Unemployed / m.Employed) for m in majors]

# 12. Create a "sample_unemployment_rate" colun
# this column should be 1 - "sample_employment_rate"
