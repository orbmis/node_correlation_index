# Scripts for measuring correlation between datapoints from rated.network

See the rated-api-info.txt file for info on their API calls

See the problem-statement.txt file for info on the problem statement this is trying to address

Install the requirements using the following command:

`pip install -r requirements.txt`

To run these scripts, run them in the following order:

1. getdata.py
2. transform.py
3. collate.py

and then any of the other scripts to get the required data

`index.py` calculates the modified HHI from the `data.csv` file, which comes from the Miga Labs dataset
note that this isn't particularly useful

the `miga_labs_correlations.py` script runs a more useful analysis on this dataset

the script `rated_correlations.py` calculates the modified HHI for the rated labs dataset

the `staking_pools_HHI.py` file calculates the HHI and modified HHI for node operators

----

Seed Data:

results.json: this is the data pulled down from the rated.network API, on the 16th January 2024
data.csv: this is the data from Miga Labs