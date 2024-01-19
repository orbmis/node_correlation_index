import json
import math
import csv


def collate_operators_vs_relays(
    input_file="collated.json",
    json_output_file="operators_vs_relayers.json",
    csv_output_file="operators_vs_relayers.csv",
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
        result_dict[entity_name]["relayers"] = {}

        # Initialize dictionary with zero values for all relayer names
        for pool in entity.get("pools", []):
            for relayer_percentage in pool.get("relayerPercentages", []):
                relayer_name = relayer_percentage["relayer"]
                result_dict[entity_name]["relayers"][relayer_name] = 0

        total_pools = 0
        for pool in entity.get("pools", []):
            total_pools += 1

        # Iterate over each pool in the entity
        for pool in entity.get("pools", []):
            for relayer_percentage in pool.get("relayerPercentages", []):
                relayer_name = relayer_percentage["relayer"]

                # Accumulate values for each relayer name
                result_dict[entity_name]["relayers"][relayer_name] += (
                    relayer_percentage["percentage"] * 100
                ) / total_pools

    # Print the final result dictionary
    print("\nCollating Operators vs. Relayers\n")

    with open(json_output_file, "w", encoding="utf-8") as f:
        json.dump(result_dict, f, ensure_ascii=False, indent=2)

    # Writing to CSV
    with open(csv_output_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Writing header
        header = [
            "Network Penetration",
            *next(iter(result_dict.values()))["relayers"].keys(),
        ]
        writer.writerow(header)

        # Writing data
        for network_name, network_data in result_dict.items():
            network_penetration = network_data["network_penetration"]
            relayers_data = network_data["relayers"]
            row = [network_penetration, *relayers_data.values()]
            writer.writerow(row)

    print(f"CSV file '{csv_output_file}' has been created.")


def calculate_average_relayer_percentage_by_decile(
    json_data, num_deciles=10, potential_relays=None
):
    if potential_relays is None:
        potential_relays = [
            "manifold",
            "no_mev_boost",
            "agnostic",
            "aestus",
            "bloxroute_regulated",
            "edennetwork",
            "ultra_sound_money",
            "bloxroute_maxprofit",
            "flashbots",
        ]

    # Initialize decile data structure
    decile_data = {
        i: {relay: [] for relay in potential_relays} for i in range(num_deciles)
    }

    # Populate decile data structure
    for node_operator, node_data in json_data.items():
        decile = math.floor(node_data["network_penetration"])
        relays_data = node_data["relayers"]

        for relay in potential_relays:
            relay_percentage = relays_data.get(relay, 0)
            decile_data[decile][relay].append(relay_percentage)

    # Calculate average percentage for each relayer in each decile
    average_data = {
        i: {
            relay: sum(percentages) / len(percentages) if len(percentages) > 0 else 0
            for relay, percentages in decile_data[i].items()
        }
        for i in range(num_deciles)
    }

    # Writing to CSV
    csv_filename = "data/average_relayer_percentage_by_decile.csv"

    with open(csv_filename, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Writing header
        header = ["Network Penetration"] + potential_relays
        writer.writerow(header)

        # Writing data
        for decile, relay_percentages in average_data.items():
            row = [f"{decile * 10}-{(decile + 1) * 10 - 1}"] + [
                relay_percentages[relay] for relay in potential_relays
            ]
            writer.writerow(row)

    print(f"CSV file '{csv_filename}' has been created.\n")
