import requests
from bs4 import BeautifulSoup
import json
import random
import urllib.request

# Categories to be scraped
categories = ['driving', 'food-and-drink', 'afternoon-tea', 'spa-and-beauty', 'adventure', 'days-out-and-tours', 'flying', 'sports', 'animal', 'watersports-and-boating', 'short-breaks', 'arts-and-crafts', 'theatre-events', 'personality-type']

for category in categories:
    # GET request - recieve HTML
    data = requests.get('https://www.virginexperiencedays.co.uk/' + category + '?pagesize=30')

    # Parse html
    soup = BeautifulSoup(data.text, 'html.parser')

    # Initialise variables
    data = {}
    event = {}
    index = 0

    # Loop 30 times
    while index <= 30:
        for elem in soup.select('.productCard'):

            # Get event image add to event dict
            for img in elem.select('img'):
                key = str(category) + str(index) + '.jpg'
                event.update({'img':key})
                urllib.request.urlretrieve(img['src'], 'data/images/' + key)

            # Get location information
            for location in elem.select('.productCard__locationCount'):
                event.update({'location': location.text})

            # Get event price add to event dict
            for price in elem.select('.productCard__detailsRight span.currentPrice'):
                price = price.text.strip()
                event.update({'price': price})

            # Get event title add to event dict
            for title in elem.select('.js-product-name'):
                event.update({'title':title.text})

            # Get event description list add to event dict
            desc_items = [li.text for li in elem.select('.productCard__blurb li')]
            description = ""
            for line in desc_items:
                description = description + line + "\n"
            event.update({'description':description})

            # Add this event to data dict
            data.update({index:event})

            # Reset event dict & increment index
            event = {}
            index += 1

    # Encode to JSON and save in file
    json_data = json.dumps(data)
    filename = 'data/' + category + '.json'
    with open(filename, 'w') as file:
      json.dump(data, file)

    # Print to console after each category is finished scraping
    print('Finised scraping: ' + category + ' events to: ' + filename)
