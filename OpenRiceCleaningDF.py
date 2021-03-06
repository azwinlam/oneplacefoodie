# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 16:08:55 2021

@author: azwin
"""
import pandas as pd
import numpy as np
import seaborn as sns
import re
import ast 
import pickle
import requests
import json

#cuisine_d and district_d pickles
district_d_p = pickle.load( open( "district_d.p", "rb" ) )
cuisine_d_p = pickle.load( open( "cuisine_d.p", "rb" ) )

df = pd.read_csv("./data/openrice2021 - raw.csv")
df = df.dropna(thresh=5)

#Create RestaurantID and set as index
df.insert(0,"restaurantID", [i for i in range(df.shape[0])])
df = df.set_index("restaurantID")

#rename columns
df.columns = ['name', 'name2', 'stars', 'review_count', 'bookmarks', 'district_ch',
       'price_range', 'food_type', 'emoji', 'add_ch', 'add_en',
       'transport', 'telephone', 'intro', 'storehours', 'payment', 'reviews']

#fill in name2 with name1 if nan
df.name2 = df['name2'].fillna(df['name'])



#renaming restaurant_index ID

new_index = []
for i in range(df.shape[0]):
    new_index.append(f"rest{i}")

df.index = new_index

#%%

#Get GPS Lat Lon of Address
# def get_latlon(x):
#     try:
#         url = "https://www.als.ogcio.gov.hk/lookup?q="
#         headers = {"Accept": 'application/json', "Accept-Language": 'en'}
#         address = x
#         res = requests.get(url+address, headers=headers)
#         geo = json.loads(res.text)
#         lat = float(geo["SuggestedAddress"][0]["Address"]["PremisesAddress"]["GeospatialInformation"]["Latitude"])
#         lon = float(geo["SuggestedAddress"][0]["Address"]["PremisesAddress"]["GeospatialInformation"]["Longitude"])
#         return lat,lon
#     except:
#         pass
    
    
## SESSIONS
# from requests_futures.sessions import FuturesSession
# session = FuturesSession()

# def make_request(session, address):
    
#     data = {"q":address, "n":1}
#     headers ={"Accept": "application/json"}
#     api_url = "https://www.als.ogcio.gov.hk/lookup"
#     future = session.post(api_url,data=data,headers=headers)
#     return future

# import time,sys

# def print_progress(futures):

#     check_done = lambda x: x.done()
#     check_done = np.vectorize(check_done)

#     #basic percentage progress
#     while not check_done(futures).all():
#         time.sleep(1)
#         percent = check_done(futures).mean() * 100
#         sys.stdout.write("\r%d%%" % percent)
#         sys.stdout.flush()    
#     print("\n")
    
# #create session with 16 workers
# session = FuturesSession(max_workers=32)
# #make all of the requests
# futures =   np.array([ make_request(session,address) for address in df.add_en]) 
# print_progress(futures)    

# geo_add = []
# for future in futures:
#     try:
#         geo = future.result().json()
#         geo_add.append(geo)
#     except:
#         geo_add.append(np.nan)
# pickle.dump(geo_add, open( "latlon.p", "wb" ))

# geo_address_list = pickle.load(open('latlon.p','rb'))

# lst = []
# for latlon in geo_address_list:
#     try:
#         lat = float(latlon["SuggestedAddress"][0]["Address"]["PremisesAddress"]["GeospatialInformation"]["Latitude"])
#         lon = float(latlon["SuggestedAddress"][0]["Address"]["PremisesAddress"]["GeospatialInformation"]["Longitude"])
#         lst.append((lat,lon))
#     except:
#         lst.append(np.nan)
# pickle.dump(lst, open( "latlon_clean.p", "wb" ))


geo_address_list = pickle.load(open('latlon_clean.p','rb'))
df['latlon'] = geo_address_list
df['lat'] = df.latlon.apply(lambda x: x[0] if isinstance(x,tuple) else np.nan)
df['lon'] = df.latlon.apply(lambda x: x[1] if isinstance(x,tuple) else np.nan)
#district chinese to English column

district_d = {'??????': "Tai Po",
 '?????????': "Discovery Bay",
 '??????': "Kwun Tong",
 '?????????': "Kowloon City",
 '?????????': "Ma On Shan",
 '?????????': "Kowloon Bay",
 '?????????': "Ap Lei Chau",
 '??????': "Tuen Mun",
 '??????': "Fan Ling",
 '?????????': "Tseung Kwan O",
  '??????': "Mid-Levels",
  '?????????': "Tsim Sha Tsui",
  '??????' : "Yau Tong",
  '??????' : "Yuen long",
  '??????' : "Tin Hau",
  '??????' : "Mong Kok",
  '?????????':"Quarry Bay",
  '?????????': "Cheung Sha Wan",
  '??????' : "Hung Hom",
  '?????????': "Wong Tai Sin",
  '??????': "Wan Chai",
  '??????': "Ma Wan",
  '??????': "Central",
  '??????': "Jordan", 
  '??????': "Tai Wai", 
  '??????': "Lam Tin",
  '??????': "Sheung Wan",
  '??????': "Tung Chung", 
  '??????': "Tsing Yi",
  '?????????': "Yau Ma Tei",
  '?????????': "Shum Shui Po",
  '??????': "Shatin",
  '?????????' : "Lai Chi Kok",
  '??????': "Tai O",
  '??????': "Fo Tan",
  '?????????': "Causeway Bay",
  '?????????': "Sai Wan Ho",
  '?????????': "Shek Kip Mei",
  '??????': "Chai Wan",
  '?????????': "Tai Kok Tsui",
  '??????': "Sheung Shui",
  '??????': "Kwai Fong",
  '?????????': "Tin Shui Wai",
  '??????': "The Peak",
  '??????': "Sai Wan",
  '??????': "Lok Fu",
  '??????': "Tsuen Wan",
  '?????????': "Lamma Island",
  '?????????': "To Kwa Wan",
  '?????????': "Shau Kei Wan",
  '(?????????)': "Non Storefront",
  '?????????': "Ngau Tau Kok",
  '?????????': "Tsz Wan Shan",
  '?????????': "Chek Lap Kok",
  '??????': "Kwai Chung",
  '?????????': "Aberdeen",
  '?????????': "San Po Kong",
  '??????': "North Point",
  '?????????': "Wong Chuk Hang",
  '??????': "Stanley ",
  '?????????': "Ho Man Tin",
  '??????': "Prince Edward",
  '??????': "Taikoo ",
  '?????????': "Lantau",
  '?????????': "Pok Fu Lam",
  '??????': "Sai Kung",
  '??????': "Choi Hung",
  '?????????': "Lau Fau Shan",
  '??????' : "Mei Foo",
  '?????????' : "Diamond Hill",
  '?????????': "Happy Valley",
  '?????????': "Kowloon Tong", 
  '??????': "Tai Hang",
  '??????': "Cheung Chau",
  '??????': "Shek O",
  '??????': "Sham Tseng",
  '??????': "Tai Wo",
  '??????': "Admiralty",
  '??????': "Lo Wu",
  '?????????': "Lei Yue Mun",
  '??????': "Peng Chau",
  '?????????': "Repulse Bay",
  '?????????': "Deep Water Bay",
  '?????????': "Heng Fa Chuen",
  '?????????': "Lok Ma Chau",
  '?????????': "Po Toi",
  '?????????': "Hong Kong Island"}

#Price Dictionary
price_d = {50: "Less than 50 HKD",
            51: "51-100 HKD", 
            101: "101-200 HKD", 
            201: "201-400 HKD", 
            401: "401-800 HKD", 
            801: "More than 801 HKD"}

dollar_d = {50: "$",
            51: "$$", 
            101: "$$$", 
            201: "$$$$", 
            401: "$$$$$", 
            801: "$$$$$$"}

def translate_district(x):
    try:
        return district_d[x]
    except:
        return np.nan
    
def translate_cuisine(x):
    try:
        return cuisine_d_p[x]
    except:
        return np.nan
    
#Adding Main Cuisine Column
df["cuisine_ch"] = df.food_type.str.extract(r'(\w+)')

df["district_en"] = df.district_ch.apply(translate_district)
df["cuisine_en"] = df.cuisine_ch.apply(translate_cuisine)

#Cleaning price column
df['price'] = df.price_range.str.extract(r'(\d+)')
df['price'] = df.price.astype("float")
df['dollarsign'] = df.price.map(dollar_d)


# df.emoji column ast.literal_eval(ini_list) 
df.emoji = df.emoji.apply(lambda x: ast.literal_eval(x) if isinstance(x,str) else x)

#Adding Positive, Neutral, Negative
df['emoji_positive'] = df.emoji.apply(lambda x: x[0] if isinstance(x,list) else 0).astype("int16")
df['emoji_neutral'] = df.emoji.apply(lambda x: x[1] if isinstance(x,list) else 0).astype("int16")
df['emoji_negative'] = df.emoji.apply(lambda x: x[2] if isinstance(x,list) else 0).astype("int16")

def split(x):
    try:
        return x.split()
    except:
        pass

df['food_types_cleaning'] = df.food_type.apply(split)

types = []

for i in df.food_types_cleaning:
    try:
        if len(i) == 1:
            types.append(i)
        elif len(i) >1:
            for j in i:
                types.append(j)
    except:
        pass

cuisine = []
for i in types:
    if isinstance(i, str):
        cuisine.append(i)

unique_cuisine = set(cuisine)
    
    

    





    
    
# onehot_cuisine = pd.get_dummies(temp_df.cuisine_en)
    
    
# #USER INDEX, RESTAURANT COLUMNS    
# user_restaurant = pd.DataFrame(columns=temp_df.index.tolist())

# #USER DB
# user_df =pd.DataFrame()    

# from randomuser import RandomUser

# # Generate a single user
# user = RandomUser()
# # Generate a list of 10 random users
# user_list = RandomUser.generate_users(3000,get_params={'nat': 'US'})

# firstname = []
# lastname = []
# fullname = []
# gender = []
# dob = []
# age = []
# nat = []
# for i in user_list:
#     firstname.append(i.get_first_name())
#     lastname.append(i.get_last_name())
#     fullname.append(i.get_full_name())
#     gender.append(i.get_gender())
#     dob.append(i.get_dob(parse_time=False))
#     age.append(i.get_age())
#     nat.append(i.get_nat())
    

# d = {"first_name": firstname,
#      "last_name": lastname,
#      "full_name" : fullname,
#      "gender": gender,
#      "dob": dob,
#      "age": age,
#      "nationality": nat,
#      }
    
# user_df = pd.DataFrame(d)

# user_df = user_df.rename_axis("user_id")
# user_index = []
# for i in range(user_df.shape[0]):
#     user_index.append(f"user{i}")
# user_df.index = user_index
    
# user_df.to_csv("./recommendation_attempt1/fakeusers3000.csv")

temp_df = df[~df['latlon'].isnull()][["name",'name2','district_en','price','dollarsign','cuisine_en','add_en','emoji_positive','emoji_neutral','emoji_negative','stars','review_count','bookmarks','lat','lon','telephone']]
temp_df.to_csv("./recommendation_attempt1/temp_df8.csv")    
    
# district_array = np.sort(df.district_en.unique())
# district_array = np.insert(district_array, 0, values=show_all)
    
    # current
#Testing address lookup#




    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    