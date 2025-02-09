import csv
file_path = "Ml_model/csv_files/crop_growth_stages_fixed_5.csv" 

def load_bbch_data(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

def get_bbch_stage(file_path, crop, days_since_planting):
    bbch_data = load_bbch_data(file_path)
    for row in bbch_data:
        if row['Crop'] == crop and days_since_planting <= int(row['Stage Code']):
            return row
    return None
