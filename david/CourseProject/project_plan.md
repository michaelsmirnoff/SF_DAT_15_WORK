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
* PostGresSQL - houses the initial data sets.
     * may use this to house the Milwaukee data
* Psycopg2 - module used to interface between Python and PostGres

###Initial Work
* data selection
* data cleaning
* descriptive analysis
* baselining for MSA


###Analysis Plan
* Compare application and approval counts and rates by minority and non-minority over time
* Compare loan amounts by minority and non-minority status as well as by location over time



##Code Structure
* Controller
* database
* class library
