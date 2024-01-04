import pandas as pd
import numpy as np
from tqdm import tqdm

# Calculate the standard Herfindahl–Hirschman Index (HHI)
def calculate_standard_hhi(data):
    # TODO: we need to add a new column to the dataframe called "market_share"
    total_market_share = sum(data['att_subnets'])
    standard_hhi = sum((market_share / total_market_share) ** 2 for market_share in data['att_subnets'])

    return standard_hhi

# Calculate the correlation coefficient using the Kronecker delta function
def calculate_correlation_coefficient(x, y):
    n = len(x)
    delta_sum = sum(1 for xi, yi in zip(x, y) if xi == yi)
    return delta_sum / n

# Calculate the modified Herfindahl–Hirschman Index (HHI') and correlation matrix
def calculate_modified_hhi(data):
    num_entities = len(data)
    num_attributes = len(data.columns) - 1  # Exclude the 'index' column

    hhi_prime = 0.0
    correlation_matrix = np.zeros((num_entities, num_entities))

    for i in tqdm(range(num_entities), desc='Calculating HHI', unit='entity'):
        for j in range(num_entities):
            x_values = data.iloc[i, 2:]
            y_values = data.iloc[j, 2:]

            c_ij = calculate_correlation_coefficient(x_values, y_values)
            correlation_matrix[i][j] = c_ij

            # to calculate the modified HHI, we need to market share
            # so `att_subnets` should actually be `market_share`
            # but a node is a node, the market share is always 1
            n_i = data['att_subnets'].iloc[i]
            n_j = data['att_subnets'].iloc[j]

            # Normalize the product of market shares using the square root
            normalized_product = np.sqrt(n_i * n_j)

            # hhi_prime += normalized_product * c_ij
            hhi_prime += c_ij

    return hhi_prime, correlation_matrix

# Read the original CSV file and transform it into a DataFrame
file_path = 'data.csv'
raw_data = pd.read_csv(file_path)

data = raw_data[raw_data['att_subnets'] == 64]

print('\nCalculating the Correlation Coefficients and modified HHI for node operators...\n\n')

# Example usage with the DataFrame
hhi_result, correlation_matrix = calculate_modified_hhi(data)
print(f"\nModified HHI: {hhi_result}")
print("\nCorrelation Matrix:")
print(correlation_matrix)
print('\n\n')

standard_hhi_result = calculate_standard_hhi(data)
print(f"Standard HHI: {standard_hhi_result}")
print('\n\n')
