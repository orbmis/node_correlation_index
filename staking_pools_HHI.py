import math
import json

def calculate_standard_hhi(data):
    hhi = 0.0

    for entity in data:
        market_share = entity[1] * 100  # Extracting market share from the first element
        hhi += market_share ** 2

    return hhi

def calculate_modified_hhi(data):
    # Initialize lists to store unique relays, clients, and pools
    relays = ["manifold", "bloxroute_maxprofit", "agnostic", "no_mev_boost", "bloxroute_regulated", "ultra_sound_money", "aestus", "flashbots", "edennetwork"]
    clients = ["Nimbus", "Prysm", "Lighthouse", "Teku", "Lodestar", "Unknown"]
    operators = set() 
    pool_names = set()

    # Create dictionaries to store relay and client percentages for each pool
    node_operators = {}
    relay_percentages = {}
    client_percentages = {}
    market_shares = {}

    # Iterate over the data and populate relay_percentages and client_percentages dictionaries
    for item in data:
        for pool in item["pools"]:
            pool_name = pool["name"]
            pool_names.add(pool_name)

            relay_percentages.setdefault(pool_name, {})
            client_percentages.setdefault(pool_name, {})
            market_shares.setdefault(pool_name, 0)
            market_shares[pool_name] += pool["networkPenetration"]
            node_operators.setdefault(pool_name, {})
            node_operators[pool_name][item["displayName"]] = node_operators[pool_name].get(item["displayName"], 0) + pool["networkPenetration"]
            operators.add(item["displayName"])


            for relay in relays:
                relay_percentage = 0.0
                for relayer in pool["relayerPercentages"]:
                    if relayer["relayer"] == relay:
                        relay_percentage = relayer["percentage"] * 100
                        break
                relay_percentages[pool_name].setdefault(relay, []).append(relay_percentage)

            for client in clients:
                client_percentage = 0.0
                for client_percent in pool["clientPercentages"]:
                    if client_percent["client"] == client:
                        client_percentage = client_percent["percentage"] * 100
                        break
                client_percentages[pool_name].setdefault(client, []).append(client_percentage)
    
    # After calculating relay_percentages, modify it to store the average value for each relay
    for pool_name, relay_values in relay_percentages.items():
        for relay, percentages in relay_values.items():
            if percentages:
                # Calculate the average value and replace the array with the average
                average_value = sum(percentages) / len(percentages)
                relay_percentages[pool_name][relay] = average_value
            else:
                # Handle the case where there are no values for the relay
                relay_percentages[pool_name][relay] = 0.0
    
    # After calculating client_percentages, modify it to store the average value for each client
    for pool_name, client_values in client_percentages.items():
        for client, percentages in client_values.items():
            if percentages:
                # Calculate the average value and replace the array with the average
                average_value = sum(percentages) / len(percentages)
                client_percentages[pool_name][client] = average_value
            else:
                # Handle the case where there are no values for the client
                client_percentages[pool_name][client] = 0.0

    # Create a matrix for HHI calculation
    matrix = []

    for pool_name in pool_names:
        row = [pool_name]
        row.append(market_shares[pool_name])
        row.append(relay_percentages[pool_name])
        row.append(client_percentages[pool_name])
        row.append(node_operators[pool_name])
        matrix.append(row)

    # uncomment this line to view the final matrix that is used for the HHI calculation
    # print(json.dumps(matrix, indent=4, sort_keys=True))

    standard_hhi = calculate_standard_hhi(matrix)

    # Calculate HHI' value
    modified_hhi = 0.0

    for i in range(len(matrix)):
        row_correlation_value = 0.0

        for j in range(len(matrix)):
            n_i = matrix[i][1] # market share of pool i
            n_j = matrix[j][1] # market share of pool j

            relays_correlation = 0.0
            for relay in relays:
                relays_correlation += min(matrix[i][2][relay], matrix[j][2][relay])

            clients_correlation = 0.0
            for clients in clients:
                clients_correlation += min(matrix[i][3][client], matrix[j][3][client])

            operators_correlation = 0.0
            for operator in operators:
                operators_correlation += min(matrix[i][4].get(operator, 0), matrix[j][4].get(operator, 0))

            c_ij = relays_correlation + clients_correlation + operators_correlation

            row_correlation_value += ((n_i * n_j) * c_ij) * 100

        modified_hhi += row_correlation_value

    return standard_hhi, modified_hhi

json_data = []

file_path = 'collated.json'

# Load JSON data from file
with open(file_path, 'r') as file:
    json_data = json.load(file)

print("\nCalculating modified HHI for Staking Pools . . .\n")

# Calculate HHI values
hhi = calculate_modified_hhi(json_data)
standard_hhi = hhi[0]
modified_hhi = hhi[1]

print("Standard HHI Value:", round(standard_hhi))
print("Modified HHI Value:", round(modified_hhi))

print("\n")