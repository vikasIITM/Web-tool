import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns
import pandas as pd
import streamlit as st
import plotly.express as px
import os
import base64
from sklearn.cluster import KMeans
import geopandas as gpd


# from PIL import Image
# image = Image.open('Header.png')

# st.image(image)


st.set_page_config(page_title="SDA", page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
file_ = open("Header.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
)
ZOOM = 4.85
OPE = 0.99
RADIUS = 17
def preprocessor(file):
    col_name = ['remove','lon','lat']
    mon = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    for i in range(1901,2021):
        for ii in range(12):
            col_name.append(str(i)+"_"+mon[ii])
    read_path = file
    try:
        df = pd.read_csv(read_path)
        #st.write(len(df.columns))
    except:
        df = pd.read_excel(read_path)

    try:
        df.columns = col_name
    except:
        print("Already have columns Name")
        df.rename(columns = {'Long':'lon','Lat':'lat'}, inplace = True)
        df.columns = col_name 

    return df


# df = pd.read_csv("Copy of Copy of NWH-CRU_tmp_1901-2020_month_50km.csv")
# month_df = df  
# col_name = ['lon' , 'lat']
# month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
# for i in range(1901,2021):
#   for ii in range(12):
#     col_name.append(str(i)+'_'+month[ii])

# df.columns = col_name


def corr_action_new(df,yr1,yr2):
    df.rename(columns = {'Longitude':'lon','Latitude':'lat'}, inplace = True)
    col_name = ['lat','lon']
    mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in range(yr1,yr2):
        for ii in range(12):
            # if i < 10:
            #     col_name.append(mon[ii]+"-"+"0"+str(i))
            #else:
            col_name.append(mon[ii]+"-"+str(i)[2:])
    
    ndf = pd.DataFrame()
    
    #ndf['lat'] = df['lat']
    #ndf['lon'] = df['lon']
    return df[col_name]




def action_new(df,yr1,yr2):
    df.rename(columns = {'Longitude':'lon','Latitude':'lat'}, inplace = True)
    col_name = []
    mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in range(yr1,yr2):
        for ii in range(12):
            # if i < 10:
            #     col_name.append(mon[ii]+"-"+"0"+str(i))
            #else:
            col_name.append(mon[ii]+"-"+str(i)[2:])
    
    ndf = pd.DataFrame()
    
    ndf['lat'] = df['lat']
    ndf['lon'] = df['lon']
    df = df[col_name]
    ndf['Std'] = df.iloc[:,2:].std(axis = 1)
    ndf['Min'] = df.iloc[:,2:].min(axis = 1)
    ndf['Max'] = df.iloc[:,2:].max(axis = 1)
    ndf['Mean'] = df.iloc[:,2:].mean(axis = 1)
    ndf['Q1'] = df.iloc[:,2:].quantile(0.25,axis = 1)
    ndf['Q2'] = df.iloc[:,2:].quantile(0.50,axis = 1)
    ndf['Q3'] = df.iloc[:,2:].quantile(0.75,axis = 1)
    ndf['Q4'] = df.iloc[:,2:].quantile(1,axis = 1)
    ndf['IQR'] = ndf['Q3'] - ndf['Q1']
    ndf['Skewness'] = df.iloc[:,2:].skew(axis = 1)
    ndf['Kurtosis'] = df.iloc[:,2:].kurtosis(axis = 1)
    return ndf
def action(df,yr1,yr2):
    col_name = []
    mon = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
    for i in range(yr1,yr2):
        for ii in range(12):
            col_name.append(str(i)+"_"+mon[ii])
    
    ndf = pd.DataFrame()
    
    ndf['lat'] = df['lat']
    ndf['lon'] = df['lon']
    df = df[col_name]
    ndf['Std'] = df.iloc[:,2:].std(axis = 1)
    ndf['Min'] = df.iloc[:,2:].min(axis = 1)
    ndf['Max'] = df.iloc[:,2:].max(axis = 1)
    ndf['Mean'] = df.iloc[:,2:].mean(axis = 1)
    ndf['Q1'] = df.iloc[:,2:].quantile(0.25,axis = 1)
    ndf['Q2'] = df.iloc[:,2:].quantile(0.50,axis = 1)
    ndf['Q3'] = df.iloc[:,2:].quantile(0.75,axis = 1)
    ndf['Q4'] = df.iloc[:,2:].quantile(1,axis = 1)
    ndf['IQR'] = ndf['Q3'] - ndf['Q1']
    ndf['Skewness'] = df.iloc[:,2:].skew(axis = 1)
    ndf['Kurtosis'] = df.iloc[:,2:].kurtosis(axis = 1)
    return ndf
#ndf = df[['lat','lon']]
def corr_action(dfr,dft,yr1,yr2):
    pass
    

def action_normal(df,*args):
    start_grid = args[0][0]
    #st.write(start_grid)
    #end_grid = args[1]
    test_df = df.T
    normal_df  = test_df[test_df == start_grid]
    #lat_lon = test_df.iloc[:2]
    normal_df = test_df.iloc[3:,:]
    return normal_df#,lat_lon

# period = st.sidebar.slider('Select a time Period', 1901, 2020)
# #st.sidebar.write(f'The Time Period is {period}')
# endperiod = st.sidebar.slider('Select a Ending Period', period+1, 2020)

#st.title("_--_ Under-Development _--_")

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')

# option = st.sidebar.selectbox(
#     'Select a Data-set: ',
#     ('CRU 25KM Final Temp','CRU 25KM Final Rain','Precipitation_2001-2021_Monthly_Data_525_Grids','Pressure_Surface_2001-2021_Monthly_Data_525_Grids',
#     'Relative_Humidity_2M_2001-2021_Monthly_Data_525_Grids','Temperature_2M_2001-2021_Monthly_Data_525_Grids',
#     'Wind_Direction_10M_2001-2021_Monthly_Data_525_Grids','Wind_Speed_2M_2001-2021_Monthly_Data_525_Grids',
#     'Wind_Speed_10M_2001-2021_Monthly_Data_525_Grids'))

option = st.sidebar.selectbox(
    'Select a Data-set: ',
    ('Wind_Speed(10M)_NWH_1981-2021',
    'Specific_Humidity(2M)_NWH_1981-2021',
    'Surface_Pressure_NWH_1981-2021',
    'Temperature(2M)_Maximum_NWH_1981-2021',
    'Temperature(2M)_Minimum_NWH_1981-2021',
    'Temperature(2M)_NWH_1981-2021',
    'Wind_Direction(10M)_NWH_1981-2021',
    'Precipitation_NWH_1981-2021',
#      'Temperature_2M_2001-2021_Monthly_Data_525_Grids',
#      'Relative_Humidity_2M_2001-2021_Monthly_Data_525_Grids',
#      'Temperature_2M_2001-2021_Monthly_Data_525_Grids',
#      'Wind_Speed_10M_2001-2021_Monthly_Data_525_Grids',
     'CRU 25KM Final Rain',
     'CRU 25KM Final Temp'
    ))




st.sidebar.write('You selected:', option)


# if option == 'Precipitation_NWH_1981-2021':
#     # base_path = "./CRU_50km_monthly_1901-2020-20221013T040033Z-001/CRU_50km_monthly_1901-2020"
#     # files = os.listdir(base_path)
#     # select_data = []
#     # for i in files:
#     #     if '.csv' in i:
#     #         select_data.append(i)
#     # st_option = st.selectbox(
#     # 'Select Dataset from 50KM',
#     # np.array(select_data))
#     period = st.sidebar.slider('Select a time Period',
#     1901, 2021,(1950,2000 ),step = 1)
    

#     file_name =  "NWH-CRU_25km_temp-1901-2020-monthly.csv"
#     #st.write('Full path is ',base_path + file_name)
#     df = preprocessor(file_name)
    
#     ndf = action(df,period[0],period[1])
    
if option == 'CRU 25KM Final Rain':
    # base_path = "./CRU_50km_monthly_1901-2020-20221013T040033Z-001/CRU_50km_monthly_1901-2020"
    # files = os.listdir(base_path)
    # select_data = []
    # for i in files:
    #     if '.csv' in i:
    #         select_data.append(i)
    # st_option = st.selectbox(
    # 'Select Dataset from 50KM',
    # np.array(select_data))
    period = st.sidebar.slider('Select a time Period',
    1901, 2021,(2000,2005 ),step = 1)
    

    file_name =  "CRU_precipitation_25k (1).csv"
    #st.write('Full path is ',base_path + file_name)
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])

    
    
if option == 'CRU 25KM Final Temp':

# base_path = "./CRU_50km_monthly_1901-2020-20221013T040033Z-001/CRU_50km_monthly_1901-2020"
# files = os.listdir(base_path)
# select_data = []
# for i in files:
#     if '.csv' in i:
#         select_data.append(i)
# st_option = st.selectbox(
# 'Select Dataset from 50KM',
# np.array(select_data))
    period = st.sidebar.slider('Select a time Period',
    1901, 2021,(2000,2005 ),step = 1)


    file_name =  "CRU_temp_25k (1).csv"
    #st.write('Full path is ',base_path + file_name)
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])




if option == 'Wind_Speed(10M)_NWH_1981-2021':
    file_name =  "Wind_Speed(10M)_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    1981, 2021,(2009,2018 ),step = 1)    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])





if option == 'Wind_Direction(10M)_NWH_1981-2021':
    file_name =  "Wind_Direction(10M)_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    1981, 2021,(2009,2018 ),step = 1)    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])





if option == 'Temperature(2M)_NWH_1981-2021':
    file_name =  "Temperature(2M)_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    1981, 2021,(2009,2018 ),step = 1)    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])








if option == 'Temperature(2M)_Minimum_NWH_1981-2021':
    file_name =  "Temperature(2M)_Minimum_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    1981, 2021,(2009,2018 ),step = 1)    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])




if option == 'Temperature(2M)_Maximum_NWH_1981-2021':
    file_name =  "Temperature(2M)_Maximum_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    1981, 2021,(2009,2018 ),step = 1)    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])




if option == 'Surface_Pressure_NWH_1981-2021':
    file_name =  "Surface_Pressure_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    1981, 2021,(2009,2018 ),step = 1)    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])



if option == 'Precipitation_NWH_1981-2021':
    file_name =  "Precipitation_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    1981, 2021,(2009,2018 ),step = 1)    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])
    

if option == 'Specific_Humidity(2M)_NWH_1981-2021':
    file_name =  "Specific_Humidity(2M)_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    
    1981, 2021,(2009,2018 ),step = 1)
    
    #nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])
    

if option == 'Temperature_2M_2001-2021_Monthly_Data_525_Grids':
    file_name =  "Temperature_2M_2001-2021_Monthly_Data_525_Grids.csv"
    period = st.sidebar.slider('Select a time Period',
    
    2001, 2021,(2009,2018 ),step = 1)
    
    nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,nperiod[0],nperiod[1])
    


if option == 'Relative_Humidity_2M_2001-2021_Monthly_Data_525_Grids':
    file_name =  "Relative_Humidity_2M_2001-2021_Monthly_Data_525_Grids.csv"
    period = st.sidebar.slider('Select a time Period',
    
    2001, 2021,(2009,2018 ),step = 1)
    
    nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,nperiod[0],nperiod[1])
    
if option == 'Temperature_2M_2001-2021_Monthly_Data_525_Grids':
    file_name =  "Temperature_2M_2001-2021_Monthly_Data_525_Grids.csv"
    period = st.sidebar.slider('Select a time Period.',
    
    2001, 2021,(2009,2018 ),step = 1)
    
    nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,nperiod[0],nperiod[1])
    

if option == 'Wind_Direction_10M_2001-2021_Monthly_Data_525_Grids':
    file_name =  "Wind_Direction_10M_2001-2021_Monthly_Data_525_Grids.csv"
    period = st.sidebar.slider('Select a time Period',
    
    2001, 2021,(2009,2018 ),step = 1)
    
    nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,nperiod[0],nperiod[1])
    
if option == 'Wind_Speed_2M_2001-2021_Monthly_Data_525_Grids':
    file_name =  "Wind_Speed_2M_2001-2021_Monthly_Data_525_Grids.csv"
    period = st.sidebar.slider('Select a time Period',
    
    2001, 2021,(2009,2018 ),step = 1)
    
    nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,nperiod[0],nperiod[1])
    
if option == 'Wind_Speed_10M_2001-2021_Monthly_Data_525_Grids':
    file_name =  "Wind_Speed_10M_2001-2021_Monthly_Data_525_Grids.csv"
    period = st.sidebar.slider('Select a time Period',
    
    2001, 2021,(2009,2018 ),step = 1)
    
    nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,nperiod[0],nperiod[1])
    


st.sidebar.write(f'The Time Period is {period[0]}  to {period[1]}')
st_option = st.selectbox(
    'Select a statistic to be displayed as Spatial Plot',
    ('','Min', 'Max', 'Mean','Quartiles','IQR','Skewness','Kurtosis',
    'Clustering','Correlation','Standard_Deviation'
    ))

#st.write('You selected:', st_option)
colorFor = st.sidebar.selectbox(
    'Select the colorscale for heatmaps.',
    ('aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance', 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg', 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl', 'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric', 'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys', 'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet', 'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges', 'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar', 'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd'))

#st.write('You selected:', colorFor)


colorFor1 = st.sidebar.selectbox(
    'Select the colorscale for scatter plots.',
    ('CMRmap', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 
'BuPu', 'BuPu_r', '', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 
'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 
'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 
'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r'))



# colorFor1 = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 
# 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 
# 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 
# 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 
# 'twilight_shifted_r', 'viridis', 'viridis_r', 'winter', 'winter_r']

if st_option:

    if st_option == 'Standard_Deviation':
        agree = st.checkbox('<------ Click Here to switch plot')
        if not agree:
            shapefile=gpd.read_file("4-17-2018-899072.shp")
            fig,ax=plt.subplots(figsize=(4.5,4.5))
            sc = plt.scatter(x=ndf['lon'],y = ndf['lat'],c = ndf['Std'],marker = 's',cmap = colorFor1)
            plt.axis('off')
            plt.colorbar(sc)
            shapefile.plot(ax=ax,color='black')
            st.pyplot(fig,use_container_width=True)
        else:
            fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Std', radius=RADIUS,
                                    center=dict(lat=33.25, lon=77.25), zoom=ZOOM,
                                    mapbox_style="stamen-toner",title = f"Stat: {st_option} Between Year {period[0]} - {period[1]}"
                                    ,opacity=OPE ,width = 600, height=600,
                                    color_continuous_scale=colorFor)#[[0, 'green'], [0.5, colorFor[0]], [1.0, colorFor[1]]])
            #fig = px.density_mapbox(ndf, lat="lat", lon="lon",  hover_data=["Min"],
            #                 width = 300, height=200)
            # fig.update_layout(
            # mapbox_style="white-bg",
            # mapbox_layers=[
            #     {
            #         "below": 'traces',
            #         "sourcetype": "raster",
            #         "sourceattribution": "United States Geological Survey",
            #         "source": [
            #             "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/79.3105,33.5608,3.92,0/300x200?access_token=pk.eyJ1IjoicmFqYW4zMnMiLCJhIjoiY2w5ODd5enV5MDBtajNzbzZ1a3ZjMnVxcSJ9.c2CycsFb8nHLlMwFE2-7iA"
            #         ]
            #     }
            # ])
            #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            #fig.layout.xaxis.fixedrange = False
            #fig.layout.yaxis.fixedrange = False
            #fig.update_traces(autocolorscale=False, selector=dict(type='densitymapbox'))
            #fig.update_traces(colorscale=[[0, 'rgb(0,0,0)'], [1, 'rgb(0,0,0)']], selector=dict(type='densitymapbox'))
            st.plotly_chart(fig, use_container_width=False)
            downloadf = pd.DataFrame()
            downloadf = ndf[['lat','lon','Std']]
            csv = convert_df(downloadf)
            st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f"Stat: {st_option} Between Year {period[0]} - {period[1]}.csv",
                        mime='text/csv',
                    )



    if st_option == 'Correlation':
        # period = st.sidebar.slider('Select a time Period',
    
        #             1981, 2021,(2009,2018 ),step = 1)
    

        ccol1, ccol2 = st.columns(2)

        with ccol1:
            fst_df = st.selectbox(
                'Select First Data',
                ('','Wind_Speed(10M)_NWH_1981-2021',
                        'Specific_Humidity(2M)_NWH_1981-2021',
                        'Surface_Pressure_NWH_1981-2021',
                        'Temperature(2M)_Maximum_NWH_1981-2021',
                        'Temperature(2M)_Minimum_NWH_1981-2021',
                        'Temperature(2M)_NWH_1981-2021',
                        'Wind_Direction(10M)_NWH_1981-2021',
                        'Precipitation_NWH_1981-2021',
#                          'Temperature_2M_2001-2021_Monthly_Data_525_Grids',
#                          'Relative_Humidity_2M_2001-2021_Monthly_Data_525_Grids',
#                          'Temperature_2M_2001-2021_Monthly_Data_525_Grids',
#                          'Wind_Speed_10M_2001-2021_Monthly_Data_525_Grids',
                         'CRU_precipitation_25k (1)',
                         'CRU_temp_25k (1).csv'
                        ))

        with ccol2:
            second_df = st.selectbox(
                'Select second Data',
                ('','Wind_Speed(10M)_NWH_1981-2021',
                        'Specific_Humidity(2M)_NWH_1981-2021',
                        'Surface_Pressure_NWH_1981-2021',
                        'Temperature(2M)_Maximum_NWH_1981-2021',
                        'Temperature(2M)_Minimum_NWH_1981-2021',
                        'Temperature(2M)_NWH_1981-2021',
                        'Wind_Direction(10M)_NWH_1981-2021',
                        'Precipitation_NWH_1981-2021',
#                          'Temperature_2M_2001-2021_Monthly_Data_525_Grids',
#                          'Relative_Humidity_2M_2001-2021_Monthly_Data_525_Grids',
#                          'Temperature_2M_2001-2021_Monthly_Data_525_Grids',
#                          'Wind_Speed_10M_2001-2021_Monthly_Data_525_Grids',
                         'CRU_precipitation_25k (1)',
                         'CRU_temp_25k (1)'
                        ))
        try:
            if fst_df and second_df:
                res = pd.DataFrame()


                fdf = pd.read_csv(fst_df+'.csv')
                sdf = pd.read_csv(second_df+'.csv')

                # Preprocessing
                fdf = corr_action_new(fdf,period[0],period[1])
                sdf = corr_action_new(sdf,period[0],period[1])
                #st.dataframe(fdf.T)
                #t.dataframe(sdf.T)
                res['lat'] = fdf['lat']
                res['lon'] = fdf['lon']

                res['corr'] = fdf.iloc[:,2:].corrwith(sdf.iloc[:,2:], axis = 1)
                #st.dataframe(res.T)

                agree = st.checkbox('<------ Click Here to switch plot')
                if not agree:
                    shapefile=gpd.read_file("4-17-2018-899072.shp")
                    fig,ax=plt.subplots(figsize=(4.5,4.5))
                    sc = plt.scatter(x=res['lon'],y = res['lat'],c = res['corr'],marker = 's',cmap = colorFor1)
                    plt.axis('off')
                    plt.colorbar(sc)
                    shapefile.plot(ax=ax,color='black')
                    st.pyplot(fig,use_container_width=True)
                else:
                    fig = px.density_mapbox(res, lat='lat', lon='lon', z='corr', radius=RADIUS,
                                            center=dict(lat=33.25, lon=77.25), zoom=ZOOM,
                                            mapbox_style="stamen-toner",title = f"Stat: {st_option} Between Year {period[0]} - {period[1]}"
                                            ,opacity=OPE ,width = 600, height=600,
                                            color_continuous_scale=colorFor)#[[0, 'green'], [0.5, colorFor[0]], [1.0, colorFor[1]]])
                    #fig = px.density_mapbox(ndf, lat="lat", lon="lon",  hover_data=["Min"],
                    #                 width = 300, height=200)
                    # fig.update_layout(
                    # mapbox_style="white-bg",
                    # mapbox_layers=[
                    #     {
                    #         "below": 'traces',
                    #         "sourcetype": "raster",
                    #         "sourceattribution": "United States Geological Survey",
                    #         "source": [
                    #             "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/79.3105,33.5608,3.92,0/300x200?access_token=pk.eyJ1IjoicmFqYW4zMnMiLCJhIjoiY2w5ODd5enV5MDBtajNzbzZ1a3ZjMnVxcSJ9.c2CycsFb8nHLlMwFE2-7iA"
                    #         ]
                    #     }
                    # ])
                    #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
                    #fig.layout.xaxis.fixedrange = False
                    #fig.layout.yaxis.fixedrange = False
                    #fig.update_traces(autocolorscale=False, selector=dict(type='densitymapbox'))
                    #fig.update_traces(colorscale=[[0, 'rgb(0,0,0)'], [1, 'rgb(0,0,0)']], selector=dict(type='densitymapbox'))
                    st.plotly_chart(fig, use_container_width=False)
                    downloadf = pd.DataFrame()
                    downloadf = ndf[['lat','lon','corr']]
                    csv = convert_df(downloadf)
                    st.download_button(
                                label="Download data as CSV",
                                data=csv,
                                file_name=f"Stat: {st_option} Between Year {period[0]} - {period[1]}.csv",
                                mime='text/csv',
                            )
                    



        except Exception as e:
            st.warning('Please select appropiate range i.e both data should have same range.', icon="⚠️")
            #raise "Please select appropiate range"# plotting 
            


         


        else:
            st.write("Select the Datasets.")

    if st_option == 'Min':

        #st.dataframe(ndf)
        agree = st.checkbox('<------ Click Here to switch plot')
        if not agree:
            #st.title("Under Development")
            
            shapefile=gpd.read_file("4-17-2018-899072.shp")
            fig,ax=plt.subplots(figsize=(4.5,4.5))
            sc = plt.scatter(x=ndf['lon'],y = ndf['lat'],c = ndf['Min'],marker = 's',cmap = colorFor1)
            plt.axis('off')
            plt.colorbar(sc)
            shapefile.plot(ax=ax,color='black')
            st.pyplot(fig,use_container_width=True)
              
        else:
            fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Min', radius=RADIUS,
                                    center=dict(lat=33.25, lon=77.25), zoom=ZOOM,
                                    mapbox_style="stamen-toner",title = f"Stat: {st_option} Between Year {period[0]} - {period[1]}"
                                    ,opacity=OPE ,width = 600, height=600,
                                    color_continuous_scale=colorFor)#[[0, 'green'], [0.5, colorFor[0]], [1.0, colorFor[1]]])
            #fig = px.density_mapbox(ndf, lat="lat", lon="lon",  hover_data=["Min"],
            #                 width = 300, height=200)
            # fig.update_layout(
            # mapbox_style="white-bg",
            # mapbox_layers=[
            #     {
            #         "below": 'traces',
            #         "sourcetype": "raster",
            #         "sourceattribution": "United States Geological Survey",
            #         "source": [
            #             "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/79.3105,33.5608,3.92,0/300x200?access_token=pk.eyJ1IjoicmFqYW4zMnMiLCJhIjoiY2w5ODd5enV5MDBtajNzbzZ1a3ZjMnVxcSJ9.c2CycsFb8nHLlMwFE2-7iA"
            #         ]
            #     }
            # ])
            #fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            #fig.layout.xaxis.fixedrange = False
            #fig.layout.yaxis.fixedrange = False
            #fig.update_traces(autocolorscale=False, selector=dict(type='densitymapbox'))
            #fig.update_traces(colorscale=[[0, 'rgb(0,0,0)'], [1, 'rgb(0,0,0)']], selector=dict(type='densitymapbox'))
            st.plotly_chart(fig, use_container_width=False)
            downloadf = pd.DataFrame()
            downloadf = ndf[['lat','lon','Min']]
            csv = convert_df(downloadf)
            st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f"Stat: {st_option} Between Year {period[0]} - {period[1]}.csv",
                        mime='text/csv',
                    )


    if st_option == 'Max':


        agree = st.checkbox('<------ Click Here to switch plot')
        if not agree:
            shapefile=gpd.read_file("4-17-2018-899072.shp")
            fig,ax=plt.subplots(figsize=(4.5,4.5))
            sc = plt.scatter(x=ndf['lon'],y = ndf['lat'],c = ndf['Max'],marker = 's',cmap = colorFor1)
            plt.axis('off')
            plt.colorbar(sc)
            shapefile.plot(ax=ax,color='black')
            st.pyplot(fig,use_container_width=True)
            #st.title("Under Development")  
        else:


            fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Max', radius=RADIUS,
                                    center=dict(lat=33.25, lon=77.25), zoom=ZOOM,
                                    mapbox_style="stamen-toner",title = f"Stat: {st_option} Between Year {period[0]} - {period[1]}" 
                                    ,opacity=OPE,width = 600, height=600,
                                    color_continuous_scale=colorFor)

            st.plotly_chart(fig, use_container_width=False)
            downloadf = pd.DataFrame()
            downloadf = ndf[['lat','lon','Max']]
            csv = convert_df(downloadf)
            st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f"Stat: {st_option} Between Year {period[0]} - {period[1]}.csv",
                        mime='text/csv',
                    )

    if st_option == 'Mean':
            
        
        agree = st.checkbox('<------ Click Here to switch plot')
        if not agree:
            shapefile=gpd.read_file("4-17-2018-899072.shp")
            fig,ax=plt.subplots(figsize=(4.5,4.5))
            sc = plt.scatter(x=ndf['lon'],y = ndf['lat'],c = ndf['Mean'],marker = 's',cmap = colorFor1)
            plt.axis('off')
            plt.colorbar(sc)
            shapefile.plot(ax=ax,color='black')
            st.pyplot(fig,use_container_width=True)
#             st.title("Under Development")  
        else:
        
        
        
            fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Mean', radius=RADIUS,
                                    center=dict(lat=33.25, lon=77.25), zoom=ZOOM,
                                    mapbox_style="stamen-toner",title = f"Stat: {st_option} Between Year {period[0]} - {period[1]}" 
                                    ,opacity=OPE
                                    ,
                                    color_continuous_scale=colorFor)

            st.plotly_chart(fig, use_container_width=False)
            downloadf = pd.DataFrame()
            downloadf = ndf[['lat','lon','Mean']]
            csv = convert_df(downloadf)
            st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f"Stat: {st_option} Between Year {period[0]} - {period[1]}.csv",
                        mime='text/csv',
                    )


    if st_option == 'Quartiles':
        genre = st.radio(
        "Select A Quartile",
        ('Q1', 'Q2', 'Q3','Q4'))



        agree = st.checkbox('<------ Click Here to switch plot')
        if not agree:
            shapefile=gpd.read_file("4-17-2018-899072.shp")
            fig,ax=plt.subplots(figsize=(4.5,4.5))
            sc = plt.scatter(x=ndf['lon'],y = ndf['lat'],c = ndf[genre],marker = 's',cmap = colorFor1)
            plt.axis('off')
            plt.colorbar(sc)
            shapefile.plot(ax=ax,color='black')
            st.pyplot(fig,use_container_width=True)
#             st.title("Under Development")  
        else:
            
            fig = px.density_mapbox(ndf, lat='lat', lon='lon', z=genre, radius=RADIUS,
                                    center=dict(lat=33.25, lon=77.25), zoom=ZOOM,
                                    mapbox_style="stamen-toner",title = f"Stat: {st_option} Between Year {period[0]} - {period[1]}" ,
                                    opacity=OPE,width = 600, height=600,
                                    color_continuous_scale=colorFor)
            
            st.plotly_chart(fig, use_container_width=False)

            downloadf = pd.DataFrame()
            downloadf = ndf[['lat','lon',genre]]
            csv = convert_df(downloadf)
            st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f"Stat: {st_option} Between Year {period[0]} - {period[1]}.csv",
                        mime='text/csv',
                    )



    if st_option == 'IQR':



        agree = st.checkbox('<------ Click Here to switch plot')
        if not agree:
            shapefile=gpd.read_file("4-17-2018-899072.shp")
            fig,ax=plt.subplots(figsize=(4.5,4.5))
            sc = plt.scatter(x=ndf['lon'],y = ndf['lat'],c = ndf['IQR'],marker = 's',cmap = colorFor1)
            plt.axis('off')
            plt.colorbar(sc)
            shapefile.plot(ax=ax,color='black')
            st.pyplot(fig,use_container_width=True)
#             st.title("Under Development")  
        else:
            
            fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='IQR', radius=RADIUS,
                                    center=dict(lat=33.25, lon=77.25), zoom=ZOOM,
                                    mapbox_style="stamen-toner",title = f"Stat: {st_option} Between Year {period[0]} - {period[1]}" 
                                    ,opacity=OPE,width = 600, height=600,
                                    color_continuous_scale=colorFor)


            st.plotly_chart(fig, use_container_width=False)
            downloadf = pd.DataFrame()
            downloadf = ndf[['lat','lon','IQR']]
            csv = convert_df(downloadf)
            st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f"Stat: {st_option} Between Year {period[0]} - {period[1]}.csv",
                        mime='text/csv',
                    )




    if st_option == 'Skewness':
            
        
        agree = st.checkbox('<------ Click Here to switch plot')
        if not agree:
            shapefile=gpd.read_file("4-17-2018-899072.shp")
            fig,ax=plt.subplots(figsize=(4.5,4.5))
            sc = plt.scatter(x=ndf['lon'],y = ndf['lat'],c = ndf['Skewness'],marker = 's',cmap = colorFor1)
            plt.axis('off')
            plt.colorbar(sc)
            shapefile.plot(ax=ax,color='black')
            st.pyplot(fig,use_container_width=True)
#             st.title("Under Development")  
        else:
            
            
            fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Skewness', radius=RADIUS,
                                    center=dict(lat=33.25, lon=77.25), zoom=ZOOM,
                                    mapbox_style="stamen-toner",title = f"Stat: {st_option} Between Year {period[0]} - {period[1]}"
                                    ,opacity=OPE,width = 600, height=600 ,
                                    color_continuous_scale=colorFor)

            st.plotly_chart(fig, use_container_width=False)
            downloadf = pd.DataFrame()
            downloadf = ndf[['lat','lon','Skewness']]
            csv = convert_df(downloadf)
            st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f"Stat: {st_option} Between Year {period[0]} - {period[1]}.csv",
                        mime='text/csv',
                    )

    #stamen-toner

    if st_option == 'Kurtosis':

        agree = st.checkbox('<------ Click Here to switch plot')
        if not agree:
            shapefile=gpd.read_file("4-17-2018-899072.shp")
            fig,ax=plt.subplots(figsize=(4.5,4.5))
            sc = plt.scatter(x=ndf['lon'],y = ndf['lat'],c = ndf['Kurtosis'],marker = 's',cmap = colorFor1)
            plt.axis('off')
            plt.colorbar(sc)
            shapefile.plot(ax=ax,color='black')
            st.pyplot(fig,use_container_width=True)
#             st.title("Under Development")  
        else:
            


            
            fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='Kurtosis', radius=RADIUS,
                                    center=dict(lat=33.25, lon=77.25), zoom=ZOOM,
                                    mapbox_style="stamen-toner",title = f"Stat: {st_option} Between Year {period[0]} - {period[1]}" 
                                    ,opacity=OPE,width = 600, height=600,
                                    color_continuous_scale=colorFor)

            st.plotly_chart(fig, use_container_width=False)
            downloadf = pd.DataFrame()
            downloadf = ndf[['lat','lon','Kurtosis']]
            csv = convert_df(downloadf)
            st.download_button(
                        label="Download data as CSV",
                        data=csv,
                        file_name=f"Stat: {st_option} Between Year {period[0]} - {period[1]}.csv",
                        mime='text/csv',
                    )



    if st_option == 'Clustering':
        clusters = st.slider("Choose the number of clusters",2,10,3,1)
        cdf =ndf.iloc[:,:2]
        X = pd.concat([cdf,ndf['Mean']],axis = 1)
        kmeans = KMeans(n_clusters=clusters)
        kmeans.fit(X)

        # Predict the cluster labels for each data point
        y_pred = kmeans.predict(X)

        # Add the predicted cluster labels to the dataframe
        ndf['cluster'] = y_pred
        ndf['cluster']=ndf['cluster'] + 1

        agree = st.checkbox('<------ Click Here to switch plot')
        if not agree:
            shapefile=gpd.read_file("4-17-2018-899072.shp")
            fig,ax=plt.subplots(figsize=(2.5,2.5))
            plt.scatter(x=ndf['lon'],y = ndf['lat'],c = ndf['cluster'],marker = '.')
            plt.axis('off')
            plt.title(f"Fig: Using kMeans with {clusters} clusters ")
            shapefile.plot(ax=ax,color='black')
            st.pyplot(fig,use_container_width=True)
#             st.title("Under Development")  
        else:
            fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='cluster', radius=RADIUS,
                                            center=dict(lat=33.25, lon=77.25), zoom=ZOOM,
                                            mapbox_style="stamen-toner"
                                            ,opacity=OPE ,width = 600, height=600,
                                            color_continuous_scale=colorFor)#[[0, 'green'], [0.5, colorFor[0]], [1.0, colorFor[1]]])
            st.plotly_chart(fig, use_container_width=False)


        

        # fig = px.density_mapbox(ndf, lat='lat', lon='lon', z='cluster', radius=RADIUS,
        #                         center=dict(lat=33.25, lon=77.25), zoom=ZOOM,
        #                         mapbox_style="stamen-toner",title = f"Stat: {st_option} Between Year {period[0]} - {period[1]}" 
        #                         ,opacity=OPE,width = 600, height=600,
        #                         color_continuous_scale=colorFor)
        # # fig = px.scatter_mapbox(ndf, lat="lat", lon="lon",     color="cluster", 
        #            size_max=15, zoom=10)

        # st.plotly_chart(fig, use_container_width=False)
        # downloadf = pd.DataFrame()
        # downloadf = ndf[['lat','lon','Kurtosis']]
        # csv = convert_df(downloadf)
        # st.download_button(
        #             label="Download data as CSV",
        #             data=csv,
        #             file_name=f"Stat: {st_option} Between Year {period[0]} - {period[1]}.csv",
        #             mime='text/csv',
        #         )

       



col1, col2 = st.columns(2)

with col1:
   option_plot = st.selectbox(
    'Select the Plot Type:',
    ('','Line', 'Histogram', 'BoxPlot','Marginal','Violin','ECDF'))

with col2:
   sel_lat = st.slider(
    'Select the Grid Refer to the tabel below for grid number',
    0, len(df.T.columns), (50, 80),step = 1)
    
st.write('Values:', sel_lat)




if option_plot and sel_lat:

    xdf = action_normal(df,sel_lat)
    #st.write(f"The Gird is: {lat_lon}")
    if option_plot == 'Line':
        fig = px.line(xdf, y=sel_lat[0])
        st.plotly_chart(fig, use_container_width=True)
        
        #st.line_chart(df[['1901_jan','1902_jan']])



#if option_plot:
    if option_plot == 'Histogram':
        
        fig = px.histogram(xdf[sel_lat[0]])
        # Plot!
        st.plotly_chart(fig, use_container_width=True)



    if option_plot == 'BoxPlot':
            #single_grid = df.query('lat == 72.25 and lon == 32.25') 

            fig = px.box(xdf[sel_lat[0]])
            # Plot!
            st.plotly_chart(fig, use_container_width=True)

    if option_plot == 'Violin':
            
            fig = px.violin(xdf[sel_lat[0]],box=True)
            # Plot!
            st.plotly_chart(fig, use_container_width=True)



    if option_plot == 'Marginal':
            fig = px.density_heatmap(xdf, x=sel_lat[0], y=sel_lat[1], marginal_x="box", marginal_y="violin")
            #fig = px.violin(df[['1901_jan','1901_dec']],box=True)
            # Plot!
            st.plotly_chart(fig, use_container_width=True)
    if option_plot == 'ECDF':
            fig = px.ecdf(xdf, x=sel_lat[0])
            #fig = px.violin(df[['1901_jan','1901_dec']],box=True)
            # Plot!
            st.plotly_chart(fig, use_container_width=True)
    # if option_plot == 'Scatter':
    #         fig = px.scatter(df, x="lat", y= "lon",hover_data=['1901_jan'])
    #         #fig = px.violin(df[['1901_jan','1901_dec']],box=True)
    #         # Plot!
    #         st.plotly_chart(fig, use_container_width=True)
elif option_plot == '':
    st.dataframe(df.T)


file_ = open("Footer!.png", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
)
