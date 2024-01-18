import json
import csv


def collate_operators_vs_pools(
    input_file="collated.json",
    json_output_file="operators_vs_pools.json",
    csv_output_file="operators_vs_pools.csv",
):
    # Read the input JSON file
    with open(input_file, "r") as infile:
        data = json.load(infile)

    # Create a dictionary to store the desired output
    output_data = {}

    poollist = []

    # Iterate through each entry in the input data
    for entry in data:
        display_name = entry["displayName"]
        total_validator_count = entry["totalValidatorCount"]
        total_network_penetration = entry["totalNetworkPenetration"]

        pools = entry["pools"]
        pool_data = {}

        # Iterate through each pool in the entry
        for pool in pools:
            pool_name = pool["name"]
            validator_count = pool["validatorCount"]
            network_penetration = pool["networkPenetration"]

            if pool_name not in poollist:
                poollist.append(pool_name)

            # Add pool information to the dictionary
            pool_data[pool_name] = {
                "validatorCount": validator_count,
                "networkPenetration": network_penetration,
            }

        # Add entry information to the output dictionary
        output_data[display_name] = {
            "totalValidatorCount": total_validator_count,
            "totalNetworkPenetration": total_network_penetration,
            "pools": pool_data,
        }

    # Write the output data to a new JSON file
    print("\nCollating Operators vs. Pools\n")

    with open(json_output_file, "w") as outfile:
        json.dump(output_data, outfile, indent=2)

    # List of potential pools
    potential_pools = [
        "direct",
        "Stealth Pool",
        "Ledger Live",
        "Lido",
        "Swell",
        "Fireblocks",
        "Enzyme",
        "Coinbase",
        "Rocketpool",
        "StakeHound",
        "Stader - Permissionless",
        "Stader - Permissioned",
        "StakeWise",
        "Octant",
    ]

    with open(csv_output_file, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Writing header
        header = ["Node Operator", "Total Network Penetration"] + potential_pools
        writer.writerow(header)

        # Writing data
        for node_operator, node_data in output_data.items():
            total_network_penetration = node_data["totalNetworkPenetration"]
            pools_data = node_data["pools"]

            # Extracting network penetration for each pool
            pool_penetrations = [
                pools_data.get(pool, {}).get("networkPenetration", 0)
                for pool in potential_pools
            ]

            row = [node_operator, total_network_penetration] + pool_penetrations
            writer.writerow(row)

    print(f"CSV file '{csv_output_file}' has been created.\n")
