import json
import csv
import math

def calculate_common_percentage(operator1, operator2, property_name):
    percentages1 = {item[property_name]: item['percentage'] for pool in operator1['pools'] for item in pool[property_name + 'Percentages']}
    percentages2 = {item[property_name]: item['percentage'] for pool in operator2['pools'] for item in pool[property_name + 'Percentages']}
    
    common_percentages = {key: min(percentages1.get(key, 0), percentages2.get(key, 0)) for key in set(percentages1) & set(percentages2)}
    
    return sum(common_percentages.values())

# compare each pool in operator1 to each pool in operator2
# if the pool is the same, calculate the validatorCount percentage for each take the smallest percentage of the two
# the validatorCount percentage is defined as the percentage of the operators validators that the node operator runs for that staking pool
def calculate_common_pool_percentages(operator1, operator2):
    total_percentage = 0

    for pool1 in operator1['pools']:
        for pool2 in operator2['pools']:
            if pool1['name'] == pool2['name']:
                validator_count1 = pool1['validatorCount']
                validator_count2 = pool2['validatorCount']

                # Calculate the validatorCount percentage for each operator
                percentage1 = validator_count1 / operator1['totalValidatorCount']
                percentage2 = validator_count2 / operator2['totalValidatorCount']

                # Take the smallest percentage of the two
                common_percentage = min(percentage1, percentage2)

                print(pool1['name'], pool2['name'], percentage1, percentage2, math.floor(common_percentage))

                if math.floor(common_percentage) == 1519:
                    print(percentage1, percentage2, operator1['name'], operator2['name'])

                total_percentage += common_percentage
   
    # return the sum of all validatorCountPercentages
    return total_percentage

# File containin source data - should be the collated.json file derived from the raw rated.network dataset
file_path = 'collated.json'

# Load JSON data from file
with open(file_path, 'r') as file:
    data = json.load(file)

# Prepare CSV file
csv_file_path = 'output.csv'
csv_columns = ['Operator Name', 'Market Share Percentage', 'Common Pool Percentage', 'Common Client Percentage', 'Common Relay Percentage']

with open(csv_file_path, 'w', newline='') as csv_file:
    print('\ncalculating correlations . . .\n')

    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()

    # Iterate through each operator
    for i in range(len(data)):
        operator1 = data[i]
        
        # Initialize sums for each operator
        total_common_pools = 0
        total_common_client_percentage = 0
        total_common_relay_percentage = 0

        # Compare with each other operator
        for j in range(len(data)):
            if i != j:
                operator2 = data[j]

                # Calculate common client and relay percentages
                total_common_client_percentage += calculate_common_percentage(operator1, operator2, 'client')
                total_common_relay_percentage += calculate_common_percentage(operator1, operator2, 'relayer')

                # Calculate the number of common pools
                total_common_pools += calculate_common_pool_percentages(operator1, operator2)

        market_share = operator1.get('totalNetworkPenetration', 0)

        # Write to CSV
        writer.writerow({
            'Operator Name': operator1['displayName'],
            'Market Share Percentage': market_share,
            'Common Pool Percentage': total_common_pools,
            'Common Client Percentage': total_common_client_percentage,
            'Common Relay Percentage': total_common_relay_percentage
        })

print(f"CSV file created at {csv_file_path}\n")
