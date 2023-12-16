import pandas as pd

def remove_duplicates(input_file, output_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Drop duplicate rows while keeping the first occurrence
    df.drop_duplicates(keep='first', inplace=True)

    # Write the modified DataFrame to a new CSV file
    df.to_csv(output_file, index=False)

# Specify the input and output file paths
input_file_path = 'database_official.csv'
output_file_path = 'database_official_postprocessed.csv'

# Call the function to remove duplicates
remove_duplicates(input_file_path, output_file_path)