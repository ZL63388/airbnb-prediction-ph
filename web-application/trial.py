import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import geopy.distance
import pandas as pd
import geopandas
import pickle
from geopandas.tools import sjoin
import warnings
warnings.filterwarnings('ignore')

def load_css(file_name:str)->None:
    """
    Function to load and render a local stylesheet
    """
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def load_dropdown_options():
    global propertytype_options
    global provinces_options
    global amenities_options
    global yesno_options
    global badges_options
    
    yesno_options = ["Yes", "No"]

    with open('propertytype_options.txt', encoding='utf-8') as f:
        content = f.readlines()
    propertytype_options = [line.rstrip('\n').strip() for line in content]
    
    with open('provinces_options.txt',encoding='utf-8' ) as f:
        content = f.readlines()
    provinces_options = [line.rstrip('\n').strip() for line in content]
    
    with open('amenities_options.txt',encoding='utf-8' ) as f:
        content = f.readlines()
    amenities_options = [line.rstrip('\n').strip() for line in content]
    
    with open('badges_options.txt',encoding='utf-8' ) as f:
        content = f.readlines()
    badges_options = [line.rstrip('\n').strip() for line in content]

def load_geodata():
    global listings
    global mall
    global restaurant
    global supermarket
    global tourist_spot
    global public_transpo
    global airport
    global coast
    global highway
    
    listings = pd.read_csv("finaldatav11.csv")
    mall = pd.read_csv("mall.csv")
    restaurant = pd.read_csv("restaurant.csv")
    supermarket = pd.read_csv("supermarket.csv")
    tourist_spot = pd.read_csv("tourism_attractions.csv")
    public_transpo = pd.read_csv("publictranspo_data.csv")
    airport = pd.read_csv("airport_data.csv")
    coast  = geopandas.GeoDataFrame.from_file('coastbuffer.shp')
    highway  = geopandas.GeoDataFrame.from_file('highway_buffer.shp')

def compute_distairport(location, province):
    
    prov_dict={'Biliran': 'Leyte','Southern Leyte': 'Leyte','Eastern Samar': 'Leyte','Siquijor':'Negros Oriental',\
          'Sorsogon': 'Masbate','Guimaras': 'Iloilo','Zamboanga Sibugay': 'Zamboanga del Sur','Bukidnon': 'Misamis Oriental',\
           'Lanao del Norte': 'Misamis Oriental','Lanao del Sur': 'Misamis Oriental','Agusan del Sur': 'Agusan del Norte',\
           'Surigao del Sur': 'Surigao del Norte','Dinagat Islands': 'Surigao del Norte','Cotabato': 'Davao del Sur','Davao del Norte': 'Davao del Sur',\
           'Compostela Valley': 'Davao del Sur','Davao Oriental': 'Davao del Sur', 'Davao Occidental': 'Davao del Sur','Sultan Kudarat': 'Davao del Sur',\
           'Abra': 'Pampanga', 'Kalinga': 'Pampanga','Benguet': 'Pampanga', 'Mountain Province': 'Pampanga','Ifugao': 'Pampanga',\
           'La Union': 'Pampanga', 'Ilocos Sur': 'Pampanga','Zambales': 'Pampanga', 'Pangasinan': 'Pampanga','Tarlac': 'Pampanga', 'Bataan': 'Pampanga',\
           'Apayao': 'Pampanga','Nueva Ecija': 'Pampanga', 'Aurora': 'Pampanga','Nueva Vizcaya': 'Pampanga', 'Quirino': 'Pampanga','Sarangani': 'South Cotabato',\
           'Rizal': 'Metro Manila', 'Laguna': 'Metro Manila', 'Cavite': 'Metro Manila','Bulacan': 'Metro Manila','Batangas': 'Metro Manila', 'Quezon': 'Metro Manila',\
           'Camarines Norte': 'Camarines Sur','Oriental Mindoro': 'Occidental Mindoro',\
           'Caloocan City': 'Metro Manila', 'Las Piñas City': 'Metro Manila', 'Makati City': 'Metro Manila', 'Malabon City': 'Metro Manila',\
           'Mandaluyong City': 'Metro Manila', 'Manila City': 'Metro Manila', 'Marikina City': 'Metro Manila', 'Muntinlupa City': 'Metro Manila',\
           'Navotas City': 'Metro Manila', 'Parañaque City': 'Metro Manila', 'Pasay City': 'Metro Manila', 'Pasig City': 'Metro Manila',\
           'Pateros': 'Metro Manila', 'Quezon City': 'Metro Manila', 'San Juan City': 'Metro Manila', 'Taguig City': 'Metro Manila', 'Valenzuela City': 'Metro Manila'
          }

    airportrows = airport.shape[0]
    lista=[]
    for j in range(0, airportrows):
        if province ==airport['Province'].iloc[j]:
            coords_1=(location.latitude,location.longitude)
            coords_2 = (airport['latitude'].iloc[j], airport['longitude'].iloc[j])
            dist = geopy.distance.geodesic(coords_1, coords_2).km
            lista.append(dist)
            name_airport=airport['name'].iloc[j]
        elif province in prov_dict:
            dataset3=airport[airport['Province']==prov_dict[province.title()]]
            for k in range(0, dataset3.shape[0]):
                coords_1=(location.latitude,location.longitude)
                coords_2 = (dataset3['latitude'].iloc[k], dataset3['longitude'].iloc[k])
                dist = geopy.distance.geodesic(coords_1, coords_2).km
                lista.append(dist)
                name_airport=dataset3['name'].iloc[k]
    dist=sorted(lista)[0]
    return dist

def compute_withincoastal(location):
    df=pd.DataFrame({'latitude':[location.latitude],'longitude':[location.longitude]})
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude))
    listings_in_coast = sjoin(gdf, coast, how='left')
    coastal_zone = listings_in_coast.groupby('index_right')
    within_coastal=0
    if len(coastal_zone)!=0:
        within_coastal=1
    return within_coastal

def compute_withinhighway(location):
    df=pd.DataFrame({'latitude':[location.latitude],'longitude':[location.longitude]})
    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.longitude, df.latitude))
    listings_in_highway = sjoin(gdf, highway, how='left')
    highway_zone = listings_in_highway.groupby('index_right')
    within_highway=0
    if len(highway_zone)!=0:
        within_highway=1
    return within_highway

def compute_geodata(location, province):
    nearby_count_listing = compute_numnearby(listings,location, 1)
    nearby_count_mall = compute_numnearby(mall,location, 5)
    nearby_count_restaurant = compute_numnearby(restaurant,location, 5)
    nearby_count_supermarket = compute_numnearby(supermarket,location, 5)
    nearby_count_tourist_spot = compute_numnearby(tourist_spot,location, 5)
    nearby_count_public_transpo = compute_numnearby(public_transpo,location, 5)
    dist_airport = compute_distairport(location, province)
    within_coastal = compute_withincoastal(location)
    within_highway = compute_withinhighway(location)
    return nearby_count_listing, nearby_count_mall, nearby_count_restaurant, nearby_count_supermarket, nearby_count_tourist_spot, nearby_count_public_transpo, dist_airport, within_coastal, within_highway
    
def compute_numnearby(distdata, location, km):
    nrows = distdata.shape[0]
    nearby_count_listing = 0
    for j in range(0, nrows):
        coords_1=(location.latitude,location.longitude)
        coords_2 = (distdata['latitude'].iloc[j], distdata['longitude'].iloc[j])
        num_dist = abs(location.latitude-distdata['latitude'].iloc[j]) + abs(location.longitude-distdata['longitude'].iloc[j])
        if num_dist < 0.05:
            dist = geopy.distance.geodesic(coords_1, coords_2).km
            if dist < km:
                nearby_count_listing += 1
    return nearby_count_listing


def compute_location(street, barangay, city, province):
    locator = Nominatim(user_agent="fragotyron@gmail.com")
    address=street+', '+barangay+', '+city+', '+province+", philippines"
    location = locator.geocode(address)
    return address, location

def calculator_page():
    st.markdown("<font size=6><b>Airbnb Price Calculator (Philippines)</b></font>", unsafe_allow_html=True)
    st.write("<br>",unsafe_allow_html=True)

    col1, col2 = st.beta_columns([1,1])
    street = col1.text_input("Street name", value='', max_chars=None)
    barangay = col2.text_input("Barangay", value='', max_chars=None)
    city = col1.text_input("City", value='', max_chars=None)
    province = col2.selectbox('Province', options=provinces_options)

    property_type = col1.selectbox('Property type', options=propertytype_options)

    num_guests = col2.number_input("Guest capacity", min_value=1)
    num_bedrooms = col1.number_input("Number of bedrooms", min_value=0)
    num_beds = col2.number_input("Number of beds", min_value=0)
    num_bathrooms = col1.number_input("Number of bathrooms", min_value=0)
    amenities = col2.multiselect('Amenities',options=amenities_options)
    
    pets_allowed = col1.radio("Are pets allowed?",options=yesno_options)
    is_self_checkin = col2.radio("Do you provide self-checkin?",options=yesno_options)
    is_uploaded = col1.radio("Is this listing already available in Airbnb?",options=yesno_options, index=1)
    if is_uploaded == 'Yes':
        is_superhost = col1.radio("Are you an Airbnb superhost?",options=yesno_options)
        is_identityverified = col2.radio("Have you verified your identity in Airbnb?",options=yesno_options)
        is_cancellationpolicy = col1.radio("Have you set a cancellation policy for your listing?",options=yesno_options)
        is_houserules = col2.radio("Have you set some house rules for your listing?",options=yesno_options)
        is_free_parking = col2.radio("Is there free parking within premises?",options=yesno_options)
        badges = col1.multiselect('What badges have you earned?',options=badges_options)
        num_reviews = col2.number_input("How many reviews does your listing have?", min_value=0)
        is_ratings = col1.radio("Have your listing received ratings already?",options=yesno_options, index=1)
        if is_ratings == 'Yes':
            rating_cleanliness = col1.slider("Average rating for cleanliness", min_value=1.00, max_value=5.00, step=0.1)
            col2.write("<br><br><br>",unsafe_allow_html=True)           
            rating_accuracy = col2.slider("Average rating for accuracy", min_value=1.00, max_value=5.00, step=0.1)
            rating_communication = col1.slider("Average rating for communication", min_value=1.00, max_value=5.00, step=0.1)
            rating_location = col2.slider("Average rating for location", min_value=1.00, max_value=5.00, step=0.1)
            rating_checkin = col1.slider("Average rating for check-in", min_value=1.00, max_value=5.00, step=0.1)
            rating_value = col2.slider("Average rating for value", min_value=1.00, max_value=5.00, step=0.1)
        else:
            rating_cleanliness = np.nan
            rating_accuracy = np.nan
            rating_communication = np.nan
            rating_location = np.nan
            rating_checkin = np.nan
            rating_value = np.nan  
    else:
        is_superhost = np.nan 
        is_identityverified = np.nan 
        is_cancellationpolicy = np.nan 
        is_houserules = np.nan 
        is_free_parking  = np.nan
        badges = []
        num_reviews = np.nan 
        is_ratings = np.nan 
        rating_cleanliness = np.nan
        rating_accuracy = np.nan
        rating_communication = np.nan
        rating_location = np.nan
        rating_checkin = np.nan
        rating_value = np.nan         
        
    col1.write("<br>",unsafe_allow_html=True)        
    
    if col1.button("Calculate"):
        process_data(street, barangay, city, province, property_type, num_guests, num_bedrooms, num_beds, num_bathrooms, amenities, pets_allowed,is_self_checkin, is_superhost, is_identityverified, is_cancellationpolicy, is_houserules, is_free_parking, badges, num_reviews, is_ratings, rating_cleanliness, rating_accuracy, rating_communication, rating_checkin, rating_value)

def binary_encode(value):
    if value == "Yes":
        return 1
    else:
        return 0
    
def process_data(street, barangay, city, province, property_type, num_guests, num_bedrooms, num_beds, num_bathrooms, amenities, pets_allowed, is_self_checkin, is_superhost, is_identityverified, is_cancellationpolicy, is_houserules, is_free_parking, badges, num_reviews, is_ratings, rating_cleanliness, rating_accuracy, rating_communication, rating_checkin, rating_value):

    address, location = compute_location(street, barangay, city, province)
   
    nearby_count_listing, nearby_count_mall, nearby_count_restaurant, nearby_count_supermarket, nearby_count_tourist_spot, nearby_count_public_transpo, dist_airport, within_coastal, within_highway = compute_geodata(location, province)

    is_superhost = binary_encode(is_superhost)
    is_identityverified = binary_encode(is_identityverified)
    is_cancellationpolicy = binary_encode(is_cancellationpolicy)
    is_houserules = binary_encode(is_houserules)
    is_free_parking = binary_encode(is_free_parking)
    pets_allowed = binary_encode(pets_allowed)
    is_self_checkin = binary_encode(is_self_checkin)
            
    df = pd.read_csv('finaldatav10.csv')
    travel_dict = pd.Series(df.travelers2019.values,index=df.province).to_dict()
    travelers2019 = travel_dict[province]

    df8 = {'guests': [num_guests], 
           'Numberofbeds': [num_beds],
           'Numberofbedrooms': [num_bedrooms],
           'Numberofbathrooms': [num_bathrooms],
           'Cleanliness': [rating_cleanliness],
           'Accuracy': [rating_accuracy],
           'Communication': [rating_communication],
           'Location_rating': [rating_checkin],
           'Check-in': [rating_checkin],
           'Value': [rating_value],
           'travelers2019': [travelers2019],
           'superhost': [is_superhost],
           'Host_IdentityVerified': [is_identityverified],
           'cancellationpolicy': [is_cancellationpolicy],
           'houserules': [is_houserules],
           'freeparkingonpremises': [is_free_parking],
           'petsallowed': [pets_allowed],
           'num_reviews':[num_reviews],
           'selfcheckin': [is_self_checkin],
           'numnearbylistings': [nearby_count_listing],
           'numneartouristspots5km': [nearby_count_tourist_spot],
           'numnearbymall5km': [nearby_count_mall],
           'numnearbysupermarket5km': [nearby_count_supermarket],
           'numnearbyrestaurants5km': [nearby_count_restaurant],
           'numnearpublictranspo': [nearby_count_public_transpo],
           'distance_airport': [dist_airport],
           'within3km': [within_highway],
           'coast750m': [within_coastal]
      }
    
    for i in amenities_options:
        if i in amenities:
            df8[i] = 1
        else:
            df8[i] = 0
            
    for i in provinces_options:
        if i == province:
            df8[i] = 1
        else:
            df8[i] = 0

    for i in badges_options:
        if i in badges:
            df8[i] = 1
        else:
            df8[i] = 0
    
    for i in propertytype_options:
        if i == property_type:
            df8[i] = 1
        else:
            df8[i] = 0
            
    df8 = pd.DataFrame(data=df8)

    df8.to_csv('df8.csv')
#    st.write(location.address + '\n')
#    st.write(str(location.latitude) + '\n')
#    st.write(str(location.longitude) + '\n')
#    st.write(str(nearby_count_listing) + '\n')
#    st.write(str(nearby_count_mall) + '\n')
#    st.write(str(nearby_count_restaurant) + '\n')
#    st.write(str(nearby_count_supermarket) + '\n')
#    st.write(str(nearby_count_tourist_spot) + '\n')
#    st.write(str(nearby_count_public_transpo) + '\n')
#    st.write(str(dist_airport) + '\n')
#    st.write(str(within_coastal) + '\n')
#    st.write(str(within_highway) + '\n')
    
    # loading the trained model
    pickle_in = open('XGBmodel.pkl', 'rb') 
    XGBmodel = pickle.load(pickle_in)
    df8 = df8[XGBmodel.get_booster().feature_names]

    st.markdown("""
    <style>
    .price-font {
        font-size:28px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<p class='price-font'>Estimated price:   <b>" + str(int(XGBmodel.predict(df8)[0])) + " PHP </b></p>", unsafe_allow_html=True)
    st.markdown("The model used to estimate the price has an RMSE of 1804.55", unsafe_allow_html=True)

def tableau_page():   
    html_temp = """
    <div class='tableauPlaceholder' id='viz1617959384576' style='position: relative'><noscript><a href='#'><img alt='Capstone: Predicting Airbnb Price ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ai&#47;AirbnbPricePredictionCapstone&#47;CapstonePredictingAirbnbPrice&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='AirbnbPricePredictionCapstone&#47;CapstonePredictingAirbnbPrice' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ai&#47;AirbnbPricePredictionCapstone&#47;CapstonePredictingAirbnbPrice&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1617959384576');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1024px';vizElement.style.height='795px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1024px';vizElement.style.height='795px';} else { vizElement.style.width='100%';vizElement.style.height='1827px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
    components.html(html_temp, width=1600, height=800, scrolling=True)

def introduction_page():
    col1, col2 = st.beta_columns([1,20])

    col2.markdown("""
    <style>
    .page-font {
        font-size:16px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col2.markdown("<font size=6><b>The Price is Right: Airbnb Pricing Recommendation</b></font><font size=4><br>Predicting the Optimal Price of Listings in the Philippines Using a Machine Learning Model</font>", unsafe_allow_html=True)
    col2.markdown("<br>", unsafe_allow_html=True)
    col2.markdown("<h2 style='text-align: left; color:#ff5a5f;'>Introduction</h2>", unsafe_allow_html=True)
    col2.write("\n\n")
    col2.markdown("<p class='page-font'>Last year, as with most other businesses, Airbnb was rocked by COVID-19. Multiple news about Airbnb's future headlined several articles as large numbers of cancellations and slow bookings created a massive loss in revenue globally but even more appalling is the situation of its hosts.</p>", unsafe_allow_html=True)
    col2.markdown("<p class='page-font'>With the current situation, the collapse of startups has been prevalent during the pandemic.<b> Airbnb experienced a booking drop over 70% and cut its half in valuation.</b></p>", unsafe_allow_html=True)
    col2.markdown("<p class='page-font'>In the wake of the pandemic, emergence of <b>dynamic pricing</b> has become a business strategy for survival.</p>", unsafe_allow_html=True)

    col2.write("\n\n")
    col2.image(['pic1.jpg','pic2.jpg'], width=400)
    col2.markdown("<h2 style='text-align: left; color:#ff5a5f;'>The team's objectives:</h2>", unsafe_allow_html=True)
    col2.write("\n")
    col2.markdown("<p class='page-font'>1.    Identifying the factors affecting the price of Airbnb listings in the Philippines.</h2>", unsafe_allow_html=True)
    col2.markdown("<p class='page-font'>2.    Train a Machine Learning Model that identifies a pricing system for PH Airbnb hosts to optimize their listing price.", unsafe_allow_html=True)

def data_info_page():
    col1, col2 = st.beta_columns([1,20])

    col2.markdown("""
    <style>
    .page-font {
        font-size:16px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col2.markdown("<font size=6><b>Data Information</b></font>", unsafe_allow_html=True)
    col2.markdown("<h2 style='text-align: left; color:#ff5a5f;'>About the data</h2>", unsafe_allow_html=True)
    col2.write("\n\n")    
    col2.markdown("<p class='page-font'>A total of <b>12,336 listings in the Philippines</b> was scraped from the Airbnb website.</p>", unsafe_allow_html=True)
    col2.markdown("<p class='page-font'>Our data contains available Airbnb listings together with their details ranging from price to various property types along with <b>proximity analysis</b> which is the calculated distance of an Airbnb listing to a spatial feature such as if the listing is nearby an airport, supermarkets and listings.</p>", unsafe_allow_html=True)    
    col2.markdown("<p class='page-font'>Data was acquired on <b>March 26, 2021</b>. This model is a prototype for this specific timestamp in order to take into account the price variability with respect to time.</p>", unsafe_allow_html=True)      
    
    col2.image('samplelisting.JPG', width=600, caption="Sample Airbnb Listing Page")
    col2.markdown("<br>", unsafe_allow_html=True)
    col2.write("<p class='page-font'><b>The following information was scraped from each listing:</b>", unsafe_allow_html=True)
    col2.write("<p class='page-font'>1. Title", unsafe_allow_html=True)
    col2.write("<p class='page-font'>2. Location (province, latitude, and longitude)", unsafe_allow_html=True)
    col2.write("<p class='page-font'>3. Capacity Information (e.g. Number of guest, number of bedrooms)", unsafe_allow_html=True)    
    col2.write("<p class='page-font'>4. Property Type (e.g. Entire apartment)", unsafe_allow_html=True)    
    col2.write("<p class='page-font'>5. Price", unsafe_allow_html=True)
    col2.write("<p class='page-font'>6. Amenities", unsafe_allow_html=True)
    col2.write("<p class='page-font'>7. Description badges (e.g. Enhanced Clean)", unsafe_allow_html=True)
    col2.write("<p class='page-font'>8. Reviews (number only)", unsafe_allow_html=True)
    col2.write("<p class='page-font'>9. Ratings", unsafe_allow_html=True)

    col2.markdown("<h2 style='text-align: left; color:#ff5a5f;'>Spatial Distribution of the data</h2>", unsafe_allow_html=True)
    col2.write("\n\n")    
    col2.markdown("<p class='page-font'>After the data cleaning process, <b>11,409</b> listings in the Philippines were used in the analysis and regression. Most of the listings are located along the coastline.</p>", unsafe_allow_html=True)
    col2.image('datainfo.png', width=600, caption="Spatial Distribution of Airbnb Listings in the Philippines")
    col2.markdown("<p class='page-font'>The provinces with no Airbnb listings are <b>Tawi-tawi, Sulu and Basilan.</b></p>", unsafe_allow_html=True)

    col2.markdown("<h2 style='text-align: left; color:#ff5a5f;'>Distribution of price per night</h2>", unsafe_allow_html=True)
    col2.write("\n\n")    

    col2.markdown("<p class='page-font'>Airbnb prices range from <b>30 PHP to 48,160 PHP</b> with an average of <b>2,327 PHP</b> per night. The most expensive property is an <b>entire villa</b> while the cheapest is a <b>shared room.</b></p>", unsafe_allow_html=True)
    
    col2.write("\n\n")
    col2.image('datainfo2.png', width=400, caption="Spatial Distribution of Airbnb Listings in the Philippines")
    col2.write("\n\n")  
  
    
def methodology_page():
    col1, col2 = st.beta_columns([1,20])

    col2.markdown("""
    <style>
    .page-font {
        font-size:16px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col2.markdown("<font size=6><b>Strategy</b></font>", unsafe_allow_html=True)
    col2.write("\n\n")
    col2.image('Methodology.jpg', width=900)

def regression_page():
    col1, col2 = st.beta_columns([1,20])

    col2.markdown("""
    <style>
    .page-font {
        font-size:16px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    col2.markdown("<font size=6><b>Regression Modeling</b></font>\n", unsafe_allow_html=True)  
    col2.markdown("<p class='page-font'>The team implemented 7 regression models, 3 of which are ensemble models as shown on the first three columns, and 4 variants of linear regression for the remaining columns.</p>", unsafe_allow_html=True)
    col2.markdown("<p class='page-font'>The best performing model is the <b>XGBoost Regressor</b> which has undergone <b>hyperparameter optimization</b> tuning. This resulted with an R squared of <b>0.65</b>, and an RMSE of <b>1804.55</b>\n\n</p>", unsafe_allow_html=True)   
    col2.image('models.PNG', caption="Performance of the regression models", width=900)  

def conclusion_page():
    col1, col2 = st.beta_columns([1,20])

    col2.markdown("""
    <style>
    .page-font {
        font-size:16px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col2.markdown("<font size=6><b>Recommendations for the Airbnb hosts.</b></font>", unsafe_allow_html=True)
    col2.write("\n\n")    
    col2.markdown("<h2 style='text-align: left;'>The more, the merrier</h2>", unsafe_allow_html=True)
    col2.markdown("<p class='page-font'>The <b>number of guests</b> has the strongest relationship with price per night. Along with that, our model also suggests that it is the top predictor for the Airbnb pricing. As the number of guests increases, price also generally increases.<p>", unsafe_allow_html=True)   
    col2.markdown("<p class='page-font'>We do recommend <b>increasing the guest capacity</b> by adding more beds.<p>", unsafe_allow_html=True)
    
    col2.image('reco1.png', width=300, caption="Correlation of capacity features with price per night")
    
    col2.markdown("<h2 style='text-align: left;'>Spatial is special</h2>", unsafe_allow_html=True)
    col2.write("\n\n")    
    col2.markdown("<p class='page-font'>Among the spatial features that we have added from our proximity analysis, the <b>distance from the airport</b> is the most correlated feature with price per night and is also an important predictor for pricing.<p>", unsafe_allow_html=True)   
    col2.markdown("<p class='page-font'>Most of the listings are <b>near the coastline and far from the airports</b>. These listings tend to have higher price per night as compared to those not within the coastline.<p>", unsafe_allow_html=True)
    col2.markdown("<p class='page-font'>Listings near the coastline gives touristic ambience which gives an additive value to the property.<p>", unsafe_allow_html=True)    
    col2.image('reco2.png', width=500, caption="Correlation of spatial features with price per night")    
     
    col2.markdown("<h2 style='text-align: left;'>You’re in the right place!</h2>", unsafe_allow_html=True)
    col2.write("\n\n") 
    col2.markdown("<p class='page-font'><b>Batangas</b> has the most expensive median price per night followed by Bataan, Marinduque, Batanes and Zambales.<p>", unsafe_allow_html=True)
    col2.image('reco3.png', width=500)
    
    col2.markdown("<p class='page-font'>The median prices in <b>mainland Luzon</b> are generally higher compared to Visayas and Mindanao.<p>", unsafe_allow_html=True)
    col2.markdown("<p class='page-font'>Also, compared to the rest of mainland Luzon, the median prices in <b>NCR</b> are generally lower.<p>", unsafe_allow_html=True)    
    col2.image('reco4.png', width=500)
    
    col2.markdown("<h2 style='text-align: left;'>Amenity is a necessity!</h2>", unsafe_allow_html=True)
    col2.markdown("<p class='page-font'>The most common amenities that an Airbnb host should have are <b>aircon, Wi-Fi, parking and clothes storage.</b></p>", unsafe_allow_html=True) 
    col2.markdown("<p class='page-font'>A rare amenity “must have” which can help increase pricing is providing your guests with <b>board games.</b></p>", unsafe_allow_html=True)     
    col2.markdown("<p class='page-font'>Adding a <b>grill</b> can increase pricing because of its positive correlation with price.</p>", unsafe_allow_html=True)    
    col2.markdown("<p class='page-font'><b>Kettle, utensils, first aid kits, and hygiene kits</b> are amenities that a host can easily provide which can also add value to the price.</p>", unsafe_allow_html=True)       
    col2.markdown("<p class='page-font'>Investing on having a <b>hair dryer, iron, microwave, and providing a breakfast meal</b> for your guests are also the recommended ways to increase your listing price.</p><br>", unsafe_allow_html=True)    
    col2.image('reco5.png', width=600)
    
    
    
    

def contributors_page():
    col1, col2 = st.beta_columns([1,20])
    col2.markdown("<font size=6><b>The Price is Right: Airbnb Pricing Recommendation</b></font><font size=4><br>Predicting the Optimal Price of Listings in the Philippines Using a Machine Learning Model</font>", unsafe_allow_html=True)   
    col2.markdown("<br>This capstone project was created as part of the Eskwelabs Data Science Fellowship Cohort VI. Get to know more about this fellowship through: https://www.eskwelabs.com/data-science-fellowship", unsafe_allow_html=True)    
    col2.markdown("<br>", unsafe_allow_html=True)
    col2.markdown("Contributors:", unsafe_allow_html=True)
    col2.markdown("<font size=5>Edward Nataniel Apostol</font><br>edward.nataniel@gmail.com<br>https://www.linkedin.com/in/edward-apostol/", unsafe_allow_html=True)
    col2.markdown("<font size=5>Tyron Rex Frago</font><br>fragotyron@gmail.com<br>https://www.linkedin.com/in/tyron-rex-frago-754b2a1b0/", unsafe_allow_html=True)    
    col2.markdown("<font size=5>Zipporah Luna</font><br>zipporah.luna@gmail.com<br>https://www.linkedin.com/in/lunazipporahd/", unsafe_allow_html=True)       
    col2.markdown("<font size=5>Jonarie Vergara</font><br>vernarie0814@gmail.com<br>https://www.linkedin.com/in/jonarie-vergara-28865b64/", unsafe_allow_html=True)
    col2.markdown("<font size=5>John Barrion (Mentor)</font><br>barrionjohn@gmail.com<br>https://www.linkedin.com/in/johnbarrion/", unsafe_allow_html=True)
    
    
    
def main():
    """
    Main function
    """ 
    load_dropdown_options()
    load_geodata()
    load_css("styles/style.css")
    
    
    st.sidebar.image('header_sidebar.png', width=300)
    st.sidebar.markdown("<font size=4 color=#FFFFF><br> Site Contents:</font>", unsafe_allow_html=True)
    my_page = st.sidebar.radio('', ['Introduction', 'Data Information', 'Tableau Dashboard of Listings', 'Strategy', 'Regression Model', 'Airbnb Price Calculator', 'Recommendations for Airbnb Hosts', 'Contributors'])
    if my_page == 'Introduction':
        introduction_page()    
    elif my_page == 'Data Information':
        data_info_page()
    elif my_page == 'Strategy':
        methodology_page()
    elif my_page == 'Tableau Dashboard of Listings':
        tableau_page()
    elif my_page == 'Regression Model':
        regression_page()
    elif my_page == 'Airbnb Price Calculator':
        calculator_page()
    elif my_page == 'Recommendations for Airbnb Hosts':
        conclusion_page()
    elif my_page == 'Contributors':
        contributors_page()
        
if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.cache()
    main()
    
    

    
