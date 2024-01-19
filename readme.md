## Calculating Correlation Levels in the Ethereum Network

This software runs analysis on data from two sources:

 * rated.network - the data is retrieved from rated's API under the `/operators` path
 * Miga Labs - the data was kindly provided by Miga Labs, based on their crawler software


## Using the Software

1. Install dependencies by running `pip install -r requirements.txt`
2. Update your access credentials for rated.network by creating a `.env` file that looks liek this:

```
USERNAME=your-username
PASSWORD=your-password
API_KEY=your-api-key
```

3. Fetch the data from rated.network's API, by running the following command:

```
$ python getdata.py
```

This will run a script that will keep pinging the rated API repeatedly, (but throttled) until it has fetched all the available data. When the script completes, it will create a file called `results.json` in the `/data` subfolder.

4. To start running an analysis on the data, run the following command:

```
$ python main.py run-analysis
```

----

## Analysis Tasks

This will run through the various analysis tasks and output the relevant files.  The tasks it executes are described below:

 * Transforms Data the taking the raw data from the rated.network API and removes API metadata such as pagination and sorting etc. This output the file `data/data.json`.
 * Collates the data by extracting just the data that is required for analysis and computed properties such as `totalNetworkPenetration` and `totalValidatorCount` for each node operator.  This task outputs the file `data/collated.json`.
 * Analyzes node operators by reading data from the `data/collated.json` file.  This task prints out the standard HHI and modified HHI value for node operators.
 * Analyzes staking pools by reading data from the `data/collated.json` file.  This task prints out the standard HHI and modified HHI value for staking pools. It also attempts to measure any correlation between the level of variability in clients, relays and node operators between each staking pool.  This is done to try to identify if there is correlation between the size of the staking pool and the level of client diversity or or number of node operators, and indeed between any other respective attributes. This is done by first calculating the coefficient of variance in the relay, client and node operators shares for each staking pool, and then calculating the R^2 value from the set of coefficients of variation.
 * Analyses correlation between operators and clients by doing two things: the first thing it does it create a CSV file that contains a row for each node operators, a column for it's market share, and a column for the each of the consensus clients containing the percentage of that operators nodes running that client.  The second thing it does is produce a file called `average_client_percentage_by_decile.csv`.  The code calculates a correlation between the market share of node operators and the consensus clients they run.  The resulting CSV file contains rows for each decile of market share, and columns for each consensus client, which containing values for how much of a percentage of that consensus client is run by node operators with a market share respective of the current row.
 * Analyzes the correlation between node operators and staking pools.  This task outputs a file called `data/operators_vs_pools.csv` containing a row for each node operator, and columns for each staking pool, containing values corresponding to the market share for that pool and that node operator.
 * Analyzes the correlation between node operators and relayers, similar to the manner in the previous step, and outputs a file called `data/operators_vs_relays.json`.
 * Analyszes the data from Miga Labs, which is in the file `data/data.csv`.

 This last step involves trying to identify correlations between the various attributes of the nodes in the dataset, including country, client, IDP, numebr of attestation subnets advertised.  For each pairwise comparison between attributes the code calculates:

* The Chi-squared value
* The P-value
* The Cramér's V value

Finally this code runs another calculation as an alternative approach to identifying the level of correlation between the various attributes
It does this by calculating the hamming weights for each attribute.

For every record in the dataset, we compare it to every other record in the dataset along a specific attribute.
Where the attributes are equal for each record, we record a 1, where they are not equal, we record 0.
The result is a bitstring from which we can derive a hamming weight.
An easier way to calculate the hamming weight is to increment a count every time the attributes for each record being compared are equal.
We then repeat the entire process for the next attribute.

The result is a series hamming weights for each record compared to every other record, for each attribute.
We then add all the hamming weights together for each record, so every record has an aggregate hamming weight.
The results are a table with the record index in column 1, a column for the hamming weight of each attribute,

This allows us to see which attributes are more correlated than others, and by how much more, and allows us to compare the results to the Chi-squared and Cramer's V values we derived earlier.  This approach also allows us to rank the hamming weights to determine if which node operators have the highest correlations between any attributes.

## Problem Statement

The motivation for running this sort of analysis is to identify potential correlations between node operators and staking pools along various common attributes. The types of question that might be answered by such an analysis include:

* Does a staking pool with a double digit percentage share of the validator set maintain only  a single client software, or does it only rely on one or two node operators, does it prefer certain relayers?
* Are the correltations between attributes, e.g.: do all node operators in a specific jurisdiction prefer a certain client, or cloud provider, or use a certain relayer, or run certain software?
* Do cloud instances prefer certain software compared to bare metal servers?
* Do certain staking pools have similar policies that their node operators follow?
* which node operators are the most highly correlated across all attributes and why?

### Miscellaneous

You can apply formatting to all the Python modules in this package by running the following command in the root folder:

```
$ python -m black .
```