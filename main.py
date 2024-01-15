# main.py
import argparse

from modules.transform import transform_data
from modules.collate import collate_data
from modules.miga_labs_correlations import analyze_data
from modules.node_operators_HHI import analyze_node_operators_HHI
from modules.staking_pools_HHI import analyze_staking_pools_HHI
from modules.operators_vs_clients import collate_operators_vs_clients
from modules.operators_vs_pools import collate_operators_vs_pools
from modules.operators_vs_relayers import collate_operators_vs_relays

def main():
    parser = argparse.ArgumentParser(description='Your application description.')
    parser.add_argument('command', choices=['transform', 'collate', 'analyze-nodes', 'analyze-node-operators', 'analyze-staking-pools', 'operator-vs-clients', 'operator-vs-pools', 'operator-vs-relays'], help='Choose which script to run.')

    args = parser.parse_args()

    data_folder = 'data/'

    if args.command == 'transform':
        input_filename = data_folder + 'results.json'
        output_filename = data_folder + 'data.json'

        transform_data(input_filename, output_filename)
    elif args.command == 'collate':
        input_filename = data_folder + 'data.json'
        output_filename = data_folder + 'collated.json'

        collate_data(input_filename, output_filename)
    elif args.command == 'analyze-nodes':
        input_filename = data_folder + 'data.csv'

        analyze_data(input_filename)
    elif args.command == 'analyze-node-operators':
        input_filename = data_folder + 'collated.json'

        analyze_node_operators_HHI(input_filename)
    elif args.command == 'analyze-staking-pools':
        input_filename = data_folder + 'collated.json'

        analyze_staking_pools_HHI(input_filename)
    elif args.command == 'operator-vs-clients':
        input_file = data_folder + 'collated.json'
        json_output_file = data_folder + 'operators_vs_clients.json'
        csv_output_file = data_folder + 'operators_vs_clients.csv'

        collate_operators_vs_clients(input_file, json_output_file, csv_output_file)
    elif args.command == 'operator-vs-pools':
        input_file = data_folder + 'collated.json'
        json_output_file = data_folder + 'operators_vs_pools.json'
        csv_output_file = data_folder + 'operators_vs_pools.csv'

        collate_operators_vs_pools(input_file, json_output_file, csv_output_file)
    elif args.command == 'operator-vs-relays':
        input_file = data_folder + 'collated.json'
        json_output_file = data_folder + 'operators_vs_relays.json'
        csv_output_file = data_folder + 'operators_vs_relays.csv'

        collate_operators_vs_relays(input_file, json_output_file, csv_output_file)

if __name__ == "__main__":
    main()
