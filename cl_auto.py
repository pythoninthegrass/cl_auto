from craigslist import CraigslistForSale
from pprint import pprint
from prettytable import PrettyTable
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

# TODO: loop through params site (tulsa) and make (Toyota)
# CraigslistForSale.show_filters()
cl = CraigslistForSale(site='oklahomacity', category='cta', filters={"search_distance": 100,
                                                                    'zip_code': 73112,
                                                                    'has_image': True,
                                                                    'make': "Honda",
                                                                    'auto_bodytype': ['coupe', 'hatchback', 'sedan'],
                                                                    'min_price': "$1,000",
                                                                    'max_price': "$5,000"}
)

# init PrettyTable (pt)
pt = PrettyTable(['name', 'price', 'last_updated', 'where', 'url'])
pt.align = 'l'

# TODO: csv output
# res_csvfile = open(res_out, 'w', newline='')
# writer = csv.writer(res_csvfile)
# writer.writerow(['name', 'where', 'last_updated', 'price', 'url'])

if not os.path.exists("copy.txt"):
    content = []
    for _ in cl.get_results(sort_by='price_asc'):
        content.append(_)
    with open("copy.txt", "w") as file:
        file.write(str(content))
else:
    print("Local copy exists. Be a good netizen, love")

with open("copy.txt", "r") as file:
    raw = file.read()
    copy = str(raw)[1:-1]
    data = ast.literal_eval(str(copy))

# TODO: filter dupes (name, price, location)
for k in data:
    # unpack tuple (csv headers)
    # print(*k)
    # print(k['name'], k['price'], k['last_updated'], k['where'], k['url'])
    flattened = k['name'], k['price'], k['last_updated'], k['where'], k['url']
    pt.add_row(flattened)
    # writer.writerow([f"{i[0]}", f"{_}"])

print(pt)

# res_csvfile.close()
