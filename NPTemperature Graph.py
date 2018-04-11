# -*- coding: utf-8 -*-

'''This script creates high and low Temperature grid plots for all of the national parks, increasing based on the mean yearly temperature.
The data used for these plots are first scraped and organized by using the NPTemperatureScrape script, which uses NOAA data.

These plots were inspired by https://bokeh.pydata.org/en/latest/docs/gallery/unemployment.html
'''

import pandas as pd
import numpy as np
import os
from termcolor import colored
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import (
    ColumnDataSource,
    HoverTool,
    LinearColorMapper,
    LogColorMapper,
    BasicTicker,
    FixedTicker,
    LogTicker,
    PrintfTickFormatter,
    NumeralTickFormatter,
    ColorBar,
    Label,
    Title
)
from bokeh.palettes import Spectral11, Inferno11, Plasma11, inferno, plasma, OrRd9, RdBu11
from bokeh.layouts import row, widgetbox, column, gridplot, layout
from bokeh.models.widgets import Panel, Tabs

Months = ['Jan', 'Feb', "Mar", 'Apr', 'May', 'June', 'Jul', 'Aug','Sep','Oct','Nov','Dec']

dataMax = pd.read_csv("Data/Daily Max Temps NP.csv")
dataMin = pd.read_csv("Data/Daily Min Temps NP.csv")

dataMax = dataMax.set_index('Month')
dataMax = dataMax.T
dataMax.columns = Months

dataMin = dataMin.set_index('Month')
dataMin = dataMin.T
dataMin.columns = Months

dataMax['Mean'] = dataMax.mean(axis=1)
dataMax = dataMax.sort_values('Mean')
dataMin['Mean'] = dataMax.mean(axis=1)
dataMin = dataMin.sort_values('Mean')

parks = list(dataMax.index)
months = list(dataMax.columns)

parks2 = list(dataMin.index)
months2 = list(dataMin.columns)

df = pd.DataFrame(dataMax.stack(), columns=['Rec']).reset_index()
df = df.rename(columns={ df.columns[1]: "Month"})
df = df.rename(columns={ df.columns[0]: "ParkName"})
source = ColumnDataSource(df)

print df

df2 = pd.DataFrame(dataMin.stack(), columns=['Rec']).reset_index()
df2 = df2.rename(columns={ df2.columns[1]: "Month"})
df2 = df2.rename(columns={ df2.columns[0]: "ParkName"})
source2 = ColumnDataSource(df2)

#TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"
TOOLS = "save,hover"

colors2 = ["#6600CC","#8A19FF","#7A33FF","#6B4DFF","#5C66FF","#4C80FF","#3D99FF","#2EB2FF","#1FCCFF",
        "#0FE6FF","#00FFFF","#66FFFF","#80FFFF","#8CFFFF","#99FFFF","#A6FFFF","#B2FFFF","#BFFFFF","#CCFFFF","#D9FFFF","#E6FFFF","#F2FFFF","#FFFFFF"]

tempColor = ['#000066','#000080','#000099','#0019A3','#0040B2','#0066C2','#008CD1','#00B2E0','#00D9F0','#00FFFF','#73FFFF','#B2FFFF',
             '#FFF2F2','#FFCCCC','#FFB2B2','#FF9999','#FF7373','#FF4D4D','#FF0D0D','#CC0000','#A00000','#800000']

mapper = LinearColorMapper(palette=tempColor, low=-20, high=120)

color_bar = ColorBar(color_mapper=mapper,
                     ticker=BasicTicker(desired_num_ticks=5),
                     formatter=NumeralTickFormatter(format="0.0"),
                     label_standoff=15, border_line_color=None, location=(0, 0),title = "Temp.(°F)",
                     major_label_text_color = "black", title_text_color = "black",
                     major_label_text_font_size="8pt", title_text_font_size="13pt", title_standoff = 15 )

#This is the same
color_bar2 = ColorBar(color_mapper=mapper,
                     ticker=BasicTicker(desired_num_ticks=5),
                     formatter=NumeralTickFormatter(format="0.0"),
                     label_standoff=15, border_line_color=None, location=(0, 0),title = "Temp.(°F)",
                     major_label_text_color = "black", title_text_color = "black",
                     major_label_text_font_size="8pt", title_text_font_size="13pt", title_standoff = 15 )

###############################################################################################################################

p = figure(title="Daily High Temperature Averages",
           x_range=parks, y_range=list(reversed(months)),
           x_axis_location="above", plot_width=1000, plot_height=420,
           tools=TOOLS, toolbar_location='right', toolbar_sticky = False)

p.xaxis.axis_label = "Park"
p.yaxis.axis_label = "Month"

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "7pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = 3.14159 / 3

p.rect(x="ParkName", y='Month', width=1, height=1,
       source=source,
       fill_color={'field': 'Rec', 'transform': mapper},
       line_color=None)

p.add_layout(color_bar, 'right')

p.select_one(HoverTool).tooltips = [
     ('Park', '@ParkName'),
     ('Date', '@Month'),
     ('Temp', '@Rec{0.0} °F'),
]

p.add_layout(Title(text="Fill in to fix graph", text_font_style="italic", text_color = "white", text_font_size="6pt"), 'below')
#p.add_layout(Title(text="Title", text_font_size="16pt"), 'below')

layout1 = row(p)

##########################################################################################################################

p2 = figure(title="\n\n\n\nDaily Low Temperature Averages", title_location = 'above',
           x_range=parks2, y_range=list(reversed(months2)),
           x_axis_location="below", plot_width=1000, plot_height=420,
           tools=TOOLS, toolbar_location='right', toolbar_sticky= False)

#p2.xaxis.axis_label = "Park"
p2.yaxis.axis_label = "Month"

p2.grid.grid_line_color = None
p2.axis.axis_line_color = None
p2.axis.major_tick_line_color = None
p2.axis.major_label_text_font_size = "7pt"
p2.axis.major_label_standoff = 0
p2.xaxis.major_label_orientation = 3.14159 / 3

p2.rect(x="ParkName", y='Month', width=1, height=1,
       source=source2,
       fill_color={'field': 'Rec', 'transform': mapper},
       line_color=None)

p2.add_layout(color_bar2, 'right')

p2.select_one(HoverTool).tooltips = [
     ('Park', '@ParkName'),
     ('Date', '@Month'),
     ('Temp', '@Rec{0.0} °F'),
]

l = layout([
  [p],
  [p2],
], sizing_mode='fixed')

##############################################################################################################################

#Needed to be Tabbed for embedding on the website with the AllParks graph.
tabs = []
tab = Panel(child=l, title="Temperatures")
tabs.append(tab)
TABS = Tabs(tabs=tabs)

output_file("HTMLGraphs/NPTemperaturesFINAL.html", title="National Park Temperature Averages")
show(TABS)