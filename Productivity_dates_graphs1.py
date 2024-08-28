#!/usr/bin/env python
# coding: utf-8

# In[14]:


import nbformat
from nbconvert import PythonExporter

# Load the notebook
with open('/Users/juanfranciscolorussonotarofrancesco/Desktop/Progress Data Exports/Productivity_dates_graphs1.ipynb', encoding='utf-8') as f:
    notebook = nbformat.read(f, as_version=4)

# Create a PythonExporter
exporter = PythonExporter()

# Export the notebook to Python script
script, _ = exporter.from_notebook_node(notebook)

# Write the script to a file
with open('/Users/juanfranciscolorussonotarofrancesco/Desktop/Progress Data Exports/Productivity_dates_graphs1.py', 'w', encoding='utf-8') as f:
    f.write(script)


# In[2]:


#import Productivity_dates
#from Productivity_dates import figadditives, custom_colorscale, cladding_dates, flowlineactivitiesfig_layouts_datapoints, flowlineactivitiesfig_layouts, figadditivesprojection, name_legend, Flowlines1fig, southfloornamelen, timegap
#from Productivity_dates import figadditivessth, figadditivessthprojection, Flowlines1figsth
import numpy as np
import math
import pandas as pd


# In[3]:


import json
import plotly.graph_objs as go
import plotly.express as px

def json_file_to_list(filename):
    # Step 1: Open and read the JSON file
    with open(filename, 'r') as file:
        # Step 2: Load the content as a Python object (in this case, a list)
        data_list = json.load(file)
    
    # The data_list is now a Python list
    return data_list

def json_to_figure(filename):
    # Step 1: Open and read the JSON file
    with open(filename, 'r') as file:
        json_data = json.load(file)
    
    # Step 2: Convert the JSON data into a Plotly figure
    fig = go.Figure(json_data)
    
    # Step 3: Return the figure object
    return fig

def json_to_figures_list(filename):
    # Step 1: Open and read the JSON file
    with open(filename, 'r') as file:
        json_data = json.load(file)
    
    # Step 2: Convert each JSON object into a Plotly figure
    figures = [go.Figure(json.loads(fig_data)) for fig_data in json_data]
    
    # Step 3: Return the list of figures
    return figures

# Example usage
name_legend = json_file_to_list('namelegend.json')
custom_colorscale = json_file_to_list('customcolorscale.json')
southfloornamelen = json_file_to_list('southfloornamelen.json')
cladding_dates = json_file_to_list('claddingdates.json')
Flowlines1fig = json_to_figure('Flowlines1fig.json')
Flowlines1figsth = json_to_figure('Flowlines1figsth.json')
figadditives = json_to_figures_list('figadditives.json')
figadditivessth = json_to_figures_list('figadditivessth.json')
figadditivessthprojection = json_to_figures_list('figadditivessthprojection.json')
figadditivesprojection = json_to_figures_list('figadditivesprojection.json')


# In[4]:


import datetime
from datetime import date, timedelta, time

holidays = ['2025-01-01', '2024-12-26', '2024-12-25', '2024-08-26', '2024-05-27', '2024-05-06', '2024-04-01', '2024-03-29', '2024-01-01', '2023-12-26', '2023-12-25', 
 '2023-08-28', '2023-05-29', '2023-05-08', '2023-05-01', '2023-04-10', '2023-04-07', '2023-01-02', '2022-12-30', '2022-12-29', 
 '2022-12-28', '2022-12-27', '2022-12-26', '2022-12-23', '2022-12-22', '2022-12-21', '2022-12-20']

holidays = sorted([datetime.datetime.strptime(i, '%Y-%m-%d') for i in holidays])
offdays = holidays
for i in range((holidays[-1]-datetime.datetime(2022, 10, 31, 0, 0)).days+5):
    if (datetime.datetime(2022, 10, 31)+timedelta(days = i-5)).weekday() == 5:
        offdays.append(datetime.datetime(2022, 10, 31)+timedelta(days = i-5))
    if (datetime.datetime(2022, 10, 31)+timedelta(days = i-5)).weekday() == 6:
        offdays.append(datetime.datetime(2022, 10, 31)+timedelta(days = i-5))
offdays = [i.date() for i in sorted(offdays)]
offdaysranges = [offdays[0]]
for i in range(len(offdays)-1):

    if offdays[i]+timedelta(days = 1) != offdays[i+1]:
        offdaysranges.append(offdays[i])
        offdaysranges.append(offdays[i+1])


# In[5]:


format1 = "%Y-%m-%dT%H:%M:%S.%f"
format2 = "%Y-%m-%dT%H:%M:%S"

def timegap(Day1, Day2):
    i = 0
    if type(Day1) == str:
        try:
            Day1 = datetime.datetime.strptime(Day1, format1).date()
        except:
            Day1 = datetime.datetime.strptime(Day1, format2).date()
    if type(Day2) == str:
        try:
            Day2 = datetime.datetime.strptime(Day2, format1).date()
        except:
            Day2 = datetime.datetime.strptime(Day2, format2).date()

    Time_days = Day2 - Day1

    while Time_days != timedelta(days=0):

        Time_days = (Time_days-timedelta(days=1))
        i+=1

    return i


# In[15]:


import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_daq as daq
import os

lastdate = date(2023, 9, 29)
def dateconversion(x):
    if type(x) == datetime.date:
        return x
    else:
        return x.date()

def datetimeconversion(x):
    if type(x) == date:
        return datetime.datetime.combine(x, time(0, 0, 0))
    elif type(x) == str:
        try:
            x = datetime.datetime.strptime(x, format1)
            return x
        except:
            x = datetime.datetime.strptime(x, format2)
            return x
    else:
        return x
    
def MAXDATE(arr):
    return max(datetimeconversion(i) for i in arr if type(i)==datetime.datetime or type(i)==date or type(i)==str)

def mindate(arr):
    return min(datetimeconversion(i) for i in arr if type(i)==datetime.datetime or type(i)==date or type(i)==str)

app1 = dash.Dash(__name__)
server1 = app1.server

htmlbuttons = [html.Div(html.Span('Fit-out Activities', style = {'font-family': 'Arial, sans-serif', 'font-size': '20px', 'font-weight': 'bold', 'text-decoration': 'underline'}), style={'margin-bottom': '30px', 'margin-left': '20px'})]
htmlbuttons2 = []
input = []
output = []
outputchildren = []
colorset = [px.colors.qualitative.G10[i] for i in range(len(name_legend))]

for i in range(len(name_legend)+5):
    if i == 0:
        n_0 = 0
    else:
        n_0 = 1
    if i < len(name_legend):
        htmlbuttons.append(html.Button(name_legend[i], id='toggle-'+str(i+1)+'WP', n_clicks=n_0, style={'width': '100%', 'backgroundColor': 'white', 
                                                                                                     'color': 'black', 'margin-top': '3px', 'margin-bottom': '3px', 'border-width': '0'}))
        input.append(Input('toggle-'+str(i+1)+'WP', 'n_clicks'))
        output.append(Output('toggle-'+str(i+1)+'WP', 'style'))
        outputchildren.append(Output('toggle-'+str(i+1)+'WP', 'children'))
    elif i == len(name_legend):
        input.append(Input('toggle-planns', 'on'))
        output.append(Output('name-switch1', 'style'))
        outputchildren.append(Output('name-switch1', 'children'))
        htmlbuttons2.append(html.Tr([html.Td("On", id='name-switch1', style = {'font-family':'Arial, sans-serif', 'color': 'white', 'position': 'relative', 'right': '50px', 'bottom':'5px', 'backgroundColor':'green', 'padding-left': '10px', 'padding-right': '20px'}), 
                                     html.Td(daq.BooleanSwitch(id = 'toggle-planns', on = True, color = 'green', labelPosition = 'right', style={'transform': 'scale(1.5)', 'position': 'relative', 'left': '40px'})),  
                                     html.Td("Plans", id = 'title1', style = {'font-family':'Arial, sans-serif'})]))
    elif i == len(name_legend)+1:
        input.append(Input('toggle-actualns', 'on'))
        output.append(Output('name-switch2', 'style'))
        outputchildren.append(Output('name-switch2', 'children'))
        htmlbuttons2.append(html.Tr([html.Td("On", id='name-switch2', style = {'font-family':'Arial, sans-serif', 'color': 'white', 'position': 'relative', 'right': '50px', 'bottom':'5px', 'backgroundColor':'green', 'padding-left': '10px', 'padding-right': '20px'}), 
                                     html.Td(daq.BooleanSwitch(id = 'toggle-actualns', on = True, color = 'green', labelPosition = 'right', style={'transform': 'scale(1.5)', 'position': 'relative', 'left': '40px'})), 
                                     html.Td("Actuals", id = 'title2', style = {'font-family':'Arial, sans-serif'})], style={'position': 'relative', 'top': '20px'}))
    elif i == len(name_legend)+2:
        input.append(Input('toggle-flowlines', 'on'))
        output.append(Output('name-switch3', 'style'))
        outputchildren.append(Output('name-switch3', 'children'))
        htmlbuttons2.append(html.Tr([html.Td("On", id='name-switch3', style = {'font-family':'Arial, sans-serif', 'color': 'white', 'position': 'relative', 'right': '50px', 'bottom':'5px', 'backgroundColor':'green', 'padding-left': '10px', 'padding-right': '20px'}), 
                                     html.Td(daq.BooleanSwitch(id = 'toggle-flowlines', on = True, color = 'green', labelPosition = 'right', style={'transform': 'scale(1.5)', 'position': 'relative', 'left': '40px'})), 
                                     html.Td("Flowlines", id = 'title3', style = {'font-family':'Arial, sans-serif'})], style={'position': 'relative', 'top': '40px'}))
    elif i == len(name_legend)+3:
        input.append(Input('toggle-absentdaysns', 'on'))
        output.append(Output('name-switch4', 'style'))
        outputchildren.append(Output('name-switch4', 'children'))
        htmlbuttons2.append(html.Tr([html.Td("On", id='name-switch4', style = {'font-family':'Arial, sans-serif', 'color': 'white', 'position': 'relative', 'right': '50px', 'bottom':'5px', 'backgroundColor':'green', 'padding-left': '10px', 'padding-right': '20px'}), 
                                     html.Td(daq.BooleanSwitch(id = 'toggle-absentdaysns', on = True, color = 'green', labelPosition = 'right', style={'transform': 'scale(1.5)', 'position': 'relative', 'left': '40px'})), 
                                     html.Td("No progress", id = 'title4', style = {'font-family':'Arial, sans-serif'})], style={'position': 'relative', 'top': '60px'}))
    else: 
        input.append(Input('toggle-projectiondaysns', 'on'))
        output.append(Output('name-switch5', 'style'))
        outputchildren.append(Output('name-switch5', 'children'))
        htmlbuttons2.append(html.Tr([html.Td("On", id='name-switch5', style = {'font-family':'Arial, sans-serif', 'color': 'white', 'position': 'relative', 'right': '50px', 'bottom':'5px', 'backgroundColor':'green', 'padding-left': '10px', 'padding-right': '20px'}),
                                     html.Td(daq.BooleanSwitch(id = 'toggle-projectiondaysns', on = True, color = 'green', labelPosition = 'right', style={'transform': 'scale(1.5)', 'position': 'relative', 'left': '40px', 'display': 'none'})),
                                     html.Td("Projection", id = 'title5', style = {'font-family':'Arial, sans-serif'})], style={'position': 'relative', 'top': '80px'}))
    
app1.layout = html.Div([
    dcc.Graph(id='plot-outputns', style = {'width': '100%', 'height': '860px', 'backgroundColor': 'white', 'position': 'absolute'}),
    html.Div(htmlbuttons, 
             style={'width': '250px', 'display':'inline-block', 'align-items': 'center', 'vertical-align': 'top',
                    'verticalAlign': 'middle', 'left':'1435px', 'top':'60px', 'position': 'relative'}),
    html.Div(htmlbuttons2, 
             style={'display':'flex', 'flex-direction': 'column', 
                    'position': 'relative', 'top': '240px', 'left': '1410px'})], 
    style={'width': '1720px', 'background-color': 'white', 'height': '960px'})

@app1.callback(
        Output('toggle-flowlines', 'on'),
        [Input('toggle-actualns', 'on')]
)

def update_button_click(valueactual):
    
    return (
            False if valueactual == False else False
        )

@app1.callback(
        [Output('toggle-absentdaysns', 'on'),
         Output('toggle-projectiondaysns', 'on')],
        [Input('toggle-flowlines', 'on')]
)

def update_button_click(valueflowlines):
    
    return (
            False if valueflowlines == False else False,
            False if valueflowlines == False else False 
        )

@app1.callback(
    Output('plot-outputns', 'figure'),
    input)

def update_plot(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, valueplan, valueactual, valueflowlines, valueabsent, valueprojection):

    figs = px.line(template='seaborn', title='<b>Activities Progress WPs<b>')
    planfigs = px.line(template='seaborn')
    actualfigs = px.line(template='seaborn')
    planactualfigs = px.line(template='seaborn')
    workingdays = []
    nonworkingdays = []

    if n_1WP % 2 == 0:

        #Add shapes for projected days
        if valueprojection == True:
            for i in range(len(figadditivesprojection[0].data)):
                figs.add_trace(figadditivesprojection[0].data[i])
                #Add hover data for projection
                try:
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[0].data[i].x[1], figadditivesprojection[0].data[i].x[1]], 
                                               'y': [figadditivesprojection[0].data[i].y[1], figadditivesprojection[0].data[i].y[1]], 
                                               'customdata0': [datetime.datetime.strptime(figadditivesprojection[0].data[i].x[1], format1).date(), datetime.datetime.strptime(figadditivesprojection[0].data[i].x[1], format1).date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[0].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[0].data[i].y[1])))]})
                except:
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[0].data[i].x[1], figadditivesprojection[0].data[i].x[1]], 
                                               'y': [figadditivesprojection[0].data[i].y[1], figadditivesprojection[0].data[i].y[1]], 
                                               'customdata0': [datetime.datetime.strptime(figadditivesprojection[0].data[i].x[1], format2).date(), datetime.datetime.strptime(figadditivesprojection[0].data[i].x[1], format2).date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[0].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[0].data[i].y[1])))]})
                Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Level: %{customdata[1]}')
                figs.add_traces(Fadd.data[0])
        
        #Add planned flowlines
        planfigs.add_trace(Flowlines1fig.data[0])
        actualfigs.add_trace(Flowlines1fig.data[6])
        
        #Add progress flowlines
        for i in range(len(figadditives[0].data)):
            figadditives[0].data[i].name = ''
            figadditives[0].data[i].visible = True
            figs.add_trace(figadditives[0].data[i])
            if i <= 0:
                    pass
            else:
                for j in range(len(figadditives[0].data[i].x)//3):
                    for k in range(timegap(figadditives[0].data[i].x[3*j], figadditives[0].data[i].x[3*j+1])+1):
                        workingdays.append(datetime.datetime.strptime(figadditives[0].data[i].x[3*j], format2).date()+timedelta(days = k))

        for i in figadditives[0].layout.shapes:
            figs.add_shape(i)

    if n_2WP % 2 == 0:

        #Add shapes for projected days
        if valueprojection == True:
            for i in range(len(figadditivesprojection[1].data)):
                figs.add_trace(figadditivesprojection[1].data[i])
                #Add hover data for projection
                try:
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[1].data[i].x[1], figadditivesprojection[1].data[i].x[1]], 
                                               'y': [figadditivesprojection[1].data[i].y[1], figadditivesprojection[1].data[i].y[1]], 
                                               'customdata0': [datetime.datetime.strptime(figadditivesprojection[1].data[i].x[1], format1).date(), datetime.datetime.strptime(figadditivesprojection[1].data[i].x[1], format1).date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[1].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[1].data[i].y[1])))]})
                except:
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[1].data[i].x[1], figadditivesprojection[1].data[i].x[1]], 
                                               'y': [figadditivesprojection[1].data[i].y[1], figadditivesprojection[1].data[i].y[1]], 
                                               'customdata0': [datetime.datetime.strptime(figadditivesprojection[1].data[i].x[1], format2).date(), datetime.datetime.strptime(figadditivesprojection[1].data[i].x[1], format2).date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[1].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[1].data[i].y[1])))]})
                Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Level: %{customdata[1]}')
                figs.add_traces(Fadd.data[0])

        #Add planned and actual flowlines
        planfigs.add_trace(Flowlines1fig.data[1])
        actualfigs.add_trace(Flowlines1fig.data[7])
        
        #Add progress flowlines
        for i in range(len(figadditives[1].data)):
            figadditives[1].data[i].name = ''
            figadditives[1].data[i].visible = True
            figs.add_trace(figadditives[1].data[i])
            if i <= 0:
                    pass
            else:
                for j in range(len(figadditives[1].data[i].x)//3):
                    for k in range(timegap(figadditives[1].data[i].x[3*j], figadditives[1].data[i].x[3*j+1])+1):
                        workingdays.append(datetime.datetime.strptime(figadditives[1].data[i].x[3*j], format2).date()+timedelta(days = k))
        
        for i in figadditives[1].layout.shapes:
            figs.add_shape(i)

    if n_3WP % 2 == 0:

        #Add shapes for projected days
        if valueprojection == True:
            for i in range(len(figadditivesprojection[2].data)):
                figs.add_trace(figadditivesprojection[2].data[i])
                #Add hover data for projection
                try:
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[2].data[i].x[1], figadditivesprojection[2].data[i].x[1]], 
                                               'y': [figadditivesprojection[2].data[i].y[1], figadditivesprojection[2].data[i].y[1]], 
                                               'customdata0': [datetime.datetime.strptime(figadditivesprojection[2].data[i].x[1], format1).date(), datetime.datetime.strptime(figadditivesprojection[2].data[i].x[1], format1).date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[2].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[2].data[i].y[1])))]})
                except:
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[2].data[i].x[1], figadditivesprojection[2].data[i].x[1]], 
                                               'y': [figadditivesprojection[2].data[i].y[1], figadditivesprojection[2].data[i].y[1]], 
                                               'customdata0': [datetime.datetime.strptime(figadditivesprojection[2].data[i].x[1], format2).date(), datetime.datetime.strptime(figadditivesprojection[2].data[i].x[1], format2).date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[2].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[2].data[i].y[1])))]})
                Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Level: %{customdata[1]}')
                figs.add_traces(Fadd.data[0])

        #Add planned flowlines
        planfigs.add_trace(Flowlines1fig.data[2])
        actualfigs.add_trace(Flowlines1fig.data[8])
        
        #Add progress flowlines
        for i in range(len(figadditives[2].data)):
            figadditives[2].data[i].name = ''
            figadditives[2].data[i].visible = True
            figs.add_trace(figadditives[2].data[i])
            if i <= 0:
                    pass
            else:
                for j in range(len(figadditives[2].data[i].x)//3):
                    for k in range(timegap(figadditives[2].data[i].x[3*j], figadditives[2].data[i].x[3*j+1])+1):
                        workingdays.append(datetime.datetime.strptime(figadditives[2].data[i].x[3*j], format2).date()+timedelta(days = k))

        for i in figadditives[2].layout.shapes:
            figs.add_shape(i)

    if n_4WP % 2 == 0:

        #Add shapes for projected days
        if valueprojection == True:
            for i in range(len(figadditivesprojection[3].data)):
                figs.add_trace(figadditivesprojection[3].data[i])
                #Add hover data for projection
                try:
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[3].data[i].x[1], figadditivesprojection[3].data[i].x[1]], 
                                               'y': [figadditivesprojection[3].data[i].y[1], figadditivesprojection[3].data[i].y[1]], 
                                               'customdata0': [datetime.datetime.strptime(figadditivesprojection[3].data[i].x[1], format1).date(), datetime.datetime.strptime(figadditivesprojection[3].data[i].x[1], format1).date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[3].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[3].data[i].y[1])))]})
                except:
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[3].data[i].x[1], figadditivesprojection[3].data[i].x[1]], 
                                               'y': [figadditivesprojection[3].data[i].y[1], figadditivesprojection[3].data[i].y[1]], 
                                               'customdata0': [datetime.datetime.strptime(figadditivesprojection[3].data[i].x[1], format2).date(), datetime.datetime.strptime(figadditivesprojection[3].data[i].x[1], format2).date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[3].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[3].data[i].y[1])))]})
                Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Level: %{customdata[1]}')
                figs.add_traces(Fadd.data[0])

        #Add planned flowlines
        planfigs.add_trace(Flowlines1fig.data[3])
        actualfigs.add_trace(Flowlines1fig.data[9])
        
        #Add progress flowlines
        for i in range(len(figadditives[3].data)):
            figadditives[3].data[i].name = ''
            figadditives[3].data[i].visible = True
            figs.add_trace(figadditives[3].data[i])
            if i <= 0:
                    pass
            else:
                for j in range(len(figadditives[3].data[i].x)//3):
                    for k in range(timegap(figadditives[3].data[i].x[3*j], figadditives[3].data[i].x[3*j+1])+1):
                        workingdays.append(datetime.datetime.strptime(figadditives[3].data[i].x[3*j], format2).date()+timedelta(days = k))
        
        for i in figadditives[3].layout.shapes:
            figs.add_shape(i)

    if n_5WP % 2 == 0:

        #Add shapes for projected days
        if valueprojection == True:
            for i in range(len(figadditivesprojection[4].data)):
                figs.add_trace(figadditivesprojection[4].data[i])
                #Add hover data for projection
                try:
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[4].data[i].x[1], figadditivesprojection[4].data[i].x[1]], 
                                               'y': [figadditivesprojection[4].data[i].y[1], figadditivesprojection[4].data[i].y[1]], 
                                               'customdata0': [datetime.datetime.strptime(figadditivesprojection[4].data[i].x[1], format1).date(), datetime.datetime.strptime(figadditivesprojection[4].data[i].x[1], format1).date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[4].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[4].data[i].y[1])))]})
                except:
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[4].data[i].x[1], figadditivesprojection[4].data[i].x[1]], 
                                               'y': [figadditivesprojection[4].data[i].y[1], figadditivesprojection[4].data[i].y[1]], 
                                               'customdata0': [datetime.datetime.strptime(figadditivesprojection[4].data[i].x[1], format2).date(), datetime.datetime.strptime(figadditivesprojection[4].data[i].x[1], format2).date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[4].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[4].data[i].y[1])))]})
                Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Level: %{customdata[1]}')
                figs.add_traces(Fadd.data[0])

        #Add planned flowlines
        planfigs.add_trace(Flowlines1fig.data[4])
        actualfigs.add_trace(Flowlines1fig.data[10])
        
        #Add progress flowlines
        for i in range(len(figadditives[4].data)):
            figadditives[4].data[i].name = ''
            figadditives[4].data[i].visible = True
            figs.add_trace(figadditives[4].data[i])
            if i <= 0:
                    pass
            else:
                for j in range(len(figadditives[4].data[i].x)//3):
                    for k in range(timegap(figadditives[4].data[i].x[3*j], figadditives[4].data[i].x[3*j+1])+1):
                        workingdays.append(datetime.datetime.strptime(figadditives[4].data[i].x[3*j], format2).date()+timedelta(days = k))
        
        for i in figadditives[4].layout.shapes:
            figs.add_shape(i)

    if n_6WP % 2 == 0:

        #Add shapes for projected days
        if valueprojection == True:
            for i in range(len(figadditivesprojection[5].data)):
                figs.add_trace(figadditivesprojection[5].data[i])
                #Add hover data for projection
                try:
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[5].data[i].x[1], figadditivesprojection[5].data[i].x[1]], 
                                               'y': [figadditivesprojection[5].data[i].y[1], figadditivesprojection[5].data[i].y[1]], 
                                               'customdata0': [datetime.datetime.strptime(figadditivesprojection[5].data[i].x[1], format1).date(), datetime.datetime.strptime(figadditivesprojection[5].data[i].x[1], format1).date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[5].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[5].data[i].y[1])))]})
                except:
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[5].data[i].x[1], figadditivesprojection[5].data[i].x[1]], 
                                               'y': [figadditivesprojection[5].data[i].y[1], figadditivesprojection[5].data[i].y[1]], 
                                               'customdata0': [datetime.datetime.strptime(figadditivesprojection[5].data[i].x[1], format2).date(), datetime.datetime.strptime(figadditivesprojection[5].data[i].x[1], format2).date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[5].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[5].data[i].y[1])))]})
                Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Level: %{customdata[1]}')
                figs.add_traces(Fadd.data[0])

        #Add planned flowlines
        planfigs.add_trace(Flowlines1fig.data[5])
        actualfigs.add_trace(Flowlines1fig.data[11])
        
        #Add progress flowlines
        for i in range(len(figadditives[5].data)):
            figadditives[5].data[i].name = ''
            figadditives[5].data[i].visible = True
            figs.add_trace(figadditives[5].data[i])
            if i <= 0:
                    pass
            else:
                for j in range(len(figadditives[5].data[i].x)//3):
                    for k in range(timegap(figadditives[5].data[i].x[3*j], figadditives[5].data[i].x[3*j+1])+1):
                        workingdays.append(datetime.datetime.strptime(figadditives[5].data[i].x[3*j], format2).date()+timedelta(days = k))
        
        for i in figadditives[5].layout.shapes:
            figs.add_shape(i)
    
    if n_1WP % 2 != 0 and n_2WP % 2 != 0 and n_3WP % 2 != 0 and n_4WP % 2 != 0 and n_5WP % 2 != 0 and n_6WP % 2 != 0:

        raise PreventUpdate
    
    figs.update_layout(showlegend = False)

    #Creating the colorscale
    figs.add_trace(px.scatter(x=[None, None, None], y=[None, None, None], 
                         color=[0, custom_colorscale[1][0], custom_colorscale[2][0]], 
                         range_color = [0, custom_colorscale[2][0]]).data[0])
    #Update size of plot
    figs.update_layout(height=560, width=950)
    #Thicken the lines to seem as 'bars'
    figs.update_traces(line=dict(width=5))
    figs.update_layout(xaxis_title="<b>Date<b>", yaxis_title="<b>Floor<b>")
    #Ticks for yaxis
    figs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2]+1)], 
                               ticktext = ['L' + str(i) for i in range(cladding_dates[1][1][-2]+1)]))
    height = 860
    pixsize = 35
    width  = 1403
    
    #Add tablelike shapes for the yaxis
    figs.add_shape(type="rect",
              x0=-2*(pixsize/2300), x1=0,
              y0=0, y1=1,
              xref='paper', yref='paper',
              line=dict(color="#ffffff", width=1.5),
              fillcolor = '#eaeaf2',
              opacity = 1)
    
    for i in range(1, cladding_dates[1][1][-2]+1):
    # Add horizontal line to the margin
        figs.add_shape(type="line",
              x0=-2*(pixsize/2300), x1=0,
              y0=i-1, y1=i-1,
              xref='paper', yref='y',
              line=dict(color="#ffffff", width=1.5),
              opacity = 1)
    # Add annotation to the margin
        if i < cladding_dates[1][1][-2]:
            figs.add_annotation(
            text='<b>L'+str(i)+'<b>',
            x=-2*(pixsize/2300),
            y=i-1/2,
            xref='paper', yref='y',
            font=dict(size=12),
            showarrow = False )
    
    #Copy layout from original plot
    planfigs.layout = figs.layout
    actualfigs.layout = figs.layout
    planactualfigs.layout = figs.layout

    #State condition whether activities were finished in the lapse
    if False in [int(i) == round(i, 5) for i in np.concatenate([i.y for i in figs.data if i.line.color == 'black']) if i!= None]:
        finished = False
    else:
        finished = True
    
    for i in range(timegap(min(workingdays), max(workingdays))):
        if min(workingdays)+timedelta(days=i) not in workingdays and min(workingdays)+timedelta(days=i) not in offdays:
            nonworkingdays.append(min(workingdays)+timedelta(days=i))
    #Add last set of nonworking days
    if finished == False and sorted(list(set(workingdays)))[-1]+timedelta(days=1) < lastdate:
        for i in range(timegap(sorted(list(set(workingdays)))[-1]+timedelta(days=1), lastdate)):
            if sorted(list(set(workingdays)))[-1]+timedelta(days=1)+timedelta(days=i) not in offdays:
                nonworkingdays.append(sorted(list(set(workingdays)))[-1]+timedelta(days=1)+timedelta(days=i))

    nonworkingdaysranges = [nonworkingdays[0]]
    
    for i in range(len(nonworkingdays)-1):
        if nonworkingdays[i]+timedelta(days=1) != nonworkingdays[i+1]:
            nonworkingdaysranges.append(nonworkingdays[i]+timedelta(days=1))
            nonworkingdaysranges.append(nonworkingdays[i+1])
    nonworkingdaysranges.append(nonworkingdays[-1]+timedelta(days=1))

    #Add dashed line for last measurement and annotation
    if valueprojection == True and finished == False:
        figs.add_shape(type="line",
                                x0=lastdate, x1=lastdate,
                                y0=0, y1=1,
                                xref='x', yref='paper',
                                line=dict(color="black", width=1.5, dash = 'dash'),
                                opacity = 1)
        figs.add_annotation(text='Last measurement:<br>2023-9-28',
                                x=date(2023, 9, 29),
                                ax = -55,
                                align = 'left',
                                ay = 0,
                                y=13.4,
                                axref = 'pixel',
                                ayref = 'pixel',
                                xref='x', yref='y',
                                font=dict(size=10),
                                showarrow = True,
                                arrowcolor = 'rgba(0,0,0,0)')

    #Add shapes for absent days
    if valueabsent == True:
        for i in range(len(nonworkingdaysranges)//2):
            figs.add_shape(type="rect",
              x0=nonworkingdaysranges[2*i], x1=nonworkingdaysranges[2*i+1],
              y0=0, y1=1,
              xref='x', yref='paper',
              line=dict(color="black", width=1.5),
              fillcolor = 'black',
              opacity = 0.15)

    figs.update_layout(showlegend = False)

    #Update size of plot
    figs.update_layout(height=height, width=width)
    #Thicken the lines to seem as 'bars'
    figs.update_traces(line=dict(width=15))
    # Update colorbar title and scale
    figs.update_coloraxes(colorbar_title='<b>Percentage of<br>Progress (%)<br> <br><b>', colorscale = [[0, 'rgb(255,0,0)'], [custom_colorscale[1][0]/custom_colorscale[2][0], 'rgb(255,212,0)'], [1, 'rgb(52,235,0)']],
                              colorbar_tickmode = 'array', colorbar_ticktext = ['0', '5', '10', '15', '20', '25', '30+'], colorbar_tickvals = [0, 5, 10, 15, 20, 25, 30],
                              colorbar_ticks = 'outside', colorbar_tickwidth = 2, colorbar_ticklen = 8)

    figs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2])], ticktext = ['']*cladding_dates[1][1][-2], range = [-0.7, 13.7], title_standoff = 50))
    
    if valueactual == False and valueplan == True:

        planfigs.update_layout(showlegend = False)
        #Update size of plot
        planfigs.update_layout(height=height, width=width)
        #Use extra data to ensure that xaxis range is fixed
        planfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2])], ticktext = ['']*cladding_dates[1][1][-2], range = [-0.7, 13.7], title_standoff = 50),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), lastdate+timedelta(days=5)]))
        #Add weekends and holidays
        for Days in range(0, len(offdaysranges)-1, 2):
            if datetimeconversion(offdaysranges[Days])>=datetime.datetime(2022, 10, 31, 0, 0)-timedelta(days=5) and datetimeconversion(offdaysranges[Days+1]) < datetimeconversion(maxrange)+timedelta(days=5):
                planfigs.add_shape(type = 'rect', x0 = datetimeconversion(offdaysranges[Days]), x1 = datetimeconversion(offdaysranges[Days+1])+timedelta(days=1), y0 = 0, y1 = 1, xref = 'x', yref = 'paper', line=dict(color="rgba(0, 0, 0, 0)", width=1.5), fillcolor = '#6d6b15', opacity = 0.25, layer = 'below')
        planfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out - North Building (Plan)<b>', font = dict(size = 25)))
        toprightfigs = px.line(x = [lastdate+timedelta(days=5), lastdate+timedelta(days=5)], y = [13, 13])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        planfigs.add_traces(toprightfigs.data[0])
        planfigs.add_traces(bottomleftfigs.data[0])
        return planfigs
    
    elif valueactual == True and valueplan == True and valueflowlines == False:
        for i in range(len(planfigs.data)):
            planactualfigs.add_trace(planfigs.data[i])
        for i in range(len(actualfigs.data)):
            planactualfigs.add_trace(actualfigs.data[i])
        planactualfigs.update_layout(showlegend = False)
        #Update size of plot
        planactualfigs.update_layout(height=height, width=width)
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in planactualfigs.data]) if type(i) == str])
        planactualfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2])], ticktext = ['']*cladding_dates[1][1][-2], range = [-0.7, 13.7], title_standoff = 50),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=5)]))
        #Add weekends and holidays
        for Days in range(0, len(offdaysranges)-1, 2):
            if datetimeconversion(offdaysranges[Days])>=datetime.datetime(2022, 10, 31, 0, 0)-timedelta(days=5) and datetimeconversion(offdaysranges[Days+1]) < datetimeconversion(maxrange)+timedelta(days=5):
                planactualfigs.add_shape(type = 'rect', x0 = datetimeconversion(offdaysranges[Days]), x1 = datetimeconversion(offdaysranges[Days+1])+timedelta(days=1), y0 = 0, y1 = 1, xref = 'x', yref = 'paper', line=dict(color="rgba(0, 0, 0, 0)", width=1.5), fillcolor = '#6d6b15', opacity = 0.25, layer = 'below')
        planactualfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out - North Building (Plan v Actual)<b>', font = dict(size = 25)))
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [13, 13])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        planactualfigs.add_traces(toprightfigs.data[0])
        planactualfigs.add_traces(bottomleftfigs.data[0])
        return planactualfigs
        
    elif valueactual == True and valueplan == True and valueflowlines == True:

        for i in range(len(planfigs.data)):
            figs.add_trace(planfigs.data[i])
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - North Building (Plan v Actual)<b>', font = dict(size = 25)))
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in figs.data]) if type(i) == str])
        #In the case the furthest point is a shaded rectangle
        if [dateconversion(i.x1) for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black'] != []:
            if max([dateconversion(i.x1) for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black']) > dateconversion(maxrange):
                maxrange = max([dateconversion(i.x1) for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black']) 
        #Add weekends and holidays
        for Days in range(0, len(offdaysranges)-1, 2):
            if datetimeconversion(offdaysranges[Days])>=datetime.datetime(2022, 10, 31, 0, 0)-timedelta(days=5) and datetimeconversion(offdaysranges[Days+1]) < datetimeconversion(maxrange)+timedelta(days=5):
                figs.add_shape(type = 'rect', x0 = datetimeconversion(offdaysranges[Days]), x1 = datetimeconversion(offdaysranges[Days+1])+timedelta(days=1), y0 = 0, y1 = 1, xref = 'x', yref = 'paper', line=dict(color="rgba(0, 0, 0, 0)", width=1.5), fillcolor = '#6d6b15', opacity = 0.25, layer = 'below')
        #Add text regarding percentage of days without progress
        if valueabsent == True and len(workingdays) != 0:
            if finished:
                Maxdate = maxrange
            else:
                Maxdate = lastdate
            
            #Calculate ratio by summing the ranges of the shaded rectangles
            nonholidayweekdays = 0
            for i in range((MAXDATE(np.concatenate([i.x for i in figs.data if i.line.dash == 'solid' and i.line.color != 'black']))-mindate(np.concatenate([i.x for i in figs.data if i.line.dash == 'solid' and i.line.color != 'black']))).days):
                if mindate(np.concatenate([i.x for i in figs.data]))+timedelta(days=i) not in offdays:
                    nonholidayweekdays += 1 
            nonworkingratio = sum([(i.x1-i.x0).days for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black'])/nonholidayweekdays
            figs.add_annotation(x = 0, y = 13.25, text = 'Percentage of days with no progress: '+str(round(100*nonworkingratio))+'%', xref = 'paper', yref = 'y', showarrow = False, font = dict(size = 15))
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [13, 13])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        figs.add_traces(toprightfigs.data[0])
        figs.add_traces(bottomleftfigs.data[0])
        return figs
    
    elif valueactual == True and valueplan == False and valueflowlines == False:

        actualfigs.update_layout(showlegend = False)
        #Update size of plot
        actualfigs.update_layout(height=height, width=width)
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in actualfigs.data]) if type(i) == str])
        actualfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2])], ticktext = ['']*cladding_dates[1][1][-2], range = [-0.7, 13.7], title_standoff = 50),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=5)]))
        #Add weekends and holidays
        for Days in range(0, len(offdaysranges)-1, 2):
            if datetimeconversion(offdaysranges[Days])>=datetime.datetime(2022, 10, 31, 0, 0)-timedelta(days=5) and datetimeconversion(offdaysranges[Days+1]) < maxrange+timedelta(days=5):
                actualfigs.add_shape(type = 'rect', x0 = datetimeconversion(offdaysranges[Days]), x1 = datetimeconversion(offdaysranges[Days+1])+timedelta(days=1), y0 = 0, y1 = 1, xref = 'x', yref = 'paper', line=dict(color="rgba(0, 0, 0, 0)", width=1.5), fillcolor = '#6d6b15', opacity = 0.25, layer = 'below')
        actualfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out - North Building (Actual)<b>', font = dict(size = 25)))
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [13, 13])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        actualfigs.add_traces(toprightfigs.data[0])
        actualfigs.add_traces(bottomleftfigs.data[0])
        return actualfigs

    elif valueactual == True and valueplan == False and valueflowlines == True:
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - North Building (Actual)<b>', font = dict(size = 25)))
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in figs.data]) if type(i) == str])
        #In the case the furthest point is a shaded rectangle
        if [dateconversion(i.x1) for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black'] != []:
            if max([dateconversion(i.x1) for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black']) > dateconversion(maxrange):
                maxrange = max([dateconversion(i.x1) for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black']) 
        #Add weekends and holidays
        for Days in range(0, len(offdaysranges)-1, 2):
            if datetimeconversion(offdaysranges[Days])>=datetime.datetime(2022, 10, 31, 0, 0)-timedelta(days=5) and datetimeconversion(offdaysranges[Days+1]) < datetimeconversion(maxrange)+timedelta(days=5):
                figs.add_shape(type = 'rect', x0 = datetimeconversion(offdaysranges[Days]), x1 = datetimeconversion(offdaysranges[Days+1])+timedelta(days=1), y0 = 0, y1 = 1, xref = 'x', yref = 'paper', line=dict(color="rgba(0, 0, 0, 0)", width=1.5), fillcolor = '#6d6b15', opacity = 0.25, layer = 'below')
        #Add text regarding percentage of days without progress
        if valueabsent == True and len(workingdays) != 0:
            if finished:
                Maxdate = maxrange
            else:
                Maxdate = lastdate
            
            #Calculate ratio by summing the ranges of the shaded rectangles
            nonholidayweekdays = 0
            for i in range((MAXDATE(np.concatenate([i.x for i in figs.data if i.line.dash == 'solid' and i.line.color != 'black']))-mindate(np.concatenate([i.x for i in figs.data if i.line.dash == 'solid' and i.line.color != 'black']))).days):
                if mindate(np.concatenate([i.x for i in figs.data]))+timedelta(days=i) not in offdays:
                    nonholidayweekdays += 1 
            nonworkingratio = sum([(i.x1-i.x0).days for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black'])/nonholidayweekdays
            figs.add_annotation(x = 0, y = 13.25, text = 'Percentage of days with no progress: '+str(round(100*nonworkingratio))+'%', xref = 'paper', yref = 'y', showarrow = False, font = dict(size = 15))
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [13, 13])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        figs.add_traces(toprightfigs.data[0])
        figs.add_traces(bottomleftfigs.data[0])
        return figs
    
    else:
        raise PreventUpdate
    
@app1.callback(
    output,
    input
)
def update_button_style(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, valueplan, valueactual, valueflowlines, valueabsent, valueprojection):
    # Default style for buttons
    default_style = {'width': '100%', 'backgroundColor': 'white', 'color': 'black', 'margin-bottom':'5px', 'margin-bottom':'5px', 'height': '30px', 'border-radius': '10px', 'text-align': 'left', 'border-width': '0'}
    active_style = default_style.copy()
    default_style['color'] = 'black'
    active_style['color'] = '#aaa'
    default_style0 = {'font-family':'Arial, sans-serif', 'backgroundColor': 'green', 'color': 'white', 'height': '38px', 'border-radius': '19px', 'margin-top': '0px', 'width': '100px', 'border-width': '0', 'position': 'relative', 'left': '30px', 'bottom': '5px', 'text-align': 'left', 'padding-left': '15px'}
    active_style0 = {'font-family':'Arial, sans-serif', 'backgroundColor': '#e6e6e6', 'color': 'white', 'height': '38px', 'border-radius': '19px', 'margin-top': '0px', 'width': '100px', 'border-width': '0', 'position': 'relative', 'left': '30px', 'bottom': '5px', 'text-align': 'right', 'padding-right': '15px'}
    default_style1 = {'font-family':'Arial, sans-serif', 'backgroundColor': 'green', 'color': 'white', 'height': '38px', 'border-radius': '19px', 'margin-top': '10px', 'width': '100px', 'border-width': '0', 'position': 'relative', 'left': '30px', 'bottom': '5px', 'text-align': 'left', 'padding-left': '15px'}
    active_style1 = {'font-family':'Arial, sans-serif', 'backgroundColor': '#e6e6e6', 'color': 'white', 'height': '38px', 'border-radius': '19px', 'margin-top': '10px', 'width': '100px', 'border-width': '0', 'position': 'relative', 'left': '30px', 'bottom': '5px', 'text-align': 'right', 'padding-right': '15px'}
    if valueactual == False:
        default_style1['display'] = 'None'
        active_style1['display'] = 'None'
    default_style2 = {'font-family':'Arial, sans-serif', 'backgroundColor': 'green', 'color': 'white', 'height': '38px', 'border-radius': '19px', 'margin-top': '10px', 'width': '100px', 'border-width': '0', 'position': 'relative', 'left': '30px', 'bottom': '5px', 'text-align': 'left', 'padding-left': '15px'}
    active_style2 = {'font-family':'Arial, sans-serif', 'backgroundColor': '#e6e6e6', 'color': 'white', 'height': '38px', 'border-radius': '19px', 'margin-top': '10px', 'width': '100px', 'border-width': '0', 'position': 'relative', 'left': '30px', 'bottom': '5px', 'text-align': 'right', 'padding-right': '15px'}
    if valueactual == False or valueflowlines == False:
        default_style2['display'] = 'None'
        active_style2['display'] = 'None'

    return (
        default_style if n_1WP % 2 == 0 else active_style,
        default_style if n_2WP % 2 == 0 else active_style,
        default_style if n_3WP % 2 == 0 else active_style,
        default_style if n_4WP % 2 == 0 else active_style,
        default_style if n_5WP % 2 == 0 else active_style,
        default_style if n_6WP % 2 == 0 else active_style,
        default_style0 if valueplan == True else active_style0,
        default_style0 if valueactual == True else active_style0,
        default_style1 if valueflowlines == True else active_style1,
        default_style2 if valueabsent == True else active_style2,
        default_style2 if valueprojection == True else active_style2
    )

@app1.callback(
    [Output('toggle-planns', 'style'),
     Output('toggle-actualns', 'style'),
     Output('toggle-flowlines', 'style'),
     Output('toggle-absentdaysns', 'style'),
     Output('toggle-projectiondaysns', 'style')],
    [Input('toggle-planns', 'on'),
     Input('toggle-actualns', 'on'),
     Input('toggle-flowlines', 'on'),
     Input('toggle-absentdaysns', 'on'),
     Input('toggle-projectiondaysns', 'on')]
)

def update_button_style(valueplan, valueactual, valueflowlines, valueabsent, valueprojection):
    # Default style for buttons
    default_style = {'transform': 'scale(1.4)', 'position': 'relative', 'right': '32px'}
    active_style = {'transform': 'scale(1.4)', 'position': 'relative', 'right': '80px'}
    default_style1 = {'transform': 'scale(1.4)', 'position': 'relative', 'right': '32px'}
    active_style1 = {'transform': 'scale(1.4)', 'position': 'relative', 'right': '80px'}
    default_style2 = {'transform': 'scale(1.4)', 'position': 'relative', 'right': '32px'}
    active_style2 = {'transform': 'scale(1.4)', 'position': 'relative', 'right': '80px'}
    if valueactual == False:
        default_style1 = {'opacity': '0'}
        active_style1 = {'opacity': '0'}
        default_style2 = {'opacity': '0'}
        active_style2 = {'opacity': '0'}
    if valueflowlines == False:
        default_style2 = {'opacity': '0'}
        active_style2 = {'opacity': '0'}

    return (
        default_style if valueplan == True else active_style,
        default_style if valueactual == True else active_style,
        default_style1 if valueflowlines == True else active_style1,
        default_style2 if valueabsent == True else active_style2,
        default_style2 if valueprojection == True else active_style2
    )

@app1.callback(
    [Output('title1', 'style'),
     Output('title2', 'style'),
     Output('title3', 'style'),
     Output('title4', 'style'),
     Output('title5', 'style')],
    [Input('toggle-planns', 'on'),
     Input('toggle-actualns', 'on'),
     Input('toggle-flowlines', 'on'),
     Input('toggle-absentdaysns', 'on'),
     Input('toggle-projectiondaysns', 'on')]
)

def update_button_style(valueplan, valueactual, valueflowlines, valueabsent, valueprojection):
    # Default style for buttons
    default_style = {'font-family':'Arial, sans-serif', 'position': 'relative', 'right': '12px', 'bottom': '5px'}
    active_style = {'font-family':'Arial, sans-serif', 'position': 'relative', 'right': '12px', 'bottom': '5px'}
    default_style1 = {'font-family':'Arial, sans-serif', 'position': 'relative', 'right': '12px', 'bottom': '5px'}
    active_style1 = {'font-family':'Arial, sans-serif', 'position': 'relative', 'right': '12px', 'bottom': '5px'}
    default_style2 = {'font-family':'Arial, sans-serif', 'position': 'relative', 'right': '12px', 'bottom': '5px'}
    active_style2 = {'font-family':'Arial, sans-serif', 'position': 'relative', 'right': '12px', 'bottom': '5px'}
    if valueactual == False:
        default_style1 = {'opacity': '0'}
        active_style1 = {'opacity': '0'}
        default_style2 = {'opacity': '0'}
        active_style2 = {'opacity': '0'}
    if valueflowlines == False:
        default_style2 = {'opacity': '0'}
        active_style2 = {'opacity': '0'}

    return (
        default_style if valueplan == True else active_style,
        default_style if valueactual == True else active_style,
        default_style1 if valueflowlines == True else active_style1,
        default_style2 if valueabsent == True else active_style2,
        default_style2 if valueprojection == True else active_style2
    )

@app1.callback(
    outputchildren,
    input
)
def update_button_children(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, valueplan, valueactual, valueflowlines, valueabsent, valueprojection):
    on = []
    off = []
    # Change button style
    for i in range(len(name_legend)):
        on.append(html.Div([html.Hr(style={'height': '15px', 'width': '15px', 'border-color': colorset[i], 'background-color': colorset[i], 'border-width': 'medium', 'margin-right': '12px'}), name_legend[i]], 
                           style={'display': 'flex', 'display-direction': 'row', 'float': 'left', 'align-items': 'center'}))
        off.append(html.Div([html.Hr(style={'height': '15px', 'width': '15px', 'border-color': colorset[i], 'background-color': 'white', 'border-width': 'medium', 'margin-right': '12px'}), name_legend[i]], 
                            style={'display': 'flex', 'display-direction': 'row', 'float': 'left', 'align-items': 'center'}))

    return (
        on[0] if n_1WP % 2 == 0 else off[0],
        on[1] if n_2WP % 2 == 0 else off[1],
        on[2] if n_3WP % 2 == 0 else off[2],
        on[3] if n_4WP % 2 == 0 else off[3],
        on[4] if n_5WP % 2 == 0 else off[4],
        on[5] if n_6WP % 2 == 0 else off[5],
        'On' if valueplan == True else 'Off',
        'On' if valueactual == True else 'Off',
        'On' if valueflowlines == True else 'Off',
        'On' if valueabsent == True else 'Off',
        'On' if valueprojection == True else 'Off'
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000)) 
    app1.run_server(debug=True, port=port)


# In[7]:


app2 = dash.Dash(__name__)

htmlbuttons = [html.Div(html.Span('Fit-out Activities', style = {'font-family': 'Arial, sans-serif', 'font-size': '20px', 'font-weight': 'bold', 'text-decoration': 'underline'}), style={'margin-bottom': '30px', 'margin-left': '20px'})]
htmlbuttons2 = []
input = []
output = []
outputchildren = []
colorset = [px.colors.qualitative.G10[i] for i in range(len(name_legend))]

for i in range(len(name_legend)+5):
    if i == 0:
        n_0 = 0
    else:
        n_0 = 1
    if i < len(name_legend):
        htmlbuttons.append(html.Button(name_legend[i], id='toggle-'+str(i+1)+'WPsth', n_clicks=n_0, style={'width': '100%', 'backgroundColor': 'white', 
                                                                                                     'color': 'black', 'margin-top': '3px', 'margin-bottom': '3px', 'border-width': '0'}))
        input.append(Input('toggle-'+str(i+1)+'WPsth', 'n_clicks'))
        output.append(Output('toggle-'+str(i+1)+'WPsth', 'style'))
        outputchildren.append(Output('toggle-'+str(i+1)+'WPsth', 'children'))
    elif i == len(name_legend):
        input.append(Input('toggle-planns', 'on'))
        output.append(Output('name-switch1', 'style'))
        outputchildren.append(Output('name-switch1', 'children'))
        htmlbuttons2.append(html.Tr([html.Td("On", id='name-switch1', style = {'font-family':'Arial, sans-serif', 'color': 'white', 'position': 'relative', 'right': '50px', 'bottom':'5px', 'backgroundColor':'green', 'padding-left': '10px', 'padding-right': '20px'}), 
                                     html.Td(daq.BooleanSwitch(id = 'toggle-planns', on = True, color = 'green', labelPosition = 'right', style={'transform': 'scale(1.5)', 'position': 'relative', 'left': '40px'})),  
                                     html.Td("Plans", id = 'title1', style = {'font-family':'Arial, sans-serif'})]))
    elif i == len(name_legend)+1:
        input.append(Input('toggle-actualns', 'on'))
        output.append(Output('name-switch2', 'style'))
        outputchildren.append(Output('name-switch2', 'children'))
        htmlbuttons2.append(html.Tr([html.Td("On", id='name-switch2', style = {'font-family':'Arial, sans-serif', 'color': 'white', 'position': 'relative', 'right': '50px', 'bottom':'5px', 'backgroundColor':'green', 'padding-left': '10px', 'padding-right': '20px'}), 
                                     html.Td(daq.BooleanSwitch(id = 'toggle-actualns', on = True, color = 'green', labelPosition = 'right', style={'transform': 'scale(1.5)', 'position': 'relative', 'left': '40px'})), 
                                     html.Td("Actuals", id = 'title2', style = {'font-family':'Arial, sans-serif'})], style={'position': 'relative', 'top': '20px'}))
    elif i == len(name_legend)+2:
        input.append(Input('toggle-flowlines', 'on'))
        output.append(Output('name-switch3', 'style'))
        outputchildren.append(Output('name-switch3', 'children'))
        htmlbuttons2.append(html.Tr([html.Td("On", id='name-switch3', style = {'font-family':'Arial, sans-serif', 'color': 'white', 'position': 'relative', 'right': '50px', 'bottom':'5px', 'backgroundColor':'green', 'padding-left': '10px', 'padding-right': '20px'}), 
                                     html.Td(daq.BooleanSwitch(id = 'toggle-flowlines', on = True, color = 'green', labelPosition = 'right', style={'transform': 'scale(1.5)', 'position': 'relative', 'left': '40px'})), 
                                     html.Td("Flowlines", id = 'title3', style = {'font-family':'Arial, sans-serif'})], style={'position': 'relative', 'top': '40px'}))
    elif i == len(name_legend)+3:
        input.append(Input('toggle-absentdaysns', 'on'))
        output.append(Output('name-switch4', 'style'))
        outputchildren.append(Output('name-switch4', 'children'))
        htmlbuttons2.append(html.Tr([html.Td("On", id='name-switch4', style = {'font-family':'Arial, sans-serif', 'color': 'white', 'position': 'relative', 'right': '50px', 'bottom':'5px', 'backgroundColor':'green', 'padding-left': '10px', 'padding-right': '20px'}), 
                                     html.Td(daq.BooleanSwitch(id = 'toggle-absentdaysns', on = True, color = 'green', labelPosition = 'right', style={'transform': 'scale(1.5)', 'position': 'relative', 'left': '40px'})), 
                                     html.Td("No progress", id = 'title4', style = {'font-family':'Arial, sans-serif'})], style={'position': 'relative', 'top': '60px'}))
    else: 
        input.append(Input('toggle-projectiondaysns', 'on'))
        output.append(Output('name-switch5', 'style'))
        outputchildren.append(Output('name-switch5', 'children'))
        htmlbuttons2.append(html.Tr([html.Td("On", id='name-switch5', style = {'font-family':'Arial, sans-serif', 'color': 'white', 'position': 'relative', 'right': '50px', 'bottom':'5px', 'backgroundColor':'green', 'padding-left': '10px', 'padding-right': '20px'}),
                                     html.Td(daq.BooleanSwitch(id = 'toggle-projectiondaysns', on = True, color = 'green', labelPosition = 'right', style={'transform': 'scale(1.5)', 'position': 'relative', 'left': '40px', 'display': 'none'})),
                                     html.Td("Projection", id = 'title5', style = {'font-family':'Arial, sans-serif'})], style={'position': 'relative', 'top': '80px'}))
    
app2.layout = html.Div([
    dcc.Graph(id='plot-outputns', style = {'width': '100%', 'height': '860px', 'backgroundColor': 'white', 'position': 'absolute'}),
    html.Div(htmlbuttons, 
             style={'width': '250px', 'display':'inline-block', 'align-items': 'center', 'vertical-align': 'top',
                    'verticalAlign': 'middle', 'left':'1435px', 'top':'60px', 'position': 'relative'}),
    html.Div(htmlbuttons2, 
             style={'display':'flex', 'flex-direction': 'column', 
                    'position': 'relative', 'top': '240px', 'left': '1410px'})], 
    style={'width': '1720px', 'background-color': 'white', 'height': '960px'})

@app2.callback(
        Output('toggle-flowlines', 'on'),
        [Input('toggle-actualns', 'on')]
)

def update_button_click(valueactual):
    
    return (
            False if valueactual == False else False
        )

@app2.callback(
        [Output('toggle-absentdaysns', 'on'),
         Output('toggle-projectiondaysns', 'on')],
        [Input('toggle-flowlines', 'on')]
)

def update_button_click(valueflowlines):
    
    return (
            False if valueflowlines == False else False,
            False if valueflowlines == False else False 
        )

@app2.callback(
    Output('plot-outputns', 'figure'),
    input)

def update_plot(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, valueplan, valueactual, valueflowlines, valueabsent, valueprojection):

    figs = px.line(template='seaborn', title='<b>Activities Progress WPs<b>')
    planfigs = px.line(template='seaborn')
    actualfigs = px.line(template='seaborn')
    planactualfigs = px.line(template='seaborn')
    workingdays = []
    nonworkingdays = []

    if n_1WP % 2 == 0:

        #Add shapes for projected days
        if valueprojection == True:
            for i in range(len(figadditivessthprojection[0].data)):
                figs.add_trace(figadditivessthprojection[0].data[i])
                #Add hover data for projection
                dataprojection = pd.DataFrame({'x': [figadditivessthprojection[0].data[i].x[1], figadditivessthprojection[0].data[i].x[1]], 
                                               'y': [figadditivessthprojection[0].data[i].y[1], figadditivessthprojection[0].data[i].y[1]], 
                                               'customdata0': [figadditivessthprojection[0].data[i].x[1].date(), figadditivessthprojection[0].data[i].x[1].date()],
                                               'customdata1': ['L'+str(int(round(figadditivessthprojection[0].data[i].y[1]))), 'L'+str(int(round(figadditivessthprojection[0].data[i].y[1])))]})
                Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Level: %{customdata[1]}')
                figs.add_traces(Fadd.data[0])
        
        #Add planned flowlines
        planfigs.add_trace(Flowlines1figsth.data[0])
        actualfigs.add_trace(Flowlines1figsth.data[6])
        
        #Add progress flowlines
        for i in range(len(figadditivessth[0].data)):
            figadditivessth[0].data[i].name = ''
            figadditivessth[0].data[i].visible = True
            figs.add_trace(figadditivessth[0].data[i])
            if i <= 0:
                    pass
            else:
                for j in range(len(figadditivessth[0].data[i].x)//3):
                    for k in range(timegap(figadditivessth[0].data[i].x[3*j].date(), figadditivessth[0].data[i].x[3*j+1].date())+1):
                        workingdays.append(figadditivessth[0].data[i].x[3*j].date()+timedelta(days = k))

        for i in figadditivessth[0].layout.shapes:
            figs.add_shape(i)

    if n_2WP % 2 == 0:

        #Add shapes for projected days
        if valueprojection == True:
            for i in range(len(figadditivessthprojection[1].data)):
                figs.add_trace(figadditivessthprojection[1].data[i])
                #Add hover data for projection
                dataprojection = pd.DataFrame({'x': [figadditivessthprojection[1].data[i].x[1], figadditivessthprojection[1].data[i].x[1]], 
                                               'y': [figadditivessthprojection[1].data[i].y[1], figadditivessthprojection[1].data[i].y[1]], 
                                               'customdata0': [figadditivessthprojection[1].data[i].x[1].date(), figadditivessthprojection[1].data[i].x[1].date()],
                                               'customdata1': ['L'+str(int(round(figadditivessthprojection[1].data[i].y[1]))), 'L'+str(int(round(figadditivessthprojection[1].data[i].y[1])))]})
                Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Level: %{customdata[1]}')
                figs.add_traces(Fadd.data[0])

        #Add planned flowlines
        planfigs.add_trace(Flowlines1figsth.data[1])
        actualfigs.add_trace(Flowlines1figsth.data[7])
        
        #Add progress flowlines
        for i in range(len(figadditivessth[1].data)):
            figadditivessth[1].data[i].name = ''
            figadditivessth[1].data[i].visible = True
            figs.add_trace(figadditivessth[1].data[i])
            if i <= 0:
                    pass
            else:
                for j in range(len(figadditivessth[1].data[i].x)//3):
                    for k in range(timegap(figadditivessth[1].data[i].x[3*j].date(), figadditivessth[1].data[i].x[3*j+1].date())+1):
                        workingdays.append(figadditivessth[1].data[i].x[3*j].date()+timedelta(days = k))
        
        for i in figadditivessth[1].layout.shapes:
            figs.add_shape(i)

    if n_3WP % 2 == 0:

        #Add shapes for projected days
        if valueprojection == True:
            for i in range(len(figadditivessthprojection[2].data)):
                figs.add_trace(figadditivessthprojection[2].data[i])
                #Add hover data for projection
                dataprojection = pd.DataFrame({'x': [figadditivessthprojection[2].data[i].x[1], figadditivessthprojection[2].data[i].x[1]], 
                                               'y': [figadditivessthprojection[2].data[i].y[1], figadditivessthprojection[2].data[i].y[1]], 
                                               'customdata0': [figadditivessthprojection[2].data[i].x[1].date(), figadditivessthprojection[2].data[i].x[1].date()],
                                               'customdata1': ['L'+str(int(round(figadditivessthprojection[2].data[i].y[1]))), 'L'+str(int(round(figadditivessthprojection[2].data[i].y[1])))]})
                Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Level: %{customdata[1]}')
                figs.add_traces(Fadd.data[0])

        #Add planned flowlines
        planfigs.add_trace(Flowlines1figsth.data[2])
        actualfigs.add_trace(Flowlines1figsth.data[8])
        
        #Add progress flowlines
        for i in range(len(figadditivessth[2].data)):
            figadditivessth[2].data[i].name = ''
            figadditivessth[2].data[i].visible = True
            figs.add_trace(figadditivessth[2].data[i])
            if i <= 0:
                    pass
            else:
                for j in range(len(figadditivessth[2].data[i].x)//3):
                    for k in range(timegap(figadditivessth[2].data[i].x[3*j].date(), figadditivessth[2].data[i].x[3*j+1].date())+1):
                        workingdays.append(figadditivessth[2].data[i].x[3*j].date()+timedelta(days = k))

        for i in figadditivessth[2].layout.shapes:
            figs.add_shape(i)

    if n_4WP % 2 == 0:

        #Add planned flowlines 
        planfigs.add_trace(Flowlines1figsth.data[3])

    if n_5WP % 2 == 0:

        #Add shapes for projected days
        if valueprojection == True:
            for i in range(len(figadditivessthprojection[4].data)):
                figs.add_trace(figadditivessthprojection[4].data[i])
                #Add hover data for projection
                dataprojection = pd.DataFrame({'x': [figadditivessthprojection[4].data[i].x[1], figadditivessthprojection[4].data[i].x[1]], 
                                               'y': [figadditivessthprojection[4].data[i].y[1], figadditivessthprojection[4].data[i].y[1]], 
                                               'customdata0': [figadditivessthprojection[4].data[i].x[1].date(), figadditivessthprojection[4].data[i].x[1].date()],
                                               'customdata1': ['L'+str(int(round(figadditivessthprojection[4].data[i].y[1]))), 'L'+str(int(round(figadditivessthprojection[4].data[i].y[1])))]})
                Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Level: %{customdata[1]}')
                figs.add_traces(Fadd.data[0])

        #Add planned flowlines
        planfigs.add_trace(Flowlines1figsth.data[4])
        actualfigs.add_trace(Flowlines1figsth.data[10])
        
        #Add progress flowlines
        for i in range(len(figadditivessth[4].data)):
            figadditivessth[4].data[i].name = ''
            figadditivessth[4].data[i].visible = True
            figs.add_trace(figadditivessth[4].data[i])
            if i <= 0:
                    pass
            else:
                for j in range(len(figadditivessth[4].data[i].x)//3):
                    for k in range(timegap(figadditivessth[4].data[i].x[3*j].date(), figadditivessth[4].data[i].x[3*j+1].date())+1):
                        workingdays.append(figadditivessth[4].data[i].x[3*j].date()+timedelta(days = k))
        
        for i in figadditivessth[4].layout.shapes:
            figs.add_shape(i)

    if n_6WP % 2 == 0:

        #Add shapes for projected days
        if valueprojection == True:
            for i in range(len(figadditivessthprojection[5].data)):
                figs.add_trace(figadditivessthprojection[5].data[i])
                #Add hover data for projection
                dataprojection = pd.DataFrame({'x': [figadditivessthprojection[5].data[i].x[1], figadditivessthprojection[5].data[i].x[1]], 
                                               'y': [figadditivessthprojection[5].data[i].y[1], figadditivessthprojection[5].data[i].y[1]], 
                                               'customdata0': [figadditivessthprojection[5].data[i].x[1].date(), figadditivessthprojection[5].data[i].x[1].date()],
                                               'customdata1': ['L'+str(int(round(figadditivessthprojection[5].data[i].y[1]))), 'L'+str(int(round(figadditivessthprojection[5].data[i].y[1])))]})
                Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Level: %{customdata[1]}')
                figs.add_traces(Fadd.data[0])

        #Add planned flowlines
        planfigs.add_trace(Flowlines1figsth.data[5])
        actualfigs.add_trace(Flowlines1figsth.data[11])
        
        #Add progress flowlines
        for i in range(len(figadditivessth[5].data)):
            figadditivessth[5].data[i].name = ''
            figadditivessth[5].data[i].visible = True
            figs.add_trace(figadditivessth[5].data[i])
            if i <= 0:
                    pass
            else:
                for j in range(len(figadditivessth[5].data[i].x)//3):
                    for k in range(timegap(figadditivessth[5].data[i].x[3*j].date(), figadditivessth[5].data[i].x[3*j+1].date())+1):
                        workingdays.append(figadditivessth[5].data[i].x[3*j].date()+timedelta(days = k))
        
        for i in figadditivessth[5].layout.shapes:
            figs.add_shape(i)
    
    if n_1WP % 2 != 0 and n_2WP % 2 != 0 and n_3WP % 2 != 0 and n_4WP % 2 != 0 and n_5WP % 2 != 0 and n_6WP % 2 != 0:

        raise PreventUpdate

    figs.update_layout(showlegend = False)

    #Creating the colorscale
    figs.add_trace(px.scatter(x=[None, None, None], y=[None, None, None], 
                         color=[0, custom_colorscale[1][0], custom_colorscale[2][0]], 
                         range_color = [0, custom_colorscale[2][0]]).data[0])
    #Update size of plot
    figs.update_layout(height=560, width=950)
    #Thicken the lines to seem as 'bars'
    figs.update_traces(line=dict(width=5))
    figs.update_layout(xaxis_title="<b>Date<b>", yaxis_title="<b>Floor<b>")

    height = 860
    pixsize = 35
    width  = 1403
    
    #Add tablelike shapes for the yaxis
    figs.add_shape(type="rect",
              x0=-2*(pixsize/2300), x1=0,
              y0=0, y1=1,
              xref='paper', yref='paper',
              line=dict(color="#ffffff", width=1.5),
              fillcolor = '#eaeaf2',
              opacity = 1)

    for i in range(1, southfloornamelen+2):
    # Add horizontal line to the margin
        figs.add_shape(type="line",
              x0=-2*(pixsize/2300), x1=0,
              y0=i-1, y1=i-1,
              xref='paper', yref='y',
              line=dict(color="#ffffff", width=1.5),
              opacity = 1)
    # Add annotation to the margin
        if i < southfloornamelen+1:
            figs.add_annotation(
            text='<b>L'+str(i)+'<b>',
            x=-2*(pixsize/2300),
            y=i-1/2,
            xref='paper', yref='y',
            font=dict(size=12),
            showarrow = False )

    #Copy layout from original plot
    planfigs.layout = figs.layout
    actualfigs.layout = figs.layout
    planactualfigs.layout = figs.layout

    #State condition whether activities were finished in the lapse
    if False in [int(i) == round(i, 5) for i in np.concatenate([i.y for i in figs.data if i.line.color == 'black']) if math.isnan(i) == False]:
        finished = False
    else:
        finished = True

    #Avoid error from exception
    if n_1WP % 2 != 0 and n_2WP % 2 != 0 and n_3WP % 2 != 0 and n_4WP % 2 == 0 and n_5WP % 2 != 0 and n_6WP % 2 != 0:
        pass
    else:
        for i in range(timegap(min(workingdays), max(workingdays))):
            if min(workingdays)+timedelta(days=i) not in workingdays not in workingdays and min(workingdays)+timedelta(days=i) not in offdays:
                nonworkingdays.append(min(workingdays)+timedelta(days=i))
            #Add last set of nonworking days
        if finished == False and sorted(list(set(workingdays)))[-1]+timedelta(days=1) < lastdate:
            for i in range(timegap(sorted(list(set(workingdays)))[-1]+timedelta(days=1), lastdate)):
                if sorted(list(set(workingdays)))[-1]+timedelta(days=1)+timedelta(days=i) not in offdays:
                    nonworkingdays.append(sorted(list(set(workingdays)))[-1]+timedelta(days=1)+timedelta(days=i))

        nonworkingdaysranges = [nonworkingdays[0]]
        
        for i in range(len(nonworkingdays)-1):
            if nonworkingdays[i]+timedelta(days=1) != nonworkingdays[i+1]:
                nonworkingdaysranges.append(nonworkingdays[i]+timedelta(days=1))
                nonworkingdaysranges.append(nonworkingdays[i+1])
        nonworkingdaysranges.append(nonworkingdays[-1]+timedelta(days=1))

    #Add shapes for absent days
    if valueabsent == True and n_1WP % 2 != 0 and n_2WP % 2 != 0 and n_3WP % 2 != 0 and n_4WP % 2 == 0 and n_5WP % 2 != 0 and n_6WP % 2 != 0:
        pass
    elif valueabsent == True:
        for i in range(len(nonworkingdaysranges)//2):
            figs.add_shape(type="rect",
              x0=nonworkingdaysranges[2*i], x1=nonworkingdaysranges[2*i+1],
              y0=0, y1=1,
              xref='x', yref='paper',
              line=dict(color="black", width=1.5),
              fillcolor = 'black',
              opacity = 0.15)
  
    figs.update_layout(showlegend = False)

    #Add dashed line for last measurement and annotation in the conditional forecast
    if valueprojection == True and finished == False:
        
        figs.add_shape(type="line",
                                x0=lastdate, x1=lastdate,
                                y0=0, y1=1,
                                xref='x', yref='paper',
                                line=dict(color="black", width=1.5, dash = 'dash'),
                                opacity = 1)
        figs.add_annotation(text='Last measurement:<br>2023-9-28',
                                x=date(2023, 9, 29),
                                ax = -55,
                                align = 'left',
                                ay = 0,
                                y=8.25,
                                axref = 'pixel',
                                ayref = 'pixel',
                                xref='x', yref='y',
                                font=dict(size=10),
                                showarrow = True,
                                arrowcolor = 'rgba(0,0,0,0)')

    #Update size of plot
    figs.update_layout(height=height, width=width)
    #Thicken the lines to seem as 'bars'
    figs.update_traces(line=dict(width=15))
    #Make fix of the yaxis of planfigs.data and actualfigs.data
    for i in range(len(planfigs.data)):
        planfigs.data[i].y = [j-1 if j!=None else None for j in planfigs.data[i].y]
    for i in range(len(actualfigs.data)):
        actualfigs.data[i].y = [j-1 if j!=None else None for j in actualfigs.data[i].y]
    #Add planned data for the case of the toggle button
    if valueflowlines == True:
        for i in range(len(planfigs.data)):
            figs.add_trace(planfigs.data[i])
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Plan v Actual)<b>', font = dict(size = 20)))
    else:
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Actual)<b>', font = dict(size = 20)))

    #Provide scenario for the particular case
    if n_1WP % 2 != 0 and n_2WP % 2 != 0 and n_3WP % 2 != 0 and n_4WP % 2 == 0 and n_5WP % 2 != 0 and n_6WP % 2 != 0:

        #Prevent plan error in this case
        if valueflowlines == False:
            raise PreventUpdate
        else:
            maxdate = max([j for j in [i.x for i in planfigs.data][0] if j!=  None])
            #Add tablelike shapes for the yaxis
            planfigs.add_shape(type="rect",
                x0=-2*(pixsize/2300), x1=0,
                y0=0, y1=1,
                xref='paper', yref='paper',
                line=dict(color="#ffffff", width=1.5),
                fillcolor = '#eaeaf2',
                opacity = 1)
            for i in range(1, southfloornamelen+2):
            # Add horizontal line to the margin
                planfigs.add_shape(type="line",
                x0=-2*(pixsize/2300), x1=0,
                y0=i-1, y1=i-1,
                xref='paper', yref='y',
                line=dict(color="#ffffff", width=1.5),
                opacity = 1)
            # Add annotation to the margin
                if i < southfloornamelen+1:
                    planfigs.add_annotation(
                text='<b>L'+str(i)+'<b>',
                x=-2*(pixsize/2300),
                y=i-1/2,
                xref='paper', yref='y',
                font=dict(size=12),
                showarrow = False )
            maxdate = max([j for j in [i.x for i in planfigs.data][0] if j!=  None])
            planfigs.update_layout(showlegend = False)
            # Update colorbar title and scale
            planfigs.update_coloraxes(colorbar_title='<b>Percentage of<br>Progress (%)<br> <br><b>', colorscale = [[0, 'rgb(255,0,0)'], [custom_colorscale[1][0]/custom_colorscale[2][0], 'rgb(255,212,0)'], [1, 'rgb(52,235,0)']],
                                colorbar_tickmode = 'array', colorbar_ticktext = ['0', '5', '10', '15', '20', '25', '30+'], colorbar_tickvals = [0, 5, 10, 15, 20, 25, 30],
                                colorbar_ticks = 'outside', colorbar_tickwidth = 2, colorbar_ticklen = 8)

            planfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(southfloornamelen+1)], ticktext = ['']*(southfloornamelen+1), range = [-0.43, southfloornamelen+0.43], title_standoff = 35),
                            xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxdate+timedelta(days=5)]), title = '<b>Flowlines, '+name_legend[3]+' - South Building (Plan)<b>')

    else:
        maxdate = max([dateconversion(j) for j in list(np.concatenate([i.x for i in figs.data])) if type(j) == datetime.date or type(j) == datetime.datetime])
        # Update colorbar title and scale
        figs.update_coloraxes(colorbar_title='<b>Percentage of<br>Progress (%)<br> <br><b>', colorscale = [[0, 'rgb(255,0,0)'], [custom_colorscale[1][0]/custom_colorscale[2][0], 'rgb(255,212,0)'], [1, 'rgb(52,235,0)']],
                              colorbar_tickmode = 'array', colorbar_ticktext = ['0', '5', '10', '15', '20', '25', '30+'], colorbar_tickvals = [0, 5, 10, 15, 20, 25, 30],
                              colorbar_ticks = 'outside', colorbar_tickwidth = 2, colorbar_ticklen = 8)

        figs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(southfloornamelen+1)], ticktext = ['']*(southfloornamelen+1), range = [-0.43, southfloornamelen+0.43], title_standoff = 50),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxdate+timedelta(days=5)]))

    if valueactual == False and valueplan == True:

        planfigs.update_layout(showlegend = False)
        #Update size of plot
        planfigs.update_layout(height=height, width=width)
        planfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(southfloornamelen+1)], ticktext = ['']*(southfloornamelen+1), range = [-0.43, southfloornamelen+0.43], title_standoff = 50),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), lastdate+timedelta(days=5)]))
        planfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Plan)<b>', font = dict(size = 25)))
        #Use extra data to ensure that xaxis range is fixed
        maxrange = lastdate
        #Add weekends and holidays
        for Days in range(0, len(offdaysranges)-1, 2):
            if datetimeconversion(offdaysranges[Days])>=datetime.datetime(2022, 10, 31, 0, 0)-timedelta(days=5) and datetimeconversion(offdaysranges[Days+1]) < datetimeconversion(maxrange)+timedelta(days=5):
                planfigs.add_shape(type = 'rect', x0 = datetimeconversion(offdaysranges[Days]), x1 = datetimeconversion(offdaysranges[Days+1])+timedelta(days=1), y0 = 0, y1 = 1, xref = 'x', yref = 'paper', line=dict(color="rgba(0, 0, 0, 0)", width=1.5), fillcolor = '#6d6b15', opacity = 0.25, layer = 'below')
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [8, 8])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        planfigs.add_traces(toprightfigs.data[0])
        planfigs.add_traces(bottomleftfigs.data[0])
        return planfigs
    
    elif valueactual == True and valueplan == True and valueflowlines == False:
        for i in range(len(planfigs.data)):
            planactualfigs.add_trace(planfigs.data[i])
        for i in range(len(actualfigs.data)):
            planactualfigs.add_trace(actualfigs.data[i])
        planactualfigs.update_layout(showlegend = False)
        #Update size of plot
        planactualfigs.update_layout(height=height, width=width)
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in planactualfigs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        #Add weekends and holidays
        for Days in range(0, len(offdaysranges)-1, 2):
            if datetimeconversion(offdaysranges[Days])>=datetime.datetime(2022, 10, 31, 0, 0)-timedelta(days=5) and datetimeconversion(offdaysranges[Days+1]) < datetimeconversion(maxrange)+timedelta(days=5):
                planactualfigs.add_shape(type = 'rect', x0 = datetimeconversion(offdaysranges[Days]), x1 = datetimeconversion(offdaysranges[Days+1])+timedelta(days=1), y0 = 0, y1 = 1, xref = 'x', yref = 'paper', line=dict(color="rgba(0, 0, 0, 0)", width=1.5), fillcolor = '#6d6b15', opacity = 0.25, layer = 'below')
        planactualfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(southfloornamelen+1)], ticktext = ['']*(southfloornamelen+1), range = [-0.43, southfloornamelen+0.43], title_standoff = 50),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), max([dateconversion(i) for i in np.concatenate([i.x for i in planactualfigs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])+timedelta(days=5)]))
        planactualfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Plan v Actual)<b>', font = dict(size = 25)))
        toprightfigs = px.line(x = [maxrange+timedelta(days=4), maxrange+timedelta(days=4)], y = [8, 8])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        planactualfigs.add_traces(toprightfigs.data[0])
        planactualfigs.add_traces(bottomleftfigs.data[0])
        return planactualfigs
    
    elif valueactual == True and valueplan == True and valueflowlines == True:

        for i in range(len(planfigs.data)):
            figs.add_trace(planfigs.data[i])
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in figs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        if finished == False and valueprojection == False:
            maxrange = lastdate
        #In the case the furthest point is a shaded rectangle
        if [dateconversion(i.x1) for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black'] != []:
            if max([dateconversion(i.x1) for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black']) > dateconversion(maxrange):
                maxrange = max([dateconversion(i.x1) for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black']) 
        #Add weekends and holidays
        for Days in range(0, len(offdaysranges)-1, 2):
            if datetimeconversion(offdaysranges[Days])>=datetime.datetime(2022, 10, 31, 0, 0)-timedelta(days=5) and datetimeconversion(offdaysranges[Days+1]) < datetimeconversion(maxrange)+timedelta(days=5):
                figs.add_shape(type = 'rect', x0 = datetimeconversion(offdaysranges[Days]), x1 = datetimeconversion(offdaysranges[Days+1])+timedelta(days=1), y0 = 0, y1 = 1, xref = 'x', yref = 'paper', line=dict(color="rgba(0, 0, 0, 0)", width=1.5), fillcolor = '#6d6b15', opacity = 0.25, layer = 'below')
        #Add text regarding percentage of days without progress
        if valueabsent == True and len(workingdays) != 0:
            if finished:
                Maxdate = maxrange
            else:
                Maxdate = lastdate
            
            #Calculate ratio by summing the ranges of the shaded rectangles
            nonholidayweekdays = 0
            for i in range((MAXDATE(np.concatenate([i.x for i in figs.data if i.line.dash == 'solid' and i.line.color != 'black']))-mindate(np.concatenate([i.x for i in figs.data if i.line.dash == 'solid' and i.line.color != 'black']))).days):
                if mindate(np.concatenate([i.x for i in figs.data]))+timedelta(days=i) not in offdays:
                    nonholidayweekdays += 1 
            nonworkingratio = sum([(i.x1-i.x0).days for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black'])/nonholidayweekdays
            figs.add_annotation(x = 0, y = 8.125, text = 'Percentage of days with no progress: '+str(round(100*nonworkingratio))+'%', xref = 'paper', yref = 'y', showarrow = False, font = dict(size = 15))
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Plan v Actual)<b>', font = dict(size = 25)), xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=5)]))
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [8, 8])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        figs.add_traces(toprightfigs.data[0])
        figs.add_traces(bottomleftfigs.data[0])
        return figs
    
    elif valueactual == True and valueplan == False and valueflowlines == False:

        actualfigs.update_layout(showlegend = False)
        #Update size of plot
        actualfigs.update_layout(height=height, width=width)
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in actualfigs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        actualfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(southfloornamelen+1)], ticktext = ['']*(southfloornamelen+1), range = [-0.43, southfloornamelen+0.43], title_standoff = 50),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=5)]))
        #Add weekends and holidays
        for Days in range(0, len(offdaysranges)-1, 2):
            if datetimeconversion(offdaysranges[Days])>=datetime.datetime(2022, 10, 31, 0, 0)-timedelta(days=5) and datetimeconversion(offdaysranges[Days+1]) < maxrange+timedelta(days=5):
                actualfigs.add_shape(type = 'rect', x0 = datetimeconversion(offdaysranges[Days]), x1 = datetimeconversion(offdaysranges[Days+1])+timedelta(days=1), y0 = 0, y1 = 1, xref = 'x', yref = 'paper', line=dict(color="rgba(0, 0, 0, 0)", width=1.5), fillcolor = '#6d6b15', opacity = 0.25, layer = 'below')
        actualfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Actual)<b>', font = dict(size = 25)))
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [8, 8])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        actualfigs.add_traces(toprightfigs.data[0])
        actualfigs.add_traces(bottomleftfigs.data[0])
        return actualfigs

    elif valueactual == True and valueplan == False and valueflowlines == True:
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in figs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        if finished == False and valueprojection == False:
            maxrange = lastdate
        #In the case the furthest point is a shaded rectangle
        if [dateconversion(i.x1) for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black'] != []:
            if max([dateconversion(i.x1) for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black']) > dateconversion(maxrange):
                maxrange = max([dateconversion(i.x1) for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black']) 
        #Add weekends and holidays
        for Days in range(0, len(offdaysranges)-1, 2):
            if datetimeconversion(offdaysranges[Days])>=datetime.datetime(2022, 10, 31, 0, 0)-timedelta(days=5) and datetimeconversion(offdaysranges[Days+1]) < datetimeconversion(maxrange)+timedelta(days=5):
                figs.add_shape(type = 'rect', x0 = datetimeconversion(offdaysranges[Days]), x1 = datetimeconversion(offdaysranges[Days+1])+timedelta(days=1), y0 = 0, y1 = 1, xref = 'x', yref = 'paper', line=dict(color="rgba(0, 0, 0, 0)", width=1.5), fillcolor = '#6d6b15', opacity = 0.25, layer = 'below')
        #Add text regarding percentage of days without progress
        if valueabsent == True and len(workingdays) != 0:
            if finished:
                Maxdate = maxrange
            else:
                Maxdate = lastdate
            
            #Calculate ratio by summing the ranges of the shaded rectangles
            nonholidayweekdays = 0
            for i in range((MAXDATE(np.concatenate([i.x for i in figs.data if i.line.dash == 'solid' and i.line.color != 'black']))-mindate(np.concatenate([i.x for i in figs.data if i.line.dash == 'solid' and i.line.color != 'black']))).days):
                if mindate(np.concatenate([i.x for i in figs.data]))+timedelta(days=i) not in offdays:
                    nonholidayweekdays += 1 
            nonworkingratio = sum([(i.x1-i.x0).days for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black'])/nonholidayweekdays
            figs.add_annotation(x = 0, y = 8.125, text = 'Percentage of days with no progress: '+str(round(100*nonworkingratio))+'%', xref = 'paper', yref = 'y', showarrow = False, font = dict(size = 15))
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Actual)<b>', font = dict(size = 25)), xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=5)]))
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [8, 8])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        figs.add_traces(toprightfigs.data[0])
        figs.add_traces(bottomleftfigs.data[0])
        return figs
    
    else:
        raise PreventUpdate    

@app2.callback(
    output,
    input
)
def update_button_style(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, valueplan, valueactual, valueflowlines, valueabsent, valueprojection):
    # Default style for buttons
    default_style = {'width': '100%', 'backgroundColor': 'white', 'color': 'black', 'margin-bottom':'5px', 'margin-bottom':'5px', 'height': '30px', 'border-radius': '10px', 'text-align': 'left', 'border-width': '0'}
    active_style = default_style.copy()
    default_style['color'] = 'black'
    active_style['color'] = '#aaa'
    default_style0 = {'font-family':'Arial, sans-serif', 'backgroundColor': 'green', 'color': 'white', 'height': '38px', 'border-radius': '19px', 'margin-top': '0px', 'width': '100px', 'border-width': '0', 'position': 'relative', 'left': '30px', 'bottom': '5px', 'text-align': 'left', 'padding-left': '15px'}
    active_style0 = {'font-family':'Arial, sans-serif', 'backgroundColor': '#e6e6e6', 'color': 'white', 'height': '38px', 'border-radius': '19px', 'margin-top': '0px', 'width': '100px', 'border-width': '0', 'position': 'relative', 'left': '30px', 'bottom': '5px', 'text-align': 'right', 'padding-right': '15px'}
    default_style1 = {'font-family':'Arial, sans-serif', 'backgroundColor': 'green', 'color': 'white', 'height': '38px', 'border-radius': '19px', 'margin-top': '10px', 'width': '100px', 'border-width': '0', 'position': 'relative', 'left': '30px', 'bottom': '5px', 'text-align': 'left', 'padding-left': '15px'}
    active_style1 = {'font-family':'Arial, sans-serif', 'backgroundColor': '#e6e6e6', 'color': 'white', 'height': '38px', 'border-radius': '19px', 'margin-top': '10px', 'width': '100px', 'border-width': '0', 'position': 'relative', 'left': '30px', 'bottom': '5px', 'text-align': 'right', 'padding-right': '15px'}
    if valueactual == False:
        default_style1['display'] = 'None'
        active_style1['display'] = 'None'
    default_style2 = {'font-family':'Arial, sans-serif', 'backgroundColor': 'green', 'color': 'white', 'height': '38px', 'border-radius': '19px', 'margin-top': '10px', 'width': '100px', 'border-width': '0', 'position': 'relative', 'left': '30px', 'bottom': '5px', 'text-align': 'left', 'padding-left': '15px'}
    active_style2 = {'font-family':'Arial, sans-serif', 'backgroundColor': '#e6e6e6', 'color': 'white', 'height': '38px', 'border-radius': '19px', 'margin-top': '10px', 'width': '100px', 'border-width': '0', 'position': 'relative', 'left': '30px', 'bottom': '5px', 'text-align': 'right', 'padding-right': '15px'}
    if valueactual == False or valueflowlines == False:
        default_style2['display'] = 'None'
        active_style2['display'] = 'None'

    return (
        default_style if n_1WP % 2 == 0 else active_style,
        default_style if n_2WP % 2 == 0 else active_style,
        default_style if n_3WP % 2 == 0 else active_style,
        default_style if n_4WP % 2 == 0 else active_style,
        default_style if n_5WP % 2 == 0 else active_style,
        default_style if n_6WP % 2 == 0 else active_style,
        default_style0 if valueplan == True else active_style0,
        default_style0 if valueactual == True else active_style0,
        default_style1 if valueflowlines == True else active_style1,
        default_style2 if valueabsent == True else active_style2,
        default_style2 if valueprojection == True else active_style2
    )

@app2.callback(
    [Output('toggle-planns', 'style'),
     Output('toggle-actualns', 'style'),
     Output('toggle-flowlines', 'style'),
     Output('toggle-absentdaysns', 'style'),
     Output('toggle-projectiondaysns', 'style')],
    [Input('toggle-planns', 'on'),
     Input('toggle-actualns', 'on'),
     Input('toggle-flowlines', 'on'),
     Input('toggle-absentdaysns', 'on'),
     Input('toggle-projectiondaysns', 'on')]
)

def update_button_style(valueplan, valueactual, valueflowlines, valueabsent, valueprojection):
    # Default style for buttons
    default_style = {'transform': 'scale(1.4)', 'position': 'relative', 'right': '32px'}
    active_style = {'transform': 'scale(1.4)', 'position': 'relative', 'right': '80px'}
    default_style1 = {'transform': 'scale(1.4)', 'position': 'relative', 'right': '32px'}
    active_style1 = {'transform': 'scale(1.4)', 'position': 'relative', 'right': '80px'}
    default_style2 = {'transform': 'scale(1.4)', 'position': 'relative', 'right': '32px'}
    active_style2 = {'transform': 'scale(1.4)', 'position': 'relative', 'right': '80px'}
    if valueactual == False:
        default_style1 = {'opacity': '0'}
        active_style1 = {'opacity': '0'}
        default_style2 = {'opacity': '0'}
        active_style2 = {'opacity': '0'}
    if valueflowlines == False:
        default_style2 = {'opacity': '0'}
        active_style2 = {'opacity': '0'}

    return (
        default_style if valueplan == True else active_style,
        default_style if valueactual == True else active_style,
        default_style1 if valueflowlines == True else active_style1,
        default_style2 if valueabsent == True else active_style2,
        default_style2 if valueprojection == True else active_style2
    )

@app2.callback(
    [Output('title1', 'style'),
     Output('title2', 'style'),
     Output('title3', 'style'),
     Output('title4', 'style'),
     Output('title5', 'style')],
    [Input('toggle-planns', 'on'),
     Input('toggle-actualns', 'on'),
     Input('toggle-flowlines', 'on'),
     Input('toggle-absentdaysns', 'on'),
     Input('toggle-projectiondaysns', 'on')]
)

def update_button_style(valueplan, valueactual, valueflowlines, valueabsent, valueprojection):
    # Default style for buttons
    default_style = {'font-family':'Arial, sans-serif', 'position': 'relative', 'right': '12px', 'bottom': '5px'}
    active_style = {'font-family':'Arial, sans-serif', 'position': 'relative', 'right': '12px', 'bottom': '5px'}
    default_style1 = {'font-family':'Arial, sans-serif', 'position': 'relative', 'right': '12px', 'bottom': '5px'}
    active_style1 = {'font-family':'Arial, sans-serif', 'position': 'relative', 'right': '12px', 'bottom': '5px'}
    default_style2 = {'font-family':'Arial, sans-serif', 'position': 'relative', 'right': '12px', 'bottom': '5px'}
    active_style2 = {'font-family':'Arial, sans-serif', 'position': 'relative', 'right': '12px', 'bottom': '5px'}
    if valueactual == False:
        default_style1 = {'opacity': '0'}
        active_style1 = {'opacity': '0'}
        default_style2 = {'opacity': '0'}
        active_style2 = {'opacity': '0'}
    if valueflowlines == False:
        default_style2 = {'opacity': '0'}
        active_style2 = {'opacity': '0'}

    return (
        default_style if valueplan == True else active_style,
        default_style if valueactual == True else active_style,
        default_style1 if valueflowlines == True else active_style1,
        default_style2 if valueabsent == True else active_style2,
        default_style2 if valueprojection == True else active_style2
    )

@app2.callback(
    outputchildren,
    input
)
def update_button_style(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, valueplan, valueactual, valueflowlines, valueabsent, valueprojection):
    on = []
    off = []
    # Change button style
    for i in range(len(name_legend)):
        on.append(html.Div([html.Hr(style={'height': '15px', 'width': '15px', 'border-color': colorset[i], 'background-color': colorset[i], 'border-width': 'medium', 'margin-right': '12px'}), name_legend[i]], 
                           style={'display': 'flex', 'display-direction': 'row', 'float': 'left', 'align-items': 'center'}))
        off.append(html.Div([html.Hr(style={'height': '15px', 'width': '15px', 'border-color': colorset[i], 'background-color': 'white', 'border-width': 'medium', 'margin-right': '12px'}), name_legend[i]], 
                            style={'display': 'flex', 'display-direction': 'row', 'float': 'left', 'align-items': 'center'}))

    return (
        on[0] if n_1WP % 2 == 0 else off[0],
        on[1] if n_2WP % 2 == 0 else off[1],
        on[2] if n_3WP % 2 == 0 else off[2],
        on[3] if n_4WP % 2 == 0 else off[3],
        on[4] if n_5WP % 2 == 0 else off[4],
        on[5] if n_6WP % 2 == 0 else off[5],
        'On' if valueplan == True else 'Off',
        'On' if valueactual == True else 'Off',
        'On' if valueflowlines == True else 'Off',
        'On' if valueabsent == True else 'Off',
        'On' if valueprojection == True else 'Off'
    )
#app2.write_html('testapp2')
if __name__ == '__main__':
    app2.run_server(debug=True, port=8052)


# In[8]:


figadditives[0].data[0].line


# In[9]:


Flowlines1fig.layout.title.text ='<b>Plan v Actual activity lines North<b>'
app4 = dash.Dash(__name__)

app4.layout = html.Div([
    html.Div([dcc.Graph(id='plot-output', figure = Flowlines1fig, style = {'width': '100%', 'height': '860px'})], style={'width': '1600px', 'position': 'absolute'})
])

#if __name__ == '__main__':
 #   app3.run(debug=True, port=8051)


# In[10]:


print(figadditivessth[4].layout.coloraxis)


# In[11]:


Flowlines1figsth.layout.title.text ='<b>Plan v Actual activity lines South<b>'
app5 = dash.Dash(__name__)

app5.layout = html.Div([dcc.Graph(id='plot-output', figure = Flowlines1figsth, style = {'width': '100%', 'height': '860px'})], style={'width': '1600px', 'position': 'absolute'})


#if __name__ == '__main__':
 #   app4.run(debug=True, port=8051)


# In[12]:


app6 = dash.Dash(__name__)

locationlist = ['North', 'South']
graphlist = ['Progress flow', 'Activity lines']

app6.layout = html.Div([
    html.Div(id='dd-output-container', style={'position': 'absolute', 'width': '1600px', 'height':'860'}),
    html.Div([html.Div([dcc.Dropdown(locationlist, 'North', id='location-dropdown', style={'width':'100px', 'backgroundColor': '#f6f6f6'})], style = {'position': 'relative', 'left': '50px'}),
              html.Div([dcc.Dropdown(graphlist, 'Progress flow', id='graph-dropdown', style={'width':'150px', 'backgroundColor': '#f6f6f6'})], style = {'position': 'relative', 'left': '1160px'})], 
             style={'display': 'flex', 'display-direction': 'row', 'position': 'relative', 'top': '20px'})
])

@app6.callback(
    Output('dd-output-container', 'children'),
    [Input('location-dropdown', 'value'),
     Input('graph-dropdown', 'value')]
)

def update_plot_output(locationvalue, graphvalue):

    if locationvalue == 'North' and graphvalue == 'Progress flow':
        return app1.layout
    elif locationvalue == 'South' and graphvalue == 'Progress flow':
        return app2.layout
    elif locationvalue == 'North' and graphvalue == 'Activity lines':
        return app3.layout
    elif locationvalue == 'South' and graphvalue == 'Activity lines':
        return app4.layout
    else:
        raise PreventUpdate


#if __name__ == '__main__':
 #   app5.run(debug=True, port=8051)

