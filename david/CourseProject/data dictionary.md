asofdate: the year of the HMDA LAR file            
respondentid: the financial institutions HMDA reporting number (institutions may have more than 1)
respondent_name: name of financial institution
agencycode: code for the financial instutution's regulator
loantype: type of loan applied for or received (1 = conventional, 2 = FHA insured, 3 = VA guaranteed, 4 = FSA/RHS guaranteed)            
propertytype: type of property securing the loan (1 = 1-4 family home, 2 = manufactured housing, 3 = multifamily dwelling)
loanpurpose: purpose of the loand (1 = home purchase, 2 = home improvement, 3 = refinancing)
occupancy: flag for owner occupied dwelling (1 = owner-occupied as a principle dwelling, 2 = not owner-occupied, 3 = not applicable)
loanamount: the amount of the loan, rounded to the nearest thousand dollars
preapproval: preapproval status of the loan (1 = preapproval was requested, 2 = preapproval was not requested, 3 = not applicable)
actiontype: lender's action on the loan (1 = loan originated, 2 = application approved but not accepted, 3 = application denied by financial institution, 4 = application withdrawn by applicant, 5 = file closed for incompleteness, 6 = loan purchased by your institution, 7 = preapproval request denied by financial institution, 8 = preapproval request approved but not accepted)
msaofproperty: the 5 digit MSA of the property (this field may be blank or NA if a dwelling is located outside an MSA or in a county with population less than 30,000)
statecode: the two digit code for the stat in which the property is located        
statename: the 2 letter abbreviation of the state in which the property is located
countycode: the 3 digit county code in which the property is located, this may be blank if the county has a population of less than 30,000
countyname: the name of the county corresponding to the 3 digit countycode
censustractnumber: the 6 digit (in format ####.##) tract identifier of the property (note: this is an incorrect representation of actual 11 digit census tract numbers)
applicantethnicity: the ethnicity of the applicant (1 = hispanic or latino, 2 = not hispanic or latino, 3 = information not provided and application not received in person, 4 = not applicable, 5 = no co-applicant)          
coapplicantethnicity: the ethnicity of the co-applicant (see applicantethnicity for valid codes)            
applicantrace1: applicant's race selection, up to 5 choices may be submitted (1 = american indian or alaska native, 2 = asian, 3 = black or african american, 4 = native hawaiian or other pacific islander, 6 = information not provided, application not in person, 7 = not applicable, 8 = no co-applicant)  
applicantrace2: see applicantrace1          
applicantrace3: see applicantrace1           
applicantrace4: see applicantrace1                     
applicantrace5: see applicantrace1                     
coapplicantrace1: the race of the co-applicant (see applicantrace1 for a valid value list)            
coapplicantrace2: see coapplicantrace1            
coapplicantrace3: see coapplicantrace1                        
coapplicantrace4: see coapplicantrace1            
coapplicantrace5: see coapplicantrace1            
applicantsex: the gender of the applicant (1 = male, 2 = female, 3 = information provided, application not in person, 4 = not applicable, 5 = no co-applicant)    
coapplicantsex: the gender of the co-applicant
applicantincome: the income relied upon during underwriting decision making, rounded to the nearest 500 dollars         
purchasertype: the type of institution purchasing a loan if the loan was sold after origination (0 = loanw as not originated or was not sold in calendar year, 1 = fannie mae, 2 = ginnie mae, 3 = freddie mac, 4 = farmer mac, 5 = private securitization, 6 = commercial bank, savings bank or savings association, 7 = life insurance company, credit union, mortgage bank, or finance company, 8 = affiliate institution, 9 = other type of purchaser)
denialreason1: optional reporting field for the reason an application was denied (1 = debt to income ratio, 2 = employment history, 3 = credit history, 4 = collateral, 5 = insufficient cash (down payment, closing costs), 6 = unverifiable information, 7 = credit application incomplete, 8 = mortgage insurance denied, 9 = other)           
denialreason2: see denialreason1      
denialreason3: see denialreason1           
ratespread: the difference between the mortgage note rate and APOR (average prime offer rate) shown in format ##.##%, this field is NA or blank if the spread is less than 1.5%           
hoepastatus: flag for Home Owndership Equity Protection Act status of the loan (1 = HOEPA loan, 2 = not a HOEPA loan)
lienstatus: shows the priority of the lien securing the dwelling (1 = first lien, 2 = subordinate lien, 3 = not secured by a lien, 4 = not applicable - for purchased loans)          
sequencenumber: loan sequence number, added in 2012          
areapopulation:           
minoritypopulationpct           
ffiec_median_family_income: the median family income for the census tract (in previous years this was HUD median income)          
tract_to_msa_md_income: ratio of the tract's median income ot the MSA/MD in which it is located
num_of_owner_occupied_units: number of units in a dwelling in which the owner claims residence
num_of_1_to_4_family_units: number of 1-4 family residences in a dwelling
application_date_indicator:
fipscode:            
latitude: latitude of property's geocoded location, as a decimal            
longitude: longitude of a property's geocoded location, as a decimal