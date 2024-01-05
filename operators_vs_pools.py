import json

# Read the input JSON file
with open('collated.json', 'r') as infile:
    data = json.load(infile)

# Create a dictionary to store the desired output
output_data = {}

# Iterate through each entry in the input data
for entry in data:
    display_name = entry['displayName']
    total_validator_count = entry['totalValidatorCount']
    total_network_penetration = entry['totalNetworkPenetration']

    pools = entry['pools']
    pool_data = {}

    # Iterate through each pool in the entry
    for pool in pools:
        pool_name = pool['name']
        validator_count = pool['validatorCount']
        network_penetration = pool['networkPenetration']

        # Add pool information to the dictionary
        pool_data[pool_name] = {
            'validatorCount': validator_count,
            'networkPenetration': network_penetration
        }

    # Add entry information to the output dictionary
    output_data[display_name] = {
        'totalValidatorCount': total_validator_count,
        'totalNetworkPenetration': total_network_penetration,
        'pools': pool_data
    }

# Write the output data to a new JSON file
print("\nCollating Operators vs. Pools\n")
with open('operators_vs_pools.json', 'w') as outfile:
    json.dump(output_data, outfile, indent=2)
