##Project Question
How have demographics changed in an MSA in the years since the financial crisis?
Analysis will focus on the following data attributes:
     * Race (in terms of minority or non-minority)
     * Loan Amount
     * Location (Baseline for the MSA and comparing changes in tracts compared to the baseline)
     
##Datasets
* HMDA LAR files from the FFIEC for 2009 to 2013
* HMDA LAR files for Milwaukee (MSA 33340) for 2009 to 2013

##Tools
* Python
* PostGresSQL - houses the initial and Milwaukee data sets.
* Psycopg2 - module used to interface between Python and PostGres
* pandas
* sci-kit learn
###Initial Work
* data selection - one MSA chosen to work with. Milwaukee (33340) is an MSA with historic racial separation. 
* data cleaning - select fields which will be useful in the analysis and which fields need to be filtered prior to analysis
    - fields selected:
        - applicant race 1-5
        - co-applicant race 1-5
        - ethnicity
        - co applicant ethnicity
        - action taken: outcome variable for loan analysis, descriptive counts of applications vs originations by tract and minority status (this will be the outcome of the logistic regression model)
        - loan amount (is there a relationship between minority status and loan amounts? between location and loan amounts?)
        - applicant income: to control for credit decisions
        - as of date: to sort the analysis over time
        - minority population percent: as a proxy baseline for application and origination rate
        - FFIEC/HUD median family inomce: show the relationship between borrower and area income (compare to miniority population and loan amount)
        - minority status: derived attributed using FFIEC logic (takes inputs of applicant and co-applicant races and ethnicities to determine if the loan was made to a minority borrower)
    - filters applied: 
        - loan type: 1-4 family 
        - property type: 1-4 family
        - loan purpose: home purchase
        - occupancy: owner occupied
        - lien status: first lien only
        - as of date: 2009-2013 (potential to expand to 2002 if time allows, this would show pre-crisis trends)
        - location: Milwaukee MSA number 33340, analysis will show baseline for the MSA and compare individual tracts to that baseline
        - 
* descriptive analysis
    - application and origination counts by minority status (by tract and year) 
    - % applications by minorities
    - % originations to minorities
    - tract minority % of population
    - change in tract minority % population over time
    - average loan amount to minority and non-minority by tract and year
    - 
* baselining for MSA
    - application and origination counts by minority status (by tract and year)
    - % applications by minorities
    - % originations to minorities
    - MSA minority population %
    - average loan amount to minority and non-minority for the MSA by year

###Analysis Plan
* Compare application and origination counts and rates by minority and non-minority over time for each tract in Milwaukee
* Compare loan amounts by minority and non-minority status as well as by location over time for each tract in Milwaukee
    - this could include a comparison of minority/non-minority income to tract median income and MSA median income
        + MSA to tract income comparison will be a proxy for a wealth/income disparity due to minority status
* Develop a logistic regression model that predicts the outcome of a loan application


##Code Structure
* Controller
* database
* class library
