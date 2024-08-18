#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
from datetime import datetime, date, timedelta, time
import pandas as pd
#import seaborn as sns
import numpy as np
import plotly.express as px
from glob import glob 

# csvs will contain all CSV files names ends with .csv in a list
csvs = glob('/Users/juanfranciscolorussonotarofrancesco/Desktop/Progress Data Exports/*.csv')

# remove the trailing .csv from CSV files names
new_table_list = [csv[:-3] for csv in csvs[:-1]]

#List of strings of activity names
Necessary_list = ['Unnamed: 1', 'Demising Walls', 'FCU & Ductwork', 'Perimeter Walls Stud & Board',
                  'Internal Walls - Frame & One Side', 'Internal Walls - Closure', 'Perimeter Bulkheads',
                  'HVAC 2nd Fix', 'Ceilings - Frame', 'Ceilings - Closure', 'Ceilings - T&J', 'Mist Coat',
                  'Subfloor', 'Hard Flooring', 'Carpentry & Joinery']

#read begin by first activity
df1 = pd.read_csv(csvs[0])[Necessary_list[0]]
dfs = [pd.read_csv(csv)['Demising Walls'] for csv in csvs[:-1]]
df = pd.concat(dfs, axis=1, ignore_index=True)
df = pd.concat([df1, df], axis=1, ignore_index=True)

for i in range(2, len(Necessary_list)):

    #Get csvs by activities and their dates

    dfs = [pd.read_csv(csv)[Necessary_list[i]] for csv in csvs[:-1]]

    #concatenate all dataframes into a single dataframe
    #By date by columns
    df0 = pd.concat(dfs, axis=1, ignore_index=True)
    df0 = pd.concat([df1, df0], axis=1, ignore_index=True)
    #By activity by rows
    df = pd.concat([df, df0], ignore_index=True)

#Here the apartments are renamed/corrected in the dataframe to avoid confusion
for i in range(len(Necessary_list)-1):

    df.iat[248+i*len(df0),0] = 'A0904'
    df.iat[268+i*len(df0),0] = 'A1004'
    df.iat[289+i*len(df0),0] = 'A1104'
    df.iat[306+i*len(df0),0] = 'A1301'
    df.iat[307+i*len(df0),0] = 'A1302'
    df.iat[308+i*len(df0),0] = 'A1303'
    df.iat[309+i*len(df0),0] = 'A1304'
    df.iat[310+i*len(df0),0] = 'A1305'

column_name_0 = {0: 'Location'}
column_name = {i+1: new_table_list[i][-11:-1] for i in range(len(new_table_list))}
index_name = {i: Necessary_list[i//len(df0)+1] for i in range(len(df))}
df = df.rename(columns=column_name_0|column_name)
df = df.rename(index=index_name)
df = df.replace('---', '0%')
df = df.replace('V', '100%')
df = df.replace(np.nan, '0%')
sorteddfcolumns = ['Location']
for i in sorted(df.columns)[:-1]:

    sorteddfcolumns.append(i)

sorteddfcolumns
df = df.reindex(sorteddfcolumns, axis=1)
df


# In[2]:


from datetime import date

column_name = ['Location']
new_table_list = sorted(new_table_list)
for i in new_table_list:
    column_name.append(i[-11:-1])

progress_activities = df[column_name].to_numpy()
floorname = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'A01', 'A02', 
             'A03', 'A04', 'A05', 'A06', 'A07', 'A08', 'A09', 'A10', 'A11', 'A12', 
             'A13']
interest_floors = []
interest_floors_dates = []
Date_format = '%Y-%m-%d'

for name in floorname:

    interest_floor = []

    if name[0]=='B':
        for i in range(len(progress_activities)):
            #Pick apartments in South Building from 1-6 
            if type(progress_activities[i,0]) == str and progress_activities[i,0][0:3] == name and progress_activities[i,0][-1] != '7' and len(progress_activities[i,0]) == 5:
                interest_floor.append(progress_activities[i])
    else:
        for i in range(len(progress_activities)):
            #Pick apartments in North Building from 1-10
            if type(progress_activities[i,0]) == str and progress_activities[i,0][0:3] == name and progress_activities[i,0][-2:] != '11' and len(progress_activities[i,0]) == 5:
                interest_floor.append(progress_activities[i])

    #Splits arrays multiples of 14 into their respective work packages
    floor_index = [[0, int(len(interest_floor)/14)], [int(len(interest_floor)/14), int(len(interest_floor)/7)], 
                   [int(len(interest_floor)/7), int(3*len(interest_floor)/7)],
                    [int(3*len(interest_floor)/7), int(len(interest_floor)/2)],
                    [int(len(interest_floor)/2), int(11*len(interest_floor)/14)],
                    [int(11*len(interest_floor)/14), int(len(interest_floor))]]


    for i in range(1, len(new_table_list)+1):
        for j in range(len(interest_floor)):
            interest_floor[j][i]=int(interest_floor[j][i][:-1])
    
    #Eliminate the condition for all zero progress in a floor/no data
    removalinterestfloor = []
    for i in range(len(interest_floor)):
        #print(list(i[1:]) == list([0]*len(new_table_list)))
        if name in floorname[7:-2] and floor_index[0][0]<=i and i<floor_index[0][1] and list(interest_floor[i][1:]) == list([0]*len(new_table_list)):
            #print(interest_floor[i], floor_index[0][0], floor_index[0][1])
            removalinterestfloor.append(i)
        if name in floorname[8:-2] and floor_index[1][0]<=i and i<floor_index[1][1] and list(interest_floor[i][1:]) == list([0]*len(new_table_list)):
            #print(interest_floor[i], floor_index[1][0], floor_index[1][1])
            removalinterestfloor.append(i)
        if name in floorname[8:-2] and floor_index[2][0]<=i and i<floor_index[2][1] and list(interest_floor[i][1:]) == list([0]*len(new_table_list)):
            #print(interest_floor[i], floor_index[2][0], floor_index[2][1])
            removalinterestfloor.append(i)
        if name in floorname[8:-4] and floor_index[3][0]<=i and i<floor_index[3][1] and list(interest_floor[i][1:]) == list([0]*len(new_table_list)):
            #print(interest_floor[i], floor_index[3][0], floor_index[3][1])
            removalinterestfloor.append(i)
        if name in floorname[8:-3] and floor_index[4][0]<=i and i<floor_index[4][1] and list(interest_floor[i][1:]) == list([0]*len(new_table_list)):
            #print(interest_floor[i], floor_index[4][0], floor_index[4][1])
            removalinterestfloor.append(i)
    #for i in removalinterestfloor:
     #   interest_floor.remove(interest_floor[i])
        #if name in floorname[8:-3] and floor_index[5][0]<=i and i<floor_index[5][1] and list(interest_floor[i][1:]) == list([0]*len(new_table_list)):
         #   print(interest_floor[i], floor_index[5][0], floor_index[5][1])
          #  removalinterestfloor.append(interest_floor[i])
        #if list(i[1:]) == list([0]*len(new_table_list)) and :
         #   interest_floor.remove(i)

    for index in floor_index:

        interest_floor_dates = []

        interest_floor_progress_activities = [[np.average([interest_floor[i][j] for i in range(index[0], index[1]) if i not in removalinterestfloor]), datetime.strptime(new_table_list[j-1][-11:-1], Date_format).date()+timedelta(days=1)] for j in range(1, len(new_table_list)+1)]

        for i in range(len(interest_floor_progress_activities)):

            if interest_floor_progress_activities[0][0]==interest_floor_progress_activities[-1][0] and i<=1:
                interest_floor_dates.append(None)
            elif interest_floor_progress_activities[0][0]==interest_floor_progress_activities[-1][0]:
                pass
            elif interest_floor_progress_activities[i][0]==interest_floor_progress_activities[0][0] and interest_floor_progress_activities[i+1][0]!=interest_floor_progress_activities[0][0]:
                interest_floor_dates.append(interest_floor_progress_activities[i][1])
            elif interest_floor_progress_activities[i][0]==interest_floor_progress_activities[-1][0] and interest_floor_progress_activities[i-1][0]!=interest_floor_progress_activities[-1][0]:
                interest_floor_dates.append(interest_floor_progress_activities[i][1])

        interest_floors.append(interest_floor_progress_activities)
        interest_floors_dates.append(interest_floor_dates)

        for i in range(len(interest_floors)):
            a_1 = 0
            a_2 = 0
            for j in range(len(interest_floors[i])):
                if interest_floors[i][j][1] == interest_floors_dates[i][0]:
                    a_1 = j
                elif interest_floors[i][j][1] == interest_floors_dates[i][1]:
                    a_2 = j
            interest_floors[i] = interest_floors[i][a_1:a_2+1]

for i in range(len(interest_floors)):
    if len(interest_floors[i])==1:
        interest_floors[i] = [None, None]

interest_floors


# In[3]:


lastdate = date(2023, 9, 29)
Time = time(0, 0, 0)


# In[4]:


def timegap(Day1, Day2):
    i = 0
    Time_days = Day2 - Day1

    while Time_days != timedelta(days=0):

        Time_days = (Time_days-timedelta(days=1))
        i+=1

    return i

rgb_dictionary = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, 
                  '8': 8, '9': 9, 'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}

def color_interpolation(colorarray, x):

    red_0 = rgb_dictionary[colorarray[0][1][1]]*16+rgb_dictionary[colorarray[0][1][2]]
    red_1 = rgb_dictionary[colorarray[1][1][1]]*16+rgb_dictionary[colorarray[1][1][2]]
    red_2 = rgb_dictionary[colorarray[2][1][1]]*16+rgb_dictionary[colorarray[2][1][2]]
    green_0 = rgb_dictionary[colorarray[0][1][3]]*16+rgb_dictionary[colorarray[0][1][4]]
    green_1 = rgb_dictionary[colorarray[1][1][3]]*16+rgb_dictionary[colorarray[1][1][4]]
    green_2 = rgb_dictionary[colorarray[2][1][3]]*16+rgb_dictionary[colorarray[2][1][4]]
    blue_0 = rgb_dictionary[colorarray[0][1][5]]*16+rgb_dictionary[colorarray[0][1][6]]
    blue_1 = rgb_dictionary[colorarray[1][1][5]]*16+rgb_dictionary[colorarray[1][1][6]]
    blue_2 = rgb_dictionary[colorarray[2][1][5]]*16+rgb_dictionary[colorarray[2][1][6]]

    if x < colorarray[1][0]:

        red = red_0 + (red_1-red_0)*(x-colorarray[0][0])/(colorarray[1][0]-colorarray[0][0])
        green = green_0 + (green_1-green_0)*(x-colorarray[0][0])/(colorarray[1][0]-colorarray[0][0])
        blue = blue_0 + (blue_1-blue_0)*(x-colorarray[0][0])/(colorarray[1][0]-colorarray[0][0])

    elif x > colorarray[2][0]:

        red = red_2
        green = green_2
        blue = blue_2

    else:

        red = red_1 + (red_2-red_1)*(x-colorarray[1][0])/(colorarray[2][0]-colorarray[1][0])
        green = green_1 + (green_2-green_1)*(x-colorarray[1][0])/(colorarray[2][0]-colorarray[1][0])
        blue = blue_1 + (blue_2-blue_1)*(x-colorarray[1][0])/(colorarray[2][0]-colorarray[1][0])
   
    color_hex = "#{:02x}{:02x}{:02x}".format(round(red), round(green), round(blue))

    return color_hex


# In[5]:


import json

# Function to read and parse the JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

cladding_dates = []
superstructure_dates = []

for i in range(6):
    # Specify the file path
    file_path = 'data'+str(i)+'.json'

    # Read and parse the JSON file
    data = read_json_file(file_path)
    if i < 3:
        cladding_dates.append(data)
    else:
        superstructure_dates.append(data)


# In[6]:


datadf = pd.read_csv("/Users/juanfranciscolorussonotarofrancesco/Desktop/Data_north_wp.csv")
datadf.head()
north_wp_dates = datadf[['Level', 'apartments', 'name', 'planned_start', 'planned_finish']].to_numpy()

for i in north_wp_dates:

    i[3] = datetime.strptime(i[3], Date_format).date()
    i[4] = datetime.strptime(i[4], Date_format).date()

north_wp_dates = [np.array(i) for i in north_wp_dates]
north_activity_dates = []
for i in north_wp_dates:
    for j in north_wp_dates:
        if np.all(i==j) == np.False_ and np.all(i[0] == j[0]) and np.all(i[2] == j[2]):
            north_activity_dates.append([i[0], i[2], np.concatenate([i[3:], j[3:]]).tolist()])

north_wp_dates = []

for j in range(len(set([i[0] for i in north_activity_dates]))):
    north_wp_dates.append(north_activity_dates[int(len(north_activity_dates)*j/len(set([i[0] for i in north_activity_dates]))):int(len(north_activity_dates)*j/len(set([i[0] for i in north_activity_dates])))+6])

north_wp_dates


# In[7]:


datadf = pd.read_csv("/Users/juanfranciscolorussonotarofrancesco/Desktop/Data_south_wp.csv")
datadf.head()
south_wp_dates = datadf[['Level', 'apartments', 'name', 'planned_start', 'planned_finish']].to_numpy()
#print(south_wp_dates)
for i in south_wp_dates:

    i[3] = datetime.strptime(i[3], Date_format).date()
    i[4] = datetime.strptime(i[4], Date_format).date()

south_wp_dates = [np.array(i) for i in south_wp_dates]
south_wp_dates


# In[8]:


southfloornamelen = 0
for i in range(len(floorname)-1):
    if floorname[i][0] != floorname[i+1][0]:
        southfloornamelen = i+1
southfloornamelen


# In[9]:


def datereadjust(x):
    if x == None:
        return None
    else:
        return datetime.combine(x, time(0, 0, 0))-timedelta(hours=1)

def datereadjust2(x):
    if x == None:
        return None
    else:
        return datereadjust(x)+timedelta(days=1)
    
def datereadjust3(x):
    if x == None:
        return None
    else:
        return datetime.combine(x, Time)+timedelta(days=1)
    
def datereadjust4(x):
    if x == None:
        return None
    elif type(x) == date:
        return x
    else:
        return datereadjust3(x).date()

def datereadjust5(x):
    if x == None:
        return None
    elif type(x) == date:
        return datetime.combine(x, Time)
    else:
        return x

def datereadjust6(x):
    if x == None:
        return None
    elif type(x) == date:
        return x
    else:
        return x.date()
    


# In[10]:


[interest_floors[i] for i in range(0, len(interest_floors),6)]
interest_floors_progress = []

for i in interest_floors:
    interest_floors_progress_element = []
    if i==[None, None]:
        interest_floors_progress_element.append(i)
    else:
        for j in range(len(i)-1):

            interest_floors_progress_element.append([i[j+1][0]-i[j][0], i[j][1], i[j+1][1], i[j][0], i[j+1][0]])
    interest_floors_progress.append(interest_floors_progress_element)

interest_floors_progress[0]
for i in range(len(interest_floors_progress)):
    j = [item for item in interest_floors_progress[i] if item[0] != 0]
    interest_floors_progress[i] = j

interest_floors_progress


# In[11]:


#Make code to exclude outliers in interest_floors_progress
for i in range(len(interest_floors_progress)):

    if interest_floors_progress[i] == [[None, None]]:
        pass
    else:

        # Calculate median and quartiles
        for j in interest_floors_progress[i]:
            if j[3] <= 50 and j[4] > 50:
                median = timegap(interest_floors_progress[i][0][1], j[1])+timegap(j[1], j[2])*(50-j[3])/(j[4]-j[3])
            if j[3] <= 75 and j[4] > 75:
                q3 = timegap(interest_floors_progress[i][0][1], j[1])+timegap(j[1], j[2])*(75-j[3])/(j[4]-j[3])
            if j[3] <= 25 and j[4] > 25:
                q1 = timegap(interest_floors_progress[i][0][1], j[1])+timegap(j[1], j[2])*(25-j[3])/(j[4]-j[3])
        iqr = q3-q1
        removal = []
        
        for j in interest_floors_progress[i]:    
            if j[-2] > 95 and (timegap(interest_floors_progress[i][0][1], j[1])+timegap(interest_floors_progress[i][0][1], j[2]))/2>median+1.5*iqr:
                removal.append(j)
            else:
                pass       
            if j[-1] < 5 and timegap(interest_floors_progress[i][0][1], j[2])/2<median-1.5*iqr:
                removal.append(j)
            else:
                pass
        
        for j in removal:
            interest_floors_progress[i].remove(j)

for i in range(len(interest_floors_dates)):
    if interest_floors_dates[i] != [None, None]:
        interest_floors_dates[i] = [interest_floors_progress[i][0][1], interest_floors_progress[i][-1][2]]

interest_floors_progress[64]


# In[12]:


progress_gradients = []
for i in interest_floors_progress:
    if i[-1][-1] == None:
        progress_gradients.append(0)
    else:
        if i[-1][-1] < 95:
            progress_gradients.append(i[-1][-1]/100*(datereadjust(i[-1][2])-datereadjust5(i[0][1]))/(datereadjust(lastdate)-datereadjust5(i[0][1])))
        else: 
            progress_gradients.append(1)
interest_floors_progress[0], progress_gradients


# In[13]:


interest_floors_Dates = [[interest_floors_dates[i][0], datereadjust5(interest_floors_dates[i][0]) + (datereadjust(interest_floors_dates[i][1])-datereadjust5(interest_floors_dates[i][0]))/progress_gradients[i]] if interest_floors_dates[i] != [None, None] else [interest_floors_dates[i][0], interest_floors_dates[i][1]] for i in range(len(interest_floors_dates))]
interest_floors_progress[41]


# In[14]:


Time = time(0, 0, 0)
fig = px.line()
fig6 = px.line()
fig7 = px.line()
# Add a custom legend trace using a scatter plot with the desired shape
legend_trace = px.line()
pixsize = 35
width = 2300

colorset = [px.colors.qualitative.G10[i] for i in range(len(set([i[2] for i in south_wp_dates]))+2)]

fig = px.line(labels={'x': 'Date', 'y': 'Floor'}, 
              title='<b>Flowlines 6WP Plan v Actual South<b>',
              template='seaborn')

fig.add_shape(type="rect",
              x0=-2*(pixsize/width), x1=0,
              y0=0, y1=1,
              xref='paper', yref='paper',
              line=dict(color="#ffffff", width=1.5),
              fillcolor = '#eaeaf2',
              opacity = 1)

for i in range(1, southfloornamelen+2):
    # Add horizontal line to the margin
    fig.add_shape(type="line",
              x0=-2*(pixsize/width), x1=0,
              y0=i, y1=i,
              xref='paper', yref='y',
              line=dict(color="#ffffff", width=1.5),
              opacity = 1)
    # Add horizontal line to the margin
    if i < southfloornamelen+1:
        fig.add_annotation(
            text='<b>L'+str(i)+'<b>',
            x=-2*(pixsize/width),
            y=i+1/2,
            xref='paper', yref='y',
            font=dict(size=12),
            showarrow = False )

for i in range(len(set([i[2] for i in south_wp_dates]))):
    data = pd.DataFrame({
        'x': np.concatenate([[south_wp_dates[j][3], datereadjust(south_wp_dates[j][4]+timedelta(days=1)), None] for j in range(i, len(south_wp_dates), len(set([i[2] for i in south_wp_dates])))]).tolist(),
        'y': np.concatenate([[int(south_wp_dates[j][0][-2:]), int(south_wp_dates[j][0][-2:])+1, None] for j in range(i, len(south_wp_dates), len(set([i[2] for i in south_wp_dates])))]).tolist(),
        'Color': [str(i)+', '+str(i)]*len(np.concatenate([[south_wp_dates[j][3], south_wp_dates[j][4], None] for j in range(i, len(south_wp_dates), len(set([i[2] for i in south_wp_dates])))]).tolist())
    })
    # Define custom hover text for each bar in each set
    custom_hover_text = [
        np.concatenate([[south_wp_dates[j][3], south_wp_dates[j][3], None] for j in range(i, len(south_wp_dates), len(set([i[2] for i in south_wp_dates])))]).tolist(),
        np.concatenate([[south_wp_dates[j][4], south_wp_dates[j][4], None] for j in range(i, len(south_wp_dates), len(set([i[2] for i in south_wp_dates])))]).tolist(),
        np.concatenate([['L'+str(int(south_wp_dates[j][0][-2:])), 'L'+str(int(south_wp_dates[j][0][-2:])), None] for j in range(i, len(south_wp_dates), len(set([i[2] for i in south_wp_dates])))]).tolist()
    ]
    fig6.add_trace(px.line(data, x='x', y = 'y', color_discrete_sequence=[colorset[i]], color = 'Color', hover_data = custom_hover_text).data[0])
    fig6.update_traces(line=dict(dash='dash'))
    #Update hovertext
    fig6.update_traces(
        hovertemplate='Initial Date: %{customdata[0]}<br>Final Date: %{customdata[1]}<br>Level: %{customdata[2]}',
    )

for i in range(len(set([i[2] for i in south_wp_dates]))):
    data = pd.DataFrame({
        'x': np.concatenate([np.array([interest_floors_Dates[j][0], interest_floors_Dates[j][1], None]) for j in range(i, southfloornamelen*6, len(set([i[2] for i in south_wp_dates])))]).tolist(),
        'y': np.concatenate([np.array([int((j-i)/len(set([i[2] for i in south_wp_dates])))+1, int((j-i)/len(set([i[2] for i in south_wp_dates])))+2, None]) for j in range(i, southfloornamelen*6, len(set([i[2] for i in south_wp_dates])))]).tolist(),
        'Color': [str(i)]*len(np.concatenate([np.array([interest_floors_Dates[j][0], interest_floors_Dates[j][1], None]) for j in range(i, southfloornamelen*6, len(set([i[2] for i in south_wp_dates])))]).tolist())
    })
    # Define custom hover text for each bar in each set
    custom_hover_text = [
        np.concatenate([np.array([interest_floors_Dates[j][0], interest_floors_Dates[j][0], None]) for j in range(i, southfloornamelen*6, len(set([i[2] for i in south_wp_dates])))]).tolist(),
        np.concatenate([np.array([datereadjust6(interest_floors_Dates[j][1]), datereadjust6(interest_floors_Dates[j][1]), None]) for j in range(i, southfloornamelen*6, len(set([i[2] for i in south_wp_dates])))]).tolist(),
        np.concatenate([np.array(['L'+str(int((j-i)/len(set([i[2] for i in south_wp_dates])))+1), 'L'+str(int((j-i)/len(set([i[2] for i in south_wp_dates])))+1), None]) for j in range(i, southfloornamelen*6, len(set([i[2] for i in south_wp_dates])))]).tolist()
    ]
    fig7.add_trace(px.line(data, x='x', y = 'y', color_discrete_sequence=[colorset[i]], color = 'Color', hover_data = custom_hover_text).data[0])
    #Update hovertext
    fig7.update_traces(
        hovertemplate='Initial Date: %{customdata[0]}<br>Final Date: %{customdata[1]}<br>Level: %{customdata[2]}',
    )

for i in range(len(fig6.data)):
    fig.add_trace(fig6.data[i])
for i in range(len(fig7.data)):
    fig.add_trace(fig7.data[i])

# Add the custom legend trace to the figure
fig.add_traces(legend_trace.data)
#Define text of legend list
name_legend = ['Demising Walls', 'HL MEP Services (1st Fix)', 'Internal walls 2nd Drylining Visit', 
               'HL MEP Services (2nd Fix)', 'Final Drylining / Install Ceilings', 'Screed / Joinery / Kitchens']
# Define a dictionary to map trace names to custom legend labels
legend_labels = {}
for i in range(len(set([i[2] for i in south_wp_dates]))):

    legend_labels.update({
        str(i): name_legend[i]+' Actuals', 
        str(i)+', '+str(i): name_legend[i]+' Planned'
    })


# Customize the legend labels for each trace
fig.for_each_trace(lambda trace: trace.update(name=legend_labels.get(trace.name, trace.name)))

#Update size of plot
fig.update_layout(height=860, width=1403)
#fig.update_layout(showlegend = True)
fig.update_yaxes(tickvals=[i for i in range(southfloornamelen+2)], range = [0.75, 9.25])
fig.update_layout(xaxis_title="<b>Date<b>", yaxis_title="<b>Floor<b>", yaxis = dict(title_standoff = 30))
fig.update_xaxes(range = [datetime(2022, 10, 31)-timedelta(days=5), max([interest_floors_Dates[i][1] for i in range(southfloornamelen*6) if interest_floors_Dates[i]!=[None, None]])+timedelta(days=5)])
Flowlines1figsth = fig
fig.show()
#fig.write_html("figfiout6WP.html")


# In[15]:


fig = px.line()
fig1 = px.line()
fig2 = px.line()
# Add a custom legend trace using a scatter plot with the desired shape
legend_trace = px.line()
pixsize = 35
width = 2300

colorset = [px.colors.qualitative.G10[i] for i in range(len(set([i[2] for i in south_wp_dates]))+2)]

fig = px.line(labels={'x': 'Date', 'y': 'Floor'}, 
              title='<b>Flowlines 6WP Plan v Actual North<b>',
              template='seaborn')

fig.add_shape(type="rect",
              x0=-2*(pixsize/width), x1=0,
              y0=0, y1=1,
              xref='paper', yref='paper',
              line=dict(color="#ffffff", width=1.5),
              fillcolor = '#eaeaf2',
              opacity = 1)

for i in range(1, cladding_dates[1][1][-2]+1):
    # Add horizontal line to the margin
    fig.add_shape(type="line",
              x0=-2*(pixsize/width), x1=0,
              y0=i-1, y1=i-1,
              xref='paper', yref='y',
              line=dict(color="#ffffff", width=1.5),
              opacity = 1)
    # Add annotation to the margin
    if i < cladding_dates[1][1][-2]:
        fig.add_annotation(
            text='<b>L'+str(i)+'<b>',
            x=-2*(pixsize/width),
            y=i-1/2,
            xref='paper', yref='y',
            font=dict(size=12),
            showarrow = False )

for i in range(len(set(np.concatenate([np.array([j[1] for j in i]) for i in north_wp_dates]).tolist()))):
    data = pd.DataFrame({
        'x': np.concatenate([np.array([min(north_wp_dates[j][i][2]), datereadjust2(max(north_wp_dates[j][i][2])), None]) for j in range(len(north_wp_dates))]).tolist(),
        'y': np.concatenate([np.array([int(north_wp_dates[j][i][0][-2:])-1, int(north_wp_dates[j][i][0][-2:]), None]) for j in range(len(north_wp_dates))]).tolist(),
        'Color': [str(i)+', '+str(i)]*len(np.concatenate([np.array([min(north_wp_dates[j][i][2]), max(north_wp_dates[j][i][2]), None]) for j in range(len(north_wp_dates))]).tolist())
    })
    # Define custom hover text for each bar in each set
    custom_hover_text = [
        np.concatenate([np.array([min(north_wp_dates[j][i][2]), min(north_wp_dates[j][i][2]), None]) for j in range(len(north_wp_dates))]),
        np.concatenate([np.array([max(north_wp_dates[j][i][2]), max(north_wp_dates[j][i][2]), None]) for j in range(len(north_wp_dates))]),
        np.concatenate([np.array(['L'+str(j+1), 'L'+str(j+1), None]) for j in range(len(north_wp_dates))])
    ]
    fig1.add_trace(px.line(data, x='x', y = 'y', color = 'Color', color_discrete_sequence=[colorset[i]], hover_data = custom_hover_text).data[0])
    fig1.update_traces(line=dict(dash='dash'))
    #Update hovertext
    fig1.update_traces(
        hovertemplate='Initial Date: %{customdata[0]}<br>Final Date: %{customdata[1]}<br>Level: %{customdata[2]}',
    )

for i in range(len(set([i[2] for i in south_wp_dates]))):
    data = pd.DataFrame({
        'x': np.concatenate([np.array([interest_floors_Dates[j][0], interest_floors_Dates[j][1], None]) for j in range(southfloornamelen*6+i, len(interest_floors_Dates), len(set([i[2] for i in south_wp_dates])))]).tolist(),
        'y': np.concatenate([np.array([int((j-i)/len(set([i[2] for i in south_wp_dates])))-southfloornamelen, int((j-i)/len(set([i[2] for i in south_wp_dates])))+1-southfloornamelen, None]) for j in range(southfloornamelen*6+i, len(interest_floors_Dates), len(set([i[2] for i in south_wp_dates])))]).tolist(),#
        'Color': [i]*len(np.concatenate([np.array([interest_floors_Dates[j][0], interest_floors_Dates[j][1], None]) for j in range(southfloornamelen*6+i, len(interest_floors_Dates), len(set([i[2] for i in south_wp_dates])))]).tolist())
    })
    # Define custom hover text for each bar in each set
    custom_hover_text = [
        np.concatenate([np.array([interest_floors_Dates[j][0], interest_floors_Dates[j][0], None]) for j in range(southfloornamelen*6+i, len(interest_floors_Dates), len(set([i[2] for i in south_wp_dates])))]),
        np.concatenate([np.array([datereadjust6(interest_floors_Dates[j][1]), datereadjust6(interest_floors_Dates[j][1]), None]) for j in range(southfloornamelen*6+i, len(interest_floors_Dates), len(set([i[2] for i in south_wp_dates])))]),
        np.concatenate([np.array(['L'+str(int(j/len(set([i[2] for i in south_wp_dates])))+1-southfloornamelen), 'L'+str(int(j/len(set([i[2] for i in south_wp_dates])))+1-southfloornamelen), None]) for j in range(southfloornamelen*6+i, len(interest_floors_Dates), len(set([i[2] for i in south_wp_dates])))])
    ]
    fig2.add_trace(px.line(data, x='x', y = 'y', color='Color', color_discrete_sequence=[colorset[i]], hover_data = custom_hover_text).data[0])
    #Update hovertext
    fig2.update_traces(
        hovertemplate='Initial Date: %{customdata[0]}<br>Final Date: %{customdata[1]}<br>Level: %{customdata[2]}',
    )

#Add data from figures to fig
for i in range(len(fig1.data)):
    fig.add_trace(fig1.data[i])
for i in range(len(fig2.data)):
    fig.add_trace(fig2.data[i])

# Add the custom legend trace to the figure
fig.add_traces(legend_trace.data)
#Define text of legend list
name_legend = ['Demising Walls', 'HL MEP Services (1st Fix)', 'Internal walls 2nd Drylining Visit', 
               'HL MEP Services (2nd Fix)', 'Final Drylining / Install Ceilings', 'Screed / Joinery / Kitchens']
# Define a dictionary to map trace names to custom legend labels
legend_labels = {}
for i in range(len(set([i[2] for i in south_wp_dates]))):

    legend_labels.update({
        str(i): name_legend[i]+' Actuals', 
        str(i)+', '+str(i): name_legend[i]+' Planned'
    })


# Customize the legend labels for each trace
fig.for_each_trace(lambda trace: trace.update(name=legend_labels.get(trace.name, trace.name)))

#Update size of plot
fig.update_layout(height=860, width=1403)
fig.update_yaxes(tickvals=[i for i in range(cladding_dates[1][1][-2]+1)], range = [-0.25, 13.25])
fig.update_layout(xaxis_title="<b>Date<b>", yaxis_title="<b>Floor<b>", yaxis = dict(title_standoff = 30))
fig.update_layout(title_x=0.3)
fig.update_xaxes(range = [datetime(2022, 10, 31)-timedelta(days=5), max([interest_floors_Dates[i][1] for i in range(southfloornamelen*6, len(interest_floors_Dates)) if interest_floors_Dates[i]!=[None, None]])+timedelta(days=5)])
Flowlines1fig = fig
fig.show()
#fig.write_html("figfiout6WP.html")


# In[16]:


#Create colorscale
custom_colorscale = [
    [0, "#ff0000"],
    [15, "#ffd400"], 
    [30,"#34eb00"]
]

fig = px.line(labels={'x': 'Date', 'y': 'Floor'}, 
              title='<b>Flowlines Demising Walls North<b>',
              template='seaborn')

WPfig1 = px.line()
WPfig2 = px.line()
WPfig3 = px.line()
WPfig4 = px.line()
WPfig5 = px.line()
WPfig6 = px.line()
WPfig1projection = px.line()
WPfig2projection = px.line()
WPfig3projection = px.line()
WPfig4projection = px.line()
WPfig5projection = px.line()
WPfig6projection = px.line()

figadditivessth = [WPfig1, WPfig2, WPfig3, WPfig4, WPfig5, WPfig6]
figadditivessthprojection = [WPfig1projection, WPfig2projection, WPfig3projection, 
                             WPfig4projection, WPfig5projection, WPfig6projection]

k = 0

while k < 6:

    data = pd.DataFrame({
        'x': np.concatenate([np.array([interest_floors_dates[j][0], datereadjust(interest_floors_dates[j][1]), None]) for j in range(k, southfloornamelen*6, len(set([i[2] for i in south_wp_dates])))]).tolist(),
        'y': np.concatenate([np.array([int((j)/len(set([i[2] for i in south_wp_dates]))), int((j)/len(set([i[2] for i in south_wp_dates])))+progress_gradients[j], None]) for j in range(k, southfloornamelen*6, len(set([i[2] for i in south_wp_dates])))]).tolist()
    })
    figadditivessth[k].add_trace(px.line(data, x='x', y = 'y', color_discrete_sequence=['black']).data[0])
    figadditivessth[k].update_traces(opacity = 0.05, hoverinfo = 'none', hovertemplate = None)
    #figadditivessth[k].update_layout(hovermode = False)
    
    for j in range(k, southfloornamelen*len(set([i[2] for i in south_wp_dates])), len(set([i[2] for i in south_wp_dates]))):

        if interest_floors_progress[j] == [[None, None]]:
            pass

        else:

            gradient_factor = 1

            if interest_floors_progress[j][-1][-1] < 95:
                
                gradient_factor = progress_gradients[j]
                figadditivessthprojection[k].add_trace(px.line(x = list([datereadjust(interest_floors_dates[j][1]), interest_floors_Dates[j][1], None]), 
                                      y = list([(j-k)/6+gradient_factor,(j-k)/6+1, None]), color_discrete_sequence = ['black']).data[0])
                #Update hovertext
                figadditivessthprojection[k].update_traces(hoverinfo = 'none', hovertemplate = None)
                figadditivessthprojection[k].update_traces(opacity = 0.05)

            #Generate initial/final dates per week and their progress
            floordates = np.array([[i[1], datereadjust(i[2]), None] for i in interest_floors_progress[j]])
            floornum = np.array([[(j-k)/6+gradient_factor*(datetime.combine(i[1], Time)-datetime.combine(interest_floors_progress[j][0][1], Time))/(datereadjust(interest_floors_progress[j][-1][2])-datetime.combine(interest_floors_progress[j][0][1], Time)),
                          (j-k)/6+gradient_factor*(datereadjust(i[2])-datetime.combine(interest_floors_progress[j][0][1], Time))/(datereadjust(interest_floors_progress[j][-1][2])-datetime.combine(interest_floors_progress[j][0][1], Time)), 
                          None] for i in interest_floors_progress[j]])
            floorcolor = np.array([[i[0], i[0], i[0]] for i in interest_floors_progress[j]])

            #Color workout array to simulate the continuous scenario
            color_discrete_sequence=np.array([[color_interpolation(custom_colorscale, i[0]),
                                       color_interpolation(custom_colorscale, i[0]),
                                       color_interpolation(custom_colorscale, i[0])
                                       ] for i in interest_floors_progress[j]])
            
            customdata0 = np.concatenate(np.array([[i[1], i[1], None] for i in interest_floors_progress[j]])).tolist()
            customdata1 = np.concatenate(np.array([[i[2]-timedelta(days=1), i[2]-timedelta(days=1), None] for i in interest_floors_progress[j]])).tolist()
            customdata2 = np.concatenate(floorcolor).tolist()
            customdata3 = np.concatenate(np.array([[i[3], i[4], None] for i in interest_floors_progress[j]])).tolist()
            customdata4 = np.concatenate(np.array([['L'+str(int(1+(j-k)/6)), 'L'+str(int(1+(j-k)/6)), None] for i in interest_floors_progress[j]])).tolist()

            # Define custom hover text for each bar in each set
            custom_hover_text = ['Date Range: '+str(customdata0[i])+' to '+str(customdata1[i])+' <br>Cumulative Progress: '+str(np.round(customdata3[i], 2))+'% <br>Level: '+str(customdata4[i]) if i%3 == 0 
                                    else 'Date Range: '+str(customdata0[i])+' to '+str(customdata1[i])+'<br>Progress in period: '+
                                                           str(np.round(customdata2[i], 2))+'% <br>Cumulative Progress: '+str(np.round(customdata3[i], 2))+'% <br>Level: '+str(customdata4[i]) if i%3 == 1
                                                           else None for i in range(len(customdata0))]
    
            #Show dataframe
            data1 = pd.DataFrame({
            'x': np.concatenate(floordates).tolist(),
            'y': np.concatenate(floornum).tolist(),
            'Number': np.concatenate(floorcolor).tolist(),
            'customdata': custom_hover_text
            })

            custom_hover_text = ['customdata']
    
            #Create color map for discrete sequence
            color_map = {} 

            for i in range(len(interest_floors_progress[j])):
        
                color_map.update({interest_floors_progress[j][i][0]: np.concatenate(color_discrete_sequence)[3*i]})

            #Add data of the flowlines

            fig1 = px.line(data1, x='x', y='y',
                  #hover_data = {'Number': ':.2f'},
                  color = 'Number',
                  color_discrete_map=color_map,
                  labels={'x': 'Date', 'y': 'Floor'},
                  range_x = [np.concatenate(floordates)[0]-timedelta(days = 5), np.concatenate(floordates)[-2]+timedelta(days = 5)],
                  hover_data = custom_hover_text)
            
            #Update hovertext
            fig1.update_traces(
                hovertemplate='%{customdata[0]}',
            )

            for i in range(len(fig1.data)):
                figadditivessth[k].add_trace(fig1.data[i])
            
    #for i in range(len(figadditivessthprojection[k].data)):
     #   fig.add_trace(figadditivessthprojection[k].data[i])
    
    for i in range(len(figadditivessth[k].data)):
        figadditivessth[k].data[i].name = ''
        fig.add_trace(figadditivessth[k].data[i])

    k += 1

fig.update_layout(showlegend = False)

#Creating the colorscale
fig.add_trace(px.scatter(x=[None, None, None], y=[None, None, None], 
                         color=[0, custom_colorscale[1][0], custom_colorscale[2][0]], 
                         range_color = [0, custom_colorscale[2][0]]).data[0])
#Update size of plot
fig.update_layout(height=560, width=950)
#Thicken the lines to seem as 'bars'
fig.update_traces(line=dict(width=5))
# Update colorbar title and scale
fig.update_coloraxes(colorbar_title='Percentage progress (%)<br> <br>', colorbar_title_side = 'top', colorscale = [[0, 'rgb(255,0,0)'], [custom_colorscale[1][0]/custom_colorscale[2][0], 'rgb(255,212,0)'], [1, 'rgb(52,235,0)']])
fig.update_layout(xaxis_title="<b>Date<b>", yaxis_title="<b>Floor<b>")
#Ticks for yaxis
fig.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(southfloornamelen+1)], 
                               ticktext = ['L' + str(i) for i in range(southfloornamelen+1)]))

fig.show()


# In[17]:


figadditivessth[0].data


# In[18]:


#Create colorscale
custom_colorscale = [
    [0, "#ff0000"],
    [15, "#ffd400"], 
    [30,"#34eb00"]
]

fig = px.line(labels={'x': 'Date', 'y': 'Floor'}, 
              title='<b>Flowlines Demising Walls North<b>',
              template='seaborn')

WPfig1 = px.line()
WPfig2 = px.line()
WPfig3 = px.line()
WPfig4 = px.line()
WPfig5 = px.line()
WPfig6 = px.line()
WPfig1projection = px.line()
WPfig2projection = px.line()
WPfig3projection = px.line()
WPfig4projection = px.line()
WPfig5projection = px.line()
WPfig6projection = px.line()

figadditives = [WPfig1, WPfig2, WPfig3, WPfig4, WPfig5, WPfig6]
figadditivesprojection = [WPfig1projection, WPfig2projection, WPfig3projection, 
                             WPfig4projection, WPfig5projection, WPfig6projection]

k = 0

while k < 6:

    data = pd.DataFrame({
        'x': np.concatenate([np.array([interest_floors_dates[j][0], datereadjust(interest_floors_dates[j][1]), None]) for j in range(southfloornamelen*6+k, len(interest_floors_dates), len(set([i[2] for i in south_wp_dates])))]).tolist(),
        'y': np.concatenate([np.array([int((j)/len(set([i[2] for i in south_wp_dates])))-southfloornamelen, int((j)/len(set([i[2] for i in south_wp_dates])))+progress_gradients[j]-southfloornamelen, None]) for j in range(southfloornamelen*6+k, len(interest_floors_dates), len(set([i[2] for i in south_wp_dates])))]).tolist()
    })
    figadditives[k].add_trace(px.line(data, x='x', y = 'y', color_discrete_sequence=['black']).data[0])
    figadditives[k].update_traces(opacity = 0.05, hoverinfo = 'none', hovertemplate = None)
    #figadditives[k].update_layout(hovermode = False)
    
    for j in range(southfloornamelen*len(set([i[2] for i in south_wp_dates]))+k, len(interest_floors_progress), len(set([i[2] for i in south_wp_dates]))):

        if interest_floors_progress[j] == [[None, None]]:
            pass

        else:

            gradient_factor = 1

            if interest_floors_progress[j][-1][-1] < 95:
                
                gradient_factor = progress_gradients[j]
                figadditivesprojection[k].add_trace(px.line(x = list([datereadjust(interest_floors_dates[j][1]), interest_floors_Dates[j][1], None]), 
                                      y = list([(j-k)/6+gradient_factor-southfloornamelen,(j-k)/6+1-southfloornamelen, None]), color_discrete_sequence = ['black']).data[0])
                #Update hovertext
                figadditivesprojection[k].update_traces(hoverinfo = 'none', hovertemplate = None)
                figadditivesprojection[k].update_traces(opacity = 0.05)

            #Generate initial/final dates per week and their progress
            floordates = np.array([[i[1], datereadjust(i[2]), None] for i in interest_floors_progress[j]])
            floornum = np.array([[(j-k)/6+gradient_factor*(datetime.combine(i[1], Time)-datetime.combine(interest_floors_progress[j][0][1], Time))/(datereadjust(interest_floors_progress[j][-1][2])-datetime.combine(interest_floors_progress[j][0][1], Time))-southfloornamelen,
                          (j-k)/6+gradient_factor*(datereadjust(i[2])-datetime.combine(interest_floors_progress[j][0][1], Time))/(datereadjust(interest_floors_progress[j][-1][2])-datetime.combine(interest_floors_progress[j][0][1], Time))-southfloornamelen, 
                          None] for i in interest_floors_progress[j]])
            floorcolor = np.array([[i[0], i[0], i[0]] for i in interest_floors_progress[j]])

            #Color workout array to simulate the continuous scenario
            color_discrete_sequence=np.array([[color_interpolation(custom_colorscale, i[0]),
                                       color_interpolation(custom_colorscale, i[0]),
                                       color_interpolation(custom_colorscale, i[0])
                                       ] for i in interest_floors_progress[j]])
    
            # Define custom hover text for each bar in each set
            customdata0 = np.concatenate(np.array([[i[1], i[1], None] for i in interest_floors_progress[j]])).tolist()
            customdata1 = np.concatenate(np.array([[i[2]-timedelta(days=1), i[2]-timedelta(days=1), None] for i in interest_floors_progress[j]])).tolist()
            customdata2 = np.concatenate(floorcolor).tolist()
            customdata3 = np.concatenate(np.array([[i[3], i[4], None] for i in interest_floors_progress[j]])).tolist()
            customdata4 = np.concatenate(np.array([['L'+str(int(1+(j-k)/6-southfloornamelen)),
                          'L'+str(int(1+(j-k)/6-southfloornamelen)), None] for i in interest_floors_progress[j]])).tolist()
            
            custom_hover_text = ['Date Range: '+str(customdata0[i])+' to '+str(customdata1[i])+' <br>Cumulative Progress: '+str(np.round(customdata3[i], 2))+'% <br>Level: '+str(customdata4[i]) if i%3 == 0 
                                    else 'Date Range: '+str(customdata0[i])+' to '+str(customdata1[i])+'<br>Progress in period: '+
                                                           str(np.round(customdata2[i], 2))+'% <br>Cumulative Progress: '+str(np.round(customdata3[i], 2))+'% <br>Level: '+str(customdata4[i]) if i%3 == 1
                                                           else None for i in range(len(customdata0))]
            
            #Show dataframe
            data1 = pd.DataFrame({
            'x': np.concatenate(floordates).tolist(),
            'y': np.concatenate(floornum).tolist(),
            'Number': np.concatenate(floorcolor).tolist(),
            'customdata': custom_hover_text
            })
    
            #Create color map for discrete sequence
            color_map = {} 

            for i in range(len(interest_floors_progress[j])):
        
                color_map.update({interest_floors_progress[j][i][0]: np.concatenate(color_discrete_sequence)[3*i]})

            custom_hover_text = ['customdata']

            #Add data of the flowlines

            fig1 = px.line(data1, x='x', y='y',
                  #hover_data = {'Number': ':.2f'},
                  color = 'Number',
                  color_discrete_map=color_map,
                  labels={'x': 'Date', 'y': 'Floor'},
                  range_x = [np.concatenate(floordates)[0]-timedelta(days = 5), np.concatenate(floordates)[-2]+timedelta(days = 5)],
                  hover_data = custom_hover_text)
            
            #Update hovertext
            fig1.update_traces(
                hovertemplate='%{customdata[0]}'
            )


            for i in range(len(fig1.data)):
                figadditives[k].add_trace(fig1.data[i])
            
    #for i in range(len(figadditivesprojection[k].data)):
     #   fig.add_trace(figadditivesprojection[k].data[i])

    for i in range(len(figadditives[k].data)):
        figadditives[k].data[i].name = ''
        fig.add_trace(figadditives[k].data[i])

    k += 1

fig.update_layout(showlegend = False)

#Creating the colorscale
fig.add_trace(px.scatter(x=[None, None, None], y=[None, None, None], 
                         color=[0, custom_colorscale[1][0], custom_colorscale[2][0]], 
                         range_color = [0, custom_colorscale[2][0]]).data[0])
#Update size of plot
fig.update_layout(height=560, width=950)
#Thicken the lines to seem as 'bars'
fig.update_traces(line=dict(width=5))
# Update colorbar title and scale
fig.update_coloraxes(colorbar_title='Percentage progress (%)', colorscale = [[0, 'rgb(255,0,0)'], [custom_colorscale[1][0]/custom_colorscale[2][0], 'rgb(255,212,0)'], [1, 'rgb(52,235,0)']])
fig.update_layout(xaxis_title="<b>Date<b>", yaxis_title="<b>Floor<b>")
#Ticks for yaxis
fig.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2]+1)], 
                               ticktext = ['']*(cladding_dates[1][1][-2]+1)))

#fig.show()


# In[19]:


from datetime import date

column_name = ['Location']
for i in new_table_list:
    column_name.append(i[-11:-1])

progress_activities = df[column_name].to_numpy()
floorname = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 
             'A08', 'A09', 'A10', 'A11', 'A12', 'A13']
interest_floors_A = []
interest_floors_dates_A = []
Date_format = '%Y-%m-%d'

for name in floorname:

    interest_floor_A = []

    for i in range(len(progress_activities)):
            if progress_activities[i,0][0:3] == name and int(progress_activities[i,0][3:5]) <= 5:
                interest_floor_A.append(progress_activities[i])

    #print(len(interest_floor_B))

    floor_index = [[0, int(len(interest_floor_A)/14)], [int(len(interest_floor_A)/14), int(len(interest_floor_A)/7)], 
                   [int(len(interest_floor_A)/7), int(3*len(interest_floor_A)/7)],
                    [int(3*len(interest_floor_A)/7), int(len(interest_floor_A)/2)],
                    [int(len(interest_floor_A)/2), int(11*len(interest_floor_A)/14)],
                    [int(11*len(interest_floor_A)/14), int(len(interest_floor_A))]]


    for i in range(1, len(new_table_list)+1):
        for j in range(len(interest_floor_A)):
            interest_floor_A[j][i]=int(interest_floor_A[j][i][:-1])

    for index in floor_index:

        interest_floor_dates_A = []

        interest_floor_progress_activities_A = [[np.average([interest_floor_A[i][j] for i in range(index[0], index[1])]), datetime.strptime(new_table_list[j-1][-11:-1], Date_format).date()] for j in range(1, len(new_table_list)+1)]

        for i in range(len(interest_floor_progress_activities_A)):

            if interest_floor_progress_activities_A[0][0]==interest_floor_progress_activities_A[-1][0] and i<=1:
                interest_floor_dates_A.append(None)
            elif interest_floor_progress_activities_A[0][0]==interest_floor_progress_activities_A[-1][0]:
                pass
            elif interest_floor_progress_activities_A[i][0]==interest_floor_progress_activities_A[0][0] and interest_floor_progress_activities_A[i+1][0]!=interest_floor_progress_activities_A[0][0]:
                interest_floor_dates_A.append(interest_floor_progress_activities_A[i][1])
            elif interest_floor_progress_activities_A[i][0]==interest_floor_progress_activities_A[-1][0] and interest_floor_progress_activities_A[i-1][0]!=interest_floor_progress_activities_A[-1][0]:
                interest_floor_dates_A.append(interest_floor_progress_activities_A[i][1])

        interest_floors_A.append(interest_floor_progress_activities_A)
        interest_floors_dates_A.append(interest_floor_dates_A)

        for i in range(len(interest_floors_A)):
            a_1 = 0
            a_2 = 0
            for j in range(len(interest_floors_A[i])):
                if interest_floors_A[i][j][1] == interest_floors_dates_A[i][0]:
                    a_1 = j
                elif interest_floors_A[i][j][1] == interest_floors_dates_A[i][1]:
                    a_2 = j
            interest_floors_A[i] = interest_floors_A[i][a_1:a_2+1]

for i in range(len(interest_floors_A)):
    if len(interest_floors_A[i])==1:
        interest_floors_A[i] = [None, None]

interest_floors_dates_A


# In[20]:


[interest_floors_A[i] for i in range(0, len(interest_floors_A),6)]
interest_floors_progress_A = []

for i in interest_floors_A:
    interest_floors_progress_element_A = []
    if i==[None, None]:
        interest_floors_progress_element_A.append(i)
    else:
        for j in range(len(i)-1):

            interest_floors_progress_element_A.append([i[j+1][0]-i[j][0], i[j][1], i[j+1][1], i[j][0], i[j+1][0]])
    interest_floors_progress_A.append(interest_floors_progress_element_A)

interest_floors_progress_A[0]
for i in range(len(interest_floors_progress_A)):
    j = [item for item in interest_floors_progress_A[i] if item[0] != 0]
    interest_floors_progress_A[i] = j

interest_floors_progress_A

#Make code to exclude outliers in interest_floors_progress
for i in range(len(interest_floors_progress_A)):

    if interest_floors_progress_A[i] == [[None, None]]:
        pass
    else:

        # Calculate median and quartiles
        for j in interest_floors_progress_A[i]:
            if j[3] <= 50 and j[4] > 50:
                median = timegap(interest_floors_progress_A[i][0][1], j[1])+timegap(j[1], j[2])*(50-j[3])/(j[4]-j[3])
            if j[3] <= 75 and j[4] > 75:
                q3 = timegap(interest_floors_progress_A[i][0][1], j[1])+timegap(j[1], j[2])*(75-j[3])/(j[4]-j[3])
            if j[3] <= 25 and j[4] > 25:
                q1 = timegap(interest_floors_progress_A[i][0][1], j[1])+timegap(j[1], j[2])*(25-j[3])/(j[4]-j[3])
        iqr = q3-q1
        removal = []
        
        for j in interest_floors_progress_A[i]:    
            if j[-2] > 95 and (timegap(interest_floors_progress_A[i][0][1], j[1])+timegap(interest_floors_progress_A[i][0][1], j[2]))/2>median+1.5*iqr:
                removal.append(j)
            else:
                pass       
            if j[-1] < 5 and timegap(interest_floors_progress_A[i][0][1], j[2])/2<median-1.5*iqr:
                removal.append(j)
            else:
                pass
        
        for j in removal:
            interest_floors_progress_A[i].remove(j)

for i in range(len(interest_floors_dates_A)):
    if interest_floors_dates_A[i] != [None, None]:
        interest_floors_dates_A[i] = [interest_floors_progress_A[i][0][1], interest_floors_progress_A[i][-1][2]]

interest_floors_progress_A[64]
progress_gradients_A = []
for i in interest_floors_progress_A:
    if i[-1][-1] == None:
        progress_gradients_A.append(0)
    else:
        if i[-1][-1] < 95:
            progress_gradients_A.append(i[-1][-1]/100*(datereadjust2(i[-1][2])-datereadjust3(i[0][1]))/(datereadjust(lastdate)-datereadjust3(i[0][1])))
        else: 
            progress_gradients_A.append(1)
interest_floors_progress_A[0], progress_gradients_A

interest_floors_Dates_A = [[interest_floors_dates_A[i][0], datereadjust3(interest_floors_dates_A[i][0]) + (datereadjust2(interest_floors_dates_A[i][1])-datereadjust3(interest_floors_dates_A[i][0]))/progress_gradients_A[i]] if interest_floors_dates_A[i] != [None, None] else [interest_floors_dates_A[i][0], interest_floors_dates_A[i][1]] for i in range(len(interest_floors_dates_A))]
interest_floors_Dates_A


# In[21]:


from datetime import date

column_name = ['Location']
for i in new_table_list:
    column_name.append(i[-11:-1])

progress_activities = df[column_name].to_numpy()
floorname = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'A07', 
             'A08', 'A09', 'A10', 'A11']
interest_floors_B = []
interest_floors_dates_B = []
Date_format = '%Y-%m-%d'

for name in floorname:

    interest_floor_B = []

    for i in range(len(progress_activities)):
            if progress_activities[i,0][0:3] == name and 10 >= int(progress_activities[i,0][3:5]) > 5:
                interest_floor_B.append(progress_activities[i])

    #print(len(interest_floor_B))

    floor_index = [[0, int(len(interest_floor_B)/14)], [int(len(interest_floor_B)/14), int(len(interest_floor_B)/7)], 
                   [int(len(interest_floor_B)/7), int(3*len(interest_floor_B)/7)],
                    [int(3*len(interest_floor_B)/7), int(len(interest_floor_B)/2)],
                    [int(len(interest_floor_B)/2), int(11*len(interest_floor_B)/14)],
                    [int(11*len(interest_floor_B)/14), int(len(interest_floor_B))]]


    for i in range(1, len(new_table_list)+1):
        for j in range(len(interest_floor_B)):
            interest_floor_B[j][i]=int(interest_floor_B[j][i][:-1])

    for index in floor_index:

        interest_floor_dates_B = []

        interest_floor_progress_activities_B = [[np.average([interest_floor_B[i][j] for i in range(index[0], index[1])]), datetime.strptime(new_table_list[j-1][-11:-1], Date_format).date()] for j in range(1, len(new_table_list)+1)]

        #print(interest_floor_progress_activities_B)
        for i in range(len(interest_floor_progress_activities_B)):

            if interest_floor_progress_activities_B[0][0]==interest_floor_progress_activities_B[-1][0] and i<=1:
                interest_floor_dates_B.append(None)
            elif interest_floor_progress_activities_B[0][0]==interest_floor_progress_activities_B[-1][0]:
                pass
            elif interest_floor_progress_activities_B[i][0]==interest_floor_progress_activities_B[0][0] and interest_floor_progress_activities_B[i+1][0]!=interest_floor_progress_activities_B[0][0]:
                interest_floor_dates_B.append(interest_floor_progress_activities_B[i][1])
            elif interest_floor_progress_activities_B[i][0]==interest_floor_progress_activities_B[-1][0] and interest_floor_progress_activities_B[i-1][0]!=interest_floor_progress_activities_B[-1][0]:
                interest_floor_dates_B.append(interest_floor_progress_activities_B[i][1])

        interest_floors_B.append(interest_floor_progress_activities_B)
        interest_floors_dates_B.append(interest_floor_dates_B)
        #print(interest_floors_dates_B[-1])

        for i in range(len(interest_floors_B)):
            a_1 = 0
            a_2 = 0
            #print(len(interest_floors_B[i]))
            if len(interest_floors_B[i]) !=0:
                #print(interest_floors_B[i][0])
                for j in range(len(interest_floors_B[i])):
                    if interest_floors_B[i][j][1] == interest_floors_dates_B[i][0]:
                        a_1 = j
                    elif interest_floors_B[i][j][1] == interest_floors_dates_B[i][1]:
                        a_2 = j
                interest_floors_B[i] = interest_floors_B[i][a_1:a_2+1]

for i in range(len(interest_floors_B)):
    if len(interest_floors_B[i])==1:
        interest_floors_B[i] = [None, None]

interest_floors_A


# In[22]:


[interest_floors_B[i] for i in range(0, len(interest_floors_B),6)]
interest_floors_progress_B = []

for i in interest_floors_B:
    interest_floors_progress_element_B = []
    if i==[None, None]:
        interest_floors_progress_element_B.append(i)
    else:
        for j in range(len(i)-1):

            interest_floors_progress_element_B.append([i[j+1][0]-i[j][0], i[j][1], i[j+1][1], i[j][0], i[j+1][0]])
    interest_floors_progress_B.append(interest_floors_progress_element_B)

interest_floors_progress_B[0]
for i in range(len(interest_floors_progress_B)):
    j = [item for item in interest_floors_progress_B[i] if item[0] != 0]
    interest_floors_progress_B[i] = j

interest_floors_progress_B

#Make code to exclude outliers in interest_floors_progress
for i in range(len(interest_floors_progress_B)):

    if interest_floors_progress_B[i] == [[None, None]]:
        pass
    else:

        # Calculate median and quartiles
        for j in interest_floors_progress_B[i]:
            if j[3] <= 50 and j[4] > 50:
                median = timegap(interest_floors_progress_B[i][0][1], j[1])+timegap(j[1], j[2])*(50-j[3])/(j[4]-j[3])
            if j[3] <= 75 and j[4] > 75:
                q3 = timegap(interest_floors_progress_B[i][0][1], j[1])+timegap(j[1], j[2])*(75-j[3])/(j[4]-j[3])
            if j[3] <= 25 and j[4] > 25:
                q1 = timegap(interest_floors_progress_B[i][0][1], j[1])+timegap(j[1], j[2])*(25-j[3])/(j[4]-j[3])
        iqr = q3-q1
        removal = []
        
        for j in interest_floors_progress_B[i]:    
            if j[-2] > 95 and (timegap(interest_floors_progress_B[i][0][1], j[1])+timegap(interest_floors_progress_B[i][0][1], j[2]))/2>median+1.5*iqr:
                removal.append(j)
            else:
                pass       
            if j[-1] < 5 and timegap(interest_floors_progress_B[i][0][1], j[2])/2<median-1.5*iqr:
                removal.append(j)
            else:
                pass
        
        for j in removal:
            interest_floors_progress_B[i].remove(j)

for i in range(len(interest_floors_dates_B)):
    if interest_floors_dates_B[i] != [None, None]:
        interest_floors_dates_B[i] = [interest_floors_progress_B[i][0][1], interest_floors_progress_B[i][-1][2]]

interest_floors_progress_B[64]
progress_gradients_B = []
for i in interest_floors_progress_B:
    if i[-1][-1] == None:
        progress_gradients_B.append(0)
    else:
        if i[-1][-1] < 95:
            progress_gradients_B.append(i[-1][-1]/100*(datereadjust2(i[-1][2])-datereadjust3(i[0][1]))/(datereadjust(lastdate)-datereadjust3(i[0][1])))
        else: 
            progress_gradients_B.append(1)
interest_floors_progress_B[0], progress_gradients_B

interest_floors_Dates_B = [[interest_floors_dates_B[i][0], datereadjust3(interest_floors_dates_B[i][0]) + (datereadjust2(interest_floors_dates_B[i][1])-datereadjust3(interest_floors_dates_B[i][0]))/progress_gradients_B[i]] if interest_floors_dates_B[i] != [None, None] else [interest_floors_dates_B[i][0], interest_floors_dates_B[i][1]] for i in range(len(interest_floors_dates_B))]
interest_floors_Dates_B


# In[23]:


interest_floors_Dates_A
interest_floors_Dates_B
north_wp_dates[0][0][2]
for i in range((cladding_dates[1][1][-2]+1)*len(set([i[2] for i in south_wp_dates]))):
    if i<len(interest_floors_Dates_A):
        pass
    else:
        interest_floors_Dates_A.append([None, None])

for i in range((cladding_dates[1][1][-2]+1)*len(set([i[2] for i in south_wp_dates]))):
    if i<len(interest_floors_Dates_B):
        pass
    else:
        interest_floors_Dates_B.append([None, None])
interest_floors_Dates_B


# In[24]:


fig = px.line()
fig1 = px.line()
fig2 = px.line()

# Add a custom legend trace using a scatter plot with the desired shape
legend_trace = px.line()
#Set height and width
height = 860
width = 2300
pixsize = 60

fig = px.line(labels={'x': 'Date', 'y': 'Floor'}, 
              title='<b>Flowlines 6WP Plan v Actual North by Location<b>',
              template='seaborn')

fig.add_shape(type="rect",
              x0=-2*(pixsize/width), x1=0,
              y0=0, y1=1,
              xref='paper', yref='paper',
              line=dict(color="#ffffff", width=1.5),
              fillcolor = '#eaeaf2',
              opacity = 1)

annotation_list1 = ['<b>1-5<b>', '<b>6-10<b>']

for i in range(2*cladding_dates[1][1][-2]):
    # Add horizontal lines to the margin
    fig.add_shape(type="line",
              x0=-2*(pixsize/width)*(1-i/2+i//2), x1=0,
              y0=i/2, y1=i/2,
              xref='paper', yref='y',
              line=dict(color="#ffffff", width=1.5),
              opacity = 1)
    
    if i < 2*(cladding_dates[1][1][-2]-1):
    # Add annotation to the margin
        fig.add_annotation(
            text=annotation_list1[i-2*(i//2)],
            x=-(pixsize/width),
            y=i/2+1/4,
            xref='paper', yref='y',
            font=dict(size=8),
            showarrow = False )

for i in range(cladding_dates[1][1][-2]-1):

    fig.add_annotation(
        text='<b>L'+str(i+1)+'<b>',
        x=-2*(pixsize/width),
        y=i+1/2,
        xref='paper', yref='y',
        font=dict(size=9),
        showarrow = False )

for i in range(0, 2*(cladding_dates[1][1][-2]), 2):
    #Interchanging background per floor location    
    fig.add_shape(type="rect",
          x0=-2*(pixsize/width)*(1-i/2+i//2), x1=1,
          y0=(i)/2, y1=(i+1)/2,
          xref='paper', yref='y',
          line=dict(color="#dadae2", width=0),
          opacity = 0.1)
    
fig.add_shape(type="line",
              x0=-(pixsize/width), x1=-(pixsize/width),
              y0=0, y1=1,
              xref='paper', yref='paper',
              line=dict(color="#ffffff", width=1.5),
              opacity = 1)

fig.add_shape(type="line",
              x0=-2*(pixsize/width), x1=-2*(pixsize/width),
              y0=0, y1=1,
              xref='paper', yref='paper',
              line=dict(color="#ffffff", width=1.5),
              opacity = 1)

colorset = [px.colors.qualitative.G10[i] for i in range(len(set([i[2] for i in south_wp_dates]))+2)]

for i in range(len(set(np.concatenate([np.array([j[1] for j in i]) for i in north_wp_dates]).tolist()))):
    data = pd.DataFrame({
        'x': np.concatenate([np.array([north_wp_dates[j][i][2][0], north_wp_dates[j][i][2][1], None, north_wp_dates[j][i][2][2], north_wp_dates[j][i][2][3], None]) for j in range(len(north_wp_dates))]).tolist(), 
        'y': np.concatenate([np.array([int(north_wp_dates[j][i][0][-2:])-1, int(north_wp_dates[j][i][0][-2:])-1/2, None, int(north_wp_dates[j][i][0][-2:])-1/2, int(north_wp_dates[j][i][0][-2:]), None]) for j in range(len(north_wp_dates))]).tolist(),
        'Color': [str(i)+', '+str(i)]*len(np.concatenate([np.array([north_wp_dates[j][i][2][0], north_wp_dates[j][i][2][1], None, north_wp_dates[j][i][2][2], north_wp_dates[j][i][2][3], None]) for j in range(len(north_wp_dates))]).tolist())
    })
    # Define custom hover text for each bar in each set
    custom_hover_text = [
        np.concatenate([np.array([north_wp_dates[j][i][2][0], north_wp_dates[j][i][2][0], None, north_wp_dates[j][i][2][2], north_wp_dates[j][i][2][2], None]) for j in range(len(north_wp_dates))]),
        np.concatenate([np.array([north_wp_dates[j][i][2][1], north_wp_dates[j][i][2][1], None, north_wp_dates[j][i][2][3], north_wp_dates[j][i][2][3], None]) for j in range(len(north_wp_dates))]),
        np.concatenate([np.array(['L'+str(int(north_wp_dates[j][i][0][-2:])), 'L'+str(int(north_wp_dates[j][i][0][-2:])), None, 
                                  'L'+str(int(north_wp_dates[j][i][0][-2:])), 'L'+str(int(north_wp_dates[j][i][0][-2:])), None]) for j in range(len(north_wp_dates))]),
    ]
    fig1.add_trace(px.line(data, x='x', y = 'y', color = 'Color', color_discrete_sequence=[colorset[i]], hover_data = custom_hover_text).data[0])
    fig1.update_traces(line=dict(dash='dash'))
    #Update hovertext
    fig1.update_traces(
        hovertemplate='Initial Date: %{customdata[0]}<br>Final Date: %{customdata[1]}<br>Level: %{customdata[2]}',
    )

for i in range(len(set([i[2] for i in south_wp_dates]))):
    data = pd.DataFrame({
        'x': np.concatenate([np.array([interest_floors_Dates_A[j][0], interest_floors_Dates_A[j][1], None, interest_floors_Dates_B[j][0], interest_floors_Dates_B[j][1], None]) for j in range(i, len(interest_floors_Dates_A), len(set([i[2] for i in south_wp_dates])))]).tolist(),
        'y': np.concatenate([np.array([int((j-i)/len(set([i[2] for i in south_wp_dates]))), int((j-i)/len(set([i[2] for i in south_wp_dates])))+1/2, None,
                                       int((j-i)/len(set([i[2] for i in south_wp_dates])))+1/2, int((j-i)/len(set([i[2] for i in south_wp_dates])))+1, None]) for j in range(i, len(interest_floors_Dates_A), len(set([i[2] for i in south_wp_dates])))]).tolist(),
        'Color': [str(i)]*len(np.concatenate([np.array([interest_floors_Dates_A[j][0], interest_floors_Dates_A[j][1], None, interest_floors_Dates_B[j][0], interest_floors_Dates_B[j][1], None]) for j in range(i, len(interest_floors_Dates_A), len(set([i[2] for i in south_wp_dates])))]).tolist())
    })
    # Define custom hover text for each bar in each set
    custom_hover_text = [
        np.concatenate([np.array([interest_floors_Dates_A[j][0], interest_floors_Dates_A[j][0], None, interest_floors_Dates_B[j][0], interest_floors_Dates_B[j][0], None]) for j in range(i, len(interest_floors_Dates_A), len(set([i[2] for i in south_wp_dates])))]),
        np.concatenate([np.array([interest_floors_Dates_A[j][1], interest_floors_Dates_A[j][1], None, interest_floors_Dates_B[j][1], interest_floors_Dates_B[j][1], None]) for j in range(i, len(interest_floors_Dates_A), len(set([i[2] for i in south_wp_dates])))]),
        np.concatenate([np.array(['L'+str(int((j-i)/len(set([i[2] for i in south_wp_dates]))+1)), 'L'+str(int((j-i)/len(set([i[2] for i in south_wp_dates]))+1)), None,
                                  'L'+str(int((j-i)/len(set([i[2] for i in south_wp_dates]))+1)), 'L'+str(int((j-i)/len(set([i[2] for i in south_wp_dates]))+1)), None]) for j in range(i, len(interest_floors_Dates_A), len(set([i[2] for i in south_wp_dates])))])
    ]
    fig2.add_trace(px.line(data, x='x', y = 'y', color='Color', color_discrete_sequence=[colorset[i]], hover_data = custom_hover_text).data[0])
    #Update hovertext
    fig2.update_traces(
        hovertemplate='Initial Date: %{customdata[0]}<br>Final Date: %{customdata[1]}<br>Level: %{customdata[2]}',
    )

for i in range(len(fig1.data)):
    fig.add_trace(fig1.data[i])
for i in range(len(fig2.data)):
    fig.add_trace(fig2.data[i])

# Add the custom legend trace to the figure
fig.add_traces(legend_trace.data)
#Define text of legend list
name_legend = ['Demising Walls', 'HL MEP Services (1st Fix)', 'Internal walls 2nd Drylining Visit', 
               'HL MEP Services (2nd Fix)', 'Final Drylining / Install Ceilings', 'Screed / Joinery / Kitchens']
# Define a dictionary to map trace names to custom legend labels
legend_labels = {}
for i in range(len(set([i[2] for i in south_wp_dates]))):

    legend_labels.update({
        str(i): name_legend[i]+' Actuals', 
        str(i)+', '+str(i): name_legend[i]+' Planned'
    })
    
# Customize the legend labels for each trace
fig.for_each_trace(lambda trace: trace.update(name=legend_labels.get(trace.name, trace.name)))
    
#Update size of plot
fig.update_layout(height=height, width=1403)
tickvals = [(i)/2 for i in range(2*(cladding_dates[1][1][-2]))]
fig.update_yaxes(range = [-1/4, 13.25])
fig.update_layout(xaxis_title="<b>Date<b>", yaxis_title="<b>Floor<b>")
#fig.update_xaxes(range = [datetime(2022, 10, 31)-timedelta(days=5), max([i for i in list(np.concatenate([i.x for i in fig.data])) if i!=None])+timedelta(days=5)])
fig.update_yaxes(tickvals=tickvals, ticktext = ['']*2*(cladding_dates[1][1][-2]), title_standoff = 30)
fig.update_layout(plot_bgcolor='#eaeaf2')
fig.update_layout(title_x=0.3)
Flowlines2fig = fig
fig.show()
#fig.write_html("figfitout6WP2.html")


# In[25]:


name_yaxis = ['Demising Walls', 'HL MEP Services<br>(1st Fix)', 'Internal walls<br>2nd Drylining Visit',
              'HL MEP Services<br>(2nd Fix)', 'Final Drylining /<br>Install Ceilings', 'Screed / Joinery /<br>Kitchens']


# In[26]:


def projectedtext(x):
    if x == None:
        return ''
    elif x < lastdate:
        return ''
    else:
        return ' (Projected)'


# In[27]:


nameyaxisposition = [-0.079, -0.083, -0.086, -0.082, -0.08, -0.084]

def plot_making(a, b):

    colorset = [px.colors.qualitative.G10[i] for i in range(len(set([i[2] for i in south_wp_dates])))]

    data0 = pd.DataFrame({
        'x': np.concatenate([np.array([i[2][0], datereadjust2(i[2][1]), None]) for i in a]).tolist(),
        'y': np.concatenate([np.array([i, i+1, None]) for i in range(len(a))]).tolist()
    })

    data1 = pd.DataFrame({
        'x': np.concatenate([np.array([datereadjust3(i[0]), i[1], None]) for i in b]).tolist(),
        'y': np.concatenate([np.array([i, i+1, None]) for i in range(len(b))]).tolist()
    })

    flowlineactivityfig = px.line(template = 'seaborn')

    flowlineactivityfig.add_shape(type='rect',
                              x0=-0.09, x1=0,
                              y0=0, y1=1,
                              xref='paper', yref='paper',
                              fillcolor = '#eaeaf2',
                              opacity = 1)

    for i in range(len(set([i[2] for i in south_wp_dates]))+1):

        flowlineactivityfig.add_shape(type='line',
                                  x0=-0.09, x1=0,
                                  y0=i, y1=i,
                                  xref='paper', yref='y',
                                  line=dict(color="#ffffff", width=1.5),
                                  opacity = 1)
    
        if i < len(set([i[2] for i in south_wp_dates])):

            flowlineactivityfig.add_shape(type='rect',
                                  x0=-0.09, x1=1,
                                  y0=i, y1=i+1,
                                  xref='paper', yref='y',
                                  fillcolor=colorset[i],
                                  opacity = 0.1)

            flowlineactivityfig.add_annotation(text=name_yaxis[i],
                                  x=nameyaxisposition[i], y=i+1/2,
                                  xref='paper', yref='y',
                                  font = dict(size=10),
                                  showarrow=False)
    
    flowlineactivityfig.add_shape(type='line',
                              x0=0, x1=0,
                              y0=0, y1=1,
                              xref='paper', yref='paper',
                              line=dict(color="#ffffff", width=1.5),
                              opacity = 1)
    custom_hover_text = [
        np.concatenate([np.array([i[2][0], i[2][0], None]) for i in a]).tolist(),
        np.concatenate([np.array([datereadjust6(i[2][1]), datereadjust6(i[2][1]), None]) for i in a]).tolist(),
        np.concatenate([np.array([name_legend[i], name_legend[i], None]) for i in range(len(a))]).tolist()
    ]
    custom_hover_text2 = [
        np.concatenate([np.array([datereadjust6(datereadjust3(i[0])), datereadjust6(datereadjust3(i[0])), None]) for i in b]).tolist(),
        np.concatenate([np.array([str(datereadjust6(i[1]))+projectedtext(datereadjust6(i[1])), str(datereadjust6(i[1]))+projectedtext(datereadjust6(i[1])), None]) for i in b]).tolist(),
        np.concatenate([np.array([name_legend[i], name_legend[i], None]) for i in range(len(b))]).tolist()
    ]
    if a==[[None, None, [None]*4]*6]:
        flowlineactivityfig.add_trace(px.line(data1, x='x', y='y', hover_data = custom_hover_text2).data[0])
    else:
        flowlineactivityfig.add_trace(px.line(data0, x='x', y='y', hover_data = custom_hover_text).data[0])
        flowlineactivityfig.update_traces(line=dict(dash='dash'))
        flowlineactivityfig.add_trace(px.line(data1, x='x', y='y', hover_data = custom_hover_text2).data[0])
    flowlineactivityfig.update_traces(
        hovertemplate='Initial Date: %{customdata[0]}<br>Final Date: %{customdata[1]}<br>Activity: %{customdata[2]}',
    )
    if [i for i in list(np.concatenate([i.x for i in flowlineactivityfig.data])) if i != None]!=[]:
        enddate = max(datereadjust5(i) for i in list(np.concatenate([i.x for i in flowlineactivityfig.data])) if type(i) == date or type(i) == datetime)
    else:
        #For the case that not enough data has been gathered
        enddate = date(2023, 9, 28)
    flowlineactivityfig.update_layout(height = 860, width = 1403, title=dict(text = '<b>Plan vs Activity lines<b>', font = dict(size = 30)), xaxis_range = [date(2022, 10, 31)-timedelta(days=5), 
                                                                                                       enddate+timedelta(days=5)], yaxis_range=[-0.25, 6.25])
    flowlineactivityfig.update_xaxes(title='<b>Date<b>')
    flowlineactivityfig.update_layout(yaxis=dict(title='<b>Activities<b>', title_standoff=120, tickvals = None))
    return flowlineactivityfig

def plot_making2(a, b):

    colorset = [px.colors.qualitative.G10[i] for i in range(len(set([i[2] for i in south_wp_dates])))]

    data0 = pd.DataFrame({
        'x': np.concatenate([np.array([i[2][2], datereadjust2(i[2][3]), None]) for i in a]).tolist(),
        'y': np.concatenate([np.array([i, i+1, None]) for i in range(len(a))]).tolist()
    })

    data1 = pd.DataFrame({
        'x': np.concatenate([np.array([i[0] + timedelta(days = 1), i[1], None]) if i != [None, None] else np.array([None, None, None]) for i in b]).tolist(),
        'y': np.concatenate([np.array([i, i+1, None]) for i in range(len(b))]).tolist()
    })

    flowlineactivityfig = px.line(template = 'seaborn')

    flowlineactivityfig.add_shape(type='rect',
                              x0=-0.09, x1=0,
                              y0=0, y1=1,
                              xref='paper', yref='paper',
                              fillcolor = '#eaeaf2',
                              opacity = 1)

    for i in range(len(set([i[2] for i in south_wp_dates]))+1):

        flowlineactivityfig.add_shape(type='line',
                                  x0=-0.09, x1=0,
                                  y0=i, y1=i,
                                  xref='paper', yref='y',
                                  line=dict(color="#ffffff", width=1.5),
                                  opacity = 1)
    
        if i < len(set([i[2] for i in south_wp_dates])):

            flowlineactivityfig.add_shape(type='rect',
                                  x0=-0.09, x1=1,
                                  y0=i, y1=i+1,
                                  xref='paper', yref='y',
                                  fillcolor=colorset[i],
                                  opacity = 0.1)

            flowlineactivityfig.add_annotation(text=name_yaxis[i],
                                  x=nameyaxisposition[i], y=i+1/2,
                                  xref='paper', yref='y',
                                  font = dict(size=10),
                                  showarrow=False)
    
    flowlineactivityfig.add_shape(type='line',
                              x0=0, x1=0,
                              y0=0, y1=1,
                              xref='paper', yref='paper',
                              line=dict(color="#ffffff", width=1.5),
                              opacity = 1)
    custom_hover_text = [
        np.concatenate([np.array([i[2][2], i[2][2], None])for i in a]).tolist(),
        np.concatenate([np.array([datereadjust6(i[2][3]), datereadjust6(i[2][3]), None]) for i in a]).tolist(),
        np.concatenate([np.array([name_legend[i], name_legend[i], None]) for i in range(len(a))]).tolist()
    ]
    custom_hover_text2 = [
        np.concatenate([np.array([datereadjust6(datereadjust3(i[0])), datereadjust6(datereadjust3(i[0])), None]) for i in b]).tolist(),
        np.concatenate([np.array([str(datereadjust6(i[1]))+projectedtext(datereadjust6(i[1])), str(datereadjust6(i[1]))+projectedtext(datereadjust6(i[1])), None]) for i in b]).tolist(),
        np.concatenate([np.array([name_legend[i], name_legend[i], None]) for i in range(len(b))]).tolist()
    ]
    if a==[[None, None, [None]*4]*6]:
        flowlineactivityfig.add_trace(px.line(data1, x='x', y='y', hover_data = custom_hover_text2).data[0])
    else:
        flowlineactivityfig.add_trace(px.line(data0, x='x', y='y', hover_data = custom_hover_text).data[0])
        flowlineactivityfig.update_traces(line=dict(dash='dash'))
        flowlineactivityfig.add_trace(px.line(data1, x='x', y='y', hover_data = custom_hover_text2).data[0])
    flowlineactivityfig.update_traces(
        hovertemplate='Initial Date: %{customdata[0]}<br>Final Date: %{customdata[1]}<br>Activity: %{customdata[2]}',
    )
    if [i for i in list(np.concatenate([i.x for i in flowlineactivityfig.data])) if i != None]!=[]:
        enddate = max(datereadjust5(i) for i in list(np.concatenate([i.x for i in flowlineactivityfig.data])) if type(i) == date or type(i) == datetime)
    else:
        #For the case that not enough data has been gathered
        enddate = date(2023, 9, 28)
    flowlineactivityfig.update_layout(height = 860, width = 1403, title=dict(text = '<b>Plan vs Activity lines<b>', font = dict(size = 30)), xaxis_range = [date(2022, 10, 31)-timedelta(days=5), 
                                                                                                       enddate+timedelta(days=5)], yaxis_range=[-0.25, 6.25])
    flowlineactivityfig.update_xaxes(title='<b>Date<b>')
    flowlineactivityfig.update_layout(yaxis=dict(title='<b>Activities<b>', title_standoff=120, tickvals = None))
    return flowlineactivityfig

def plot_making3(a, b):

    colorset = [px.colors.qualitative.G10[i] for i in range(len(set([i[2] for i in south_wp_dates])))]

    data0 = pd.DataFrame({
        'x': np.concatenate([np.array([i[3], datereadjust2(i[4]), None]) if i != [None, None, [None]*4] else np.array([None, None, None]) for i in a]).tolist(),
        'y': np.concatenate([np.array([i, i+1, None]) for i in range(len(a))]).tolist()
    })

    data1 = pd.DataFrame({
        'x': np.concatenate([np.array([i[0], i[1], None]) if i != [None, None] else np.array([None, None, None]) for i in b]).tolist(),
        'y': np.concatenate([np.array([i, i+1, None]) for i in range(len(b))]).tolist()
    })

    flowlineactivityfig = px.line(template = 'seaborn')

    flowlineactivityfig.add_shape(type='rect',
                              x0=-0.09, x1=0,
                              y0=0, y1=1,
                              xref='paper', yref='paper',
                              fillcolor = '#eaeaf2',
                              opacity = 1)

    for i in range(len(set([i[2] for i in south_wp_dates]))+1):

        flowlineactivityfig.add_shape(type='line',
                                  x0=-0.09, x1=0,
                                  y0=i, y1=i,
                                  xref='paper', yref='y',
                                  line=dict(color="#ffffff", width=1.5),
                                  opacity = 1)
    
        if i < len(set([i[2] for i in south_wp_dates])):

            flowlineactivityfig.add_shape(type='rect',
                                  x0=-0.09, x1=1,
                                  y0=i, y1=i+1,
                                  xref='paper', yref='y',
                                  fillcolor=colorset[i],
                                  opacity = 0.1)

            flowlineactivityfig.add_annotation(text=name_yaxis[i],
                                  x=nameyaxisposition[i], y=i+1/2,
                                  xref='paper', yref='y',
                                  font = dict(size=10),
                                  showarrow=False)
    
    flowlineactivityfig.add_shape(type='line',
                              x0=0, x1=0,
                              y0=0, y1=1,
                              xref='paper', yref='paper',
                              line=dict(color="#ffffff", width=1.5),
                              opacity = 1)
    custom_hover_text = [
        np.concatenate([np.array([i[3], i[3], None]) for i in a]).tolist(),
        np.concatenate([np.array([datereadjust6(i[4]), datereadjust6(i[4]), None]) for i in a]).tolist(),
        np.concatenate([np.array([name_legend[i], name_legend[i], None]) for i in range(len(a))]).tolist()
    ]
    custom_hover_text2 = [
        np.concatenate([np.array([datereadjust6(i[0]), datereadjust6(i[0]), None]) for i in b]).tolist(),
        np.concatenate([np.array([str(datereadjust6(i[1]))+projectedtext(datereadjust6(i[1])), str(datereadjust6(i[1]))+projectedtext(datereadjust6(i[1])), None]) for i in b]).tolist(),
        np.concatenate([np.array([name_legend[i], name_legend[i], None]) for i in range(len(b))]).tolist()
    ]
    if a==[[None]*5]*6:
        flowlineactivityfig.add_trace(px.line(data1, x='x', y='y', hover_data = custom_hover_text2).data[0])
    else:
        flowlineactivityfig.add_trace(px.line(data0, x='x', y='y', hover_data = custom_hover_text).data[0])
        flowlineactivityfig.update_traces(line=dict(dash='dash'))
        flowlineactivityfig.add_trace(px.line(data1, x='x', y='y', hover_data = custom_hover_text2).data[0])
    flowlineactivityfig.update_traces(
        hovertemplate='Initial Date: %{customdata[0]}<br>Final Date: %{customdata[1]}<br>Activity: %{customdata[2]}',
    )
    if [i for i in list(np.concatenate([i.x for i in flowlineactivityfig.data])) if i != None]!=[]:
        enddate = max(datereadjust5(i) for i in list(np.concatenate([i.x for i in flowlineactivityfig.data])) if type(i) == date or type(i) == datetime)
    else:
        #For the case that not enough data has been gathered
        enddate = date(2023, 9, 28)
    flowlineactivityfig.update_layout(height = 860, width = 1403, title=dict(text = '<b>Plan vs Activity lines<b>', font = dict(size = 30)), xaxis_range = [date(2022, 10, 31)-timedelta(days=5), 
                                                                                                       enddate+timedelta(days=5)], yaxis_range=[-0.25, 6.25])
    flowlineactivityfig.update_xaxes(title='<b>Date<b>')
    flowlineactivityfig.update_layout(yaxis=dict(title='<b>Activities<b>', title_standoff=120, tickvals = None))
    return flowlineactivityfig


# In[28]:


flowlineactivitiesfigsth = px.line()
flowlineactivitiesfig_layouts_datapointssth = []
flowlineactivitiesfig_layoutssth = []

for i in range(southfloornamelen):

    datapointsA = []

    a = plot_making3([list(south_wp_dates[j]) for j in range(i*len(set([i[2] for i in south_wp_dates])), (i+1)*len(set([i[2] for i in south_wp_dates])))], interest_floors_Dates[6*i:6*i+6])

    for i in range(len(plot_making3([list(south_wp_dates[j]) for j in range(i*len(set([i[2] for i in south_wp_dates])), (i+1)*len(set([i[2] for i in south_wp_dates])))], interest_floors_Dates[6*i:6*i+6]).data)):

        flowlineactivitiesfigsth.add_trace(a.data[i])
        datapointsA.append(a.data[i])
        
    flowlineactivitiesfig_layoutssth.append(a.layout)

    flowlineactivitiesfig_layouts_datapointssth.append(datapointsA)

plot_making3([list(south_wp_dates[j]) for j in range(6, 12)], interest_floors_Dates[6:12])


# In[29]:


datereadjust6(datetime(2023, 9, 28, 23, 0))


# In[30]:


[i.x for i in plot_making3([list(south_wp_dates[j]) for j in range(24, 30)], interest_floors_Dates[24:30]).data if i.line.dash == 'dash'][0]


# In[31]:


timedelta(days=2, hours = 8).days


# In[32]:


plot_making3([list(south_wp_dates[j]) for j in range(12, 18)], interest_floors_Dates[12:18])


# In[33]:


flowlineactivitiesfig = px.line()
flowlineactivitiesfig_layouts_datapoints = []
flowlineactivitiesfig_layouts = []

for i in range(cladding_dates[1][1][-2]-1):

    datapointsA = []
    datapointsB = []

    if i<11:

        a = plot_making(north_wp_dates[i], interest_floors_Dates_A[6*i:6*i+6])
        b = plot_making2(north_wp_dates[i], interest_floors_Dates_B[6*i:6*i+6])

        for i in range(len(plot_making(north_wp_dates[i], interest_floors_Dates_A[6*i:6*i+6]).data)):
            flowlineactivitiesfig.add_trace(a.data[i])
            datapointsA.append(a.data[i])
            flowlineactivitiesfig.add_trace(b.data[i])
            datapointsB.append(b.data[i])
        flowlineactivitiesfig_layouts.append(a.layout)
        flowlineactivitiesfig_layouts.append(b.layout)
    else:

        a = plot_making([[None, None, [None]*4]*6], interest_floors_Dates_A[6*i:6*i+6])
        b = plot_making2([[None, None, [None]*4]*6], interest_floors_Dates_B[6*i:6*i+6])

        for i in range(len(plot_making([[None, None, [None]*4]*6], interest_floors_Dates_A[6*i:6*i+6]).data)):
            flowlineactivitiesfig.add_trace(a.data[i])
            datapointsA.append(a.data[i])
            flowlineactivitiesfig.add_trace(b.data[i])
            datapointsB.append(b.data[i])
        flowlineactivitiesfig_layouts.append(a.layout)
        flowlineactivitiesfig_layouts.append(b.layout)

    flowlineactivitiesfig_layouts_datapoints.append([datapointsA, datapointsB])


# In[34]:


plot_making(north_wp_dates[i], interest_floors_Dates_A[6*0:6*0+6])


# In[35]:


[i.x for i in plot_making(north_wp_dates[i], interest_floors_Dates_A[6*0:6*0+6]).data if i.line.dash == 'solid'], [i.y for i in plot_making(north_wp_dates[i], interest_floors_Dates_A[6*0:6*0+6]).data if i.line.dash == 'solid']


# In[36]:


interest_floors_Dates_A, progress_gradients_A


# In[37]:


plot_making([[None, None, [None]*4]*6], interest_floors_Dates_A[6*12:6*12+6])


# In[38]:


#a = plot_making(north_wp_dates[0], interest_floors_Dates_A[6*0:6*0+6])
#max(np.concatenate([np.array([datereadjust3(i[2][0]), i[2][1]]) for i in a]).tolist())
north_wp_dates[0]


# In[39]:


flowlineactivitiesfig_layouts_datapoints[0][0]
flowlineactivitiesfig


# In[40]:


interest_floors_progress_A[74]


# In[41]:


name_legend


# In[82]:


activitiesfigadditivesA = []
activitiesprojectionA = []

for i in range(len(interest_floors_progress_A)):
      Activitiesfig = px.line(template = 'seaborn')
      activityprojection = px.line(template = 'seaborn')

      Activitiesfig.add_trace(px.line(x = np.concatenate([np.array([datetime.combine(interest_floors_progress_A[i][0][1], Time)+timedelta(days = 1), datereadjust2(interest_floors_progress_A[i][-1][2]), None]) if interest_floors_progress_A[i] != [[None, None]] else np.array([None, None, None])]).tolist(),
                              y = [i % 6, i % 6 + progress_gradients_A[i], None], color_discrete_sequence=['black']).data[0])
      Activitiesfig.update_traces(opacity = 0.05, hoverinfo = 'none', hovertemplate = None)

      if interest_floors_progress_A[i] != [[None, None]] and interest_floors_progress_A[i][-1][-1] < 95:

                data = pd.DataFrame({
                  'x': list([datereadjust2(interest_floors_dates_A[i][1]), interest_floors_Dates_A[i][1], None]),
                  'y': list([i%6+progress_gradients_A[i],i%6+1, None]),
                  'Color': ['black']*3
                })
                # Define custom hover text for each bar in each set
                custom_hover_text_projection = ['customdata']

                activityprojection.add_trace(px.line(data, x = 'x', y = 'y', color_discrete_sequence = ['black']*3).data[0])
                #Update hovertext
                activityprojection.update_traces(hoverinfo = 'none', hovertemplate = None)
                activityprojection.update_traces(opacity = 0.05)
                activityprojection.update_traces(line=dict(width=15))
      else:
           activityprojection = px.line(x = [None, None, None], y = [None, None, None])
      
      activitiesprojectionA.append(activityprojection)

      customdata0 = np.concatenate([np.array([datetime.combine(j[1], Time)+timedelta(days = 1), datetime.combine(j[1], Time)+timedelta(days = 1), None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress_A[i]]).tolist()
      customdata1 = np.concatenate([np.array([datereadjust2(j[2]), datereadjust2(j[2]), None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress_A[i]]).tolist()
      customdata2 = np.concatenate([np.array([j[0], j[0], j[0]]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress_A[i]]).tolist()
      customdata3 = np.concatenate([np.array([j[3], j[4], None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress_A[i]]).tolist()
      customdata4 = [name_legend[i%6]]*len(customdata0)
      
      if interest_floors_progress_A[i] != [[None, None]]:      
            custom_hover_text = ['Date Range: '+str(datereadjust6(customdata0[i]))+' to '+str(datereadjust6(customdata1[i]))+' <br>Cumulative Progress: '+str(np.round(customdata3[i], 2))+'% <br>Activity: '+customdata4[i] if i%3 == 0 
                                    else 'Date Range: '+str(datereadjust6(customdata0[i]))+' to '+str(datereadjust6(customdata1[i]))+'<br>Progress in period: '+
                                                           str(np.round(customdata2[i], 2))+'% <br>Cumulative Progress: '+str(np.round(customdata3[i], 2))+'% <br>Activity: '+customdata4[i] if i%3 == 1
                                                           else None for i in range(len(customdata0))]
      else:
            custom_hover_text = [None]*len(customdata0)

      dataactivities = pd.DataFrame({
            'x': np.concatenate([np.array([datetime.combine(j[1], Time)+timedelta(days = 1), datereadjust2(j[2]), None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress_A[i]]).tolist(),
            'y': np.concatenate([np.array([i%6+progress_gradients_A[i]*(datetime.combine(j[1], Time)-datetime.combine(interest_floors_progress_A[i][0][1], Time))/(datereadjust2(interest_floors_progress_A[i][-1][2])-datetime.combine(interest_floors_progress_A[i][0][1], Time)-timedelta(days = 1)), 
                                          i%6+progress_gradients_A[i]*(datereadjust2(j[2])-timedelta(days = 1)-datetime.combine(interest_floors_progress_A[i][0][1], Time))/(datereadjust2(interest_floors_progress_A[i][-1][2])-datetime.combine(interest_floors_progress_A[i][0][1], Time)-timedelta(days = 1)), None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress_A[i]]).tolist(),
            'Color': np.concatenate([np.array([j[0], j[0], j[0]]) for j in interest_floors_progress_A[i]]).tolist(),
            'customdata': custom_hover_text
      })

      custom_hover_text = ['customdata']
      #Create color map for discrete sequence
      color_map = {} 

      for j in range(len(interest_floors_progress_A[i])):
            
            if interest_floors_progress_A[i] != [[None, None]]:
                  color_map.update({interest_floors_progress_A[i][j][0]: color_interpolation(custom_colorscale, interest_floors_progress_A[i][j][0])})
                  activitiesfig = px.line(dataactivities, x='x', y='y',
                  color = 'Color',
                  color_discrete_map=color_map,
                  labels={'x': 'Date', 'y': 'Activities'},
                  template = 'seaborn',
                  hover_data = custom_hover_text)
                  
                  activitiesfig.update_traces(hovertemplate = '%{customdata[0]}')
            else:
                  activitiesfig = px.line(x=[None, None], y=[None, None])

      for k in range(len(activitiesfig.data)):
            activitiesfig.data[k].name = ''
            Activitiesfig.add_trace(activitiesfig.data[k])
      
      Activitiesfig.update_layout(showlegend = False)
      Activitiesfig.update_traces(line=dict(width=15))

      activitiesfigadditivesA.append(Activitiesfig)            


# In[83]:


activitiesfigadditivesA[72].update_xaxes(type = 'date')


# In[77]:


interest_floors_progress_A[72]


# In[46]:


activitiesfigadditivesB = []
activitiesprojectionB = []

for i in range(len(interest_floors_progress_B)):
      Activitiesfig = px.line(template = 'seaborn')
      activityprojection = px.line(template = 'seaborn')

      Activitiesfig.add_trace(px.line(x = np.concatenate([np.array([datetime.combine(interest_floors_progress_B[i][0][1], Time)+timedelta(days = 1), datereadjust2(interest_floors_progress_B[i][-1][2]), None]) if interest_floors_progress_B[i] != [[None, None]] else np.array([None, None, None])]).tolist(),
                              y = [i % 6, i % 6 + progress_gradients_B[i], None], color_discrete_sequence=['black']).data[0])
      Activitiesfig.update_traces(opacity = 0.05, hoverinfo = 'none', hovertemplate = None)

      if interest_floors_progress_B[i] != [[None, None]] and interest_floors_progress_B[i][-1][-1] < 95:
                
                activityprojection.add_trace(px.line(x = list([datereadjust2(interest_floors_dates_B[i][1]), interest_floors_Dates_B[i][1], None]), 
                                      y = list([i%6+progress_gradients_B[i],i%6+1, None]), color_discrete_sequence = ['black']).data[0])
                #Update hovertext
                activityprojection.update_traces(hoverinfo = 'none', hovertemplate = None)
                activityprojection.update_traces(opacity = 0.05)
                activityprojection.update_traces(line=dict(width=15))
      else:
           activityprojection = px.line(x = [None, None, None], y = [None, None, None])
      
      activitiesprojectionB.append(activityprojection)

      customdata0 = np.concatenate([np.array([datetime.combine(j[1], Time)+timedelta(days = 1), datetime.combine(j[1], Time)+timedelta(days = 1), None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress_B[i]]).tolist()
      customdata1 = np.concatenate([np.array([datereadjust2(j[2]), datereadjust2(j[2]), None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress_B[i]]).tolist()
      customdata2 = np.concatenate([np.array([j[0], j[0], j[0]]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress_B[i]]).tolist()
      customdata3 = np.concatenate([np.array([j[3], j[4], None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress_B[i]]).tolist()
      customdata4 = [name_legend[i%6]]*len(customdata0)

      if interest_floors_progress_B[i] != [[None, None]]:      
            custom_hover_text = ['Date Range: '+str(datereadjust6(customdata0[i]))+' to '+str(datereadjust6(customdata1[i]))+' <br>Cumulative Progress: '+str(np.round(customdata3[i], 2))+'% <br>Activity: '+customdata4[i] if i%3 == 0 
                                    else 'Date Range: '+str(datereadjust6(customdata0[i]))+' to '+str(datereadjust6(customdata1[i]))+'<br>Progress in period: '+
                                                           str(np.round(customdata2[i], 2))+'% <br>Cumulative Progress: '+str(np.round(customdata3[i], 2))+'% <br>Activity: '+customdata4[i] if i%3 == 1
                                                           else None for i in range(len(customdata0))]
      else:
            custom_hover_text = [None]*len(customdata0)

      dataactivities = pd.DataFrame({
            'x': np.concatenate([np.array([datetime.combine(j[1], Time)+timedelta(days = 1), datereadjust2(j[2]), None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress_B[i]]).tolist(),
            'y': np.concatenate([np.array([i%6+progress_gradients_B[i]*(datetime.combine(j[1], Time)-datetime.combine(interest_floors_progress_B[i][0][1], Time))/(datereadjust2(interest_floors_progress_B[i][-1][2])-datetime.combine(interest_floors_progress_B[i][0][1], Time)-timedelta(days = 1)), 
                                          i%6+progress_gradients_B[i]*(datereadjust2(j[2])-timedelta(days = 1)-datetime.combine(interest_floors_progress_B[i][0][1], Time))/(datereadjust2(interest_floors_progress_B[i][-1][2])-datetime.combine(interest_floors_progress_B[i][0][1], Time)-timedelta(days = 1)), None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress_B[i]]).tolist(),
            'Color': np.concatenate([np.array([j[0], j[0], j[0]]) for j in interest_floors_progress_B[i]]).tolist(),
            'customdata': custom_hover_text
      })

      custom_hover_text = ['customdata']
      
      #Create color map for discrete sequence
      color_map = {} 

      for j in range(len(interest_floors_progress_B[i])):
            
            if interest_floors_progress_B[i] != [[None, None]]:
                  color_map.update({interest_floors_progress_B[i][j][0]: color_interpolation(custom_colorscale, interest_floors_progress_B[i][j][0])})
                  activitiesfig = px.line(dataactivities, x='x', y='y',
                  color = 'Color',
                  color_discrete_map=color_map,
                  labels={'x': 'Date', 'y': 'Activities'},
                  template = 'seaborn',
                  hover_data = custom_hover_text)

                  activitiesfig.update_traces(hovertemplate = '%{customdata[0]}')
            else:
                  activitiesfig = px.line(x=[None, None], y=[None, None])

      for i in range(len(activitiesfig.data)):
            activitiesfig.data[i].name = ''
            Activitiesfig.add_trace(activitiesfig.data[i])
      
      Activitiesfig.update_layout(showlegend = False)
      Activitiesfig.update_traces(line=dict(width=15))

      activitiesfigadditivesB.append(Activitiesfig)            


# In[48]:


activitiesfigadditivesC = []
activitiesprojectionC = []

for i in range(len(name_legend)*southfloornamelen):
      Activitiesfig = px.line(template = 'seaborn')
      activityprojection = px.line(template = 'seaborn')

      Activitiesfig.add_trace(px.line(x = np.concatenate([np.array([datetime.combine(interest_floors_progress[i][0][1], Time), datereadjust(interest_floors_progress[i][-1][2]), None]) if interest_floors_progress[i] != [[None, None]] else np.array([None, None, None])]).tolist(),
                              y = [i % 6, i % 6 + progress_gradients[i], None], color_discrete_sequence=['black']).data[0])
      Activitiesfig.update_traces(opacity = 0.05, hoverinfo = 'none', hovertemplate = None)

      if interest_floors_progress[i] != [[None, None]] and interest_floors_progress[i][-1][-1] < 95:
                
                activityprojection.add_trace(px.line(x = list([datereadjust(interest_floors_dates[i][1]), interest_floors_Dates[i][1], None]), 
                                      y = list([i%6+progress_gradients[i],i%6+1, None]), color_discrete_sequence = ['black']).data[0])
                #Update hovertext
                activityprojection.update_traces(hoverinfo = 'none', hovertemplate = None)
                activityprojection.update_traces(opacity = 0.05)
                activityprojection.update_traces(line=dict(width=15))
      else:
           activityprojection = px.line(x = [None, None, None], y = [None, None, None])
      
      activitiesprojectionC.append(activityprojection)

      customdata0 = np.concatenate([np.array([j[1], j[1], None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress[i]]).tolist()
      customdata1 = np.concatenate([np.array([datereadjust(j[2]), datereadjust(j[2]), None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress[i]]).tolist()
      customdata2 = np.concatenate([np.array([j[0], j[0], j[0]]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress[i]]).tolist()
      customdata3 = np.concatenate([np.array([j[3], j[4], None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress[i]]).tolist()
      customdata4 = [name_legend[i%6]]*len(customdata0)

      if interest_floors_progress[i] != [[None, None]]:      
            custom_hover_text = ['Date Range: '+str(customdata0[i])+' to '+str(datereadjust6(customdata1[i]))+' <br>Cumulative Progress: '+str(np.round(customdata3[i], 2))+'% <br>Activity: '+customdata4[i] if i%3 == 0 
                                    else 'Date Range: '+str(customdata0[i])+' to '+str(datereadjust6(customdata1[i]))+'<br>Progress in period: '+
                                                           str(np.round(customdata2[i], 2))+'% <br>Cumulative Progress: '+str(np.round(customdata3[i], 2))+'% <br>Activity: '+customdata4[i] if i%3 == 1
                                                           else None for i in range(len(customdata0))]
      else:
            custom_hover_text = [None]*len(customdata0)

      dataactivities = pd.DataFrame({
            'x': np.concatenate([np.array([datetime.combine(j[1], Time), datereadjust(j[2]), None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress[i]]).tolist(),
            'y': np.concatenate([np.array([i%6+progress_gradients[i]*(datetime.combine(j[1], Time)-datetime.combine(interest_floors_progress[i][0][1], Time))/(datereadjust2(interest_floors_progress[i][-1][2])-datetime.combine(interest_floors_progress[i][0][1], Time)-timedelta(days = 1)), 
                                          i%6+progress_gradients[i]*(datereadjust2(j[2])-timedelta(days = 1)-datetime.combine(interest_floors_progress[i][0][1], Time))/(datereadjust2(interest_floors_progress[i][-1][2])-datetime.combine(interest_floors_progress[i][0][1], Time)-timedelta(days = 1)), None]) if j != [None, None] else np.array([None, None, None]) for j in interest_floors_progress[i]]).tolist(),
            'Color': np.concatenate([np.array([j[0], j[0], j[0]]) for j in interest_floors_progress[i]]).tolist(),
            'customdata': custom_hover_text
      })

      custom_hover_text = ['customdata']
      
      #Create color map for discrete sequence
      color_map = {} 

      for j in range(len(interest_floors_progress[i])):
            
            if interest_floors_progress[i] != [[None, None]]:
                  color_map.update({interest_floors_progress[i][j][0]: color_interpolation(custom_colorscale, interest_floors_progress[i][j][0])})
                  activitiesfig = px.line(dataactivities, x='x', y='y',
                  color = 'Color',
                  color_discrete_map=color_map,
                  labels={'x': 'Date', 'y': 'Activities'},
                  template = 'seaborn',
                  hover_data = custom_hover_text)

                  activitiesfig.update_traces(hovertemplate = '%{customdata[0]}')
            else:
                  activitiesfig = px.line(x=[None, None], y=[None, None])

      for i in range(len(activitiesfig.data)):
            activitiesfig.data[i].name = ''
            Activitiesfig.add_trace(activitiesfig.data[i])
      
      Activitiesfig.update_layout(showlegend = False)
      Activitiesfig.update_traces(line=dict(width=15))

      activitiesfigadditivesC.append(Activitiesfig)            

