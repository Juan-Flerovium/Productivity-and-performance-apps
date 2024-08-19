#!/usr/bin/env python
# coding: utf-8

# In[1]:


import Productivity_dates
from Productivity_dates import figadditives, custom_colorscale, cladding_dates, flowlineactivitiesfig_layouts_datapoints, flowlineactivitiesfig_layouts, figadditivesprojection, name_legend, Flowlines1fig, southfloornamelen, timegap
from Productivity_dates import figadditivessth, figadditivessthprojection, Flowlines1figsth
import numpy as np


# In[2]:


import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import datetime
from datetime import date, timedelta, time
from dash.exceptions import PreventUpdate
import math
import pandas as pd

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


# In[3]:


app3 = dash.Dash(__name__)

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
        htmlbuttons.append(html.Button(name_legend[i], id='toggle-'+str(i+1)+'WPns', n_clicks=n_0, style={'width': '100%', 'backgroundColor': 'white', 
                                                                                                     'color': 'black', 'margin-top': '3px', 'margin-bottom': '3px', 'border-width': '0'}))
        input.append(Input('toggle-'+str(i+1)+'WPns', 'n_clicks'))
        output.append(Output('toggle-'+str(i+1)+'WPns', 'style'))
        outputchildren.append(Output('toggle-'+str(i+1)+'WPns', 'children'))
    elif i == len(name_legend):
        input.append(Input('toggle-planactualssns', 'n_clicks'))
        output.append(Output('toggle-planactualssns', 'style'))
        outputchildren.append(Output('toggle-planactualssns', 'children'))
        htmlbuttons2.append(html.Button('Plan', id='toggle-planactualssns', n_clicks=0, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}))
    elif i == len(name_legend)+1:
        input.append(Input('toggle-plansns', 'n_clicks'))
        output.append(Output('toggle-plansns', 'style'))
        outputchildren.append(Output('toggle-plansns', 'children'))
        htmlbuttons2.append(html.Button('Toggle planned dates', id='toggle-plansns', n_clicks=0, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}))
    elif i == len(name_legend)+2:
        input.append(Input('toggle-absent-daysns', 'n_clicks'))
        output.append(Output('toggle-absent-daysns', 'style'))
        outputchildren.append(Output('toggle-absent-daysns', 'children'))
        htmlbuttons2.append(html.Button('Toggle days with no progress', id='toggle-absent-daysns', n_clicks=0, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}))
    else: 
        input.append(Input('toggle-projection-daysns', 'n_clicks'))
        output.append(Output('toggle-projection-daysns', 'style'))
        outputchildren.append(Output('toggle-projection-daysns', 'children'))
        htmlbuttons2.append(html.Button('Toggle projection days', id='toggle-projection-daysns', n_clicks=0, style={'width': '250px', 'backgroundColor': 'green', 'color': 'white'}))
    
app3.layout = html.Div([
    dcc.Graph(id='plot-outputns', style = {'width': '100%', 'height': '860px', 'backgroundColor': 'white', 'position': 'absolute'}),
    html.Div(htmlbuttons, 
             style={'width': '250px', 'display':'inline-block', 'align-items': 'center', 'vertical-align': 'top',
                    'verticalAlign': 'middle', 'left':'1435px', 'top':'60px', 'position': 'relative'}),
    html.Div(htmlbuttons2, 
             style={'display':'flex', 'flex-direction': 'row', 
                    'position': 'relative', 'top': '570px', 'left': '20px'})], 
    style={'width': '1720px', 'background-color': 'white', 'height': '960px'})

@app3.callback(
        Output('toggle-plansns', 'n_clicks'),
        [Input('toggle-planactualssns', 'n_clicks')]
)

def update_button_click(n_A):
    
    return (
            0 if n_A % 3 == 0 else 0
        )

@app3.callback(
        [Output('toggle-absent-daysns', 'n_clicks'),
         Output('toggle-projection-daysns', 'n_clicks')],
        [Input('toggle-plansns', 'n_clicks')]
)

def update_button_click(n_R):
    
    return (
            1 if n_R % 2 == 0 else 1,
            1 if n_R % 2 == 0 else 1 
        )


@app3.callback(
    Output('plot-outputns', 'figure'),
    input)

def update_plot(n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP, n_A, n_R, n_C, n_P):

    ns = [n_1WP, n_2WP, n_3WP, n_4WP, n_5WP, n_6WP]
    figs = px.line(template='seaborn', title='<b>Activities Progress WPs<b>')
    figssth = px.line(template='seaborn')
    figsnth = px.line(template='seaborn')
    planfigs= px.line(template='seaborn')
    planfigssth = px.line(template='seaborn')
    planfigsnth = px.line(template='seaborn')
    actualfigs = px.line(template='seaborn')
    actualfigssth = px.line(template='seaborn')
    actualfigsnth = px.line(template='seaborn')
    planactualfigs = px.line(template='seaborn')
    planactualfigssth = px.line(template='seaborn')
    planactualfigsnth = px.line(template='seaborn')
    workingdays = []
    nonworkingdays = []

    height = 860
    pixsize = 60
    width  = 1403
    
    #Add tablelike shapes for the yaxis for north and south
    figs.add_shape(type="rect",
              x0=-2*(pixsize/2300), x1=0,
              y0=0, y1=1,
              xref='paper', yref='paper',
              line=dict(color="#ffffff", width=1.5),
              fillcolor = '#eaeaf2',
              opacity = 1,
              layer='below')
    figs.add_shape(type="line",
              x0=-(pixsize/2300), x1=-(pixsize/2300),
              y0=0, y1=1,
              xref='paper', yref='paper',
              line=dict(color="#ffffff", width=1.5),
              opacity = 1)
    
    for i in range(1, 2*cladding_dates[1][1][-2]):
    # Add horizontal line to the margin
        figs.add_shape(type="line",
              x0=-(1+i % 2)*(pixsize/2300), x1=0,
              y0=i/2-1/2, y1=i/2-1/2,
              xref='paper', yref='y',
              line=dict(color="#ffffff", width=1.5),
              opacity = 1)
    # Add annotation to the margin
    for i in range(1, cladding_dates[1][1][-2]):
        figs.add_annotation(
            text='<b>L'+str(i)+'<b>',
            x=-2*(pixsize/2300),
            y=i-1/2,
            xref='paper', yref='y',
            font=dict(size=12),
            showarrow = False )
        figs.add_annotation(
            text='<b>N<b>',
            x=-(pixsize/2300),
            y=i-1/4,
            xref='paper', yref='y',
            font=dict(size=12),
            showarrow = False )
        if i<southfloornamelen+1:
            figs.add_annotation(
            text='<b>S<b>',
            x=-(pixsize/2300),
            y=i-3/4,
            xref='paper', yref='y',
            font=dict(size=12),
            showarrow = False )
        #Add shading for the north building
        figs.add_shape(type="rect",
              x0=-(pixsize/2300), x1=1,
              y0=i-1, y1=i-1/2,
              xref='paper', yref='y',
              line=dict(color="#ffffff", width=1.5),
              fillcolor = '#dadaea',
              opacity = 1,
              layer = 'below')
    figs.add_shape(type="line",
              x0=0, x1=0,
              y0=0, y1=1,
              xref='paper', yref='paper',
              line=dict(color="#ffffff", width=1.5),
              opacity = 1)

    for n in range(len(name_legend)):

        if ns[n] % 2 == 0:

            #Add shapes for projected days
            if n_P % 2 == 0:
                #Add forecast data into main plot
                for i in range(len(figadditivessthprojection[n].data)):
                    figssth.add_trace(figadditivessthprojection[n].data[i])
                    #Add hover data for projection
                    dataprojection = pd.DataFrame({'x': [figadditivessthprojection[n].data[i].x[1], figadditivessthprojection[n].data[i].x[1]], 
                                               'y': [figadditivessthprojection[n].data[i].y[1]-1/2, figadditivessthprojection[n].data[i].y[1]-1/2], 
                                               'customdata0': [figadditivessthprojection[n].data[i].x[1].date(), figadditivessthprojection[n].data[i].x[1].date()],
                                               'customdata1': ['L'+str(int(round(figadditivessthprojection[n].data[i].y[1]))), 'L'+str(int(round(figadditivessthprojection[n].data[i].y[1])))]})
                    Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                    Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Location: South<br>Level: %{customdata[1]}')
                    figssth.add_traces(Fadd.data[0])
                for i in range(len(figadditivesprojection[n].data)):
                    figsnth.add_trace(figadditivesprojection[n].data[i])
                    #Add hover data for projection
                    dataprojection = pd.DataFrame({'x': [figadditivesprojection[n].data[i].x[1], figadditivesprojection[n].data[i].x[1]], 
                                               'y': [figadditivesprojection[n].data[i].y[1], figadditivesprojection[n].data[i].y[1]], 
                                               'customdata0': [figadditivesprojection[n].data[i].x[1].date(), figadditivesprojection[n].data[i].x[1].date()],
                                               'customdata1': ['L'+str(int(round(figadditivesprojection[n].data[i].y[1]))), 'L'+str(int(round(figadditivesprojection[n].data[i].y[1])))]})
                    Fadd = px.line(dataprojection, x = 'x', y = 'y', color_discrete_sequence = 2*['black'], hover_data = ['customdata0', 'customdata1'])
                    Fadd.update_traces(hovertemplate = 'Projected finish: %{customdata[0]}<br>Location: North<br>Level: %{customdata[1]}')
                    figsnth.add_traces(Fadd.data[0])
                
            #Add planned and actual flowlines for north and south except for activity 4
            planfigssth.add_trace(Flowlines1figsth.data[n])
            planfigsnth.add_trace(Flowlines1fig.data[n])
            actualfigsnth.add_trace(Flowlines1fig.data[n+6])
                
            #Add progress flowlines for north and south and account for particular case
            if n != 3:
                #Which is added here instead
                actualfigssth.add_trace(Flowlines1figsth.data[n+6])
                for i in range(len(figadditivessth[n].data)):
                    figadditivessth[n].data[i].name = ''
                    figadditivessth[n].data[i].visible = True
                    figssth.add_trace(figadditivessth[n].data[i])
                    if i <= 0:
                        pass
                    else:
                        for j in range(len(figadditivessth[n].data[i].x)//3):
                            for k in range(timegap(figadditivessth[n].data[i].x[3*j].date(), figadditivessth[n].data[i].x[3*j+1].date())+1):
                                workingdays.append(figadditivessth[n].data[i].x[3*j].date()+timedelta(days = k))
            for i in range(len(figadditives[n].data)):
                figadditives[n].data[i].name = ''
                figadditives[n].data[i].visible = True
                figsnth.add_trace(figadditives[n].data[i])
                if i <= 0:
                        pass
                else:
                    for j in range(len(figadditives[n].data[i].x)//3):
                        for k in range(timegap(figadditives[n].data[i].x[3*j].date(), figadditives[n].data[i].x[3*j+1].date())+1):
                            workingdays.append(figadditives[n].data[i].x[3*j].date()+timedelta(days = k))
    
    #Amend data for y axis to split north and south
    for i in range(len(figssth.data)):
        if len(figssth.data[i].y) >= 3:
            for j in range(len(figssth.data[i].y)//3):
                figssth.data[i].y[3*j] = (figssth.data[i].y[3*j]+int(figssth.data[i].y[3*j]))/2
                figssth.data[i].y[3*j+1] = (figssth.data[i].y[3*j+1]+int(figssth.data[i].y[3*j]))/2
        elif len(figssth.data[i].y) == 2 and figssth.data[i].y[0] != figssth.data[i].y[1]:
            figssth.data[i].y[0] = (figssth.data[i].y[0]+int(figssth.data[i].y[0]))/2
            figssth.data[i].y[1] = (figssth.data[i].y[1]+int(figssth.data[i].y[0]))/2
        else:
            pass
    for i in range(len(figsnth.data)):
        if len(figsnth.data[i].y) >= 3:
            for j in range(len(figsnth.data[i].y)//3):
                figsnth.data[i].y[3*j] = (figsnth.data[i].y[3*j]+int(figsnth.data[i].y[3*j])+1)/2
                figsnth.data[i].y[3*j+1] = (figsnth.data[i].y[3*j+1]+int(figsnth.data[i].y[3*j])+1)/2
        elif len(figsnth.data[i].y) < 3 and figsnth.data[i].y[0] != figsnth.data[i].y[1]:
            figsnth.data[i].y[0] = (figsnth.data[i].y[0]+int(figsnth.data[i].y[0])+1)/2
            figsnth.data[i].y[1] = (figsnth.data[i].y[1]+int(figsnth.data[i].y[0])+1)/2
        else:
            pass
        
    #Add north and south data
    if len(figssth.data) != 0:
        for i in range(len(figssth.data)):
            figs.add_trace(figssth.data[i])
    for i in range(len(figsnth.data)):
        figs.add_trace(figsnth.data[i])
    
    if n_1WP % 2 != 0 and n_2WP % 2 != 0 and n_3WP % 2 != 0 and n_4WP % 2 != 0 and n_5WP % 2 != 0 and n_6WP % 2 != 0:

        raise PreventUpdate

    for i in range(timegap(min(workingdays), max(workingdays))):
        if min(workingdays)+timedelta(days=i) not in workingdays:
            nonworkingdays.append(min(workingdays)+timedelta(days=i))
    
    nonworkingdaysranges = []

    if nonworkingdays != []:
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

    #Copy layout from original plot
    planfigs.layout = figs.layout
    actualfigs.layout = figs.layout
    planactualfigs.layout = figs.layout

    #Add data to planfigs and actualfigs while making a fix on the y axis for planned and actual data for north and south
    for i in range(len(planfigssth.data)):
        for j in range(len(planfigssth.data[i].y)//3):
            planfigssth.data[i].y[3*j] = planfigssth.data[i].y[3*j]-1
            planfigssth.data[i].y[3*j+1] = planfigssth.data[i].y[3*j]+1/2
        planfigs.add_trace(planfigssth.data[i])
    for i in range(len(planfigsnth.data)):
        for j in range(len(planfigsnth.data[i].y)//3):
            planfigsnth.data[i].y[3*j] = planfigsnth.data[i].y[3*j]+1/2
        planfigs.add_trace(planfigsnth.data[i])
    for i in range(len(actualfigssth.data)):
        for j in range(len(actualfigssth.data[i].y)//3):
            actualfigssth.data[i].y[3*j] = actualfigssth.data[i].y[3*j]-1
            actualfigssth.data[i].y[3*j+1] = actualfigssth.data[i].y[3*j]+1/2
        actualfigs.add_trace(actualfigssth.data[i])
    for i in range(len(actualfigsnth.data)):
        for j in range(len(actualfigsnth.data[i].y)//3):
            actualfigsnth.data[i].y[3*j] = actualfigsnth.data[i].y[3*j]+1/2
        actualfigs.add_trace(actualfigsnth.data[i])

    #State condition whether activities were finished in the lapse
    if False in [int(i) == round(i, 5) for i in np.concatenate([i.y for i in figs.data if i.line.color == 'black']) if math.isnan(i) == False]:
        finished = False
    else:
        finished = True

    #Add shapes for absent days
    if n_C % 2 == 0 and nonworkingdaysranges != []:
        if finished == False and sorted(list(set(workingdays)))[-1]+timedelta(days=1) < lastdate:
            figs.add_shape(type="rect",
              x0=sorted(list(set(workingdays)))[-1], x1=lastdate,
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
    if n_P % 2 == 0:
        
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

    #Update size of plot
    figs.update_layout(height=height, width=width)
    #Thicken the lines to seem as 'bars'
    figs.update_traces(line=dict(width=10))
    #Add planned data for the case of the toggle button
    if n_R % 2 == 0:
        for i in range(len(planfigs.data)):
            figs.add_trace(planfigs.data[i])
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Plan v Actual)<b>', font = dict(size = 30)))
    else:
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out - South Building (Actual)<b>', font = dict(size = 30)))

    #Provide scenario for the particular case
    maxdate = max([dateconversion(j) for j in list(np.concatenate([i.x for i in figs.data])) if type(j) == datetime.date or type(j) == datetime.datetime])
    # Update colorbar title and scale
    figs.update_coloraxes(colorbar_title='<b>Percentage of<br>Progress (%)<br> <br><b>', colorscale = [[0, 'rgb(255,0,0)'], [custom_colorscale[1][0]/custom_colorscale[2][0], 'rgb(255,212,0)'], [1, 'rgb(52,235,0)']],
                              colorbar_tickmode = 'array', colorbar_ticktext = ['0', '5', '10', '15', '20', '25', '30+'], colorbar_tickvals = [0, 5, 10, 15, 20, 25, 30],
                              colorbar_ticks = 'outside', colorbar_tickwidth = 2, colorbar_ticklen = 8)

    figs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2])], ticktext = ['']*(cladding_dates[1][1][-2]+1), range = [-0.72, cladding_dates[1][1][-2]-0.28], title_standoff = 80),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxdate+timedelta(days=5)]))

    if n_A % 3 == 0:

        planfigs.update_layout(showlegend = False)
        #Update size of plot
        planfigs.update_layout(height=height, width=width)
        planfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2])], ticktext = ['']*cladding_dates[1][1][-2], range = [-0.72, 13.72], title_standoff = 80),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), lastdate+timedelta(days=5)]))
        planfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out (Plan)<b>', font = dict(size = 30)))
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
        planactualfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2])], ticktext = ['']*cladding_dates[1][1][-2], range = [-0.72, 13.72], title_standoff = 80),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=5)]))
        planactualfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out (Plan v Actual)<b>', font = dict(size = 30)))
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
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out (Plan v Actual)<b>', font = dict(size = 30)))
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in figs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        toprightfigs = px.line(x = [maxrange+timedelta(days=4), maxrange+timedelta(days=4)], y = [13, 13])
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
        actualfigs.update_layout(yaxis = dict(tickmode='array', tickvals = [i for i in range(cladding_dates[1][1][-2])], ticktext = ['']*cladding_dates[1][1][-2], range = [-0.72, 13.72], title_standoff = 80),
                           xaxis = dict(range = [date(2022, 10, 31)-timedelta(days=5), maxrange+timedelta(days=5)]))
        actualfigs.update_layout(title = dict(text = '<b>Flowlines Fit-out (Actual)<b>', font = dict(size = 30)))
        toprightfigs = px.line(x = [maxrange+timedelta(days=4), maxrange+timedelta(days=4)], y = [13, 13])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        actualfigs.add_traces(toprightfigs.data[0])
        actualfigs.add_traces(bottomleftfigs.data[0])
        return actualfigs

    else:
        figs.update_layout(title = dict(text = '<b>Flowlines Fit-out (Actual)<b>', font = dict(size = 30)))
        #Use extra data to ensure that xaxis range is fixed
        maxrange = max([datetimeconversion(i) for i in np.concatenate([i.x for i in figs.data]) if type(i) == datetime.date or type(i) == datetime.datetime])
        toprightfigs = px.line(x = [maxrange+timedelta(days=4), maxrange+timedelta(days=4)], y = [13, 13])
        toprightfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        bottomleftfigs = px.line(x = [date(2022, 10, 31)-timedelta(days=5), date(2022, 10, 31)-timedelta(days=5)], y = [0, 0])
        bottomleftfigs.update_traces(hoverinfo = 'none', hovertemplate = None)
        figs.add_traces(toprightfigs.data[0])
        figs.add_traces(bottomleftfigs.data[0])
        return figs

@app3.callback(
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
        default_style3 if n_P % 2 == 0 else active_style3
    )

@app3.callback(
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
    app3.run_server(debug=True, port=8053)

