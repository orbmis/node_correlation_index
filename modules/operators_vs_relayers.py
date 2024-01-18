import json

def collate_operators_vs_relays(input_file='collated.json', json_output_file='operators_vs_relayers.json', csv_output_file='operators_vs_relayers.csv'):
    # Load the data
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    # Create a dictionary to store the result
    result_dict = {}

    # Iterate over each object in the top-level array
    for entity in data:
        entity_name = entity['displayName']
        result_dict[entity_name] = {}
        result_dict[entity_name]['network_penetration'] = entity.get('totalNetworkPenetration') * 100
        result_dict[entity_name]['relayers'] = {}

        # Initialize dictionary with zero values for all client names
        for pool in entity.get('pools', []):
            for relayer_percentage in pool.get('relayerPercentages', []):
                relayer_name = relayer_percentage['relayer']
                result_dict[entity_name]['relayers'][relayer_name] = 0

        total_pools = 0
        for pool in entity.get('pools', []):
            total_pools += 1

        # Iterate over each pool in the entity
        for pool in entity.get('pools', []):
            for relayer_percentage in pool.get('relayerPercentages', []):
                relayer_name = relayer_percentage['relayer']

                # Accumulate values for each client name
                result_dict[entity_name]['relayers'][relayer_name] += (relayer_percentage['percentage'] * 100) / total_pools

    # Print the final result dictionary
    print("\nCollating Operators vs. Relayers\n")

    with open(json_output_file, 'w', encoding='utf-8') as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)
