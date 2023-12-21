import csv
import json

csv_file = 'database_official_postprocessed_final.csv'
json_file = 'sample.json'

data = []

# Read the CSV file with the correct encoding
with open(csv_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

# Write the data to JSON file
with open(json_file, 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)