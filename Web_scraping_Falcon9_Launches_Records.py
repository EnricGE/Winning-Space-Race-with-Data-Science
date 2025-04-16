# Web scraping Falcon 9 Launches Records from Wikipedia

# Import required libraries
import sys
import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd

# Helper functions for processing web scraped HTML table
def date_time(table_cells):
    """
    This function returns the date and time from the HTML table cell
    Input: the element of a table data cell extracts extra row
    """
    return [data_time.strip() for data_time in list(table_cells.strings)][0:2]

def booster_version(table_cells):
    """
    This function returns the booster version from the HTML table cell
    Input: the element of a table data cell extracts extra row
    """
    out = ""
    # Convert generator to list first
    cell_strings = list(table_cells.strings)
    
    for i in range(len(cell_strings)):
        if i > 0:
            out += ' '.join(item.strip() for item in cell_strings[i:i+1])
    return out

def landing_status(table_cells):
    """
    This function returns the landing status from the HTML table cell
    Input: the element of a table data cell extracts extra row
    """
    out = [i for i in table_cells.strings][0]
    return out

def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        mass_re = re.findall(r'[0-9]+', mass)
        if mass_re:
            mass = mass_re[0]
        else:
            mass = 0
    else:
        mass = 0
    return mass

def extract_column_from_header(row):
    """
    This function returns the landing status from the HTML table cell
    Input: the element of a table data cell extracts extra row
    """
    if (row.br):
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
        
    column_name = ' '.join(row.contents)
    
    # Filter the digit and empty names
    if not(column_name.strip().isdigit()):
        column_name = column_name.strip()
        return column_name

# TASK 1: Request the Falcon9 Launch Wiki page from its URL
static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"

# Use requests.get() method with the provided static_url
# Assign the response to a object
response = requests.get(static_url)

# Create a BeautifulSoup object from the HTML response
soup = BeautifulSoup(response.text, 'html.parser')

# Print the page title to verify if the BeautifulSoup object was created properly
print(soup.title)

# TASK 2: Extract all column/variable names from the HTML table header
# Let's try to find all tables on the web page first
# If you need to refresh your memory about BeautifulSoup, please check the external reference link
falcon_9_tables = soup.find_all('table', {'class': 'wikitable plainrowheaders collapsible'})

# Starting from the third table is our target table contains the actual launch records
first_launch_table = falcon_9_tables[2]
print(first_launch_table)

# You should able to see the columns names embedded in the table header elements <th> as follows:
column_names = []

# Apply find_all() function with 'th' element on first_launch_table
# Iterate each element and apply the provided extract_column_from_header() to get a column name
# Append the Non-empty column name (if name is not None and len(name) > 0) into a list called column_names
for th_element in first_launch_table.find_all('th'):
    column_name = extract_column_from_header(th_element)
    if column_name is not None and len(column_name) > 0:
        column_names.append(column_name)

# Check the extracted column names
print(column_names)

# TASK 3: Create a data frame by parsing the launch HTML tables
launch_dict = dict.fromkeys(column_names)

# Instead of directly deleting
if 'Date and time (UTC)' in launch_dict:
    del launch_dict['Date and time (UTC)']

# Let's initialize the launch_dict with each value to be an empty list
launch_dict['Flight No.'] = []
launch_dict['Date'] = []
launch_dict['Time'] = []
launch_dict['Version Booster'] = []
launch_dict['Launch Site'] = []
launch_dict['Payload'] = []
launch_dict['Payload mass'] = []
launch_dict['Orbit'] = []
launch_dict['Customer'] = []
launch_dict['Launch outcome'] = []
launch_dict['Booster landing'] = []

# Next, we need to fill up the launch_dict with launch records extracted from table rows
# Usually, HTML tables in Wiki pages are likely to contain unexpected annotations and other types of noises
# To simplify the parsing process, we have provided an incomplete code snippet below to help you to fill up the launch_dict

extracted_row = 0
# Extract each table
for table_number, table in enumerate(soup.find_all('table', {'class': 'wikitable plainrowheaders collapsible'})):
    # get table row
    for rows in table.find_all("tr"):
        # check to see if first table heading is as number corresponding to launch a number
        if rows.th:
            if rows.th.string:
                flight_number = rows.th.string.strip()
                flag = flight_number.isdigit()
        else:
            flag = False
        # get table element
        row = rows.find_all('td')
        # if it is number save cells in a dictionary
        if flag:
            extracted_row += 1
            # Flight Number value
            # TODO: Append the flight_number into launch_dict with key 'Flight No.'
            launch_dict['Flight No.'].append(flight_number)
            
            # Date value
            # TODO: Append the date into launch_dict with key 'Date'
            date = date_time(row[0])[0]
            launch_dict['Date'].append(date)
            
            # Time value
            # TODO: Append the time into launch_dict with key 'Time'
            time = date_time(row[0])[1]
            launch_dict['Time'].append(time)
            
            # Booster version value
            # TODO: Append the bv into launch_dict with key 'Version Booster'
            bv = booster_version(row[1])
            launch_dict['Version Booster'].append(bv)
            
            # Launch Site value
            # TODO: Append the bv into launch_dict with key 'Launch Site'
            launch_site = row[2].a.string
            launch_dict['Launch Site'].append(launch_site)
            
            # Payload value
            # TODO: Append the payload into launch_dict with key 'Payload'
            payload = row[3].a.string
            launch_dict['Payload'].append(payload)
            
            # Payload Mass value
            # TODO: Append the payload_mass into launch_dict with key 'Payload mass'
            payload_mass = get_mass(row[4])
            launch_dict['Payload mass'].append(payload_mass)
            
            # Orbit value
            # TODO: Append the orbit into launch_dict with key 'Orbit'
            orbit = row[5].a.string
            launch_dict['Orbit'].append(orbit)
            
            # Customer value
            # Handle cases where there might not be an anchor tag
            if row[6].a:
                customer = row[6].a.string
            else:
                # Try to get the text directly from the cell
                customer = row[6].get_text(strip=True)
                # If still empty, use a default value
                if not customer:
                    customer = "Unknown"

            launch_dict['Customer'].append(customer)
            
            # Launch outcome value
            # TODO: Append the launch_outcome into launch_dict with key 'Launch outcome'
            launch_outcome = list(row[7].strings)[0]
            launch_dict['Launch outcome'].append(launch_outcome)
            
            # Booster landing
            # TODO: Append the booster_landing into launch_dict with key 'Booster landing'
            booster_landing = landing_status(row[8])
            launch_dict['Booster landing'].append(booster_landing)

# After you have fill in the parsed launch record values into launch_dict, you can create a dataframe from it
df = pd.DataFrame(launch_dict)

# We can now export it to a CSV for the next section, but to make the answers consistent
# and in case you have difficulties finishing this lab, we will provide a completed CSV
df.to_csv('spacex_web_scraped.csv', index=False)

# Authors
# Yan Luo
# Nayef Abou Tayoun





