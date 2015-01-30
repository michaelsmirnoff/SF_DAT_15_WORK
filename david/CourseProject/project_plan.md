##Project Question
How have demographics changed in an MSA in the years since the financial crisis?
Analysis will focus on the following data attributes:
     * Race (in terms of minority or non-minority)
     * Loan Amount
     * Location (Baseline for the MSA and comparing changes in tracts compared to the baseline)
     
##Code Structure
* controller
    * keep this script short for style reasons, push all functions into the class library  
* database
    * store data in SQL or csv?
* class library
    * generalized functions for sorting data by demographics, location, loan value etc.

##Datasets
* HMDA LAR files from the FFIEC for 2009 to 2013
* HMDA LAR files for Milwaukee (MSA 33340) for 2009 to 2013

##Tools
* Python
* PostGresSQL - houses the initial data sets.
     * may use this to house the Milwaukee data
* Psycopg2 - module used to interface between Python and PostGres

###Initial Work
* data selection
* data cleaning
    * group into minority, non-minority
    * remove junior lien data
    * re-do query to remove non-used data
    * remove non 1-4 family conventional data (or separate out non-conventional loans prior to analysis)
    * verifty that all loans have all geo-code data points
    
###Analysis Plan
* Compare application and approval counts and rates by minority and non-minority over time
* Compare loan amounts by minority and non-minority status as well as by location over time
* For the MSA baseline and each tract:
    * Application count by minority and non-minority
    * Origination rate/count by minority and non-minority
    * Descriptive statistics on loan amounts
* investigate disimilarity indices from the Census
* descriptive analysis for tracts
* baselining for MSA
* value count histograms by tract and year
    * check for divergence between minority and non-minority
* approval count histograms by tract and year for minority and non-minority

I will be spending more time getting my base analysis done tomorrow and this weekend.
After some data exploration I will try to decide on what kind of model might work for a project. 
Typical fair lending analysis uses classification to determine approve/deny on loans and linear regressions to evaluate 
the terms and conditions of a loan for evidence of disparate treatment.

Advice on how to turn shift from data exploration into model use would be appreciated. I spoke with Brandon about working
primarily on a descriptive project. HMDA data are commonly used to tell a story of how different communities have been
treated by the mortgage industry. I'll post an intersting article tomorrow in slack.
