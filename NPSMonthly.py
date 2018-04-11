'''This script creates a 2D grid of monthly visitation for each park and organizes the data based on the month of July.

The code for this plot was inspired by https://bokeh.pydata.org/en/latest/docs/gallery/unemployment.html

'''

import pandas as pd
import numpy as np
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
)
from bokeh.palettes import Spectral11, Inferno11, Plasma11, inferno, plasma, OrRd9
from bokeh.models.widgets import Panel, Tabs

#custom teal/purple color pallete
colors2 = ["#6600CC","#8A19FF","#7A33FF","#6B4DFF","#5C66FF","#4C80FF","#3D99FF","#2EB2FF","#1FCCFF",
        "#0FE6FF","#00FFFF","#66FFFF","#80FFFF","#8CFFFF","#99FFFF","#A6FFFF","#B2FFFF","#BFFFFF","#CCFFFF","#D9FFFF","#E6FFFF","#F2FFFF","#FFFFFF"]

pd.options.display.float_format = '{:,.0f}'.format

data = pd.read_csv("Data/NPSMonthly.csv", skiprows=2)
col_list = ["ParkName","Month","RecreationVisits"]
#data2 = data.apply(lambda x: x.str.replace(',',''))
data['Rec'] = data['RecreationVisits'].str.replace(',', '')
data.drop(['RecreationVisits'],axis=1, inplace=True)
data3 = data.apply(pd.to_numeric, errors = 'ignore', downcast = 'float')
data3 = data3.pivot(index="ParkName",columns="Month",values = "Rec")
#print data3.head()

data3.sort_values(7, inplace=True)
data4 = data3.T
data4['Total Month'] = data4.sum(axis=1)
data4 = data4.T
data4['Total'] = data4.sum(axis=1)
#print data4
#data3["Annual"] = data3.sum(axis=1)

monthname = ['Jan', 'Feb', "Mar", 'Apr', 'May', 'June', 'Jul', 'Aug','Sep','Oct','Nov','Dec']
#data3 = data3.pivot(index="ParkName",columns="Month",values = "Rec")
data3.columns = monthname
#print data3

parks = list(data3.index)
months = list(data3.columns)

df = pd.DataFrame(data3.stack(), columns=['Rec']).reset_index()
df = df.rename(columns={ df.columns[1]: "Month" })

source = ColumnDataSource(df)

TOOLS = "hover,save,pan,box_zoom,reset,wheel_zoom"

p = figure(title="Monthly Recreational Visitors 2017",
           x_range=parks, y_range=list(reversed(months)),
           x_axis_location="above", plot_width=1000, plot_height=420,
           tools=TOOLS, toolbar_location='below')

p.xaxis.axis_label = "Park"
p.yaxis.axis_label = "Month"

p.grid.grid_line_color = None
p.axis.axis_line_color = None
p.axis.major_tick_line_color = None
p.axis.major_label_text_font_size = "7pt"
p.axis.major_label_standoff = 0
p.xaxis.major_label_orientation = 3.14159 / 3

mapper = LogColorMapper(palette=list(reversed(colors2)), low=0, high=1500000)
p.rect(x="ParkName", y='Month', width=1, height=1,
       source=source,
       fill_color={'field': 'Rec', 'transform': mapper},
       line_color=None)

color_bar = ColorBar(color_mapper=mapper,
                     ticker=FixedTicker(ticks=[0,1,10,100,1000,10000,100000, 1000000]),
                     formatter=NumeralTickFormatter(format="0,0"),
                     label_standoff=15, border_line_color=None, location=(0, 0),title = "# of Visitors",
                     major_label_text_color = "black", title_text_color = "black",
                     major_label_text_font_size="8pt", title_text_font_size="12pt" )
p.add_layout(color_bar, 'right')

p.select_one(HoverTool).tooltips = [
     ('Park', '@ParkName'),
     ('Date', '@Month'),
     ('Visitors', '@Rec{0,0}'),
]

#Tabs were needed for embedding on the website. If tabs were not used for all bokeh graphs, only non tabbed graphs would appear.

tabs = []
tab = Panel(child=p, title="Monthly Visitor Statistics")
tabs.append(tab)
TABS = Tabs(tabs=tabs)

output_file("HTMLGraphs/NPMontlyVisitors2017.html", title="National Park Monthly Visitors 2017")

show(TABS)      # show the plot




