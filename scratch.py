import tools

import json
import pandas as pd
import os

# with open("Data/natural/spreadsheet.xlsx", 'rb') as f:
#     df = pd.read_excel(f, sheet_name='testName')
#
# df2 = df.head(n=25)
#
# mapColumns = []
# for col in df2.columns[1:]:
#     mapColumns.append(col)
#
# print(mapColumns)
# with open("Data/natural/spreadsheet_copy.xlsx", "wb") as f:
#     df2.to_excel(f, sheet_name="testName", columns=mapColumns)

def cleanString(string):
    clean = ""
    for ch in string:
        if ch != " ":
            clean += ch.lower()
    return clean

columns = ['Last Name', 'First Name']

df = pd.DataFrame(columns=columns)

for col in df.columns:
    if cleanString(col).__contains__('firstname'):
        print("Success!")
