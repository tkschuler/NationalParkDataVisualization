'''This script creates two html plots. One plot has the total visitors for all of the parks. The other plot has a graph of all parks plotted, as well
as some individual parks with interesting visitation trends'''

import pandas as pd
from numpy import nan
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool,NumeralTickFormatter, WheelZoomTool
from bokeh.models.widgets import Panel, Tabs
from itertools import cycle
import time

data = pd.read_csv('Data/NPSAnnualSummary2017.csv', skiprows= [0,1,2])
data.drop(['TotalRecreationVisitors', 'TotalNonRecreationVisitors', 'TotalRecreationHours', 'TotalNonRecreationHours',
           'TotalConcessionerLodging', 'TotalConcessionerCamping' , 'TotalTentCampers',
           'TotalRVCampers', 'TotalBackcountry', 'TotalNonRecreationOvernightStays',
            'TotalMiscellaneousOvernightStays' ], axis = 1, inplace = True) #  Don't need any of these columns

#formatting stuff
data.drop(data.index[4600:4720], inplace = True) # For 2017, remove summary data
newData1 = data.apply(lambda x: x.str.replace(',',''))
newData2 = newData1.apply(pd.to_numeric, errors='ignore', downcast = 'float') #Convert strings to numbers
newData = newData2.fillna(0)
newData['RecreationVisits'] = newData['RecreationVisitors']  #+ newData['NonRecreationVisitors'] #Sum Total Visits of Each Park
newData.to_csv('Data/UnorganizedNPS.csv', sep=',')

D = newData.pivot(index='Year', columns = 'ParkName')['RecreationVisits'] #pivot table for plotting
D.fillna(value=nan, inplace=True) #Convert None Values to Nan
D['TotalVisits'] = D.sum(axis=1) #Some total visits of all National Parks
D.to_csv('Data/NPSVisits.csv', sep=',')

Parks = list(D.columns.values)
#print Parks

tools_to_show = 'hover,box_zoom,pan,save,reset,wheel_zoom'
p = figure(plot_width=1100, plot_height=600, tools = tools_to_show, y_axis_type="linear", title = "All Visitor Statistics for Individual National Parks" ) # Main Figure
colors = ['#7c1616','#ff0000','#9b5611','#ff6e00','#5dff00','#156818','#2f775c','#00c9a4','#00a4e0','#1354f7', '#081f63','#412a7c','#7526ff','#c23bef', '#ef13ec']
colorcycler = cycle(colors)

# These parks have interesting trends and will be included as tabs on the main layout
RogueParks = ['Acadia NP', 'Big Bend NP','Biscayne NP','Carlsbad Caverns NP','Wind Cave NP','Channel Islands NP',
              'Hawaii Volcanoes NP','Hot Springs NP','Katmai NP & PRES','North Cascades NP','Shenandoah NP',
              'Great Smoky Mountains NP','Lake Clark NP & PRES', 'Yellowstone NP', 'Yosemite NP','TotalVisits']

TotalVisits = ['TotalVisits']

tabs = []

#Create Main plot including Visitor trends for all parks
for i in xrange(59):
    source = ColumnDataSource(data={
                'Year': D.index,
                'Visitors': D[Parks[i]],
                'ParkName': [Parks[i] for n in xrange(120)]
            })
    line = p.line('Year', 'Visitors',source=source,legend=Parks[i],color = next(colorcycler), line_width = 2, muted_alpha = .2, alpha = .9)
    #line.muted = True
    #circle = p.circle('Year', 'Visitors',source=source, size=4, legend=Parks[i],fill_color  = next(colorcycler), color = next(colorcycler))

    #to avoid some strange behavior(as shown in the picture at the end), only add the circle glyph to the renders of hover tool
    #so tooltip only takes effect on circle glyph
    p.tools[0].renderers.append(line)

hover = p.select(dict(type=HoverTool))
p.toolbar.active_scroll = WheelZoomTool()
hover.tooltips = [("Park", "@ParkName"),("Year", "@Year{0}"), ("Visitors", "@Visitors{0,0}")]
hover.mode = 'mouse'

p.yaxis.axis_label = 'Some Numbers'
p.yaxis.formatter=NumeralTickFormatter(format="0,0")
p.xaxis.axis_label = 'Year'
p.legend.location = "top_left"
p.legend.click_policy="mute"
p.yaxis.axis_label = 'Total Visitors'
p.xaxis.axis_label = 'Year'
p.legend.label_text_font_size = "6pt"
p.legend.padding = -4
p.legend.spacing = -11
MAINTAB = Panel(child=p, title="All Parks")
tabs.append(MAINTAB)
#show(p)

hover2 = HoverTool(
    tooltips=[
        ( 'Year',   '$x{0}'),
        ( 'Visitors', '$y{0,0}')
    ]
)

# Create unique plots for all of the Parks listed in Rogue Parks and ad them to a list of tabs
for i in range(-1,60):
    if Parks[i] in RogueParks:
        print Parks[i], '\n'
        time.sleep(.25)
        p1 = figure(plot_width=900, plot_height=500, tools = [hover2])
        p1.line(x=D.index, y=D[Parks[i]], color=next(colorcycler), line_width = 2, legend = Parks[i])
        p1.legend.location = "top_left"
        p1.legend.click_policy = "hide"
        p1.yaxis.formatter = NumeralTickFormatter(format="0,0")
        p1.yaxis.axis_label = 'Total Visitors'
        p1.xaxis.axis_label = 'Year'
        tab = Panel(child=p1, title=Parks[i])
        tabs.append(tab)

tabs.insert(1, tabs.pop(len(RogueParks)+1)) #move Total Visits to second position
tabs.pop(2)
TABS = Tabs(tabs=tabs)
output_file("ALLPARKSTABS.html", title="ALLPARKSTABS")
show(TABS)

time.sleep(.25)

for i in range(-1,60):
    if Parks[i] in TotalVisits:
        print Parks[i], '\n'
        time.sleep(.25)
        p1 = figure(plot_width=900, plot_height=500, tools = [hover2], title = "Total National Park Visitors")
        p1.line(x=D.index, y=D[Parks[i]], color=next(colorcycler), line_width = 2, legend = Parks[i])
        p1.legend.location = "top_left"
        p1.legend.click_policy = "hide"
        p1.yaxis.formatter = NumeralTickFormatter(format="0,0")
        p1.yaxis.axis_label = 'Total Visitors'
        p1.xaxis.axis_label = 'Year'

tabs2=[]
tab = Panel(child=p1, title=Parks[i])
tabs2.append(tab)
TABS2 = Tabs(tabs=tabs2)

output_file("TOTALVISITS.html", title="Total Visits")
show(TABS2)