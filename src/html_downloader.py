import os
import requests
from dotenv import load_dotenv
from tqdm import tqdm
from bs4 import BeautifulSoup

# Loading Environment Variables from '.env' file in current environment
load_dotenv()

# Getting the API key from '.env' file
apiKey = os.getenv('APIKEY')

# Setting up Target and Scraper URLs
baseTargetUrl = 'https://www.flipkart.com'
endpointWithQuery = '/search?q=iphone+15'
scraperUrl = 'http://api.scraperapi.com'

# Defining GET parameters for request
payload = {
    'api_key': apiKey,
    'url': baseTargetUrl+endpointWithQuery
}

# Making a GET request to the Scraper API URL with GET parameters
response = requests.get(scraperUrl, params=payload)

# Creating a BeautifulSoup object to parse the HTML content received from above request
soup = BeautifulSoup(response.text, 'html.parser')

# Fetching the list of all the anchor tags which contains path and query for subsequent pages
anchorTags = soup.find_all('a', class_="ge-49M", limit=10)

# Extracted the name of the Query Item 
queryItem = endpointWithQuery.split('=')[-1].replace('+','-')

# Make sure the "html" directory exists or create it
os.makedirs("html", exist_ok=True)

print('\n')

# Extracting the 'hrefs' from these anchor tags by looping through each anchor tag
# Using tqdm for progess bar
for anchorTag in tqdm(anchorTags, desc="Downloading HTML pages"):
    link = anchorTag.get('href')
    pageNum = link.split('&')[-1].split('=')[0] + link.split('&')[-1].split('=')[-1] 

    getParam = {
        'api_key': apiKey,
        'url': baseTargetUrl+link
    }

    fileName = queryItem + '-' + pageNum

# Making GET request to each 'href' and saving the response(html files) in html folder by prettifying it with beautiful soup
    with open(f"html/{fileName}.html", 'w') as f:
        resp = requests.get(scraperUrl, params=getParam)
        soup = BeautifulSoup(resp.content, 'html.parser')
        f.write(soup.prettify())
        
print('\n')