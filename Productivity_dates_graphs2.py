#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


import Productivity_dates
from Productivity_dates import cladding_dates, flowlineactivitiesfig_layouts_datapoints, flowlineactivitiesfig_layouts, flowlineactivitiesfig_layouts_datapointssth, flowlineactivitiesfig_layoutssth, southfloornamelen, activitiesfigadditivesA, name_legend, activitiesprojectionA, timegap, lastdate, activitiesfigadditivesB, activitiesprojectionB, activitiesfigadditivesC, activitiesprojectionC, custom_colorscale


# In[2]:


import datetime
from datetime import date, timedelta, time
lastdate = date(2023, 9, 29)
def dateconversion(x):
    if type(x) == datetime.date:
        return x
    elif x == None:
        return None
    else:
        return x.date()

def datetimeconversion(x):
    if type(x) == date:
        return datetime.combine(x, time(0, 0, 0))
    else:
        return x

def maxdate(arr):
    return max(datetimeconversion(i) for i in arr if type(i)==datetime.datetime or type(i)==date)

def mindate(arr):
    return min(datetimeconversion(i) for i in arr if type(i)==datetime.datetime or type(i)==date)

datetime.datetime.combine(date(2023, 4, 5), time(0, 0, 0))


# In[3]:


import dash
from dash import dcc, html, Dash, callback
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import datetime
from datetime import date, timedelta
import numpy as np
from dash.exceptions import PreventUpdate
import math
import pandas as pd

Buildinglist = ['North', 'South']
buildinglist = [{
            "label": html.Span('North', style={'font-family': 'Arial, sans-serif'}),
            "value": 'North',
        }, {
            "label": html.Span('South', style={'font-family': 'Arial, sans-serif'}),
            "value": 'South',
        }]
floorlist = []
Floorlist = np.concatenate([np.array(['L'+str(i+1)]) for i in range(cladding_dates[1][1][-2]-1)]).tolist()
for i in range(cladding_dates[1][1][-2]-1):
    floorlist.append({
            "label": html.Span('L'+str(i+1), style={'font-family': 'Arial, sans-serif'}),
            "value": "L"+str(i+1),
        })
floorliststh = np.concatenate([np.array(['L'+str(i+1)]) for i in range(southfloornamelen)]).tolist()
Locationlist = ['1-5', '6-10']
locationlist = [{
            "label": html.Span('1-5', style={'font-family': 'Arial, sans-serif'}),
            "value": '1-5',
        }, {
            "label": html.Span('6-10', style={'font-family': 'Arial, sans-serif'}),
            "value": '6-10',
        }]
buildingindexlist = [0, 0]
floorindexlist = [0]
locationindexlist = [0]
htmlbuttons2 = [html.Button('Plan', id='toggle-planactualssns', n_clicks=0, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}),
                html.Button('Toggle planned dates', id='toggle-plansns', n_clicks=0, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}),
                html.Button('Toggle days with no progress', id='toggle-absent-daysns', n_clicks=1, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}),
                html.Button('Toggle projection days', id='toggle-projection-daysns', n_clicks=1, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'})]
Inputs = [Input('building-dropdown', 'value'),
          Input('floor-dropdown', 'value'),
          Input('location-dropdown', 'value')]

app = Dash(__name__)
server3 = app.server

# Get the port from the environment variable
port = int(os.environ.get("PORT", 8054))
app.layout = html.Div(id = 'Activity-dropdowns', children = [
     
    html.Div([dcc.Graph(id='plot-output', style = {'width': '1700px', 'height': '900px'})], style = {'position': 'absolute'}),
    html.Div([dcc.Dropdown(buildinglist, 'North', id='building-dropdown', style={'width':'90px', 'backgroundColor': '#f6f6f6'}),
    dcc.Dropdown(floorlist, value = 'L1', id='floor-dropdown', style={'width':'90px', 'backgroundColor': '#f6f6f6'}),
    dcc.Dropdown(locationlist, '1-5', id='location-dropdown', style={'width':'90px', 'backgroundColor': '#f6f6f6'})], 
    style = {'display': 'flex', 'flex-direction': 'row', 'position': 'relative', 'top': '10px'}),
    html.Div(htmlbuttons2, 
             style={'display':'flex', 'flex-direction': 'row', 
                    'position': 'relative', 'top': '870px'})
])

@app.callback(
        Output('toggle-plansns', 'n_clicks'),
        [Input('toggle-planactualssns', 'n_clicks')]
)

def update_button_click(n_A):
    
    return (
            0 if n_A % 3 == 0 else 0
        )

@app.callback(
        [Output('toggle-absent-daysns', 'n_clicks'),
         Output('toggle-projection-daysns', 'n_clicks')],
        [Input('toggle-plansns', 'n_clicks')]
)

def update_button_click(n_R):
    
    return (
            0 if n_R % 2 == 0 else 0,
            0 if n_R % 2 == 0 else 0 
        )

@app.callback(
    Output('plot-output', 'figure'),
    [Input('building-dropdown', 'value'),
    Input('floor-dropdown', 'value'),
    Input('location-dropdown', 'value'),
    Input('toggle-planactualssns', 'n_clicks'),
    Input('toggle-plansns', 'n_clicks'),
    Input('toggle-absent-daysns', 'n_clicks'), 
    Input('toggle-projection-daysns', 'n_clicks')]
)

def update_plot_output(value_building, value_floor, value_location, n_A, n_R, n_C, n_P):

    workingdays = []
    nonworkingdays = []

    if value_building != None:
        buildingindex = Buildinglist.index(value_building)
        buildingindexlist.append(buildingindex)

    else:
        buildingindex = buildingindexlist[-1]
        buildingindexlist.append(buildingindex)

    if value_floor != None and buildingindex == 0:
        floorindex = Floorlist.index(value_floor)
        floorindexlist.append(floorindex)

    elif value_floor != None and buildingindex == 1:
        floorindex = floorliststh.index(value_floor)
        floorindexlist.append(floorindex)

    else:
        floorindex = floorindexlist[-1]
        floorindexlist.append(floorindex)
    
    if value_location != None:
        locationindex = Locationlist.index(value_location)
        locationindexlist.append(locationindex)

    else:
        locationindex = locationindexlist[-1]
        locationindexlist.append(locationindex)
    
    if buildingindexlist[-1] != buildingindexlist[-2] and value_building != None:

        floorindexlist.append(0)
        floorindex = floorindexlist[-1]
    
    if value_floor == None or value_location == None and buildingindex == 0:

        raise PreventUpdate


    figs = px.line(template='seaborn')
    
    if buildingindex == 0:

        #Plan case
        if n_A % 3 == 0:
            if floorindex == 11 or floorindex == 12:
                    pass
            else:
                figs.add_trace(flowlineactivitiesfig_layouts_datapoints[floorindex][locationindex][0])

        elif n_A % 3 == 1:

            if (floorindex == 11 and locationindex == 1) or (floorindex == 12 and locationindex == 1):
                pass
            
            else:
            #Copy north dataplot plan and actuals
                for i in flowlineactivitiesfig_layouts_datapoints[floorindex][locationindex]:
                
                    if n_R % 2 ==0:    
                        i.name = ''
                        figs.add_trace(i)
                    
                    else:
                        if i.line.dash == 'dash':
                            i.name = ''
                            figs.add_trace(i)
                    
                if locationindex==0:
                        activitiesfigadditives = activitiesfigadditivesA
                        activitiesprojection = activitiesprojectionA
                    
                else: 
                        activitiesfigadditives = activitiesfigadditivesB
                        activitiesprojection = activitiesprojectionB

                #Add projection data first
                if n_P % 2 == 1 and n_R % 2 == 1:
                        k = 0
                        while k < len(name_legend):
                            for j in range(len(activitiesprojection[len(name_legend)*floorindex+k].data)):
                                activitiesprojection[len(name_legend)*floorindex+k].data[j].name = ''
                                figs.add_trace(activitiesprojection[len(name_legend)*floorindex+k].data[j])
                                #Add hover data for projection when needed
                                if all(activitiesprojection[len(name_legend)*floorindex+k].data[j].x != np.array([None, None, None])):
                                     
                                    dataprojection = pd.DataFrame({'x': [activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1], activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1]], 
                                                'y': [activitiesprojection[len(name_legend)*floorindex+k].data[j].y[1], activitiesprojection[len(name_legend)*floorindex+k].data[j].y[1]], 
                                                'customdata0': [dateconversion(activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1]), dateconversion(activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1])]})
                                    Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0'])
                                    Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Location: North<br>Level: '+Floorlist[floorindex]+', '+Locationlist[locationindex]+'<br>Activity: '+name_legend[k])
                                    figs.add_traces(Fadd.data[0])
                            k+=1
                k = 0
                if n_R % 2 == 1:
                    while k < len(name_legend):
                            for j in range(len(activitiesfigadditives[len(name_legend)*floorindex+k].data)):
                                activitiesfigadditives[len(name_legend)*floorindex+k].data[j].name = ''
                                figs.add_trace(activitiesfigadditives[len(name_legend)*floorindex+k].data[j])
                                if j <= 0:
                                    pass
                                else:
                                    for a in range(len(activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x)//3):
                                        for b in range(timegap(activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x[3*a].date(), activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x[3*a+1].date())+1):
                                            workingdays.append(activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x[3*a].date()+timedelta(days = b))
                            k+=1             
        
        else:
            if (floorindex == 11 and locationindex == 1) or (floorindex == 12 and locationindex == 1):
                pass
            else:

                #Copy north dataplot actuals flowlines
                if n_R % 2 == 0 and len(flowlineactivitiesfig_layouts_datapoints[floorindex][locationindex])>1:
                    figs.add_trace(flowlineactivitiesfig_layouts_datapoints[floorindex][locationindex][1])
                elif n_R % 2 == 0 and len(flowlineactivitiesfig_layouts_datapoints[floorindex][locationindex])==1:
                    figs.add_trace(flowlineactivitiesfig_layouts_datapoints[floorindex][locationindex][0])
                
                if locationindex==0:
                    activitiesfigadditives = activitiesfigadditivesA
                    activitiesprojection = activitiesprojectionA
                else: 
                    activitiesfigadditives = activitiesfigadditivesB
                    activitiesprojection = activitiesprojectionB
                #Copy north dataplot actuals line of balance
                #Add projection data
                if n_P % 2 == 1 and n_R % 2 == 1:
                        k = 0
                        while k < len(name_legend):
                            for j in range(len(activitiesprojection[len(name_legend)*floorindex+k].data)):
                                activitiesprojection[len(name_legend)*floorindex+k].data[j].name = ''
                                figs.add_trace(activitiesprojection[len(name_legend)*floorindex+k].data[j])
                                #Add hover data for projection when needed
                                if all(activitiesprojection[len(name_legend)*floorindex+k].data[j].x != np.array([None, None, None])):
                                     
                                    dataprojection = pd.DataFrame({'x': [activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1], activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1]], 
                                                'y': [activitiesprojection[len(name_legend)*floorindex+k].data[j].y[1], activitiesprojection[len(name_legend)*floorindex+k].data[j].y[1]], 
                                                'customdata0': [dateconversion(activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1]), dateconversion(activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1])]})
                                    Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0'])
                                    Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Location: North<br>Level: '+Floorlist[floorindex]+', '+Locationlist[locationindex]+'<br>Activity: '+name_legend[k])
                                    figs.add_traces(Fadd.data[0])
                            k+=1
                if n_R % 2 == 1:
                        k = 0
                        while k < len(name_legend):
                            for j in range(len(activitiesfigadditives[len(name_legend)*floorindex+k].data)):
                                activitiesfigadditives[len(name_legend)*floorindex+k].data[j].name = ''
                                figs.add_trace(activitiesfigadditives[len(name_legend)*floorindex+k].data[j])
                                if j <= 0:
                                    pass
                                else:
                                    for a in range(len(activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x)//3):
                                        for b in range(timegap(activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x[3*a].date(), activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x[3*a+1].date())+1):
                                            workingdays.append(activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x[3*a].date()+timedelta(days = b))
                            k+=1
        
        #Copy this layout
        figs.layout = flowlineactivitiesfig_layouts[2*floorindex+locationindex]

    else:

        #Plan case
        if n_A % 3 == 0:
            figs.add_trace(flowlineactivitiesfig_layouts_datapointssth[floorindex][0])

        elif n_A % 3 == 1:
            #Copy south dataplot flowlines
            for i in flowlineactivitiesfig_layouts_datapointssth[floorindex]:
                
                if n_R % 2 == 0:    
                        i.name = ''
                        figs.add_trace(i)
                
                if n_R % 2 == 1:
                        if i.line.dash == 'dash':
                            i.name = ''
                            figs.add_trace(i)

            #Copy south dataplot line of balance
            activitiesfigadditives = activitiesfigadditivesC
            activitiesprojection = activitiesprojectionC

            #Add projection first
            if n_P % 2 == 1 and n_R % 2 == 1:
                        k = 0
                        while k < len(name_legend):
                            for j in range(len(activitiesprojection[len(name_legend)*floorindex+k].data)):
                                activitiesprojection[len(name_legend)*floorindex+k].data[j].name = ''
                                figs.add_trace(activitiesprojection[len(name_legend)*floorindex+k].data[j])
                                #Add hover data for projection when needed
                                if all(activitiesprojection[len(name_legend)*floorindex+k].data[j].x != np.array([None, None, None])):
                                     
                                    dataprojection = pd.DataFrame({'x': [activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1], activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1]], 
                                                'y': [activitiesprojection[len(name_legend)*floorindex+k].data[j].y[1], activitiesprojection[len(name_legend)*floorindex+k].data[j].y[1]], 
                                                'customdata0': [dateconversion(activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1]), dateconversion(activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1])]})
                                    Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0'])
                                    Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Location: South<br>Level: '+Floorlist[floorindex]+'<br>Activity: '+name_legend[k])
                                    figs.add_traces(Fadd.data[0])
                            k+=1

            k = 0
            if n_R % 2 == 1:
                while k < len(name_legend):
                            for j in range(len(activitiesfigadditives[len(name_legend)*floorindex+k].data)):
                                activitiesfigadditives[len(name_legend)*floorindex+k].data[j].name = ''
                                figs.add_trace(activitiesfigadditives[len(name_legend)*floorindex+k].data[j])
                                if j <= 0:
                                    pass
                                else:
                                    for a in range(len(activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x)//3):
                                        for b in range(timegap(activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x[3*a].date(), activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x[3*a+1].date())+1):
                                            workingdays.append(activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x[3*a].date()+timedelta(days = b))
                            k+=1
        
        else:
            if n_R % 2 == 0:
                figs.add_trace(flowlineactivitiesfig_layouts_datapointssth[floorindex][1])
                
            activitiesfigadditives = activitiesfigadditivesC
            activitiesprojection = activitiesprojectionC
            #Copy south dataplot actuals
            #Add projection first
            if n_P % 2 == 1 and n_R % 2 == 1:
                        k = 0
                        while k < len(name_legend):
                            for j in range(len(activitiesprojection[len(name_legend)*floorindex+k].data)):
                                activitiesprojection[len(name_legend)*floorindex+k].data[j].name = ''
                                figs.add_trace(activitiesprojection[len(name_legend)*floorindex+k].data[j])
                                #Add hover data for projection when needed
                                if all(activitiesprojection[len(name_legend)*floorindex+k].data[j].x != np.array([None, None, None])):
                                     
                                    dataprojection = pd.DataFrame({'x': [activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1], activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1]], 
                                                'y': [activitiesprojection[len(name_legend)*floorindex+k].data[j].y[1], activitiesprojection[len(name_legend)*floorindex+k].data[j].y[1]], 
                                                'customdata0': [dateconversion(activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1]), dateconversion(activitiesprojection[len(name_legend)*floorindex+k].data[j].x[1])]})
                                    Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0'])
                                    Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Location: South<br>Level: '+Floorlist[floorindex]+'<br>Activity: '+name_legend[k])
                                    figs.add_traces(Fadd.data[0])
                            k+=1
            if n_R % 2 == 1:
                        k = 0
                        while k < len(name_legend):
                            for j in range(len(activitiesfigadditives[len(name_legend)*floorindex+k].data)):
                                activitiesfigadditives[len(name_legend)*floorindex+k].data[j].name = ''
                                figs.add_trace(activitiesfigadditives[len(name_legend)*floorindex+k].data[j])
                                if j <= 0:
                                    pass
                                else:
                                    for a in range(len(activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x)//3):
                                        for b in range(timegap(activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x[3*a].date(), activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x[3*a+1].date())+1):
                                            workingdays.append(activitiesfigadditives[len(name_legend)*floorindex+k].data[j].x[3*a].date()+timedelta(days = b))
                            k+=1



        #Copy this layout
        figs.layout = flowlineactivitiesfig_layoutssth[floorindex]
    
    #State condition whether activities were finished in the lapse for flowlines and line of flow
    finished = False

    if (n_A % 3 == 1 or n_A % 3 == 2) and n_R % 2 == 0 and [i.y for i in figs.data if i.line.dash == 'solid'] != []:
        if False in [int(i) == round(i, 5) for i in np.concatenate([i.y for i in figs.data if i.line.dash == 'solid']) if math.isnan(i) == False]:
            finished = False
        else:
            finished = True

    if (n_A % 3 == 1 or n_A % 3 == 2) and n_R % 2 == 1 and [i.y for i in figs.data if i.line.color == 'black'] != []:
        if False in [int(i) == round(i, 5) for i in np.concatenate([i.y for i in figs.data if i.line.color == 'black']) if math.isnan(i) == False]:
            finished = False
        else:
            finished = True
    
    if len(workingdays) != 0:
            for i in range(timegap(min(workingdays), max(workingdays))):
                if min(workingdays)+timedelta(days=i) not in workingdays:
                    nonworkingdays.append(min(workingdays)+timedelta(days=i))

            nonworkingdaysranges = [nonworkingdays[0]]

            for i in range(len(nonworkingdays)-1):
                if nonworkingdays[i]+timedelta(days=1) != nonworkingdays[i+1]:
                    nonworkingdaysranges.append(nonworkingdays[i]+timedelta(days=1))
                    nonworkingdaysranges.append(nonworkingdays[i+1])
            nonworkingdaysranges.append(nonworkingdays[-1]+timedelta(days=1))

    #Add shapes for absent days
    if n_C % 2 == 1 and len(workingdays) != 0:
            if finished == False and sorted(list(set(workingdays)))[-1]+timedelta(days=1) < lastdate:
                figs.add_shape(type="rect",
              x0=sorted(list(set(workingdays)))[-1]+timedelta(days=1), x1=lastdate,
              y0=0, y1=1,
              xref='x', yref='paper',
              line=dict(color="black", width=1.5),
              fillcolor = 'black',
              opacity = 0.1)
            for i in range(len(nonworkingdaysranges)//2):
                figs.add_shape(type="rect",
              x0=nonworkingdaysranges[2*i], x1=nonworkingdaysranges[2*i+1],
              y0=0, y1=1,
              xref='x', yref='paper',
              line=dict(color="black", width=1.5),
              fillcolor = 'black',
              opacity = 0.1)
        
    #Add dashed line for last measurement and annotation
    if n_P % 2 == 1 and n_A % 3 != 0 and n_R % 2 == 1 and finished == False:
        if (floorindex == 11 and locationindex == 1) or (floorindex == 12 and locationindex == 1):   
            pass
        else:
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
                                y=6.375,
                                axref = 'pixel',
                                ayref = 'pixel',
                                xref='x', yref='y',
                                font=dict(size=10),
                                showarrow = True,
                                arrowcolor = 'rgba(0,0,0,0)')

    figs.update_layout(showlegend = False)
    
    if n_R % 2 == 1:
        #Creating the colorscale
        figs.add_trace(px.scatter(x=[None, None, None], y=[None, None, None], 
                         color=[0, custom_colorscale[1][0], custom_colorscale[2][0]], 
                         range_color = [0, custom_colorscale[2][0]]).data[0])
        figs.update_coloraxes(colorbar_title='<b>Percentage of<br>Progress (%)<br> <br><b>', colorscale = [[0, 'rgb(255,0,0)'], [custom_colorscale[1][0]/custom_colorscale[2][0], 'rgb(255,212,0)'], [1, 'rgb(52,235,0)']],
                                colorbar_tickmode = 'array', colorbar_ticktext = ['0', '5', '10', '15', '20', '25', '30+'], colorbar_tickvals = [0, 5, 10, 15, 20, 25, 30],
                                colorbar_ticks = 'outside', colorbar_tickwidth = 2, colorbar_ticklen = 8)
    
    if buildingindex == 0:

        if n_A % 3 == 0:
            figs.update_layout(title = dict(text = '<b>Process Flow - North Building (Plan)<b>', font = dict(size = 20)))
        elif n_A % 3 == 1:
            figs.update_layout(title = dict(text = '<b>Process Flow - North Building (Plan v Actual)<b>', font = dict(size = 20)))
        else:
            figs.update_layout(title = dict(text = '<b>Process Flow - North Building (Actual)<b>', font = dict(size = 20)))
    
    else:

        if n_A % 3 == 0:
            figs.update_layout(title = dict(text = '<b>Process Flow - South Building (Plan)<b>', font = dict(size = 20)))
        elif n_A % 3 == 1:
            figs.update_layout(title = dict(text = '<b>Process Flow - South Building (Plan v Actual)<b>', font = dict(size = 20)))
        else:
            figs.update_layout(title = dict(text = '<b>Process Flow - South Building (Actual)<b>', font = dict(size = 20)))
    
    lenplans = len([i for i in figs.data if i.line.dash == 'dash'])
    lenactuals = len([i for i in figs.data if i.line.dash == 'solid'])

    #Replace forecast points from plan+actuals (only actuals with no forecast)
    if n_A % 3 == 1 and n_R % 2 == 0:
        for i in range(len(figs.data)):
            for j in range(len(figs.data[i].x)):
                if figs.data[i].line.dash == 'solid' and figs.data[i].x[j] > datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours = 1):

                    figs.data[i].y[j] = figs.data[i].y[j-1] + (datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours = 1)-figs.data[i].x[j-1])/(figs.data[i].x[j]-figs.data[i].x[j-1])
                    figs.data[i].x[j] = datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours = 1)

    #Add arrows 
    if n_A % 3 == 1 and lenplans != 0 and lenactuals != 0:

        maxplans = maxdate(list([i.x for i in figs.data if i.line.dash == 'dash'][0]))
        maxactuals = maxdate(np.concatenate([i.x for i in figs.data if i.line.dash == 'solid']))

        if n_P % 2 == 0 and maxactuals <= datetime.datetime.combine(lastdate, time(0, 0, 0)):
            #Adjust for finished condition
            if finished == False:
                maxactuals = datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours=1)
            figs.add_shape(type = 'line', x0 = maxplans, x1 = maxactuals, y0 = 6, y1 = 6, xref = 'x', yref = 'y', line=dict(color="red", width=4, dash="solid"), opacity=1)
            figs.add_annotation(x = maxplans+(maxactuals-maxplans)/2, y = 6.125, text = str((maxactuals-maxplans).days)+' days', showarrow = False, font=dict(size = 15, color = 'red'))
            #Create arrowheads
            figs.add_annotation(x=maxplans, y=6, ax=10, ay=10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=maxplans, y=6, ax=10, ay=-10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=maxactuals, y=6, ax=-10, ay=10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=maxactuals, y=6, ax=-10, ay=-10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
        
        if n_P % 2 == 1 and maxactuals > datetime.datetime.combine(lastdate, time(0, 0, 0)):

            figs.add_shape(type = 'line', x0 = maxplans, x1 = datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours=1), y0 = 6, y1 = 6, xref = 'x', yref = 'y', line=dict(color="red", width=4, dash="solid"), opacity=1)
            figs.add_shape(type = 'line', x0 = datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours=1), x1 = maxactuals, y0 = 6, y1 = 6, xref = 'x', yref = 'y', line=dict(color="red", width=4, dash="dash"), opacity=1)
            figs.add_annotation(x = maxplans+(datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours=1)-maxplans)/2, y = 6.125, text = str((datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours=1)-maxplans).days)+' days', showarrow = False, font=dict(size = 15, color = 'red'))
            figs.add_annotation(x = datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours=1)+(maxactuals-datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours=1))/2, y = 6.125, text = str((maxactuals-datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours=1)).days)+' days', showarrow = False, font=dict(size = 15, color = 'red'))
            #Create arrowheads
            figs.add_annotation(x=maxplans, y=6, ax=10, ay=10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=maxplans, y=6, ax=10, ay=-10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours=1), y=6, ax=-10, ay=10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours=1), y=6, ax=-10, ay=-10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours=1), y=6, ax=10, ay=10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=datetime.datetime.combine(lastdate, time(0, 0, 0))-timedelta(hours=1), y=6, ax=10, ay=-10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=maxactuals, y=6, ax=-10, ay=10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=maxactuals, y=6, ax=-10, ay=-10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
        
        if n_P % 2 == 1 and maxactuals <= datetime.datetime.combine(lastdate, time(0, 0, 0)):
            figs.add_shape(type = 'line', x0 = maxplans, x1 = maxactuals, y0 = 6, y1 = 6, xref = 'x', yref = 'y', line=dict(color="red", width=4, dash="solid"), opacity=1)
            figs.add_annotation(x = maxplans+(maxactuals-maxplans)/2, y = 6.125, text = str((maxactuals-maxplans).days)+' days', showarrow = False, font=dict(size = 15, color = 'red'))
            #Create arrowheads
            figs.add_annotation(x=maxplans, y=6, ax=10, ay=10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=maxplans, y=6, ax=10, ay=-10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=maxactuals, y=6, ax=-10, ay=10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
            figs.add_annotation(x=maxactuals, y=6, ax=-10, ay=-10, xref="x", yref="y", axref="pixel", ayref="pixel", text="", showarrow=True, arrowhead=0, arrowwidth=4, arrowcolor="red")
    
    #Add text regarding percentage of days without progress
    if n_C % 2 == 1 and len(workingdays) != 0:
            
            #Calculate ratio by summing the ranges of the shaded rectangles
            nonworkingratio = sum([(i.x1-i.x0).days for i in figs.layout.shapes if i.type == 'rect' and i.fillcolor == 'black'])/(datetime.datetime.combine(lastdate, time(0, 0, 0))-mindate(np.concatenate([i.x for i in figs.data]))).days
            figs.add_annotation(x = 0, y = 6.375, text = 'Percentage of days with no progress: '+str(np.round(100*nonworkingratio, 2))+'%', xref = 'paper', yref = 'y', showarrow = False)
    
    #Fix yaxis range to fit necessary data
    figs.layout.yaxis.range = [-0.25, 6.5]

    #Use extra data to ensure that xaxis range is fixed
    if [i.x for i in figs.data] != []:
        try:
            maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in figs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        except ValueError:
            maxrange = lastdate
    else:
        maxrange = lastdate
    if n_R % 2 == 1 and n_P % 2 == 0 and finished == False:
        maxrange = lastdate
    figs.update_layout(yaxis = dict(range = [-0.35, 6.5]), xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=8)]))
    # Ensuring the x-axis stays as datetime
    figs.update_xaxes(type='date')
    toprightfigs = px.line(x = [maxrange+timedelta(days=8), maxrange+timedelta(days=8)], y = [6.155, 6.155])
    toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
    bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
    bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
    figs.add_traces(toprightfigs.data[0])
    figs.add_traces(bottomleftfigs.data[0])

    return figs

@app.callback(
    [Output('toggle-planactualssns', 'style'),
     Output('toggle-plansns', 'style'),
     Output('toggle-absent-daysns', 'style'),
     Output('toggle-projection-daysns', 'style')],
    [Input('toggle-planactualssns', 'n_clicks'),
     Input('toggle-plansns', 'n_clicks'),
     Input('toggle-absent-daysns', 'n_clicks'),
     Input('toggle-projection-daysns', 'n_clicks')]
)
def update_button_style(n_A, n_R, n_C, n_P):
    # Default style for buttons
    default_style0 = {'backgroundColor': 'green', 'color': 'white', 'height': '30px', 'border-radius': '15px', 'position': 'relative', 'left': '20px', 'width': '210px', 'border-width': '0'}
    active_styleA = default_style0.copy()
    active_styleB = default_style0.copy()
    default_style0['background-color'] = 'green'
    active_styleA['background-color'] = 'red'
    active_styleB['background-color'] = 'blue'
    default_style1 = {'backgroundColor': 'green', 'color': 'white', 'height': '30px', 'border-radius': '15px', 'position': 'relative', 'left': '148px', 'width': '210px', 'border-width': '0'}
    active_style1 = default_style1.copy()
    default_style1['background-color'] = 'green'
    active_style1['background-color'] = 'red'
    if n_A % 3 == 0:
        default_style1['display'] = 'None'
        active_style1['display'] = 'None'
    default_style2 = {'backgroundColor': 'green', 'color': 'white', 'height': '30px', 'border-radius': '15px', 'position': 'relative', 'left': '276px', 'width': '210px', 'border-width': '0'}
    active_style2 = default_style2.copy()
    default_style2['background-color'] = 'green'
    active_style2['background-color'] = 'red'
    if n_A % 3 == 0 or n_R % 2 == 0:
        default_style2['display'] = 'None'
        active_style2['display'] = 'None'
    default_style3 = {'backgroundColor': 'green', 'color': 'white', 'height': '30px', 'border-radius': '15px', 'position': 'relative', 'left': '404px', 'width': '210px', 'border-width': '0'}
    active_style3 = default_style3.copy()
    default_style3['background-color'] = 'green'
    active_style3['background-color'] = 'red'
    if n_A % 3 == 0 or n_R % 2 == 0:
        default_style3['display'] = 'None'
        active_style3['display'] = 'None'

    return (
        default_style0 if n_A % 3 == 0 else active_styleA if n_A % 3 == 1 else active_styleB,
        default_style1 if n_R % 2 == 0 else active_style1,
        default_style2 if n_C % 2 == 1 else active_style2,
        default_style3 if n_P % 2 == 1 else active_style3
    )

@app.callback(
    [Output('toggle-planactualssns', 'children'),
     Output('toggle-plansns', 'children'),
     Output('toggle-absent-daysns', 'children'),
     Output('toggle-projection-daysns', 'children')],
    [Input('toggle-planactualssns', 'n_clicks'),
     Input('toggle-plansns', 'n_clicks'),
     Input('toggle-absent-daysns', 'n_clicks'),
     Input('toggle-projection-daysns', 'n_clicks')]
)
def update_button_style(n_A, n_R, n_C, n_P):

    return (
        'Show Plan and Actual' if n_A % 3 == 0 else 'Show Actual' if n_A % 3 == 1 else 'Show Plan',
        'Thin Flowlines' if n_R % 2 == 0 else 'Line of balance',
        'Hide days with no progress' if n_C % 2 == 1 else 'Show days with no progress',
        'Hide forecast' if n_P % 2 == 1 else 'Show forecast'
    )


@app.callback(
    Output('Activity-dropdowns', 'children'),
    [Input('building-dropdown', 'value')]
)

def update_figure_output(value_building):

    if value_building != None:
        buildingindex = Buildinglist.index(value_building)
        buildingindexlist.append(buildingindex)

    else:
        buildingindex = buildingindexlist[-1]

    if buildingindex == 0 and value_building != None:

        Figure = [
     
    html.Div([dcc.Graph(id='plot-output', style = {'width': '1500px', 'height': '950px'})], style = {'position': 'absolute', 'background-color': 'white'}),
    html.Div([html.Div([dcc.Dropdown(buildinglist, 'North', id='building-dropdown', style={'width':'90px', 'backgroundColor': '#f6f6f6', 'fontFamily': 'Calibri'})], style={'position': 'absolute', 'left': '44px'}),
    html.Div([dcc.Dropdown(floorlist, value = 'L1', id='floor-dropdown', style={'width':'90px', 'backgroundColor': '#f6f6f6', 'fontFamily': 'Calibri'})], style={'position': 'absolute', 'left': '1134px'}),
    html.Div([dcc.Dropdown(locationlist, '1-5', id='location-dropdown', style={'width':'90px', 'backgroundColor': '#f6f6f6', 'fontFamily': 'Calibri'})], style={'position': 'absolute', 'left': '1234px'}),
    html.Div(htmlbuttons2, 
             style={'display':'flex', 'flex-direction': 'row', 
                    'position': 'relative', 'top': '850px', 'left': '22px'})], style = {'display': 'flex', 'flex-direction': 'row', 'position': 'relative', 'top': '10px'})
]

    elif buildingindex == 1 and value_building != None:
        Figure = [
    
    html.Div([dcc.Graph(id='plot-output', style = {'width': '1500px', 'height': '950px'})], style = {'position': 'absolute', 'background-color': 'white'}),
    html.Div([html.Div([dcc.Dropdown(buildinglist, 'South', id='building-dropdown', style={'width':'90px', 'backgroundColor': '#f6f6f6'})], style={'position': 'absolute', 'left': '44px'}),
    html.Div([dcc.Dropdown(floorliststh, value = 'L1', id='floor-dropdown', style={'width':'90px', 'backgroundColor': '#f6f6f6'})], style={'position': 'absolute', 'left': '1234px'}),
    html.Div([dcc.Dropdown(locationlist, id='location-dropdown', style={'width':'90px', 'display': 'None', 'backgroundColor': '#f6f6f6'})], style={'position': 'absolute', 'left': '1334px'}),
    html.Div(htmlbuttons2, 
             style={'display':'flex', 'flex-direction': 'row', 
                    'position': 'relative', 'top': '850px', 'left': '22px'})], style = {'display': 'flex', 'flex-direction': 'row', 'position': 'relative', 'top': '10px'})
]
    
    else:
        raise PreventUpdate

    return Figure

if __name__ == '__main__':
    app.run(debug=True, port=port)



