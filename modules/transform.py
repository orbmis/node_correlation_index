import json


def transform_data(input_file, output_file):
    print("Transforming rated network raw data . . .")

    # Read data from the input file
    with open(input_file, "r") as infile:
        results = json.load(infile)

    # Extract the 'data' field from each object
    data_objects = [item.get("data", []) for item in results]

    # Flatten the list of data objects
    flattened_data = [item for sublist in data_objects for item in sublist]

    # Create a new dictionary for the transformed data
    transformed_data = {"data": flattened_data}

    # Write the transformed data to the output file
    with open(output_file, "w") as outfile:
        json.dump(transformed_data, outfile, indent=2)

    print("\nProcess Completed\n")


if __name__ == "__main__":
    # Specify the input and output file names
    input_filename = "results.json"
    output_filename = "data.json"

    # Call the function to transform the data
    transform_data(input_filename, output_filename)
