import csv
import json

def extract_valid_row_as_json(csv_file_path):
    with open(csv_file_path, newline='', encoding='cp1252') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if all(value is not None and str(value).strip() != "" for value in row.values()):
                return json.dumps(row, indent=4, ensure_ascii=False)
    return json.dumps({"error": "No row found with all non-null values"}, indent=4)

csv_file_path = r"E:\ETL\multi-source-ingestion\Articles.csv"
valid_row_json = extract_valid_row_as_json(csv_file_path)
print(valid_row_json)
