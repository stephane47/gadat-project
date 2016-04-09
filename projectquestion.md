Project proposal: Predicting the return of peer to peer loans
=======
###What is the question you hope to answer?

The goal of this project is to combine data on ratings & default rates of peer-to-peer loans arranged through LendingClub.com with publically available data on unemployment & housing costs to improve the prediction of default rates and net rates of returns on these loans. 

Specifically, if I can identify positive or negative trends in unemployment and cost of living (rent), I hope that these will improve my ability to predict rate of return and/or the default rate compared to only using LendingClub.com's data.


###What data are you planning to use to answer that question?

LendingClub.com has exported certain information from their loan databases and made it [available for download:]((https://www.lendingclub.com/info/download-data.action):

   > 'These files contain complete loan data for all loans issued through the time period stated, including the current loan status (Current, Late, Fully Paid, etc.) and latest payment information. The file containing loan data through the "present" contains complete loan data for all loans issued through the previous completed calendar quarter'

In addition, the data include information on the borrower's employment, living arrangement (rent/mortgage), & geographic location as well. 

I plan to take advantage of these items by combining them with data from 2 additional sources:
 
- The Bureau of Labor Statistics has published data on employment in multiple formats broken down by zip code & sector, [available as csv files](http://download.bls.gov/pub/time.series/overview.txt)

- Zillow has median [rents by zip code](http://www.zillow.com/research/data/#rental-data)
	
### What do you know about the data so far?
All 3 source are available in csv format. This will make data import straightforward. Geographic information is given in slightly different formats, but they seem to be all based on zipcode, so I hope that won't be too challenging.

###Why did you choose this topic?
LendingClub grades individual loans, but does not disclose details on how they do so. I am interested to see if by combining these different sources of information I can get a more accurate prediction of default rates & rates of return.
	
