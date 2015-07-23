##Project Question
Did the financial crisis disproportionately affect minority borrowers or borrowers in areas with significant minority populations?

Recent research has highlighted the disproportionate impact of the subprime crises on minority communities. Minority communities have historically been economically vulnerable due to proscriptive policy, market forces, and social conditions. 

Research in this area commonly combines multiple data sources such as Census, HUD, and internal Federal Reserve data (such as loan performance databases). As the HMDA LAR data is less comprehensive in terms of demographics and financial market information, it is unlikely that conclusions drawn from this work will have the same weight or specificity.

##Datasets
* Home Mortgage Disclosure Act (HMDA) Loan Application Register (LAR) files from the FFIEC for 2009 to 2013
* HMDA LAR files for Milwaukee (MSA 33340) for 2009 to 2013

## Background
The Home Mortgage Disclosure Act requires the reporting of loans and applications for most properties secured by a dwelling. The data has approximately 18 million rows annually with 50 attributes (after being combined with Census data). The data was initially collected to determine the extent of urban disinvestment that was driven by lack of credit. The data has subsequently been used as an evidentiary basis for determining racial, gender, ethnic and other forms of discrimination and to support enforcement of the Community Reinvestment Act (CRA). The CRA requires lenders to provide credit in MSAs in which they have a branch office, violations of the CRA can result in blocked branch purchases and mergers. Fair Lending analysis frequently begins by examing lending patterns in the HMDA data set.

HMDA has been expanded in scope and data attributes since its inception and in the early 1990's became a transaction-level dataset. With the passage of the Dodd Frank act in 2010, the Consumer Financial Protection Bureau assumed responsibility for the statute, regulation and associated duties (many will be shared with the FFIEC). To modernize effectuation of data collection and distribution, the CFPB has begun piloting new methods of data collection, validation, geocoding, and reporting. The CFPB will begin data collection and publication in 2018.

The HMDA datasets are public use hosted at www.FFIEC.gov and consumerfinance.gov/HMDA. I obtained the data internally at the CFPB from our internal data team who had downloaded it from the FFIEC. The HMDA data is matched with Census demographics data by the FFIEC. Data fields describing tracts and MSAs are matched to HMDA from Census datasets.

Getting the data took 3 days because of internal process issues. After receiving the data, I needed to find a Mac friendly tool to unzip it as it was zipped using Windows proprietary encoding. When loading the data files into data tables in Postgres I needed to convert the text formatting from ANSI (Windows native) to LATIN1. 

During my policy research for HMDA I learned that, for a variety of reasons, the financial crisis disproportionately affected minority borrowers and minority communities. The subprime crisis created an inverse redlining where credit flooded into neighborhoods during the housing boom and waves of foreclosures followed when the market collapsed. Academic work has shown that loans to minorities or majority-minority community areas had frequently been priced above market rates, effectively placed in subprime status, when those loans qualified as prime. Community groups began using subprime lending as a leading indicator of foreclosure and would use subprime lending data from HMDA in coordination with municipal government finance office to target their foreclosure prevention outreach efforts. 

Using the data from 2009 to 2013, I want to see if there is a difference in origination rates to minority borrowers and minority communities in a traditionally highly segregated city (Milwaukee). Additinionally, I would like to see if lending amounts changed differently for minority and non-minority borrowers over the time period. To do this I replicated the logic the FFIEC uses to determine minority status (describe steps). I use a binary flag for minority status with 1 being minority and 0 being non-minority. I added this field to the data frames in Pandas after pulling the LAR data from the Postgres server I use to locally host it. Given the large number of tracts in Milwaukee, I split my analysis into groups of minority population concentration. The groups I used were low, middle, upper, high which correspond to less than 30% minority, 30-50% minority, 51-80% minority and greater than 80% minority. Below I list the data fields I used in my analysis.

*Descriptive analysis*
Prior to conducting any analysis, I filtered the data so as to account for discrepencies for difference in collateral, loan purpose, occupancy status and lien status (see below for specifics). Differences across these data fields can change underwriting and pricing decisions so selection of a specific market segment is common.

To create a baseline for tract comparison I counted applications and originations and computed an origination rate for the entire MSA. The baseline separates minority and non-minority borrowers. The initial graph (approval_rates.png) shows the approval rates for the MSA for minority and non-minority borrowers. During my data exploration, I computed the percent of applications by minority borrowers and the percent of originations to minority borrowers (make graphs of these). These numbers were fairly close, however they both were significantly lower than the minority population of the MSA. (I still need pre-2013 data on minority population percent for the MSA).

I will graph the percent of applications and originations to minorities and the approval rates for minorities and non-minorities for each tract category (low, middle, upper, high). If there is strong divergence, I believe it will point to financial and economic factors that underpin the functioning of mortgage markets. Such as the drastically reduced subprime lending market, and the disproportionate impact of the crisis on minority areas (which can impact credit availability). Given time, I would like to see if loan values decreased during this period, and if so, if they decreased more significantly in minority areas or to minority borrowers. Examination of interest rates may also show how banks perceive risk in those areas (for reference, fair lending models typically use linear regression to approximate credit price).

I will build a logisitic regression model to predict probabiliy of approval for a loan and see how it performs on the LAR data set. My initial thought was to use the model as a time series, but having done some data exploration, there may be significant differences between the years. Training a model on each year and testing on tracts may prove more interesting. Determining if minority status or minority population percent are predictive of loan origination is my underlying goal.


##Tools
* Python
* PostGresSQL - houses the initial and Milwaukee data sets.
* Psycopg2 - module used to interface between Python and PostGres
* pandas
* sci-kit learn

###Data Processing
* Data loading - individual CSV files were loaded into a local instance of Postgres with Latin1 encoding
* Data selection - one MSA chosen to work with. Milwaukee (33340) is an MSA with historic racial separation
* Data cleaning - select fields which will be useful in the analysis and which fields need to be filtered prior to analysis
    - fields selected:
        - year
        - applicant race 1-5
        - co-applicant race 1-5
        - applicant ethnicity
        - co applicant ethnicity
        - action taken: outcome variable for loan analysis, descriptive counts of applications vs originations by tract and minority status (this will be the outcome of the logistic regression model)
        - loan amount (is there a relationship between minority status and loan amounts? between location and loan amounts?)
        - applicant income: to control for credit decisions
        - as of date: to sort the analysis over time
        - minority population percent: as a proxy baseline for application and origination rate
        - FFIEC/HUD median family inomce: show the relationship between borrower and area income (compare to miniority population and loan amount)
        - minority status: derived attributed using FFIEC logic (takes inputs of applicant and co-applicant races and ethnicities to determine if the loan was made to a minority borrower)
        - Minority population concentration category: derived attribute using the following buckets- 0-30% low minority, 31-50% middle minority, 51-80% upper minority, 81-100% high minority
    
    - filters applied: 
        - loan type: conventional purchase
        - property type: 1-4 family
        - loan purpose: home purchase
        - occupancy: owner occupied
        - lien status: first lien only
        - as of date: 2009-2013 (potential to expand to 2002 if time allows, this would show pre-crisis trends)
        - location: Milwaukee MSA number 33340, analysis will show baseline for the MSA and compare individual tracts to that baseline

*Data Cleaning* 
Prior to performing any exploration or analysis the data tables were converted from strings to integers and floats as appropriate. The original load script was appropriated from another project and had loaded all variables as varchars. The current intake process for HMDA data involves a fixed field length DAT file. This resulted in several critical fields having trailing spaces after an NA value. After several failed attempts to remove these values in Python, I changed them to '0's in Postgres and then used Pandas to replace all missing values with the series mean. One to three values were replaced this way in applicant income, minority population percent, and median family income.

*Descriptive analysis and data exploration*
MSA baselining was done by splitting all applicants and borrowers into minority and non-minority status using logic from the FFIEC (see DAT4_library.py). This initial exploration showed that minorities had a lower rate of origination than non-minorities. This approval rate difference was an interesting place to dig deeper to determine if overt discrimination was present.

Initial data exploration showed decreased market participation (as a share of market activity) for all minority tract categories except low after 2011, with middle minority (30-50%) showing the sharpest decline. The visualizions used to show this plotted the percent of originations and applications over time by tract category. Origination lines tracked application lines which pointed to market participation instead of discrimination during origination process, though pre-application phases could not be accounted for using this data set. Raw counts of applicaitons an originations showed that between 2011 and 2013 all tract categories saw increases in applications and originations, but that low minority areas experienced a much more dramatic increase in mortgage activity. That these counts were increasing for minority status applicants and borrowers while the minority share showed a decrease in minority status applicants and borrowers indicates that non-minorities may be experiencing a more robust recovery post-crisis. This is confirmed in recent papers by groups such as the Urban Institute.  

Examining income and loan values showed that, as expected, loan amounts tracked income. Graphing income and loan amount by minority concentration showed that an inverse relationship between minority concentration and income. This set of graphs was turning point where the project became a story about economic exclusion. Further work on this thought included an examination of minority and non-minority income and loan value inside each tract to determine if minority status is as predictive as minority concentration. In other words, is the quesiton about community wealth and opportunity or minority wealth and opportunity. In the four tract categories created, minorities, on average, earned less and had lower loan values than their non-minority counterparts in similar minority concentration areas. If time allows in the future, it will be informative to examine specific tracts over time to see if minority status correlates to economic status.

    - application and origination counts by minority status (by tract and year) 
    - % applications by minorities
    - % originations to minorities
    - tract minority % of population
    - change in tract minority % population over time
    - average loan amount to minority and non-minority by tract and year
    
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
