import numpy as np
import pandas as pd
import csv

def get_country_roster(country):
# get all players in a country
    return fifa_dataset[fifa_dataset['Nationality'] == country]

def get_best_squad_n(formation, nationality, df, measurement = 'Potential'):
# finds the best 11 players given formation    
# returns overall_squad_rating, squad_list, squad_stats (i.e. positions and ratings)
    df_copy = df.copy()
    df_copy = df_copy[df_copy['Nationality'] == nationality]
    store = []
    team = []
    for i in formation:
        store.append([df_copy.loc[[df_copy[df_copy['Preferred Position'].str.contains(i)][measurement].idxmax()]]['Preferred Position'].to_string(index = False), df_copy[df_copy['Preferred Position'].str.contains(i)][measurement].max()])
        team.append(df_copy.loc[[df_copy[df_copy['Preferred Position'].str.contains(i)][measurement].idxmax()]]['Name'].to_string(index = False))
        df_copy.drop(df_copy[df_copy['Preferred Position'].str.contains(i)][measurement].idxmax(), inplace = True)
    return np.mean([x[1] for x in store]).round(2), np.array(team), pd.DataFrame(np.array(store).reshape(11,2), columns = ['Position', measurement]).to_string(index = False)

def get_best_formation_all(squad_list, country):
# finds the best formation for the given team 
# returns the best_rating, best_squad_list, best_formation, and squad_stats (i.e. positions and ratings)
    best_rating = 0
    best_squad, best_formation = [], []
    for i, formation in enumerate(squad_list):
        potRating, pot_squad, squad_info = get_best_squad_n(formation, country, fifa_dataset, 'Potential')
        if potRating > best_rating:
            best_rating = potRating
            best_squad = pot_squad
            best_formation = squad_name[i]
    return best_rating, best_squad, best_formation, squad_info
    
def get_team_stats(squad_stats):
# gets the stats for attack, defence and midfield for a team
    midRating, defRating, attRating  = [], [], []
    for player in squad_stats.split('\n'):
        pos, rating = player.split()[0], player.split()[-1]
        if pos in midfield: midRating.append(float(rating))
        if pos in defense: defRating.append(float(rating))
        if pos in attack: attRating.append(float(rating))
    return np.mean(midRating).round(2), np.mean(defRating).round(2), np.mean(attRating).round(2)


# In[145]:


# create data-set with team information
def generate_team_stats():
    d = []
    for country in qualified_countries:
            best_rating, best_squad, best_formation, squad_stats = get_best_formation_all(squad_list_adj, country)
            mid_rating, def_rating, att_rating = get_team_stats(squad_stats)
            if best_rating > 84.0: tier = 1
            elif best_rating > 77.0: tier = 2
            else: tier = 3
            d.append({'Country': country, 'Rating': best_rating, 'Squad': best_squad, 'Defence': def_rating, 'Midfield': mid_rating, 'Attack': att_rating, 'Formation': best_formation,'Tier': tier})

    processed_data = pd.DataFrame(d).reindex_axis(['Country', 'Squad', 'Formation', 'Tier', 'Rating', 'Attack', 'Midfield', 'Defence'], axis = 1).set_index('Country')
    processed_data.to_csv('data/WC18_processed.csv')
    return processed_data

# create data-set with historical data of match up for prior information
def generate_prior_data(stats):
    d = []
    for countryA in qualified_countries:
        for countryB in qualified_countries:
            if countryA == countryB: continue
            try:
                xA = np.mean(map(float, prior[(prior['home_team'] == countryA) & (prior['away_team'] == countryB)]['home_score'].to_string(index = False).split('\n')) + map(float, prior[(prior['home_team'] == countryB) & (prior['away_team'] == countryA)]['away_score'].to_string(index = False).split('\n'))).round(2)
                xB = np.mean(map(float, prior[(prior['home_team'] == countryB) & (prior['away_team'] == countryA)]['home_score'].to_string(index = False).split('\n')) + map(float, prior[(prior['home_team'] == countryA) & (prior['away_team'] == countryB)]['away_score'].to_string(index = False).split('\n'))).round(2)
            except:
                # use a uniform prior
                xA = int(stats[stats.index == countryB]['Tier'].get_values()) 
                xB = int(stats[stats.index == countryA]['Tier'].get_values())
            d.append({'CountryA': countryA, 'CountryB': countryB, 'meanScoreA': xA, 'meanScoreB': xB})
    processed_data = pd.DataFrame(d).reindex_axis(['CountryA', 'meanScoreA', 'CountryB', 'meanScoreB'], axis = 1).set_index(['CountryA', 'CountryB'])
    processed_data.to_csv('data/WC18_prior.csv')


# In[146]:

if __name__ == '__main__':
    # Import player data and historical results for all countries
    raw_data_path = 'data/'

    prior = pd.read_csv(raw_data_path + 'results.csv')
    fifa_dataset = pd.read_csv(raw_data_path + 'CompleteDataset.csv')

    # drop unwanted fields from both data sets
    fifa_dataset.drop(labels = ['Unnamed: 0', 'Age', 'Photo', 'Flag', 'Club', 'Club Logo', 'Wage'], axis = 1, inplace = True)
    prior.drop(labels = ['city', 'country', 'tournament'], axis = 1, inplace = True)
    prior = prior[prior.date > '1990-01-01']


    # only interested in countries that are qualified for the WC
    # maybe reduce this to 16 countries post group stage for faster computation (other 2^32 simulations)
    qualified_countries = ['Egypt', 'Morocco', 'Nigeria', 'Senegal', 'Tunisia', 'Australia', 'Iran', 'Japan', 'Korea Republic', 'Saudi Arabia', 'Belgium', 'Croatia', 'Denmark', 'England', 'France', 'Germany', 'Iceland', 'Poland', 'Portugal', 'Russia', 'Serbia', 'Spain', 'Sweden', 'Switzerland', 'Costa Rica', 'Mexico', 'Panama', 'Argentina', 'Brazil', 'Colombia', 'Peru', 'Uruguay']

    # get data for qualified countries only
    fifa_dataset = fifa_dataset[fifa_dataset['Nationality'].isin(qualified_countries)].fillna(0)
    prior = prior[(prior['home_team'].isin(qualified_countries) & prior['away_team'].isin(qualified_countries))]

    # get remaining potential
    fifa_dataset['Remaining Potential'] = fifa_dataset['Potential'] - fifa_dataset['Overall']

    # get only one preferred position (first only)
    # i wrote a function to get the position with max value - it's in archives -- but this is simpler
    fifa_dataset['Preferred Position'] = fifa_dataset['Preferred Positions'].str.split().str[0]

    # set the general formations for squads to get the max potential 
    squad_352_strict = ['GK', 'LB|LWB', 'CB', 'RB|RWB', 'LM|W$', 'RM|W$', 'CM', 'CM|CAM|CDM', 'CM|CAM|CDM', 'W$|T$', 'W$|T$']
    squad_442_strict = ['GK', 'LB|LWB', 'CB', 'CB', 'RB|RWB', 'LM|W$', 'RM|W$', 'CM', 'CM|CAM|CDM', 'W$|T$', 'W$|T$']
    squad_433_strict = ['GK', 'LB|LWB', 'CB', 'CB', 'RB|RWB', 'CM|LM|W$', 'CM|RM|W$', 'CM|CAM|CDM', 'W$|T$', 'W$|T$', 'W$|T$']
    squad_343_strict = ['GK', 'LB|LWB', 'CB', 'RB|RWB', 'LM|W$', 'RM|W$', 'CM|CAM|CDM', 'CM|CAM|CDM', 'W$|T$', 'W$|T$', 'W$|T$']
    squad_532_strict = ['GK', 'LB|LWB', 'CB|LWB|RWB', 'CB|LWB|RWB', 'CB|LWB|RWB', 'RB|RWB', 'M$|W$', 'M$|W$', 'M$|W$', 'W$|T$', 'W$|T$']

    squad_352_adj = ['GK', 'B$', 'B$', 'B$', 'M$|W$|T$', 'M$|W$|T$', 'M$|W$|T$', 'M$|W$|T$', 'M$|W$|T$', 'W$|T$|M$', 'W$|T$|M$']
    squad_442_adj = ['GK', 'B$', 'B$', 'B$', 'B$', 'M$|W$|T$', 'M$|W$|T$', 'M$|W$|T$', 'M$|W$|T$', 'W$|T$|M$', 'W$|T$|M$']
    squad_433_adj = ['GK', 'B$', 'B$', 'B$', 'B$', 'M$|W$|T$', 'M$|W$|T$', 'M$|W$|T$', 'W$|T$|M$', 'W$|T$|M$', 'W$|T$|M$']
    squad_343_adj = ['GK', 'B$', 'B$', 'B$', 'M$|W$|T$', 'M$|W$|T$', 'M$|W$|T$', 'M$|W$|T$', 'W$|T$|M$', 'W$|T$|M$', 'W$|T$|M$']
    squad_532_adj = ['GK', 'B$', 'B$', 'B$', 'B$', 'B$', 'M$|W$|T$', 'M$|W$|T$', 'M$|W$|T$', 'W$|T$|M$', 'W$|T$|M$']

    midfield = ['CDM', 'CM', 'RM', 'LM']
    defense = ['GK', 'LB', 'CB', 'RB', 'LWB', 'RWB']
    attack = ['LW', 'RW', 'ST', 'CAM']

    squad_list_strict = [squad_352_strict, squad_442_strict, squad_433_strict, squad_343_strict, squad_532_strict]
    squad_list_adj = [squad_352_adj, squad_442_adj, squad_433_adj, squad_343_adj, squad_532_adj]
    squad_name = ['3-5-2', '4-4-2', '4-3-3', '3-4-3', '5-3-2']


    stats = generate_team_stats()
    generate_prior_data(stats)

