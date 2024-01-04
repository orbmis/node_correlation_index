import json
import pandas as pd

# Load the example data
with open('collated.json', 'r') as infile:
    data = json.load(infile)

# Create a DataFrame from the data
df_list = []
for entity in data:
    for pool in entity.get('pools', []):
        df_list.append({
            'displayName': entity['displayName'],
            'poolName': pool['name'],
            'validatorCount': pool['validatorCount'],
            'networkPenetration': pool['networkPenetration']
        })

df = pd.DataFrame(df_list)

# Pivot the DataFrame to have columns for each entity and their attributes
pivot_df = df.pivot(index='poolName', columns='displayName', values=['validatorCount', 'networkPenetration'])

# Calculate correlations
correlations = pivot_df.corr()

# Print the correlation matrix
print("Correlation Matrix:")
print(correlations)
