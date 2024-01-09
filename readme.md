# Scripts for measuring correlation between datapoints from rated.network

See the rated-api-info.txt file for info on their API calls

See the problem-statement.txt file for info on the problem statement this is trying to address

To run these scripts, run them in the following order:

1. getdata.py
2. transform.py
3. collate.py

and then any of the other scripts to get the required data


`index.py` calculates the modified HHI from the `data.csv` file, which comes from the Miga Labs dataset