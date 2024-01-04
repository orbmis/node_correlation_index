import json

# Load the example data
with open('collated.json', 'r') as infile:
    data = json.load(infile)

# Create a dictionary to store the result
result_dict = {}

# Iterate over each object in the top-level array
for entity in data:
    entity_name = entity['displayName']
    result_dict[entity_name] = {}

    # Initialize dictionary with zero values for all client names
    for pool in entity.get('pools', []):
        for client_percentage in pool.get('clientPercentages', []):
            client_name = client_percentage['client']
            result_dict[entity_name][client_name] = 0
            result_dict[entity_name]['Prysm'] = 0
            result_dict[entity_name]['Nimbus'] = 0
            result_dict[entity_name]['Lighthouse'] = 0
            result_dict[entity_name]['Teku'] = 0
            result_dict[entity_name]['Lodestar'] = 0
            result_dict[entity_name]['Unknown'] = 0

    total_pools = 0
    for pool in entity.get('pools', []):
        total_pools+=1

    # Iterate over each pool in the entity
    for pool in entity.get('pools', []):
        for client_percentage in pool.get('clientPercentages', []):
            client_name = client_percentage['client']

            # Accumulate values for each client name
            result_dict[entity_name][client_name] += (client_percentage['percentage'] * 100) / total_pools

# Print the final result dictionary
print(json.dumps(result_dict, indent=2))
