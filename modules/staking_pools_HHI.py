import math
import json
import numpy as np


def calculate_r_squared(data, x, y):
    """
    Calculate R^2 value from Pearson's correlation coefficient for the 3rd and 4th values across all elements.

    Parameters:
    - data: Two-dimensional array containing the relevant data.

    Returns:
    - r_squared: R^2 value.
    """
    # Extract the relevant columns for calculation (3rd and 4th values)
    x_values = [row[x] for row in data[1:]]
    y_values = [row[y] for row in data[1:]]

    # Calculate the mean of x_values and y_values
    mean_x = sum(x_values) / len(x_values)
    mean_y = sum(y_values) / len(y_values)

    # Calculate Pearson's correlation coefficient (r)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
    denominator_x = sum((x - mean_x) ** 2 for x in x_values)
    denominator_y = sum((y - mean_y) ** 2 for y in y_values)

    r = numerator / (denominator_x**0.5 * denominator_y**0.5)

    # Calculate R^2 from Pearson's correlation coefficient
    r_squared = r**2

    return r_squared


def calculate_coefficient_of_variation(data):
    """
    Calculate the coefficient of variation for a given array of real numbers.

    Parameters:
    - data: list of real numbers

    Returns:
    - coefficient_of_variation: float
    """
    mean_value = 0

    # Calculate the mean
    if len(data) != 0:
        mean_value = sum(data) / len(data)

    # Calculate the sum of squared differences from the mean
    sum_squared_diff = sum((x - mean_value) ** 2 for x in data)

    std_dev = 0

    # Calculate the standard deviation
    if (len(data) - 1) ** 0.5 != 0:
        std_dev = (sum_squared_diff / (len(data) - 1)) ** 0.5

    # Calculate the coefficient of variation
    coefficient_of_variation = 0

    if mean_value != 0:
        coefficient_of_variation = (std_dev / mean_value) * 100

    return coefficient_of_variation


def calculate_variability(data):
    # Extracting relevant data
    names = [entry[0] for entry in data]
    market_shares = [entry[1] for entry in data]
    relay_percentages = [
        list(value for value in entry[2].values() if value != 0) for entry in data
    ]
    client_percentages = [
        list(value for value in entry[3].values() if value != 0) for entry in data
    ]
    node_operators = [
        list(value for value in entry[4].values() if value != 0) for entry in data
    ]

    # Calculate covariance
    relay_covariance = [
        calculate_coefficient_of_variation(category) for category in relay_percentages
    ]
    client_covariance = [
        calculate_coefficient_of_variation(category) for category in client_percentages
    ]
    node_operator_covariance = [
        calculate_coefficient_of_variation(category) for category in node_operators
    ]

    # Create the result array
    result = [
        [
            "name",
            "market share",
            "relay covariance",
            "client covariance",
            "node operator covariance",
        ]
    ]

    # Populate the result array with calculated values
    for i in range(len(data)):
        result.append(
            [
                names[i],
                market_shares[i],
                relay_covariance[i],
                client_covariance[i],
                node_operator_covariance[i],
            ]
        )

    return result


def calculate_standard_hhi(data):
    hhi = 0.0

    for entity in data:
        market_share = entity[1] * 100  # Extracting market share from the first element
        hhi += market_share**2

    return hhi


def calculate_modified_hhi(data):
    # Initialize lists to store unique relays, clients, and pools
    relays = [
        "manifold",
        "bloxroute_maxprofit",
        "agnostic",
        "no_mev_boost",
        "bloxroute_regulated",
        "ultra_sound_money",
        "aestus",
        "flashbots",
        "edennetwork",
    ]
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
            node_operators[pool_name][item["displayName"]] = (
                node_operators[pool_name].get(item["displayName"], 0)
                + pool["networkPenetration"]
            )
            operators.add(item["displayName"])

            for relay in relays:
                relay_percentage = 0.0
                for relayer in pool["relayerPercentages"]:
                    if relayer["relayer"] == relay:
                        relay_percentage = relayer["percentage"] * 100
                        break
                relay_percentages[pool_name].setdefault(relay, []).append(
                    relay_percentage
                )

            for client in clients:
                client_percentage = 0.0
                for client_percent in pool["clientPercentages"]:
                    if client_percent["client"] == client:
                        client_percentage = client_percent["percentage"] * 100
                        break
                client_percentages[pool_name].setdefault(client, []).append(
                    client_percentage
                )

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

    cvs = calculate_variability(matrix)
    # print(json.dumps(cvs, indent=2))

    marketshare_clients = calculate_r_squared(cvs, 1, 3)
    marketshare_relays = calculate_r_squared(cvs, 1, 2)
    marketshare_operators = calculate_r_squared(cvs, 1, 4)
    relays_clients = calculate_r_squared(cvs, 2, 3)
    relays_operators = calculate_r_squared(cvs, 2, 4)
    clients_operators = calculate_r_squared(cvs, 3, 4)

    print(
        "\nR^2 for variability between market share and clients:",
        round(marketshare_clients, 2),
    )
    print(
        "R^2 for variability between market share and relays:",
        round(marketshare_relays, 2),
    )
    print(
        "R^2 for variability between market share and operators:",
        round(marketshare_operators, 2),
    )
    print("R^2 for variability between relays and clients:", round(relays_clients, 2))
    print(
        "R^2 for variability between relays and node operators:",
        round(relays_operators, 2),
    )
    print(
        "R^2 for variability between clients and node operators:",
        round(clients_operators, 2),
    )
    print("\n")

    standard_hhi = calculate_standard_hhi(matrix)

    # Calculate HHI' value
    modified_hhi = 0.0

    # print(json.dumps(matrix, indent=2))

    for i in range(len(matrix)):
        row_correlation_value = 0.0

        for j in range(len(matrix)):
            n_i = matrix[i][1]  # market share of pool i
            n_j = matrix[j][1]  # market share of pool j

            relays_correlation = 0.0

            for relay in relays:
                relays_correlation += min(matrix[i][2][relay], matrix[j][2][relay])

            clients_correlation = 0.0

            for client in clients:
                clients_correlation += min(matrix[i][3][client], matrix[j][3][client])

            operators_correlation = 0.0

            for operator in operators:
                operators_correlation += min(
                    matrix[i][4].get(operator, 0), matrix[j][4].get(operator, 0)
                )

            c_ij = relays_correlation + clients_correlation + operators_correlation

            row_correlation_value += ((n_i * n_j) * c_ij) * 100

        modified_hhi += row_correlation_value

    return standard_hhi, modified_hhi


def analyze_staking_pools_HHI(file_path="collated.json"):
    # Load JSON data from file
    with open(file_path, "r") as file:
        json_data = json.load(file)

    print("\nCalculating modified HHI for Staking Pools . . .\n")

    # Calculate HHI values
    hhi = calculate_modified_hhi(json_data)
    standard_hhi = hhi[0]
    modified_hhi = hhi[1]

    print("Standard HHI Value:", round(standard_hhi))
    print("Modified HHI Value:", round(modified_hhi))

    print("\n")


if __name__ == "__main__":
    analyze_staking_pools_HHI()
