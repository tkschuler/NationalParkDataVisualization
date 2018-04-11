'''This script creates a 3D scatterplot using Acreage, Camping, and Visitor Statistic data for each National Park in 2017.'''

import pandas as pd
from numpy import nan
from plotly.offline import init_notebook_mode, iplot

data = pd.read_csv('Data/NPSAnnualSummary.csv', skiprows= [0,1,2]) #Downloaded from IRMA, with the desired categories selected
data.drop(['TotalRecreationVisitors', 'TotalNonRecreationVisitors', 'TotalRecreationHours', 'TotalNonRecreationHours',
           'TotalConcessionerLodging', 'TotalConcessionerCamping' , 'TotalTentCampers',
           'TotalRVCampers', 'TotalBackcountry', 'TotalNonRecreationOvernightStays',
            'TotalMiscellaneousOvernightStays' ], axis = 1, inplace = True)

#formatting stuff, remove unecessary rows
data.drop(data.index[4541:4660], inplace = True)
newData1 = data.apply(lambda x: x.str.replace(',',''))
newData2 = newData1.apply(pd.to_numeric, errors='ignore', downcast = 'float') #Convert strings to numbers
newData = newData2.fillna(0)

newData ['RecreationVisits'] = newData['RecreationVisitors']
newData['TotalVisits'] = newData['RecreationVisitors']  + newData['NonRecreationVisitors'] #Sum Total Visits of Each Park
newCampers = newData
newCampers['TotalCampers'] = newCampers['ConcessionerCamping']+ newCampers['TentCampers'] + newCampers['RVCampers'] + newCampers['Backcountry']
#print newCampers

newData.to_csv('Data/UnorganizedNPS.csv', sep=',')

TotalCampers = newCampers.pivot(index='Year', columns = 'ParkName')['TotalCampers']
TotalCampers.fillna(value=nan, inplace=True) #Convert None Values to Nan
TotalCampers = TotalCampers.T
TotalCampers['5YearCamperAvg'] = (TotalCampers[2016] + TotalCampers[2015] + TotalCampers[2014] + TotalCampers[2013] + TotalCampers[2013])//5
#print TotalCampers

TotalHours = newData.pivot(index='Year', columns = 'ParkName')['RecreationHours']
TotalHours.fillna(value=nan, inplace=True) #Convert None Values to Nan
TotalHours = TotalHours.T
TotalHours['5YearHoursAvg'] = (TotalHours[2016] + TotalHours[2015] + TotalHours[2014] + TotalHours[2013] + TotalHours[2013])//5
#print TotalHours

D = newData.pivot(index='Year', columns = 'ParkName')['RecreationVisits'] #pivot table for plotting
D.fillna(value=nan, inplace=True) #Convert None Values to Nan
#D['TotalVisits'] = D.sum(axis=1) #Some total visits of all National Parks
D = D.T
D['5YearVisitAvg'] = (D[2016.0] + D[2015.0] + D[2014.0] + D[2013.0] + D[2013.0])//5

Acres = pd.read_csv('Data/NPSAcres.csv')
print Acres
Acres = Acres.drop(Acres.index[59]) #remove Total Acreage
Acres = Acres.set_index('ParkName')
Acres['2016Visits'] = D[2016]
Acres['5YearVisitAvg'] = D['5YearVisitAvg']
Acres['2016Campers'] = TotalCampers[2016]
Acres['5YearCamperAvg'] = TotalCampers['5YearCamperAvg']
Acres['2016Hours'] = TotalHours[2016]
Acres['5YearHoursAvg'] = TotalHours['5YearHoursAvg']
#print Acres
#print D
#Acres.drop(['Great Smoky Mountains NP'], inplace = True)
#Acres.drop(['Yosemite NP'], inplace = True)


Parks2 = list(Acres.index)

#Converts the numbers into a more readable format
def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])

#print "Parks 2: ", Parks2

i=0;
text = []
mobiletext = []
#Create custom hover text for the plot. THIS TOOK FOREVER TO FIGURE OUT
for p in Parks2:
    print Acres.loc[p]['State'] + "'"
    text.append(p + "<br>Visitors: " + human_format(Acres.loc[p]['2016Visits']) + "<br>Acres: " + human_format(Acres.loc[p]['Acres']) + "<br>Campers: " + human_format(Acres.loc[p]['2016Campers']))
    mobiletext.append(p)
    i+=1
text.append("NOT WPORKIONG")
#Mobile text was only creating the gif for the mobile version of the data visualization
#print mobiletext
#print text


#Plotly formatting code
trace1 = {
    "x" : Acres['Acres'],
    'y' : Acres['2016Campers'],
    "z" : Acres['2016Visits'],
   "marker": {
    #"cauto": True,
    #"cmax": 2.31428917959,
    #"cmin": -2.39332076244,
       #"color" : np.random.randn(500),
    "color" : "rgba(102,51,153,1)",
    #"colorscale": "Viridis"
    "size": 8,
  },
  "mode": "markers",
  "type": "scatter3d",
    "name" : "TESTING",
    "hoverinfo" : "text",
    #"mode" : "",
    "text" : text, # "{:,}".format(str(Acres['Acres'])),
  #"uid": "47d11b"
}

#data = Data([trace1])
data = [trace1]
layout = {
  "margin": {
    "r": 0,
    "t": 0,
    "b": 0,
    "l": 0
  },
  "scene": {
      "zaxis": {
        "title": "Total Visitors  ",
        "type": "log"
      },
      "xaxis": {
        "title": "Total Acreage  ",
          "type": "log"
      },
      "yaxis": {
            "title": "Total Campers ",
            "type": "log"
      }
    },
    "title": "Hello"
  }

'''Offline mode was not working embedded on the website'''

#fig = Figure(data=data, layout=layout,)
#offline.plot(fig, filename= "3DNPS.html")s


import plotly
import plotly.plotly as py
import plotly.graph_objs as go
#Add in your own credentials
plotly.tools.set_credentials_file(username='USER', api_key='API-KEY')

fig = go.Figure(data=data, layout=layout)
#offline.plot(fig, filename= "HTMLGraphs/3DNPS.html")
py.iplot(fig, filename='3DNPS')
iplot(fig)

#This is Bokeh code to create a 2D scatter plot with Acreage vs. Visitors. Not used for the final Data Visualization
'''
#D.to_csv('NPSAcres.csv', sep=',')

source = ColumnDataSource(Acres)

#p.select_one(HoverTool).tooltips = [
#     ('Hi', '@TotalVisits'),
#]



hover = HoverTool(
    tooltips=[
        ( 'Park','@index'),
        ( 'Acres','@Acres{0,0}'),
        ( 'Visitors','@5YearVisitAvg{0,0}')
        #( 'Campers','@2016Hours')
    ],
)

Purp = plasma(20)
Purp = Purp[::-1]
Purp.pop(0)
Purp.pop(0)
Purp.pop(0)
Purp.pop(0)
Purp.pop(0)


colors = ["#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce", "#ddb7b1", "#cc7878", "#933b41", "#550b1d"]
mapper = LinearColorMapper(palette=Purp, low=Acres['5YearCamperAvg'].min(), high=Acres['5YearCamperAvg'].max())

p = figure(plot_width = 700, plot_height = 600, title="NPS Visitors vs. Acreage", tools = [hover], x_axis_type="log",
           y_axis_type='log')
p.circle(source = source, x = 'Acres', y = '5YearVisitAvg', fill_color={'field': '5YearCamperAvg', 'transform': mapper},
       line_color=None, size = 9)

color_bar = ColorBar(title= '# of Campers', title_text_font_size = "7pt",color_mapper=mapper, major_label_text_font_size="5pt",
                     ticker=BasicTicker(desired_num_ticks=len(Purp)-4),
                     formatter=NumeralTickFormatter(format="0,0"),
                     border_line_color=None, location=(0, 0), orientation = 'vertical')

p.yaxis.formatter=NumeralTickFormatter(format="0,0")
p.xaxis.formatter=NumeralTickFormatter(format="0,0")
p.yaxis.axis_label = '5 Year Visitor Avg'
p.xaxis.axis_label = 'Acres'
p.toolbar_location = None

p.add_layout(color_bar, 'right')

output_file("NPSAcreage.html", title="Acres")

show(p)
'''
'''
import plotly.offline as offline
from plotly.graph_objs import *

Acres = Acres[Acres.Acres != 0 ]
Acres = Acres[Acres['5YearVisitAvg'] != 0 ]
Acres = Acres[Acres['5YearCamperAvg'] != 0 ]


Parks = list(Acres.index)
Parks = Parks[:-1]

Final = ""

for p in Parks:
    temp = "\""  + p + "<br>Fuck" + "\"," # + str(Acres.Acres[p]) + "<br>Campers: " + str(Acres['5YearCamperAvg'][p]) + ","
    Final = Final + temp
print Final

'''