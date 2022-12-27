import matplotlib.pyplot as plt
import numpy as np
#import seaborn as sns
import pandas as pd
import streamlit as st
import plotly.express as px
import os
import base64
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


def action_new(df,yr1,yr2):
    df.rename(columns = {'Longitude':'lon','Latitude':'lat'}, inplace = True)
    col_name = []
    mon = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in range(yr1,yr2):
        for ii in range(12):
            col_name.append(mon[ii]+"-"+str(i)[2:])
    
    ndf = pd.DataFrame()
    
    ndf['lat'] = df['lat']
    ndf['lon'] = df['lon']
    df = df[col_name]
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

option = st.sidebar.selectbox(
    'Select a Data-set: ',
    ('CRU 25KM Final Temp','CRU 25KM Final Rain','Precipitation_NWH_1981-2021','Specific_Humidity(2M)_NWH_1981-2021',
    'Surface_Pressure_NWH_1981-2021','Temperature(2M)_Maximum_NWH_1981-2021',
    'Temperature(2M)_Minimum_NWH_1981-2021','Temperature(2M)_NWH_1981-2021',
    'Wind_Direction(10M)_NWH_1981-2021','Wind_Speed(10M)_NWH_1981-2021'))

st.sidebar.write('You selected:', option)


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
    1901, 2021,(1950,2000 ),step = 1)
    

    file_name =  "NWH-CRU_25km_temp-1901-2020-monthly.csv"
    #st.write('Full path is ',base_path + file_name)
    df = preprocessor(file_name)
    
    ndf = action(df,period[0],period[1])
    
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
    1901, 2021,(1950,2000 ),step = 1)
    

    file_name =  "NWH-CRU_25km_precipitation_1901-2020-monthly.csv"
    #st.write('Full path is ',base_path + file_name)
    df = preprocessor(file_name)
    
    ndf = action(df,period[0],period[1])



if option == 'Precipitation_NWH_1981-2021':
    file_name =  "Precipitation_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    
    1981, 2021,(2009,2018 ),step = 1)
    
    #nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
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
    

if option == 'Surface_Pressure_NWH_1981-2021':
    file_name =  "Surface_Pressure_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    
    1981, 2021,(2009,2018 ),step = 1)
    
    #nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])    


if option == 'Temperature(2M)_Maximum_NWH_1981-2021':
    file_name =  "Temperature(2M)_Maximum_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    
    1981, 2021,(2009,2018 ),step = 1)
    
    #nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])
    
if option == 'Temperature(2M)_Minimum_NWH_1981-2021':
    file_name =  "Temperature(2M)_Minimum_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    
    1981, 2021,(2009,2018 ),step = 1)
    
    #nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])
    

if option == 'Temperature(2M)_NWH_1981-2021':
    file_name =  "Temperature(2M)_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    
    1981, 2021,(2009,2018 ),step = 1)
    
    #nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])
    
if option == 'Wind_Direction(10M)_NWH_1981-2021':
    file_name =  "Wind_Direction(10M)_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    
    1981, 2021,(2009,2018 ),step = 1)
    
    #nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])
    
if option == 'Wind_Speed(10M)_NWH_1981-2021':
    file_name =  "Wind_Speed(10M)_NWH_1981-2021.csv"
    period = st.sidebar.slider('Select a time Period',
    
    1981, 2021,(2009,2018 ),step = 1)
    
    #nperiod = (period[0]-2000,period[1]-2000)



    #st.write('Full path is ',base_path + file_name)
    
    df = pd.read_csv(file_name)
    ndf = action_new(df,period[0],period[1])
    


st.sidebar.write(f'The Time Period is {str(period[0])[2:]}  to {period[1]}')
st_option = st.selectbox(
    'Select a statistic to be displayed as Spatial Plot',
    ('','Min', 'Max', 'Mean','Quartiles','IQR','Skewness','Kurtosis'))

st.write('You selected:', st_option)
colorFor = st.sidebar.selectbox(
    'Select the colorscale.',
    ('aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance', 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg', 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl', 'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric', 'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys', 'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet', 'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges', 'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl', 'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn', 'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu', 'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar', 'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn', 'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid', 'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr', 'ylorrd'))

st.write('You selected:', colorFor)
RADIUS = st.sidebar.slider("Radius",1,50,16,1)

if st_option:
    if st_option == 'correlations':
        file_name =  "NWH-CRU_25km_precipitation_1901-2020-monthly.csv"
    #st.write('Full path is ',base_path + file_name)
        raindf = preprocessor(file_name)
        file_name =  "NWH-CRU_25km_temp-1901-2020-monthly.csv"
    #st.write('Full path is ',base_path + file_name)
        tempdf = preprocessor(file_name)
    
        st.write("Sorry !!! Under Development ")


    if st_option == 'Min':
        #st.dataframe(ndf)
        
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



    if st_option == 'Relative Increment':
    #     options = st.multiselect(
    #     'Select a Month (Multiple Selections)',
    #     ['jan', 'feb', 'mar', 'apr','may','jun','jul','jug','sep','oct','nov','dec']
    #     )
    # #   st.write("debug:" )
    #     if len(options) ==2:
    #         baseY = str(period)+"_"+options[0]
    #         compareY = str(period[0])+"_"+options[1]
    #         nndf = pd.DataFrame()
    #         nndf['lat'] = df['lat']
    #         nndf['lon'] = df['lon']
    #         nndf['Incr'] = (df[compareY] - df[baseY])/df[baseY] 
    #         fig = px.density_mapbox(nndf, lat='lat', lon='lon', z='Incr', radius=RADIUS,
    #                                 center=dict(lat=33.25, lon=77.25), zoom=ZOOM,
    #                                 mapbox_style="stamen-toner",title = f"Stat: {st_option} Between Year {period} - {endperiod}",
    #                                 opacity=OPE ,width = 600, height=600)

    #         st.plotly_chart(fig, use_container_width=False)
        pass



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
