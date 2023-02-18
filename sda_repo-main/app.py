#import reverse_geocoder as rg
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import json
import streamlit as st

#st.write("Hello World")

df = pd.read_csv("Copy of Copy of NWH-CRU_tmp_1901-2020_month_50km.csv")
#month_df = df  
col_name = ['Longitude' , 'latitude']
month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
for i in range(1901,2021):
  for ii in range(12):
    col_name.append(str(i)+'_'+month[ii])

df.columns = col_name

def compareYearTempBox(*args,lat,Long):
  plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0.3),  # red   with alpha = 30%
    "axes.facecolor":    (1.0, 1.0, 1.0, 0.5),  # green with alpha = 50%
    "savefig.facecolor": (1.0, 1.0, 1.0, 0.2),  # blue  with alpha = 20%
    })
  ndf = df[df['Longitude'] == lat ]
  res = ndf[ndf['latitude'] == Long]
  labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  search_col0 = []
  search_col1 = []
  for i in res.columns:
    if i[:4] == args[0]:
      search_col0.append(i)
  for i in res.columns:
      if i[:4] == args[1]:
        search_col1.append(i)

  per = []
  for i in range(len(search_col1)):
    per.append((res[search_col0].T.values[i]-res[search_col1].T.values[i])/res[search_col0].T.values[i])

#   data = [res[search_col0].T.values, res[search_col1].T.values]
 
#   fig = plt.figure(figsize =(10, 7))
 
# # Creating axes instance
#   ax = fig.add_axes([0, 0, 1, 1])
 
# # Creating plot
#   bp = ax.boxplot(data)
      
  fig, (ax1, ax2) = plt.subplots(1,2, sharey=True)
  ax1.boxplot(res[search_col0].T.values)
  ax2.boxplot(res[search_col1].T.values)
  ax1.set_xticklabels([str(args[0])])
  ax2.set_xticklabels([str(args[1])])
  #ax1.plot(res[search_col0].T.values, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4,label = str(args[0]))
  #ax1.plot(res[search_col1].T.values, marker='h', markerfacecolor='green', markersize=12, color='lightgreen', linewidth=4,label = str(args[1]))
  #ax1.plot(per, color='red', linewidth=2,label = "Percentage Change")


  #plt.legend([args[0],args[1],"Percentage Change"])
  #plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11],labels, rotation ='vertical')
  #plt.grid("ON")
  #plt.ylabel('Temp in °C')
  st.pyplot(fig)
        





def compareYearTemp(*args,lat,Long):
  plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0.3),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 0.0, 0.0, 0.5),  # green with alpha = 50%
    "savefig.facecolor": (0.0, 0.0, 0.6, 0.2),  # blue  with alpha = 20%
    })
  ndf = df[df['Longitude'] == lat ]
  res = ndf[ndf['latitude'] == Long]
  labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
  search_col0 = []
  search_col1 = []
  for i in res.columns:
    if i[:4] == args[0]:
      search_col0.append(i)
  for i in res.columns:
      if i[:4] == args[1]:
        search_col1.append(i)

  per = []
  for i in range(len(search_col1)):
    per.append((res[search_col0].T.values[i]-res[search_col1].T.values[i])/res[search_col0].T.values[i])


      
  fig, ax1 = plt.subplots()
  ax1.plot(res[search_col0].T.values, marker='o', markerfacecolor='blue', markersize=12, color='skyblue', linewidth=4,label = str(args[0]))
  ax1.plot(res[search_col1].T.values, marker='h', markerfacecolor='green', markersize=12, color='lightgreen', linewidth=4,label = str(args[1]))
  ax1.plot(per, color='red', linewidth=2,label = "Percentage Change")


  plt.legend([args[0],args[1],"Percentage Change"])
  plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11],labels, rotation ='vertical')
  plt.grid("ON")
  plt.ylabel('Temp in °C')
  leg = plt.legend(loc='best')
  for text in leg.get_texts():
    text.set_color("w")
  st.pyplot(fig)
  






def getLocationname_(*args):
  latitude = args[0]
  longitude = args[1]
  coordinates = (latitude,longitude)
  region_name,country=data[str(latitude)+'_'+str(longitude)]
  #results = rg.search(coordinates)
  return region_name,country


f = open('location.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)



def get_stat(*args):
    lat = args[0]
    long = args[1]
    ndf = df[df['Longitude'] == lat ]
    res = ndf[ndf['latitude'] == long]
    res = res.T
    res = res.reset_index()
    max_idx = res.iloc[2:-2,1].astype('float64').argmax()
    min_idx = res.iloc[2:-2,1].astype('float64').argmin()
    max_temp = res.iloc[max_idx,1]
    min_temp = res.iloc[min_idx,1]
    max_val = res['index'][max_idx]
    min_val = res['index'][min_idx]
    min_month_data = min_val.split('_')
    max_month_data = max_val.split('_')
    mean=res.iloc[2:-2,1].mean()
    median = res.iloc[2:-2,1].median()
    #long_lat = res.iloc[0:2,1].values    
    #st.write(f'At location {getLocationname_(long_lat)}')

    col1, col2 = st.columns(2)

    with col1:
        st.metric(label="Highest Temperature", value=str(max_temp) +"°C")
        st.caption(f'Year: {max_month_data[0]} Month : {max_month_data[1]}')

    with col2:
        st.metric(label="Lowest Temperature", value=str(min_temp) +"°C")
        st.caption(f'Year {min_month_data[0]} Month {min_month_data[1]}')
    st.write(f"The Mean temp: {round(mean,2)} °C  and Median temp is {round(median,2)} °C")
    # number = st.sidebar.number_input('Insert a number')
    # st.write('The current number is ', number)
    fig, ax = plt.subplots()
    
    plt.rcParams.update({
    "figure.facecolor":  (1.0, 0.0, 0.0, 0.3),  # red   with alpha = 30%
    "axes.facecolor":    (0.0, 0.0, 0.0, 0.5),  # green with alpha = 50%
    "savefig.facecolor": (0.0, 0.0, 0.6, 0.2),  # blue  with alpha = 20%
    })
    labels = ['Jan', 'Feb', 'Mar', 'Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    plt.rcParams['figure.figsize'] = [12, 4]
    ax.axhline(y = mean, color = 'r', linestyle = '--',label = 'Mean')
    ax.axhline(y = median, color = 'g', linestyle = '--',label = 'Median')
    ax.plot(res.iloc[2:-2,1][-12:],marker = 'o',color = 'cyan',label = 'Yr_2020')
    #ax.plot(res.iloc[2:-2,1][-24:-12],marker = '^',color = 'blue',label = 'Yr_2019')
    ax.grid("ON")
    plt.title(f"Year {2020}")
    #plt.legend(['Mean','Median',f'Year {2020}'],color='w')
    plt.xticks(res.iloc[2:-2,1][-12:].index,labels, rotation ='vertical')
    plt.ylabel('Temp in °C')
    leg = plt.legend(loc='best')
    for text in leg.get_texts():
        text.set_color("w")
    #plt.show()

    #plt.boxplot(res.iloc[2:-2,1][-12:])
    st.pyplot(fig)
    #st.area_chart(res.iloc[2:-2,1][-12:],x =labels )




Lat = float(st.sidebar.text_input('Latitude','0.0'))
Long = float(st.sidebar.text_input('longitude','0.0'))
st.write('Latitude', Lat)
st.write('Longitude', Long)

if st.sidebar.button('Click'):
    ans = getLocationname_(Lat,Long)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Location: ")    
    with col2:
        st.subheader(f'{ans[0]} , {ans[1]}')
    get_stat(Lat,Long)

BASE = st.sidebar.text_input('Base Year','0000')
COMP_YEAR = st.sidebar.text_input('Year to compare','0000')
if st.sidebar.button('Compare'):
    compareYearTemp(BASE,COMP_YEAR,lat = Lat,Long =Long)
if st.sidebar.button('Box Plot'):
    compareYearTempBox(BASE,COMP_YEAR,lat = Lat,Long =Long)

# arr= np.array([Lat,Long])
# arrdf = pd.DataFrame(arr, columns = ['latitude','longitude'])
# st.map(arrdf)

# #######

# path = "/content/drive/MyDrive/Copy of NWH-CRU_pre_1901-2020_month_50km.csv"

# data_path = "/content/NWH-CRU_pre_1901-2020_month_50km (2).csv"

# #######









