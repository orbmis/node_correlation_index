import pandas as pd
from scipy.stats import chi2_contingency
import logging
from tqdm import tqdm
import csv
from io import StringIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def array_to_csv_string(data_array):
    """
    Convert a two-dimensional array to a CSV string.

    Parameters:
    - data_array: list of lists
        The two-dimensional array to be converted.

    Returns:
    - csv_string: str
        The CSV string representation of the input array.
    """

    # Create an in-memory text stream
    csv_stream = StringIO()

    # Create a CSV writer
    csv_writer = csv.writer(csv_stream, delimiter=',')

    # Write the rows to the CSV stream
    csv_writer.writerows(data_array)

    # Get the CSV string from the stream
    csv_string = csv_stream.getvalue()

    # Close the stream
    csv_stream.close()

    return csv_string

def sort_and_get_top_entries(data_array, n=25):
    """
    Sort a 2D array by the last column in descending order and return the top n entries.

    Parameters:
    - data_array: list of lists
        The 2D array to be sorted.
    - n: int, optional
        The number of top entries to return (default is 25).

    Returns:
    - top_entries: list of lists
        The top n entries after sorting.
    """

    # Sort the array by the last column in descending order
    sorted_array = sorted(data_array, key=lambda x: x[-1], reverse=True)

    # Return the top n entries
    top_entries = sorted_array[:n]

    # Extract the first values from the first column of the top n entries
    top_first_column_entries = [entry[0] for entry in sorted_array[:n]]

    return top_first_column_entries

def get_hamming(df_full, attributes):
    # df = df_full.head(100)
    df = df_full

    matrix = [[0 for x in range(len(attributes) + 2)] for y in range(len(df))] 

    # attribute index - initiated to one to avoid comparison of "index" column
    n = 1

    for attribute in attributes:
        for i in tqdm(range(len(df) - 1), desc='Calculating Hamming Weights for ' + attribute, unit='entity'):
            hamming_weight = 0
            matrix[i][0] = df.at[i, 'index']

            for j in range(len(df) - 1):
                matrix[i][n] += int(df.at[i, attribute] == df.at[j, attribute])

        n += 1

    # iterate over array and add the sum of all "hamming weights as precentage of total records"
    for k in range(len(df) - 1):
        matrix[k][5] = sum(matrix[k][1:5]) / len(df)

    return matrix

# Cramér's V calculation method
def cramers_v(table):
    chi2, _, _, _ = chi2_contingency(table)
    n = table.sum().sum()
    phi2 = chi2 / n
    r, k = table.shape
    phi2corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    rcorr = r - ((r - 1) ** 2) / (n - 1)
    kcorr = k - ((k - 1) ** 2) / (n - 1)
    return (phi2corr / min((kcorr - 1), (rcorr - 1))) ** 0.5

def analyze_data(file_path='data.csv'):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)

    # Create a list of attribute columns to compare
    attribute_columns = df.columns[1:]

    print("\nProcessing data . . .")

    # Perform pairwise attribute comparison and calculate chi-squared values
    for i in range(len(attribute_columns) - 1):
        for j in range(i + 1, len(attribute_columns)):
            attr1 = attribute_columns[i]
            attr2 = attribute_columns[j]

            # Create a contingency table
            contingency_table = pd.crosstab(df[attr1], df[attr2])

            print(f"\nPairwise Comparison: {attr1} vs {attr2}")
            # logger.info(f"Contingency Table:\n{contingency_table}")

            # Calculate chi-squared statistic and p-value
            chi2, p, _, _ = chi2_contingency(contingency_table)

            print(f"Chi-squared Value: {chi2}")
            print(f"P-value: {p}")

            # Calculate Cramér's V
            v = cramers_v(contingency_table)
            print(f"Cramér's V: {v}")

    print("\n\n")

    attributes_to_compare = ['country_code', 'client_name', 'isp_alias', 'att_subnets']

    resulting_hamming_weights = get_hamming(df, attributes_to_compare)

    hamming_csv = array_to_csv_string(resulting_hamming_weights)

    # Print or use resulting_hamming_weights as needed
    print(hamming_csv)

    print("\n")

    # Call the function with the default value of n (25)
    result = sort_and_get_top_entries(resulting_hamming_weights, 10)

    for x in result:
        print(df.iloc[x])

    # Print or use the result as needed
    print(result)

if __name__ == "__main__":
    analyze_data()


# TODO: once we sort the results in ascending order, we can iterate over each record to determine which attribute has the highest hamming weight
# this will result in a table of "index,attrbute", where "attribute" is the attribute with the highest correlation to other node for that record
# which will naturally be the value that occurs the most
# this will allows us to see which out of the records with the highest overall correlation value, which attributes are most correlated

print("\n\n")


# Interpretation:
#
#    Pairwise Comparison: country_code vs client_name
#        Chi-squared Value: 866.56
#        P-value: 4.67×10−514.67×10−51
#        Cramér's V: 0.22
#        Interpretation: There is a significant association between country_code and client_name. The Cramér's V value (0.22) indicates a small-to-medium strength of association.
#
#    Pairwise Comparison: country_code vs isp_alias
#        Chi-squared Value: 83766.05
#        P-value: 0.0
#        Cramér's V: 0.82
#        Interpretation: There is a highly significant association between country_code and isp_alias. The Cramér's V value (0.82) indicates a strong association.
#
#    Pairwise Comparison: country_code vs att_subnets
#        Chi-squared Value: 4625.32
#        P-value: 1.23×10−481.23×10−48
#        Cramér's V: 0.12
#        Interpretation: There is a significant association between country_code and att_subnets. The Cramér's V value (0.12) indicates a small strength of association.
#
#    Pairwise Comparison: client_name vs isp_alias
#        Chi-squared Value: 2409.07
#        P-value: 2.52×10−132.52×10−13
#        Cramér's V: 0.21
#        Interpretation: There is a significant association between client_name and isp_alias. The Cramér's V value (0.21) indicates a small-to-medium strength of association.
#
#    Pairwise Comparison: client_name vs att_subnets
#        Chi-squared Value: 969.73
#        P-value: 3.91×10−563.91×10−56
#        Cramér's V: 0.23
#        Interpretation: There is a significant association between client_name and att_subnets. The Cramér's V value (0.23) indicates a small-to-medium strength of association.
#
#    Pairwise Comparison: isp_alias vs att_subnets
#        Chi-squared Value: 30525.86
#        P-value: 0.0
#        Cramér's V: 0.31
#        Interpretation: There is a highly significant association between isp_alias and att_subnets. The Cramér's V value (0.31) indicates a moderate strength of association.