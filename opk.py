import streamlit as st
import pandas as pd
import numpy as np
# import requests
# import json
import pydeck as pdk
# import webbrowser

token = "pk.eyJ1IjoiYXp3aW5sYW0iLCJhIjoiY2ttZWZ1OXlmMGhneTJvbnpmbjN0cGlncCJ9.F9dG4cOF6weMIwUx1ajL6A"

st.set_page_config(
    page_title="One Place Foodie!",
    layout="wide",
    initial_sidebar_state="expanded",
    )

@st.cache()
def default_csv():
    return pd.read_csv("temp_df8.csv", index_col=0, header=0)

st.title('Welcome to One Place Foodie! v6')
st.header("")

df = default_csv()

#District Side Bar
district_array = np.sort(df.district_en.unique())
district_array = np.insert(district_array, 0, values="All District")

pick_district = st.sidebar.selectbox(
        'Pick Location:', district_array, index=4)

#Cuisine Side Bar
if pick_district == "All District":
    cuisine_array = df["cuisine_en"].value_counts().index.unique()
else:
    cuisine_array = df.loc[(df.district_en.str.contains(pick_district))]["cuisine_en"].value_counts().index.unique()
    cuisine_array = np.insert(cuisine_array, 0, values="All Cuisine")

pick_cuisine = st.sidebar.selectbox(
        'Pick Cuisine:', cuisine_array)


if pick_district == "All District" and pick_cuisine == "All Cuisine":
    df_temp = df.iloc[:,:]
if pick_district == "All District" and pick_cuisine != "All Cuisine":
    df_temp = df.loc[df.cuisine_en.str.contains(pick_cuisine)]
if pick_district != "All District" and pick_cuisine == "All Cuisine":
    df_temp = df.loc[(df.district_en.str.contains(pick_district))]
if pick_district != "All District" and pick_cuisine != "All Cuisine":
    df_temp = df.loc[(df.district_en.str.contains(pick_district)) & (df.cuisine_en.str.contains(pick_cuisine))]


st.header(f"There are {df_temp.shape[0]} restaurants in {pick_district} for {pick_cuisine}")

df_show = df_temp[["name",'name2','dollarsign','cuisine_en','stars','emoji_positive','emoji_neutral','emoji_negative','review_count','bookmarks']]

try:
    st.write(df_show)
except:
    st.write("No restaurants from selection")
    
rest_num = st.number_input(label="Input Restaurant Number",value=int(df_temp.index[0][4:]),step = 1)

restaurant = df[df.index==f"rest{rest_num}"]


#Address Lat Lon lookup
# url = "https://www.als.ogcio.gov.hk/lookup?q="
# headers = {"Accept": 'application/json', "Accept-Language": 'en'}
# address = restaurant.add_en.values[0]
# res = requests.get(url+address, headers=headers)

# geo = json.loads(res.text)
# lat = float(geo["SuggestedAddress"][0]["Address"]["PremisesAddress"]["GeospatialInformation"]["Latitude"])
# lon = float(geo["SuggestedAddress"][0]["Address"]["PremisesAddress"]["GeospatialInformation"]["Longitude"])
geo_address = pd.DataFrame({"lat":[restaurant.lat.values[0]],
                            "lon":[restaurant.lon.values[0]],
                            "name" : [restaurant.name.values[0]],
                            "add_en" : [restaurant.add_en.values[0]],
                           "dollarsign" : [restaurant.dollarsign.values[0]],
                           }, index=None)
if {restaurant.name.values[0]} == {restaurant.name2.values[0]}:
    st.write(f"Restaurant Name: {restaurant.name.values[0]}")
else:
    st.write(f"Restaurant Name: {restaurant.name.values[0]}, {restaurant.name2.values[0]} ")
st.write(f"Cuisine: {restaurant.cuisine_en.values[0]}")
st.write(f"District: {restaurant.district_en.values[0]}")

url = 'https://www.google.com/maps/search/?api=1&query=' + restaurant.name2.values[0] + ' ' + restaurant.add_en.values[0]
address_url = f'<a href="{url}" target="_blank"> {restaurant.add_en.values[0]}</a>'
st.markdown(f"Address: {address_url}", unsafe_allow_html=True)

if restaurant.telephone.values[0] is not np.nan:
    phone_number = f'<a href="tel:{restaurant.telephone.values[0]}"> {restaurant.telephone.values[0]} </a> '
    st.markdown(f"Phone Number: {phone_number}", unsafe_allow_html=True)
else:
    st.markdown("Phone Number: None", unsafe_allow_html=True)
st.write(f"Price: {restaurant.dollarsign.values[0]}")




test = df_temp[['name','add_en','lat','lon','dollarsign']].dropna()

layer =[ pdk.Layer(
    "ScatterplotLayer",
    test,
    pickable=True,
    opacity=0.8,
    stroked=True,
    filled=True,
    radius_scale=6,
    radius_min_pixels=1,
    radius_max_pixels=100,
    line_width_min_pixels=1,
    get_position=['lon','lat'],
    get_fill_color=[0, 0, 0],
    get_line_color=[0, 255, 0],
    ),
    pdk.Layer(
        "ScatterplotLayer",
        geo_address,
        pickable=True,
        opacity=0.8,
        stroked=True,
        filled=True,
        radius_scale=6,
        radius = 200,
        radius_min_pixels=1,
        radius_max_pixels=100,
        line_width_min_pixels=1,
        get_position=['lon','lat'],
        get_fill_color=[255, 0, 0],
        get_line_color=[255, 0, 0],
    )]
view_state = pdk.ViewState(latitude=restaurant.lat.values[0], longitude=restaurant.lon.values[0], zoom=17, bearing=0, pitch=0)

try:
    st.pydeck_chart(pdk.Deck(
        layers=[layer], 
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/light-v9',
        tooltip={"text": "{name}\n{add_en}\n {dollarsign}"},
        ))
except:
    st.write("No address for this restaurant listing")
