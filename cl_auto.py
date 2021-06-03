from craigslist import CraigslistForSale
from glob import glob
# from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from pprint import pprint
from prettytable import PrettyTable
# import argparse
import ast
# import asyncio
import csv
import datetime
# import numpy as np
import os
import pandas as pd
import re
import sys

home = os.path.expandvars("$HOME")
now = datetime.datetime.now()
cwd = os.getcwd()
# env = os.getcwd() + '/.env'
res_out = f"{cwd}/result_{now:%Y%m%d}.csv"

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
res_csv = open(res_out, 'w', newline='')
writer = csv.writer(res_csv)
writer.writerow(['name', 'price', 'last_updated', 'where', 'url'])

# TODO: exclude expired posts
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

glob_csv = [fn for fn in glob(f'{cwd}/*', recursive=False)
        if os.path.basename(fn).startswith('result')]

for k in data:
    # unpack tuple (csv headers)
    # print(*k)
    # print(k['name'], k['price'], k['last_updated'], k['where'], k['url'])
    flattened = k['name'], k['price'], k['last_updated'], k['where'], k['url']
    pt.add_row(flattened)
    if not os.path.exists(str(glob_csv)):
        writer.writerow(flattened)

# print(pt)
res_csv.close()

# create empty list to store dataframes
lst = []
for f in glob_csv:
    temp_df = pd.read_csv(f)
    lst.append(temp_df)
    print(f'Successfully created dataframe for {f} with shape {temp_df.shape}')

# concatenate our list of dataframes into one
df = pd.concat(lst, axis=0)

# extract year from name
df['year'] = df.name.str.extract(r'(^\d+)', expand = True)

# move year column to front
df = df.set_index('year').reset_index()

# sorting
df.sort_values(['price', 'year', 'last_updated'], ascending=[True, True, True], inplace=True)

# drop dulicate values
df.drop_duplicates(subset='name', inplace=True)

# uppercase location
df['where'] = df['where'].str.upper()

# URLs
links = df.loc[:,"url"].to_string(index=False)  # csv
# urls = [
#     "https://scrapethissite.com/pages/ajax-javascript/#2015",
#     "https://scrapethissite.com/pages/ajax-javascript/#2014",
# ]
urls = df.loc[:,"url"].tolist()                 # playwright browser

# TODO: strip non-location strings in where col
not_loc = re.compile(r'''
(?!oklahoma city)|
(?!okc)|
(?!tulsa)|
(?!catoosa)|
(?!edmond)|
(?!broken arrow)|
(?!skiatook)|
(?!tuttle)
''', re.IGNORECASE
)
# df['where'] = df['where'].apply(lambda x: not_loc.findall(x) if type(x) is str else x)
# df['where'] = df['where'].str.replace(not_loc, np.nan)

with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.expand_frame_repr', False):
    # print(df.shape)
    df.head()
    print(df)

df.to_csv (f"{cwd}/pandas_{now:%Y%m%d}.csv", index = False, header=True)

# TODO: text selector `This posting has been deleted by its author.` or `This posting has expired.`
# Click text=This posting has been deleted by its author.
# page.click("text=This posting has been deleted by its author.")

# ASYNC
# async def main(url):
#     async with async_playwright() as playwright:
#         browser = await playwright.chromium.launch(headless=False)
#         context = await browser.new_context()
#         page = await context.new_page()
#         await page.goto(url, timeout=None)
#         await page.wait_for_timeout(15000)
#         await context.close()
#         await browser.close()

# async def go_to_url():
#     tasks = [main(url) for url in urls]
#     await asyncio.wait(tasks)

# asyncio.get_event_loop().run_until_complete(go_to_url())

# SYNC
def main():
    try:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        for url in urls:
            page = context.new_page()
            page.goto(url)
        page.wait_for_timeout(60000)    # 60 seconds
    except KeyboardInterrupt as k:
        print('\nKeyboard exception received. Exiting ')
        context.close()
        browser.close()
        sys.exit(0)
    except Exception:
        print(f"\nUncaught exception occurred. Exiting ")
        sys.exit(1)

with sync_playwright() as playwright:
    main()
