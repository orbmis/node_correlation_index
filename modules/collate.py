import json


def collate_data(input_file, output_file):
    print("\nCollating data. Reading data from input file . . .")

    # Read data from the input file
    with open(input_file, "r") as infile:
        data = json.load(infile)

    # Access the "data" property
    data_list = data.get("data", [])

    # Initialize a list to store the transformed data
    transformed_data = []

    # Iterate over each data object
    for obj in data_list:
        # Check if the object has the required properties
        if (
            "operatorTags" in obj
            and isinstance(obj["operatorTags"], list)
            and "displayName" in obj
        ):
            # Extract operator name from displayName
            operator_name = obj["displayName"]

            # Check if there is an entry in operatorTags with idType of "pool"
            pool_entry = next(
                (tag for tag in obj["operatorTags"] if tag.get("idType") == "pool"),
                None,
            )

            # Use the name of the pool entry if found, otherwise use "direct"
            pool_name = pool_entry["name"] if pool_entry else "direct"

            # Find existing entry for the operator_name
            operator_entry = next(
                (
                    entry
                    for entry in transformed_data
                    if entry["displayName"] == operator_name
                ),
                None,
            )

            # If no entry exists, create a new one
            if not operator_entry:
                operator_entry = {
                    "displayName": operator_name,
                    "totalValidatorCount": 0,
                    "totalNetworkPenetration": 0,
                    "pools": [],
                }
                transformed_data.append(operator_entry)

            # Create a pool object for the current pool or "direct"
            pool_object = {
                "name": pool_name,
                "relayerPercentages": obj.get("relayerPercentages", []),
                "clientPercentages": obj.get("clientPercentages", []),
                "validatorCount": obj.get("validatorCount", 0),
                "networkPenetration": obj.get("networkPenetration", 0),
            }

            # Add the pool object to the 'pools' array in the operator_entry
            operator_entry["pools"].append(pool_object)

            # Update totalValidatorCount and totalNetworkPenetration
            operator_entry["totalValidatorCount"] += pool_object.get(
                "validatorCount", 0
            )
            operator_entry["totalNetworkPenetration"] += pool_object.get(
                "networkPenetration", 0
            )

    # Write the transformed data to the output file
    with open(output_file, "w") as outfile:
        json.dump(transformed_data, outfile, indent=2)

    print("\nProcess completed\n")


if __name__ == "__main__":
    # Specify the input and output file names
    input_filename = "data.json"
    output_filename = "collated.json"

    # Call the function to transform the data
    collate_data(input_filename, output_filename)
