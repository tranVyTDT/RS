import json
import pandas as pd
#pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
#pd.set_option('display.width', 1000)

units = pd.read_csv('../data/donvi_contact_information.csv')
files = pd.read_csv('../data/hoso_2019.csv')


#print(files.head())

file_details = files['hs_thongtin']
list_file_details = []

for file_detail in file_details:
    list_file_details.append(json.loads(file_detail))

list_file_details = pd.DataFrame(list_file_details)

print(list_file_details.head())
