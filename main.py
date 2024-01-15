# main.py
import argparse

from transform import transform_data
from collate import collate_data
from miga_labs_correlations import analyze_data
from node_operators_HHI import analyze_node_operators_HHI
from staking_pools_HHI import analyze_staking_pools_HHI
from operators_vs_clients import collate_operators_vs_clients
from operators_vs_pools import collate_operators_vs_pools
from operators_vs_relayers import collate_operators_vs_relays

def main():
    parser = argparse.ArgumentParser(description='Your application description.')
    parser.add_argument('command', choices=['transform', 'collate', 'analyze-nodes', 'analyze-node-operators', 'analyze-staking-pools', 'operator-vs-clients', 'operator-vs-pools', 'operator-vs-relays'], help='Choose which script to run.')

    args = parser.parse_args()

    if args.command == 'transform':
        input_filename = 'results.json'
        output_filename = 'data.json'

        transform_data(input_filename, output_filename)
    elif args.command == 'collate':
        input_filename = 'data.json'
        output_filename = 'collated.json'

        collate_data(input_filename, output_filename)
    elif args.command == 'analyze-nodes':
        input_filename = 'data.csv'

        analyze_data(input_filename)
    elif args.command == 'analyze-node-operators':
        input_filename = 'collated.json'

        analyze_node_operators_HHI(input_filename)
    elif args.command == 'analyze-staking-pools':
        input_filename = 'collated.json'

        analyze_staking_pools_HHI(input_filename)
    elif args.command == 'operator-vs-clients':
        input_file='collated.json'
        json_output_file='operators_vs_clients.json'
        csv_output_file='operators_vs_clients.csv'

        collate_operators_vs_clients(input_file, json_output_file, csv_output_file)
    elif args.command == 'operator-vs-pools':
        collate_operators_vs_pools()
    elif args.command == 'operator-vs-relays':
        collate_operators_vs_relays()

if __name__ == "__main__":
    main()
