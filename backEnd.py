import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Get data from web and a local csv
def get_university_data():
    # Send a GET request to the website
    url = 'https://drafty.cs.brown.edu/csopenrankings/'
    response = requests.get(url)

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the table element
    table = soup.find('table')

    # Extract the table headers
    headers = []
    for th in table.find_all('th'):
        headers.append(th.text.strip())
    
    # Check whether the website has changed
    if len(headers) != 8:
        return "The website has changed. Please contact yushif@andrew.cmu.edu"

    # Extract the table rows
    rows = []
    for tr in table.find_all('tr'):
        row = []
        for td in tr.find_all('td'):
            row.append(td.text.strip())
        if row:
            rows.append(row)
    
    
    # Store the data into a data frame and set title
    ranking = pd.DataFrame(rows, columns=['index', 'university', 'size', 'U.S. News', 'CS Ranking', 'Placement', 'Best Paper', 'Comprehensive'])
    ranking = ranking.drop('index', axis=1)
    ranking = ranking.drop('size', axis=1)
    ranking['university'] = ranking['university'].str.replace('+', '', regex=True)
    ranking['U.S. News'] = ranking['U.S. News'].str.replace(' ', '', regex=True)
    ranking['CS Ranking'] = ranking['CS Ranking'].str.replace(' ', '', regex=True)
    ranking['Best Paper'] = ranking['Best Paper'].str.replace(' ', '', regex=True)
    ranking['Comprehensive'] = ranking['Comprehensive'].str.replace(' ', '', regex=True)
    ranking.replace('', np.nan, inplace=True)
    ranking = ranking.dropna()
    ranking['university'] = ranking['university'].str.replace('+', '', regex=False)
    
    # Read the tuition data from a local csv
    tuition = pd.read_csv('Tuition.csv', delimiter=',', header=None, names=['University', 'Tuition'])

    # Merge dataframes based on university column
    university = pd.merge(ranking, tuition, left_on='university', right_on='University')
    
    # Drop the redundant column
    university = university.drop('University', axis=1)

    # Transfer the ranking values into int for future sorting
    university['CS Ranking'] = university['CS Ranking'].astype(int)
    university['Placement'] = university['Placement'].astype(int)
    university['Best Paper'] = university['Best Paper'].astype(int)
    university['Comprehensive'] = university['Comprehensive'].astype(int)
    university['Tuition'] = university['Tuition'].astype(int)

    #return the data frame
    return university

# Read the csv downloaded from the api website
currency = pd.read_csv('Currency.csv')

# Transfer the budget into USD
def get_exchange(budget, curr):
    # This is the api key. It has monthly limit, please don't try too many times
    api_key = 'iLwbxE28ykhrpdXexrnGiJ7GXpu7MQ'
    # api_key = 'Y6zxD5HDWQ6CjCBvSGzFD8CBfBEANf'

    # Transfer the name of the currency to the abbreviation and put it in the url
    cur = currency.loc[currency['Description'] == curr].iloc[0]['Currency']

    # Use the api to transfer the budget into USD
    url = f'https://www.amdoren.com/api/currency.php?api_key={api_key}&from={cur}&to=USD&amount={budget}'
    response = requests.get(url)

    # Return the transferred value and hold exceptions
    if response.status_code == 200:
        data = response.json()
        if data['error'] == 0:
            budgetUSD = data['amount']
            return budgetUSD
        elif data['error'] == 110:
            return "Invalid API Key, Please contact yushif@andrew.cmu.edu"
        elif data['error'] == 400:
            return "API reach month limit, Please contact yushif@andrew.cmu.edu"
        elif data['error'] == 200:
            return "Please choose a currency"
        elif data['error'] == 300 or data['error'] == 310:
            return "Invalid budget input. Please reset and enter a number"
          
    else:
        return 'Failed to retrieve exchange rate'

def get_currency_list():
    return currency['Description'].to_list()

# Search for recommended schools under budget
def top_five_universities(university, budget, criteria):

    # Filter the data frame to get schools under budget
    budget_universities = university[university["Tuition"] < budget]

    # Sort the data frame by the criteria
    sorted_universities = budget_universities.sort_values(by=criteria) 

    # Return the top 5 options
    return sorted_universities.head(5)["university"].values.tolist()



