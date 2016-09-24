
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import re
import time
import dill
from datetime import timedelta
from csv_pkl_sql import save_it, pkl_it


# ## Scrape appropriate date and location for weather data
# First requires finding closest airport for each location.

# In[2]:

with open('../pkl/01_latitude_longitude_google.pkl', 'r') as fh:
    lat_long_data = dill.load(fh)
lat_long_data.head(1)


# In[4]:

with open('../pkl/02_airport_information_fallingrain.pkl', 'r') as fh:
    airport_info = dill.load(fh)
airport_info.head(1)


# The approximation for closest airport is crude, given that it doesn't convert latitude and longitude to distance but rather uses them directly. Given the relatively short distances involved, I think this is fine for a first pass of this project.

# In[6]:

airport_coords = airport_info[['latitude', 'longitude']].values[np.newaxis, :]
places_coords = np.rollaxis(lat_long_data[['latitude','longitude']].values[np.newaxis, :], 0, -1)

dist_coords = ((places_coords - airport_coords)**2).sum(axis=-1)
min_coords = dist_coords.argmin(axis=1)

print airport_coords.shape, places_coords.shape, dist_coords.shape, min_coords.shape


# In[7]:

# Transfer the coordinates to the latitude/longitude data
merge_data = lat_long_data.copy()

print merge_data.shape

merge_data['airport_index'] = airport_info.index[min_coords]

# Now grap the airport and location info
df = airport_info.loc[merge_data.airport_index, ['country','name','FAA','IATA','ICAO']]
merge_data[['country','name','FAA','IATA','ICAO']] = df.set_index(merge_data.index)

print merge_data.shape


# In[8]:

merge_data.head()


# In[9]:

# TODO WRITE THIS MATRIX OUT
pkl_it(merge_data, '../pkl/04_merged_latitude_longitude_airport_checkpoint')


# Now combine with infection date data.

# In[10]:

with open('../pkl/03_infection_data_initial_import.pkl','r') as fh:
    infection_data = dill.load(fh)
infection_data = infection_data[['report_date','location']]
infection_data.head(1)


# In[13]:

print infection_data.shape, merge_data.shape

merge_all = pd.merge(infection_data, 
                     merge_data[['location','country','FAA','IATA','ICAO']], 
                     on='location', 
                     how='left').drop_duplicates()

print merge_all.shape

merge_all.head()


# Now scrape from weather underground. I want time shifted data, so need to get one and two weeks beforehand.

# In[31]:

weather_scrape = (merge_all[['report_date','country','IATA','ICAO']]
                  .drop_duplicates()
                  .set_index(['country','IATA','ICAO'])
                  )

weather_scrape['report_date1'] = weather_scrape.report_date - timedelta(days=7)
weather_scrape['report_date2'] = weather_scrape.report_date - timedelta(days=14)

weather_scrape = (weather_scrape
                  .stack()
                  .reset_index(level=-1, drop=True)
                  .reset_index()
                  .rename(columns={0:'report_date'})
                  .dropna(subset=['IATA','ICAO'], how='all')
                 )

weather_scrape.shape


# In[50]:

# def scrape_weekly_weather(df_row):
#     # Scrape the weekly data table
#     url_fmt = 'https://www.wunderground.com/history/airport/{}/{}/{}/{}/WeeklyHistory.html'
    
#     try:
#         url = url_fmt.format(df_row.ICAO, df_row.report_date.year, 
#                              df_row.report_date.month, df_row.report_date.day)
#     except:
#         url = url_fmt.format(df_row.IATA, df_row.report_date.year, 
#                              df_row.report_date.month, df_row.report_date.day)
    
#     try:
#         table = pd.read_html(url)[0].dropna(subset=['Max','Avg','Min','Sum'], how='all')
#         table.columns = ['Measurement','Max','Avg','Min','Sum']
#         table.set_index('Measurement', inplace=True)
#         table = table.stack()
#     except:
#         table = pd.Series({'NULL':np.NaN}, index=pd.Index([0]))
    
#     return table

def scrape_weekly_weather(date, df_row):
    # Scrape the weekly data table
    url_fmt = 'https://www.wunderground.com/history/airport/{}/{}/{}/{}/WeeklyHistory.html'
    
    try:
        url = url_fmt.format(df_row.ICAO, date.year, 
                             date.month, date.day)
    except:
        url = url_fmt.format(df_row.IATA, date.year, 
                             date.month, date.day)
    
    try:
        table = pd.read_html(url)[0].dropna(subset=['Max','Avg','Min','Sum'], how='all')
        table.columns = ['Measurement','Max','Avg','Min','Sum']
        table.set_index('Measurement', inplace=True)
        table = table.stack()
        time.sleep(1.0)
    except:
        table = pd.Series({'NULL':np.NaN}, index=pd.Index([0]))
    
    return table


# In[70]:

date_list = pd.DatetimeIndex(weather_scrape.report_date.sort_values().unique())
airport_list = weather_scrape[['ICAO','IATA']].drop_duplicates()


# In[79]:

date_list.shape[0], airport_list.shape[0], date_list.shape[0] * airport_list.shape[0]


# In[ ]:

#for ndate, date in enumerate(date_list):
#    if (ndate>=40):
#    
#        print ndate0
#        df_list = list()
#        
#        for num,(row,dat) in enumerate(airport_list.iterrows()):
#            
#            try:
#                df = scrape_weekly_weather(date, dat)
#            except:
#                df = pd.Series({'NULL':np.NaN}, index=pd.Index([row]))
#    
#            df_list.append((date, dat.name, df))
#            
#        with open('../pkl/df_list{}.pkl'.format(ndate),'w') as fh:
#            dill.dump(df_list, fh)
#    

# In[83]:

# df_list1 = list()
# for num,(row,dat) in enumerate(weather_scrape.iloc[-10:].iterrows()):
#     if (num % 100) == 0:
#         print num
        
#     try:
#         df = scrape_weekly_weather(dat)
#     except:
#         df = pd.Series({'NULL':np.NaN}, index=pd.Index([row]))
        
#     df_list1.append((dat.name, df))


# In[ ]:

#weather_scrape_range = weather_scrape.groupby(['country','IATA','ICAO']).agg({'report_date':[min,max]})
#(weather_scrape_range[('report_date','max')] - weather_scrape_range[('report_date','min')]).sum()

