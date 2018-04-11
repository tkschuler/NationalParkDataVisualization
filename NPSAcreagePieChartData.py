'''This code organizes Acreage data from the NPSAcres.csv file which includes Park Name, State, and Acreage.  The data
was typed in manually by using the 2016 statistics from IRMA. (Faster to find myself than write code to scrape the website)'''

import pandas as pd
from termcolor import colored

Acres = pd.read_csv('Data/NPSAcres.csv')
#Acres = Acres.drop(Acres.index[59]) #remove Total Acreage
Acres = Acres.sort_values('Acres', ascending=False)
#print Acres


PieChartData = ''

# Generates a string for using with Google Charts
for i in range (0,int(len(Acres.index))):
    PieChartData += "['" + str(Acres.iloc[i,0]) + "', '" + str(Acres.iloc[i,2]) + "'],\n"

print colored("Acreage per Individual Park for Google Pie Chart: ",'yellow')
print PieChartData


print colored("Number of states with National Parks:",'yellow'), len((Acres['State'].value_counts())), '\n'
print colored("Parks per State:\n",'yellow'), Acres['State'].value_counts() #27 length

#Organize and condense total acreage by State
States = Acres.groupby('State')['Acres'].sum()  #sum total of each unique state ID
States = States.to_frame()  #Convert back to Dataframe for manipulating
States.reset_index(level=0, inplace=True)
States = States.sort_values('Acres', ascending=False)
#print colored("\nState Acreage:\n",'yellow'), States

StateChartData = ''
for i in range (0,int(len(States.index))):
    StateChartData += "['" + str(States.iloc[i,0]) + "', " + str(States.iloc[i,1]) + "],\n"

print '\n'

print colored("Acreage per State for Google Pie Chart:",'yellow')

print StateChartData