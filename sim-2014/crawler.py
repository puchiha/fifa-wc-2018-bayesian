
# coding: utf-8

# In[ ]:


# Initial imports
import numpy as np
import pandas as pd 
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
get_ipython().magic(u'matplotlib inline')

import random
import urllib#.request
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')


# In[ ]:


base_url = "https://sofifa.com/players?v=14&e=157711&set=true&offset="
offset = 0
columns = ['ID', 'Name', 'Age', 'Photo', 'Nationality', 'Flag', 'Overall', 'Potential', 'Club', 
           'Club Logo', 'Value', 'Wage', 'Special']
data = DataFrame(columns=columns)
for offset in range(225):
    url = base_url + str(offset*80)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    table_body = soup.find('tbody')
    counter = 0
    for row in table_body.findAll('tr'):
        td = row.findAll('td')
        picture = td[0].find('img').get('data-src')
        pid = td[0].find('img').get('id')
        nationality = td[1].find('a').get('title')
        flag_img = td[1].find('img').get('data-src')
        name = td[1].findAll('a')[1].text
        age = td[2].find('div').text.strip()
        overall = td[3].text.strip()
        potential = td[4].text.strip()
        club = td[5].find('a').text
        club_logo = td[5].find('img').get('data-src')
        value = td[7].text
        wage = td[8].text
        special = td[17].text
        player_data = DataFrame([[pid, name, age, picture, nationality, flag_img, overall, 
                                  potential, club, club_logo, value, wage, special]])
        player_data.columns = columns
        data = data.append(player_data, ignore_index=True)
        counter+=1
    offset+=1
    #print(offset)
    data.to_csv('full_player_data.csv', encoding='utf-8')


# In[ ]:


data = pd.read_csv('full_player_data.csv')


# In[ ]:


data


# In[ ]:


data.to_csv('Complete/basicplayerdata.csv', encoding='utf-8')


# In[ ]:


player_data_url = 'https://sofifa.com/player/'
r = 0
for index, row in data.iterrows():
    skill_names = []
    skill_map = {'ID' : str(row['ID'])}
    url = player_data_url + str(row['ID'])
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    categories = soup.findAll('div', {'class': 'col-3'})
    for category in categories[:-1]:
        skills = category.findAll('li')
        for skill in skills:
            a = skill.text.split()
            a.reverse()
            value = a.pop()
            a.reverse()
            n = ' '.join(a)
            skill_names.append(n)
            skill_map[str(n)] = value
    master_data = DataFrame(columns=skill_names)
    break


# In[ ]:


player_data_url = 'https://sofifa.com/player/'
r = 0
for index, row in data.iterrows():
    skill_names = []
    skill_map = {'ID' : str(row['ID'])}
    url = player_data_url + str(row['ID'])
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    categories = soup.findAll('div', {'class': 'col-3'})
    for category in categories[:-1]:
        skills = category.findAll('li')
        for skill in skills:
            a = skill.text.split()
            a.reverse()
            value = a.pop()
            a.reverse()
            n = ' '.join(a)
            skill_names.append(n)
            skill_map[str(n)] = value
    attr_data = DataFrame(columns=skill_names)
    for key in skill_map.keys():
        attr_data.loc[r,key] = skill_map[key]
    r = r + 1
    print(r)
    master_data = pd.concat([master_data, attr_data])
    if r % 100 == 0:
        master_data.to_csv('Complete/PlayerAttributeData.csv', encoding='utf-8')


# In[ ]:


master_data


# In[ ]:


full_data = pd.merge(data, master_data, left_index=True, right_index=True)


# In[ ]:


full_data.to_csv('Allplayer.csv', encoding='utf-8')


# In[ ]:


master_data.to_csv('Complete/PlayerAttributeData.csv', encoding='utf-8')


# In[ ]:


full_data.to_csv('Complete/Dataset.csv', encoding='utf-8')


# In[ ]:


full_data


# In[ ]:


full_data.drop('Unnamed: 0', 1,  inplace=True)


# In[ ]:


full_data


# In[ ]:


full_data.drop('ID_x', 1,  inplace=True)


# In[ ]:


full_data['ID_y']


# In[ ]:


f = full_data.rename(index=str, columns={"ID_y": "ID"})


# In[ ]:


f['ID']


# In[ ]:


f.to_csv('Complete/Dataset.csv', encoding='utf-8')


# In[ ]:


f

