#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
from datetime import datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
import os


def get_metadata(url):
    
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    
    if 'locations' in url:
        
        species_code = re.search('(?<=species=)\d+', url).group(0)
        
        location = soup.find('title').text.strip()
        
        location = re.sub('\s+',' ', location)
        
        location = location.replace('- Waarneming.nl', '').strip()
        
        for y in soup.find_all('option'):

            if species_code in y.attrs.values():
                
                species = y.text
                
        metadata = pd.DataFrame.from_dict({'species': [species], 'location': [location]})
        
    else:
        
        species = soup.find('title').text.strip()
        
        species = species.replace('- Waarneming.nl', '').strip()
    
        metadata = pd.DataFrame.from_dict({'species': [species]})
    
    
    return metadata


def get_coordinates(row):

    observation_details_response = requests.get(row['url'])

    soup = BeautifulSoup(observation_details_response.content, 'html.parser')

    coordinates = soup.find('span', class_='teramap-coordinates-coords')

    if coordinates is not None:
    
        observation_coordinates = coordinates.text.strip()
    
    else:
        
        observation_coordinates = 'location hidden'

    return observation_coordinates


def request_observations(url, page=1, species=None):
    
    base_url = "https://waarneming.nl"

    response = requests.get(url, {'page': str(page)})

    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table', class_='table table-bordered table-striped')
    
    observations = pd.DataFrame(columns=['url',
                                        'date_time',
                                        'number_behavior',
                                        'location',
                                        'observer'])
    
    for row in table.tbody.find_all('tr'):    
        # Find all data for each column
        columns = row.find_all('td')
    
        if(columns != []):
            
            observation = pd.DataFrame().from_dict(
                {'url': base_url + columns[0].find_all('a')[0].attrs['href'],
                 'date_time': [columns[0].text.strip()],
                 'number_behavior': [columns[1].text.strip()],
                 'location': [columns[2].text.strip()],
                 'observer': [columns[3].text.strip()]}
                )
            
            observations = pd.concat([observations, observation])

    observations['date'] = observations['date_time'].str.extract("(\d{4}-\d{2}-\d{2})")     
    observations['time'] = observations['date_time'].str.extract("(\d{2}:\d{2})") 
    observations['date_time'] = pd.to_datetime(observations['date_time'])
        
    observations['coordinates'] = observations.apply(lambda row: get_coordinates(row), axis=1)
        
    observations['lat'] = observations['coordinates'].str.extract(('(^\d+\.\d{4})')).astype(float)
    observations['lon'] = observations['coordinates'].str.extract(('(\d+\.\d{4}$)')).astype(float)

    return observations


def get_observations(species, page=1, location='all', nr_of_days=None, date_before='', date_after=''):
    """collect observations from waarneming.nl"""

    base_url = "https://waarneming.nl"

    if nr_of_days != None:
        """Collect observations from the last n days"""

        today = datetime.today()
        date_before = today.strftime('%Y-%m-%d')
        date_after = (today - timedelta(days=nr_of_days)).strftime('%Y-%m-%d')

    if date_before == None and date_after != None:

        date_before = today.strftime('%Y-%m-%d') 

    # construct the url
    species_url = '/species/{0}/observations/'.format(species)
    query = '?date_after={0}&date_before={1}'.format(date_after, date_before)

    url = base_url + species_url + query

    # including location changes the url
    if location != 'all':

        location_url = '/locations/{0}/observations/'.format(location)
        query = '?date_after={0}&date_before={1}&species={2}'.format(date_after, date_before, species)

        url = base_url + location_url + query
    
    metadata = get_metadata(url)
    
    metadata['date_after'] = date_after
    metadata['date_before'] = date_before
    
    observations = pd.DataFrame()
    
    while True:
        
        observations_page = request_observations(url, page=page, species=species)
        
        # observations_hash_new = hashlib.sha1(pd.util.hash_pandas_object(observations_page).values).hexdigest() 
        
        observations = pd.concat([observations, observations_page])
        
        if observations.shape[0] == observations.drop_duplicates().shape[0]:
            
            page += 1
            
            print(min(observations['date_time']))
        
        else:
            
            break
        
    species = re.search('.+(?= - )', metadata['species'].iloc[0]).group(0)
    
    observations.insert(0, 'species', species)
    
    observations.insert(0, 'date_range', date_after + '-' + date_before)
    
    return observations


def save_data(data, data_dir):
    
    species = data['species'].iloc[0]
    
    filename = species + '_' + data['date_range'].iloc[0]
    
    data[0].to_csv(os.path.join(data_dir, filename + '.csv'), index=False)
    data[1].to_csv(os.path.join(data_dir, filename + '_metadata.csv'), index=False)









