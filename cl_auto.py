from craigslist import CraigslistForSale
from glob import glob
from pprint import pprint
from prettytable import PrettyTable
import argparse
import ast
import csv
import datetime
import os
import pandas as pd

home = os.path.expandvars("$HOME")
now = datetime.datetime.now()
cwd = os.getcwd()
# env = os.getcwd() + '/.env'
res_out = f"{cwd}/result_{now:%Y%m%d_%H%M}.csv"

# CraigslistForSale.show_filters()

# hard-coded
# cl = CraigslistForSale(site='tulsa', category='cta', filters={'search_distance': 100,
#                                                             'zip_code': 73112,
#                                                             'has_image': True,
#                                                             'make': "Honda",
#                                                             'auto_bodytype': ['coupe', 'hatchback', 'sedan'],
#                                                             'min_price': "$1,000",
#                                                             'max_price': "$5,000"}
# )

# init PrettyTable (pt)
pt = PrettyTable(['name', 'price', 'last_updated', 'where', 'url'])
pt.align = 'l'

# csv output
res_csvfile = open(res_out, 'w', newline='')
writer = csv.writer(res_csvfile)
writer.writerow(['name', 'price', 'last_updated', 'where', 'url'])

# env vars
sites = ['oklahomacity', 'tulsa']
category = 'cta'
search_distance = ''    # 100
zip_code = ''           # 73112
has_image = 'True'
makes = ['honda', 'toyota']
auto_bodytype = ['coupe', 'hatchback', 'sedan']
min_price = "$1,000"
max_price = "$5,000"

if not os.path.exists("copy.txt"):
    content = []
    for site in sites:
        for make in makes:
            cl = CraigslistForSale(site=f"{site}", category=f"{category}", filters={'search_distance': search_distance,
                                                                                    'zip_code': zip_code,
                                                                                    'has_image': has_image,
                                                                                    'make': make,
                                                                                    'auto_bodytype': auto_bodytype,
                                                                                    'min_price': min_price,
                                                                                    'max_price': max_price}
            )
            for _ in cl.get_results():
                content.append(_)
    with open("copy.txt", "w") as file:
        file.write(str(content))
else:
    print("Local copy exists. Be a good netizen, love")

with open("copy.txt", "r") as file:
    raw = file.read()
    copy = str(raw)[1:-1]
    data = ast.literal_eval(str(copy))

csv_out = [fn for fn in glob(f'{cwd}/*', recursive=False)
        if os.path.basename(fn).startswith('result')]

for k in data:
    # unpack tuple (csv headers)
    # print(*k)
    # print(k['name'], k['price'], k['last_updated'], k['where'], k['url'])
    flattened = k['name'], k['price'], k['last_updated'], k['where'], k['url']
    pt.add_row(flattened)
    if not os.path.exists(str(csv_out)):
        writer.writerow(flattened)

print(pt)

# TODO: massage data (extract date from name, sort by price/year/last_updated, filter dupe, validate where col)
df = pd.read_csv(res_csvfile)
with pd.option_context('display.max_rows', None,
    'display.max_columns', None, 'display.expand_frame_repr', False):
        print(df)

res_csvfile.close()
