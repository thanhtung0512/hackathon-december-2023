import csv
import json
import os
from pprint import pprint, pformat
# Read raw data from the file
with open("raw_data.txt", "r", encoding="utf-8") as file:
    raw_data = file.read()

def get_html_from_json(json_path):
    with open(json_path, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        list_data = []
        for each in data:
            list_data.append(each.get('html',''))
        return list_data
def get_content(delimeter_length):
    laptop_name_start = end_index + delimeter_length

    laptop_name_end = laptop_name_start
    while raw_data[laptop_name_end] != "\\":
        # print(laptop_index_end)
        laptop_name_end = laptop_name_end + 1
    brand = raw_data[laptop_name_start:laptop_name_end:1]
    return brand


# Split the raw data into individual laptop entries
laptop_entries = raw_data.split("\n\n")
# print(laptop_entries)
# Create a CSV file and write header
csv_file_path = "laptops-hp-workstation.csv"


def get_name(delimeter,raw_data):
    string_to_get_name = "Cấu hình Laptop"
    start_index = raw_data.find(string_to_get_name) + len(string_to_get_name) + delimeter
    
    end_index = start_index
    while end_index != '(':
        end_index += 1
    laptop_name = raw_data[start_index:end_index:1]
    return laptop_name




with open(csv_file_path, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    header = [
        "Tên sản phẩm",
        "Bộ VXL",
        "Bộ nhớ RAM",
        "Ổ cứng",
        "Card màn hình",
        "Kích thước màn hình",
        "Cổng giao tiếp",
        "Hệ điều hành",
        "Kích thước",
        "Màu sắc",
        "Chất liệu",
        "Giá niêm yết",
        "Giá ưu đãi tháng 12",
        "Bảo hành",
    ]
    writer.writerow(header)
    for json_file_name in os.listdir():
        if json_file_name.endswith(".json") and json_file_name != 'package.json' and json_file_name != 'package-lock.json' and json_file_name != 'tsconfig.json':
            json_file_path = os.path.join(os.getcwd(), json_file_name)
            print(json_file_path)
            html_content = get_html_from_json(json_file_path)
            formatted_html_list = [pformat(each_content) for each_content in html_content]
            for each_content in html_content:
              
                raw_data = each_content.replace('\n', r'\n').replace('\t', r'\t')
                # print(raw_data)
                row_values = []
                for each in header:
                    # print(each)
                    start_index = raw_data.find(each)
                    end_index = start_index + len(each)
                    if each == 'Tên sản phẩm':
                        fixed_string = 'Cấu hình Laptop'
                        start_index = raw_data.find(fixed_string) 
                        end_index = start_index
                        while raw_data[end_index] != '(':
                            end_index += 1
                        laptop_name =raw_data[start_index+len(fixed_string):end_index]
                        print(laptop_name)
                        row_values.append(laptop_name)
                    elif each == 'Card màn hình':
                        value = get_content(2)
                        print(f'{each}: {value}')
                        row_values.append(value)
                    elif each == 'Kích thước màn hình':
                        value = get_content(2)
                        print(f'{each}: {value}')
                        row_values.append(value)
                    elif each == 'Hệ điều hành':
                        value = get_content(2)
                        print(f'{each}: {value}')
                        row_values.append(value)
                    elif each == 'Bộ nhớ RAM':
                        value = get_content(2)
                        print(f'{each}: {value}')
                        row_values.append(value)
                    elif each == 'Bộ VXL':
                        value = get_content(2)
                        print(f'{each}: {value}')
                        row_values.append(value)
                    elif each == 'Giá niêm yết' or each == 'Giá ưu đãi tháng 12':
                        value = get_content(3)
                        print(f'{each}: {value}')
                        row_values.append(value)
                    else: 
                        value = get_content(2)
                        print(f'{each}: {value}')

                writer.writerow(row_values)
                print(row_values)
        
    # Iterate through each laptop entry, extract and write the data to the CSV file


print(f"Data has been successfully written to {csv_file_path}")
