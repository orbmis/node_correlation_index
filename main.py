# main.py
import argparse
import json
from modules.transform import transform_data
from modules.collate import collate_data
from modules.miga_labs_correlations import analyze_data
from modules.node_operators_HHI import analyze_node_operators_HHI
from modules.staking_pools_HHI import analyze_staking_pools_HHI
from modules.operators_vs_clients import collate_operators_vs_clients
from modules.operators_vs_clients import calculate_average_client_percentage_by_decile
from modules.operators_vs_pools import collate_operators_vs_pools
from modules.operators_vs_relayers import collate_operators_vs_relays
from modules.operators_vs_relayers import calculate_average_relayer_percentage_by_decile

data_folder = "data/"


def transform():
    input_filename = f"{data_folder}/results.json"
    output_filename = f"{data_folder}/data.json"
    transform_data(input_filename, output_filename)


def collate():
    input_filename = f"{data_folder}/data.json"
    output_filename = f"{data_folder}/collated.json"
    collate_data(input_filename, output_filename)


def analyze_nodes():
    _, _, _, input_filename = get_filenames(data_folder, "data")
    analyze_data(input_filename)


def analyze_node_operators():
    input_filename, _, _, _ = get_filenames(data_folder, "collated")
    analyze_node_operators_HHI(input_filename)


def analyze_staking_pools():
    input_filename, _, _, _ = get_filenames(data_folder, "collated")
    analyze_staking_pools_HHI(input_filename)


def operator_vs_clients():
    _, _, json_output_file, csv_output_file = get_filenames(
        data_folder, "operators_vs_clients"
    )
    input_file = f"{data_folder}/collated.json"

    collate_operators_vs_clients(input_file, json_output_file, csv_output_file)

    with open("data/operators_vs_clients.json", "r") as json_file:
        json_data = json.load(json_file)
        calculate_average_client_percentage_by_decile(json_data)


def operator_vs_pools():
    input_file, _, json_output_file, csv_output_file = get_filenames(
        data_folder, "operators_vs_pools"
    )
    input_file = f"{data_folder}/collated.json"

    collate_operators_vs_pools(input_file, json_output_file, csv_output_file)


def operator_vs_relays():
    input_file, _, json_output_file, csv_output_file = get_filenames(
        data_folder, "operators_vs_relays"
    )
    input_file = f"{data_folder}/collated.json"

    collate_operators_vs_relays(input_file, json_output_file, csv_output_file)

    with open("data/operators_vs_relays.json", "r") as json_file:
        json_data = json.load(json_file)
        calculate_average_relayer_percentage_by_decile(json_data)


def get_filenames(data_folder, file_prefix):
    input_filename = f"{data_folder}{file_prefix}.json"
    output_filename = f"{data_folder}{file_prefix}.json"
    json_output_file = f"{data_folder}{file_prefix}.json"
    csv_output_file = f"{data_folder}{file_prefix}.csv"

    return input_filename, output_filename, json_output_file, csv_output_file


def main():
    parser = argparse.ArgumentParser(description="Your application description.")
    parser.add_argument(
        "command",
        choices=[
            "transform",
            "collate",
            "analyze-nodes",
            "analyze-node-operators",
            "analyze-staking-pools",
            "operators-vs-clients",
            "operators-vs-pools",
            "operators-vs-relays",
            "run-analysis",
        ],
        help="Choose which script to run.",
    )

    args = parser.parse_args()
    data_folder = "data/"

    commands = {
        "transform": transform,
        "collate": collate,
        "analyze-node-operators": analyze_node_operators,
        "analyze-staking-pools": analyze_staking_pools,
        "operators-vs-clients": operator_vs_clients,
        "operators-vs-pools": operator_vs_pools,
        "operators-vs-relays": operator_vs_relays,
        "analyze-nodes": analyze_nodes,
    }

    command_list = list(commands.values())

    selected_command = commands.get(args.command)

    if args.command == "run-analysis":
        for method in command_list:
            method()
            print("-" * 80)
    elif selected_command:
        selected_command()
    else:
        print("Invalid command. Please choose a valid command.")


if __name__ == "__main__":
    main()
