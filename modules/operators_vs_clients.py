import json
import math
import csv


def collate_operators_vs_clients(
    input_file="collated.json",
    json_output_file="operators_vs_clients.json",
    csv_output_file="operators_vs_clients.csv",
):
    # Load the data
    with open(input_file, "r") as infile:
        data = json.load(infile)

    # Create a dictionary to store the result
    result_dict = {}

    # Iterate over each object in the top-level array
    for entity in data:
        entity_name = entity["displayName"]
        result_dict[entity_name] = {}
        result_dict[entity_name]["network_penetration"] = (
            entity.get("totalNetworkPenetration") * 100
        )
        result_dict[entity_name]["clients"] = {}

        # Initialize dictionary with zero values for all client names
        for pool in entity.get("pools", []):
            for client_percentage in pool.get("clientPercentages", []):
                client_name = client_percentage["client"]
                result_dict[entity_name]["clients"][client_name] = 0
                result_dict[entity_name]["clients"]["Prysm"] = 0
                result_dict[entity_name]["clients"]["Nimbus"] = 0
                result_dict[entity_name]["clients"]["Lighthouse"] = 0
                result_dict[entity_name]["clients"]["Teku"] = 0
                result_dict[entity_name]["clients"]["Lodestar"] = 0
                result_dict[entity_name]["clients"]["Unknown"] = 0

        total_pools = 0

        for pool in entity.get("pools", []):
            total_pools += 1

        # Iterate over each pool in the entity
        for pool in entity.get("pools", []):
            for client_percentage in pool.get("clientPercentages", []):
                client_name = client_percentage["client"]

                # Accumulate values for each client name
                result_dict[entity_name]["clients"][client_name] += (
                    client_percentage["percentage"] * 100
                ) / total_pools

    # Print the final result dictionary
    print("\nCollating Operators vs. Clients\n")

    with open(json_output_file, "w", encoding="utf-8") as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)

    # Writing to CSV
    with open(csv_output_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Writing header
        header = [
            "Network Penetration",
            *next(iter(result_dict.values()))["clients"].keys(),
        ]
        writer.writerow(header)

        # Writing data
        for network_name, network_data in result_dict.items():
            network_penetration = network_data["network_penetration"]
            clients_data = network_data["clients"]
            row = [network_penetration, *clients_data.values()]
            writer.writerow(row)

    print(f"CSV file '{csv_output_file}' has been created.")


def calculate_average_client_percentage_by_decile(
    json_data, num_deciles=10, potential_clients=None
):
    if potential_clients is None:
        potential_clients = [
            "Nimbus",
            "Prysm",
            "Lighthouse",
            "Teku",
            "Lodestar",
            "Unknown",
        ]

    # Initialize decile data structure
    decile_data = {
        i: {client: [] for client in potential_clients} for i in range(num_deciles)
    }

    # Populate decile data structure
    for node_operator, node_data in json_data.items():
        decile = math.floor(node_data["network_penetration"])
        clients_data = node_data["clients"]

        for client in potential_clients:
            client_percentage = clients_data.get(client, 0)
            decile_data[decile][client].append(client_percentage)

    # Calculate average percentage for each client in each decile
    average_data = {
        i: {
            client: sum(percentages) / len(percentages) if len(percentages) > 0 else 0
            for client, percentages in decile_data[i].items()
        }
        for i in range(num_deciles)
    }

    # Writing to CSV
    csv_filename = "data/average_client_percentage_by_decile.csv"

    with open(csv_filename, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Writing header
        header = ["Network Penetration"] + potential_clients
        writer.writerow(header)

        # Writing data
        for decile, client_percentages in average_data.items():
            row = [f"{decile * 10}-{(decile + 1) * 10 - 1}"] + [
                client_percentages[client] for client in potential_clients
            ]
            writer.writerow(row)

    print(f"CSV file '{csv_filename}' has been created.\n")


if __name__ == "__main__":
    collate_operators_vs_clients()
    with open("operators_vs_clients.json", "r") as json_file:
        json_data = json.load(json_file)
        calculate_average_client_percentage_by_decile(json_data)
