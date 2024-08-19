#!/usr/bin/env python
# coding: utf-8

# In[2]:


import Productivity_dates
from Productivity_dates import figadditives, custom_colorscale, cladding_dates, flowlineactivitiesfig_layouts_datapoints, flowlineactivitiesfig_layouts, figadditivesprojection, name_legend, Flowlines1fig, southfloornamelen, timegap
from Productivity_dates import figadditivessth, figadditivessthprojection, Flowlines1figsth
import numpy as np
import math
import pandas as pd


# In[3]:


import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import datetime
from datetime import date, timedelta, time
from dash.exceptions import PreventUpdate

lastdate = date(2023, 9, 29)
def dateconversion(x):
    if type(x) == datetime.date:
        return x
    else:
        return x.date()

def datetimeconversion(x):
    if type(x) == date:
        return datetime.combine(x, time(0, 0, 0))
    else:
        return x

app1 = dash.Dash(__name__)
server1 = app1.server

# Get the port from the environment variable
port = int(os.environ.get("PORT", 8051))

htmlbuttons = [html.Div(html.Span('Fit-out Activities', style = {'font-family': 'Arial, sans-serif', 'font-size': '20px', 'font-weight': 'bold', 'text-decoration': 'underline'}), style={'margin-bottom': '30px', 'margin-left': '20px'})]
htmlbuttons2 = []
input = []
output = []
outputchildren = []
colorset = [px.colors.qualitative.G10[i] for i in range(len(name_legend))]

for i in range(len(name_legend)+4):
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
        input.append(Input('toggle-planactuals', 'n_clicks'))
        output.append(Output('toggle-planactuals', 'style'))
        outputchildren.append(Output('toggle-planactuals', 'children'))
        htmlbuttons2.append(html.Button('Plan', id='toggle-planactuals', n_clicks=0, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}))
    elif i == len(name_legend)+1:
        input.append(Input('toggle-plans', 'n_clicks'))
        output.append(Output('toggle-plans', 'style'))
        outputchildren.append(Output('toggle-plans', 'children'))
        htmlbuttons2.append(html.Button('Toggle planned dates', id='toggle-plans', n_clicks=0, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}))
    elif i == len(name_legend)+2:
        input.append(Input('toggle-absent-days', 'n_clicks'))
        output.append(Output('toggle-absent-days', 'style'))
        outputchildren.append(Output('toggle-absent-days', 'children'))
        htmlbuttons2.append(html.Button('Toggle days with no progress', id='toggle-absent-days', n_clicks=0, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}))
    else: 
        input.append(Input('toggle-projection-days', 'n_clicks'))
        output.append(Output('toggle-projection-days', 'style'))
        outputchildren.append(Output('toggle-projection-days', 'children'))
        htmlbuttons2.append(html.Button('Toggle projection days', id='toggle-projection-days', n_clicks=0, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}))
    
app1.layout = html.Div([
    dcc.Graph(id='plot-output', style = {'width': '100%', 'height': '860px', 'backgroundColor': 'white', 'position': 'absolute'}),
    html.Div(htmlbuttons, 
             style={'width': '250px', 'display':'inline-block', 'align-items': 'center', 'vertical-align': 'top',
                    'verticalAlign': 'middle', 'left':'1435px', 'top':'60px', 'position': 'relative'}),
    html.Div(htmlbuttons2, 
             style={'display':'flex', 'flex-direction': 'row', 
                    'position': 'relative', 'top': '570px', 'left': '22px'})], 
    style={'width': '1720px', 'background-color': 'white', 'height': '960px'})

@app1.callback(
        Output('toggle-plans', 'n_clicks'),
        [Input('toggle-planactuals', 'n_clicks')]
)

def update_button_click(n_A):
    
    return (
            0 if n_A % 3 == 0 else 0
        )

@app1.callback(
        [Output('toggle-absent-days', 'n_clicks'),
         Output('toggle-projection-days', 'n_clicks')],
        [Input('toggle-plans', 'n_clicks')]
)

def update_button_click(n_R):
    
    return (
            1 if n_R % 2 == 0 else 1,
            1 if n_R % 2 == 0 else 1 
        )

@app1.callback(
    Output('plot-output', 'figure'),
    input)

def update_plot(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, n_A, n_R, n_C, n_P):

    figs = px.line(template='seaborn', title='<b>Activities Progress WPs<b>')
    planfigs = px.line(template='seaborn')
    actualfigs = px.line(template='seaborn')
    planactualfigs = px.line(template='seaborn')
    workingdays = []
    nonworkingdays = []

    if n_1WP % 2 == 0:

        #Add shapes for projected days
        if n_P % 2 == 0:
            for i in range(len(figadditivesprojection[0].data)):
                figs.add_trace(figadditivesprojection[0].data[i])
                #Add hover data for projection
                dataprojection = pd.DataFrame({'x': [figadditivesprojection[0].data[i].x[1], figadditivesprojection[0].data[i].x[1]], 
                                               'y': [figadditivesprojection[0].data[i].y[1], figadditivesprojection[0].data[i].y[1]], 
                                               'customdata0': [figadditivesprojection[0].data[i].x[1].date(), figadditivesprojection[0].data[i].x[1].date()],
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
                    for k in range(timegap(figadditives[0].data[i].x[3*j].date(), figadditives[0].data[i].x[3*j+1].date())+1):
                        workingdays.append(figadditives[0].data[i].x[3*j].date()+timedelta(days = k))

        for i in figadditives[0].layout.shapes:
            figs.add_shape(i)

    if n_2WP % 2 == 0:

        #Add shapes for projected days
        if n_P % 2 == 0:
            for i in range(len(figadditivesprojection[1].data)):
                figs.add_trace(figadditivesprojection[1].data[i])
                #Add hover data for projection
                dataprojection = pd.DataFrame({'x': [figadditivesprojection[1].data[i].x[1], figadditivesprojection[1].data[i].x[1]], 
                                               'y': [figadditivesprojection[1].data[i].y[1], figadditivesprojection[1].data[i].y[1]], 
                                               'customdata0': [figadditivesprojection[1].data[i].x[1].date(), figadditivesprojection[1].data[i].x[1].date()],
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
                    for k in range(timegap(figadditives[1].data[i].x[3*j].date(), figadditives[1].data[i].x[3*j+1].date())+1):
                        workingdays.append(figadditives[1].data[i].x[3*j].date()+timedelta(days = k))
        
        for i in figadditives[1].layout.shapes:
            figs.add_shape(i)

    if n_3WP % 2 == 0:

        #Add shapes for projected days
        if n_P % 2 == 0:
            for i in range(len(figadditivesprojection[2].data)):
                figs.add_trace(figadditivesprojection[2].data[i])
                #Add hover data for projection
                dataprojection = pd.DataFrame({'x': [figadditivesprojection[2].data[i].x[1], figadditivesprojection[2].data[i].x[1]], 
                                               'y': [figadditivesprojection[2].data[i].y[1], figadditivesprojection[2].data[i].y[1]], 
                                               'customdata0': [figadditivesprojection[2].data[i].x[1].date(), figadditivesprojection[2].data[i].x[1].date()],
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
                    for k in range(timegap(figadditives[2].data[i].x[3*j].date(), figadditives[2].data[i].x[3*j+1].date())+1):
                        workingdays.append(figadditives[2].data[i].x[3*j].date()+timedelta(days = k))

        for i in figadditives[2].layout.shapes:
            figs.add_shape(i)

    if n_4WP % 2 == 0:

        #Add shapes for projected days
        if n_P % 2 == 0:
            for i in range(len(figadditivesprojection[3].data)):
                figs.add_trace(figadditivesprojection[3].data[i])
                #Add hover data for projection
                dataprojection = pd.DataFrame({'x': [figadditivesprojection[3].data[i].x[1], figadditivesprojection[3].data[i].x[1]], 
                                               'y': [figadditivesprojection[3].data[i].y[1], figadditivesprojection[3].data[i].y[1]], 
                                               'customdata0': [figadditivesprojection[3].data[i].x[1].date(), figadditivesprojection[3].data[i].x[1].date()],
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
                    for k in range(timegap(figadditives[3].data[i].x[3*j].date(), figadditives[3].data[i].x[3*j+1].date())+1):
                        workingdays.append(figadditives[3].data[i].x[3*j].date()+timedelta(days = k))
        
        for i in figadditives[3].layout.shapes:
            figs.add_shape(i)

    if n_5WP % 2 == 0:

        #Add shapes for projected days
        if n_P % 2 == 0:
            for i in range(len(figadditivesprojection[4].data)):
                figs.add_trace(figadditivesprojection[4].data[i])
                #Add hover data for projection
                dataprojection = pd.DataFrame({'x': [figadditivesprojection[4].data[i].x[1], figadditivesprojection[4].data[i].x[1]], 
                                               'y': [figadditivesprojection[4].data[i].y[1], figadditivesprojection[4].data[i].y[1]], 
                                               'customdata0': [figadditivesprojection[4].data[i].x[1].date(), figadditivesprojection[4].data[i].x[1].date()],
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
                    for k in range(timegap(figadditives[4].data[i].x[3*j].date(), figadditives[4].data[i].x[3*j+1].date())+1):
                        workingdays.append(figadditives[4].data[i].x[3*j].date()+timedelta(days = k))
        
        for i in figadditives[4].layout.shapes:
            figs.add_shape(i)

    if n_6WP % 2 == 0:

        #Add shapes for projected days
        if n_P % 2 == 0:
            for i in range(len(figadditivesprojection[5].data)):
                figs.add_trace(figadditivesprojection[5].data[i])
                #Add hover data for projection
                dataprojection = pd.DataFrame({'x': [figadditivesprojection[5].data[i].x[1], figadditivesprojection[5].data[i].x[1]], 
                                               'y': [figadditivesprojection[5].data[i].y[1], figadditivesprojection[5].data[i].y[1]], 
                                               'customdata0': [figadditivesprojection[5].data[i].x[1].date(), figadditivesprojection[5].data[i].x[1].date()],
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
                    for k in range(timegap(figadditives[5].data[i].x[3*j].date(), figadditives[5].data[i].x[3*j+1].date())+1):
                        workingdays.append(figadditives[5].data[i].x[3*j].date()+timedelta(days = k))
        
        for i in figadditives[5].layout.shapes:
            figs.add_shape(i)
    
    if n_1WP % 2 != 0 and n_2WP % 2 != 0 and n_3WP % 2 != 0 and n_4WP % 2 != 0 and n_5WP % 2 != 0 and n_6WP % 2 != 0:

        raise PreventUpdate

    for i in range(timegap(min(workingdays), max(workingdays))):
        if min(workingdays)+timedelta(days=i) not in workingdays:
            nonworkingdays.append(min(workingdays)+timedelta(days=i))

    nonworkingdaysranges = [nonworkingdays[0]]
    
    for i in range(len(nonworkingdays)-1):
        if nonworkingdays[i]+timedelta(days=1) != nonworkingdays[i+1]:
            nonworkingdaysranges.append(nonworkingdays[i]+timedelta(days=1))
            nonworkingdaysranges.append(nonworkingdays[i+1])
    nonworkingdaysranges.append(nonworkingdays[-1]+timedelta(days=1))
    
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
    if False in [int(i) == round(i, 5) for i in np.concatenate([i.y for i in figs.data if i.line.color == 'black']) if math.isnan(i) == False]:
        finished = False
    else:
        finished = True

    #Add dashed line for last measurement and annotation
    if n_P % 2 == 0 and finished == False:
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
    if n_C % 2 == 0:
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
    
    if n_A % 3 == 0:

        planfigs.update_layout(showlegend = False)
        #Update size of plot
        planfigs.update_layout(height=height, width=width)
        #Use extra data to ensure that xaxis range is fixed
        planfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2])], ticktext = ['']*cladding_dates[1][1][-2], range = [-0.7, 13.7], title_standoff = 50),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), lastdate+timedelta(days=5)]))
        planfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out - North Building (Plan)<b>', font = dict(size = 25)))
        toprightfigs = px.line(x = [lastdate+timedelta(days=5), lastdate+timedelta(days=5)], y = [13, 13])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        planfigs.add_traces(toprightfigs.data[0])
        planfigs.add_traces(bottomleftfigs.data[0])
        return planfigs
    
    elif n_A % 3 == 1 and n_R % 2 == 0:
        for i in range(len(planfigs.data)):
            planactualfigs.add_trace(planfigs.data[i])
        for i in range(len(actualfigs.data)):
            planactualfigs.add_trace(actualfigs.data[i])
        planactualfigs.update_layout(showlegend = False)
        #Update size of plot
        planactualfigs.update_layout(height=height, width=width)
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in planactualfigs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        planactualfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2])], ticktext = ['']*cladding_dates[1][1][-2], range = [-0.7, 13.7], title_standoff = 50),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=5)]))
        planactualfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out - North Building (Plan v Actual)<b>', font = dict(size = 25)))
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [13, 13])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        planactualfigs.add_traces(toprightfigs.data[0])
        planactualfigs.add_traces(bottomleftfigs.data[0])
        return planactualfigs
        
    elif n_A % 3 == 1 and n_R % 2 == 1:

        for i in range(len(planfigs.data)):
            figs.add_trace(planfigs.data[i])
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - North Building (Plan v Actual)<b>', font = dict(size = 25)))
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in figs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [13, 13])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        figs.add_traces(toprightfigs.data[0])
        figs.add_traces(bottomleftfigs.data[0])
        return figs
    
    elif n_A % 3 == 2 and n_R % 2 == 0:

        actualfigs.update_layout(showlegend = False)
        #Update size of plot
        actualfigs.update_layout(height=height, width=width)
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in actualfigs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        actualfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2])], ticktext = ['']*cladding_dates[1][1][-2], range = [-0.7, 13.7], title_standoff = 50),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=5)]))
        actualfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out - North Building (Actual)<b>', font = dict(size = 25)))
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [13, 13])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        actualfigs.add_traces(toprightfigs.data[0])
        actualfigs.add_traces(bottomleftfigs.data[0])
        return actualfigs

    else:
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - North Building (Actual)<b>', font = dict(size = 25)))
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in figs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [13, 13])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        figs.add_traces(toprightfigs.data[0])
        figs.add_traces(bottomleftfigs.data[0])
        return figs
    
@app1.callback(
    output,
    input
)
def update_button_style(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, n_A, n_R, n_C, n_P):
    # Default style for buttons
    default_style = {'width': '100%', 'backgroundColor': 'white', 'color': 'black', 'margin-bottom':'5px', 'margin-bottom':'5px', 'height': '30px', 'border-radius': '10px', 'text-align': 'left',
                     'border-width': '0'}
    active_style = default_style.copy()
    default_style['color'] = 'black'
    active_style['color'] = '#aaa'
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
        default_style if n_1WP % 2 == 0 else active_style,
        default_style if n_2WP % 2 == 0 else active_style,
        default_style if n_3WP % 2 == 0 else active_style,
        default_style if n_4WP % 2 == 0 else active_style,
        default_style if n_5WP % 2 == 0 else active_style,
        default_style if n_6WP % 2 == 0 else active_style,
        default_style0 if n_A % 3 == 0 else active_styleA if n_A % 3 == 1 else active_styleB,
        default_style1 if n_R % 2 == 0 else active_style1,
        default_style2 if n_C % 2 == 0 else active_style2,
        default_style3 if n_P % 2 == 0 else active_style3,
    )

@app1.callback(
    outputchildren,
    input
)
def update_button_style(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, n_A, n_R, n_C, n_P):
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
        'Show Plan and Actual' if n_A % 3 == 0 else 'Show Actual' if n_A % 3 == 1 else 'Show Plan',
        'Thin Flowlines' if n_R % 2 == 0 else 'Line of balance',
        'Hide days with no progress' if n_C % 2 == 0 else 'Show days with no progress',
        'Hide forecast' if n_P % 2 == 0 else 'Show forecast'
    )

if __name__ == '__main__':
    app1.run_server(debug=True, port=port)


# In[4]:


type(datetime.datetime(2023, 6, 5, 0, 0))


# In[5]:


app2 = dash.Dash(__name__)
server2 = app2.server

# Get the port from the environment variable
port = int(os.environ.get("PORT", 8052))

htmlbuttons = [html.Div(html.Span('Fit-out Activities', style = {'font-family': 'Arial, sans-serif', 'font-size': '20px', 'font-weight': 'bold', 'text-decoration': 'underline'}), style={'margin-bottom': '30px', 'margin-left': '20px'})]
htmlbuttons2 = []
input = []
output = []
outputchildren = []
colorset = [px.colors.qualitative.G10[i] for i in range(len(name_legend))]

for i in range(len(name_legend)+4):
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
        input.append(Input('toggle-planactualssth', 'n_clicks'))
        output.append(Output('toggle-planactualssth', 'style'))
        outputchildren.append(Output('toggle-planactualssth', 'children'))
        htmlbuttons2.append(html.Button('Plan', id='toggle-planactualssth', n_clicks=0, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}))
    elif i == len(name_legend)+1:
        input.append(Input('toggle-planssth', 'n_clicks'))
        output.append(Output('toggle-planssth', 'style'))
        outputchildren.append(Output('toggle-planssth', 'children'))
        htmlbuttons2.append(html.Button('Toggle planned dates', id='toggle-planssth', n_clicks=0, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}))
    elif i == len(name_legend)+2:
        input.append(Input('toggle-absent-dayssth', 'n_clicks'))
        output.append(Output('toggle-absent-dayssth', 'style'))
        outputchildren.append(Output('toggle-absent-dayssth', 'children'))
        htmlbuttons2.append(html.Button('Toggle days with no progress', id='toggle-absent-dayssth', n_clicks=1, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}))
    else: 
        input.append(Input('toggle-projection-dayssth', 'n_clicks'))
        output.append(Output('toggle-projection-dayssth', 'style'))
        outputchildren.append(Output('toggle-projection-dayssth', 'children'))
        htmlbuttons2.append(html.Button('Toggle projection days', id='toggle-projection-dayssth', n_clicks=1, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}))
    
app2.layout = html.Div([
    dcc.Graph(id='plot-outputsth', style = {'width': '100%', 'height': '860px', 'backgroundColor': 'white', 'position': 'absolute'}),
    html.Div(htmlbuttons, 
             style={'width': '250px', 'display':'inline-block', 'align-items': 'center', 'vertical-align': 'top',
                    'verticalAlign': 'middle', 'left':'1435px', 'top':'60px', 'position': 'relative'}),
    html.Div(htmlbuttons2, 
             style={'display':'flex', 'flex-direction': 'row', 
                    'position': 'relative', 'top': '570px', 'left': '22px'})], 
    style={'width': '1720px', 'background-color': 'white', 'height': '960px'})

@app2.callback(
        Output('toggle-planssth', 'n_clicks'),
        [Input('toggle-planactualssth', 'n_clicks')]
)

def update_button_click(n_A):
    
    return (
            0 if n_A % 3 == 0 else 0
        )

@app2.callback(
        [Output('toggle-absent-dayssth', 'n_clicks'),
         Output('toggle-projection-dayssth', 'n_clicks')],
        [Input('toggle-planssth', 'n_clicks')]
)

def update_button_click(n_R):
    
    return (
            1 if n_R % 2 == 0 else 1,
            1 if n_R % 2 == 0 else 1 
        )

@app2.callback(
    Output('plot-outputsth', 'figure'),
    input)

def update_plot(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, n_A, n_R, n_C, n_P):

    figs = px.line(template='seaborn', title='<b>Activities Progress WPs<b>')
    planfigs = px.line(template='seaborn')
    actualfigs = px.line(template='seaborn')
    planactualfigs = px.line(template='seaborn')
    workingdays = []
    nonworkingdays = []

    if n_1WP % 2 == 0:

        #Add shapes for projected days
        if n_P % 2 == 0:
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
        if n_P % 2 == 0:
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
        if n_P % 2 == 0:
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
        if n_P % 2 == 0:
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
        if n_P % 2 == 0:
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

    if n_1WP % 2 != 0 and n_2WP % 2 != 0 and n_3WP % 2 != 0 and n_4WP % 2 == 0 and n_5WP % 2 != 0 and n_6WP % 2 != 0:
        pass
    else:
        for i in range(timegap(min(workingdays), max(workingdays))):
            if min(workingdays)+timedelta(days=i) not in workingdays:
                nonworkingdays.append(min(workingdays)+timedelta(days=i))

        nonworkingdaysranges = [nonworkingdays[0]]
        
        for i in range(len(nonworkingdays)-1):
            if nonworkingdays[i]+timedelta(days=1) != nonworkingdays[i+1]:
                nonworkingdaysranges.append(nonworkingdays[i]+timedelta(days=1))
                nonworkingdaysranges.append(nonworkingdays[i+1])
        nonworkingdaysranges.append(nonworkingdays[-1]+timedelta(days=1))

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

    #Add shapes for absent days
    if n_C % 2 == 0 and n_1WP % 2 != 0 and n_2WP % 2 != 0 and n_3WP % 2 != 0 and n_4WP % 2 == 0 and n_5WP % 2 != 0 and n_6WP % 2 != 0:
        pass
    elif n_C % 2 == 0:
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
  
    figs.update_layout(showlegend = False)

    #Add dashed line for last measurement and annotation in the conditional forecast
    if n_P % 2 == 0 and finished == False:
        
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
    if n_R % 2 == 0:
        for i in range(len(planfigs.data)):
            figs.add_trace(planfigs.data[i])
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Plan v Actual)<b>', font = dict(size = 20)))
    else:
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Actual)<b>', font = dict(size = 20)))

    #Provide scenario for the particular case
    if n_1WP % 2 != 0 and n_2WP % 2 != 0 and n_3WP % 2 != 0 and n_4WP % 2 == 0 and n_5WP % 2 != 0 and n_6WP % 2 != 0:

        #Prevent plan error in this case
        if n_R % 2 != 0:
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

    if n_A % 3 == 0:

        planfigs.update_layout(showlegend = False)
        #Update size of plot
        planfigs.update_layout(height=height, width=width)
        planfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(southfloornamelen+1)], ticktext = ['']*(southfloornamelen+1), range = [-0.43, southfloornamelen+0.43], title_standoff = 50),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), lastdate+timedelta(days=5)]))
        planfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Plan)<b>', font = dict(size = 25)))
        #Use extra data to ensure that xaxis range is fixed
        maxrange = lastdate
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [8, 8])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        planfigs.add_traces(toprightfigs.data[0])
        planfigs.add_traces(bottomleftfigs.data[0])
        return planfigs
    
    elif n_A % 3 == 1 and n_R % 2 == 0:
        for i in range(len(planfigs.data)):
            planactualfigs.add_trace(planfigs.data[i])
        for i in range(len(actualfigs.data)):
            planactualfigs.add_trace(actualfigs.data[i])
        planactualfigs.update_layout(showlegend = False)
        #Update size of plot
        planactualfigs.update_layout(height=height, width=width)
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in planactualfigs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
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
    
    elif n_A % 3 == 1 and n_R % 2 == 1:

        for i in range(len(planfigs.data)):
            figs.add_trace(planfigs.data[i])
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in figs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        if finished == False and n_P % 2 == 1:
            maxrange = lastdate
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Plan v Actual)<b>', font = dict(size = 25)), xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=5)]))
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [8, 8])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        figs.add_traces(toprightfigs.data[0])
        figs.add_traces(bottomleftfigs.data[0])
        return figs
    
    elif n_A % 3 == 2 and n_R % 2 == 0:

        actualfigs.update_layout(showlegend = False)
        #Update size of plot
        actualfigs.update_layout(height=height, width=width)
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in actualfigs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        actualfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(southfloornamelen+1)], ticktext = ['']*(southfloornamelen+1), range = [-0.43, southfloornamelen+0.43], title_standoff = 50),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=5)]))
        actualfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Actual)<b>', font = dict(size = 25)))
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [8, 8])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        actualfigs.add_traces(toprightfigs.data[0])
        actualfigs.add_traces(bottomleftfigs.data[0])
        return actualfigs

    else:
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in figs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        if finished == False and n_P % 2 == 1:
            maxrange = lastdate
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Actual)<b>', font = dict(size = 25)), xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=5)]))
        toprightfigs = px.line(x = [maxrange+timedelta(days=5), maxrange+timedelta(days=5)], y = [8, 8])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        figs.add_traces(toprightfigs.data[0])
        figs.add_traces(bottomleftfigs.data[0])
        return figs

    
    

@app2.callback(
    output,
    input
)
def update_button_style(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, n_A, n_R, n_C, n_P):
    # Default style for buttons
    default_style = {'width': '100%', 'backgroundColor': 'white', 'color': 'black', 'margin-bottom':'5px', 'margin-bottom':'5px', 'height': '30px', 'border-radius': '10px', 'text-align': 'left',
                     'border-width': '0'}
    active_style = default_style.copy()
    default_style['color'] = 'black'
    active_style['color'] = '#aaa'
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
        default_style if n_1WP % 2 == 0 else active_style,
        default_style if n_2WP % 2 == 0 else active_style,
        default_style if n_3WP % 2 == 0 else active_style,
        default_style if n_4WP % 2 == 0 else active_style,
        default_style if n_5WP % 2 == 0 else active_style,
        default_style if n_6WP % 2 == 0 else active_style,
        default_style0 if n_A % 3 == 0 else active_styleA if n_A % 3 == 1 else active_styleB,
        default_style1 if n_R % 2 == 0 else active_style1,
        default_style2 if n_C % 2 == 0 else active_style2,
        default_style3 if n_P % 2 == 0 else active_style3,
    )

@app2.callback(
    outputchildren,
    input
)
def update_button_style(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, n_A, n_R, n_C, n_P):
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
        'Show Plan and Actual' if n_A % 3 == 0 else 'Show Actual' if n_A % 3 == 1 else 'Show Plan',
        'Thin Flowlines' if n_R % 2 == 0 else 'Line of balance',
        'Hide days with no progress' if n_C % 2 == 0 else 'Show days with no progress',
        'Hide forecast' if n_P % 2 == 0 else 'Show forecast'
    )
#app2.write_html('testapp2')
if __name__ == '__main__':
    app2.run_server(debug=True, port=port)

