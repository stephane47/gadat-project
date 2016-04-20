Predicting the default rate of peer-to-peer loans 
====

###What is the question you hope to answer?

The goal of this project is to combine data on ratings & default rates of peer-to-peer loans arranged through Lending Club with publically available data on unemployment & housing costs to improve the prediction of default rates and net rates of returns on these loans. 

Specifically, if I can identify positive or negative trends in unemployment and cost of living (rent), I hope that these will improve my ability to predict rate of return and/or the default rate compared to only using Lending Club's data.

Lending Club operates an online lending platform that enables borrowers to obtain a loan, and investors to purchase notes backed by payments made on loans. Lending Club is the world's largest peer-to-peer lending platform. 


### Available data

Lending Club publishes "complete loan data for all loans issued ", available for download as csv files. This includes information supplied about the borrower, amount of loan, loan grade, and loan purpose.

In addition, the data include information on the borrower's employment, living arrangement (rent/mortgage), & geographic location as well. 

I plan to take advantage of these items by combining them with data from 2 additional sources:

- The Bureau of Labor Statistics has published data on employment in multiple formats broken down by zip code & sector, [available as csv files](http://download.bls.gov/pub/time.series/overview.txt)

 - Zillow publishes their data on both home values (ZHVI) and median rents (ZRI) by geographic area.
This data is available for download as csv files.

###Initial pass
Many 'features' in LC data
look at how well LC grades compare with performance
rate of fully paid loans by grade

### next steps
Zillow data is very straightforward
BLS data is a mess



What data have you gathered, and how did you gather it?
Which areas of the data have you cleaned, and which areas still need cleaning?
What steps have you taken to explore the data?
What insights have you gained from your exploration?
Will you be able to answer your question with this data, or do you need to gather more data (or adjust your question)?
How might you use modeling to answer your question?