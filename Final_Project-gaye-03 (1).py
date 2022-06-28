'''
Author: Gayatri kotlo
Filename: FinalProject-gaye-03.py
Description: Analysis of the Commodity Data
Revisions: 
    00: announce,read text fileimport the data from CSV file.
    01: converting the dates and prices and creating a new list
    02: filtering the data and ploting the chart
    03:updating the chart titles and formatting
'''
#importing the required modules
import csv
from datetime import datetime
import plotly.offline as py
import plotly.graph_objs as go

'''
columnPrint() accepts list as an input and enumerate each element in the list with the index
the wid argument sets the number of spaces for the text without print the index
'''

def columnPrint(x,enum=1,wid=20):
    s=''
    for n,com in enumerate(x):
        if len(s) < 3*(wid+enum+2):
            if enum:
                s += f"<{n:2}>" #add index in brackets
            s += f" {com:<20}" #add the item text
        else:
            print(s) #print 3 clumns
            s='' #start the next 3 columns    
            if enum:
                s += f"<{n:2}>" #add index in brackets
            s += f"{com:<20}" #add the item text
    if s:
        print(s)

'''
columnPrint() accepts list as an input and enumerate each element in the list with the index
and print the date in required format .The wid argument sets the number of spaces for the text 
without print the index
'''

def columndatePrint(x,enum=1,wid=30):
    s=''
    for n,dat in enumerate(x):
        if len(s) < 3*(wid+enum+2):
            if enum:
                s += f"<{n:2}>" #add index in brackets
            s += f" {datetime.strftime(dat,'%Y-%m-%d'):<15}" #add the item text
        else:
            print(s) #print 3 clumns
            s='' #start the next 3 columns            
            if enum:
                s += f'<{n:2}>' #add index in brackets
            s += f"{datetime.strftime(dat,'%Y-%m-%d'):<15}" #add the item text
    if s:
        print(s)
   
'''
avg() accepts list argument and returns the average of the list 
elements if length of list is greater than 1 else returns 0
'''

def avg(l):
    if len(l)==0:
        return 0
    else:
        return sum(l)/len(l)
 
#Announce   
print(f"{'='*26}\n Analysis of Commodity Data \n{'='*26}")

# Read the data from the file
with open("produce_csv.csv",'r') as file:
    reader=csv.reader(file)
    data=[row for row in reader]
    
'''---------------Debug to check if the data in loaded
print('THE FIRST 8 ROWS FROM DATA FILE...')
cdata= filter(None,[print(d) for d in data[:8]])
'''   

#converting the date and prices

modData =[]                     # initialise new list to receive data
for row in data:
    newrow=list()               # empty row to receive values
    for item in row:            # transverse the values in the old rows  
        if "$" in item:         # test for price string and convert
            newrow.append(float(item.replace("$","")))  
        elif "/" in item:       # test for the date and convert
            newrow.append(datetime.strptime(item,"%m/%d/%Y"))
        else:                   # if not date or price apped to the newrow
            newrow.append(item) 
    modData.append(newrow)
    
'''------Debug to check the converted data
print("THE FIRST 8 ROWS OF CONVERTED DATA ...")
cd= filter(None,[print(d) for d in modData[1:9]])
'''

#creating the data records in required format
locations=modData.pop(0)[2:]    # remove the header
records=list()                  # initialise new list for data records
for row in modData:             # trasverse each row
    newrow=row[:2]              # first two values are common for all tthe locations
    for loc,price in zip(locations,row[2:]):    # transverse the locations and prices
        records.append(newrow+[loc,price])      #add a new data record

'''-----Debug to check the records
print("THE FIRST 20 DATA RECORDS ...")
cd= filter(None,[print(d) for d in records[:20]])
'''

print("SELECT PRODUCTS BY NUMBER ...") 
Product_list=list({i[0] for i in records})  
Product_list.sort()         # sort the product_list
columnPrint(Product_list)   # calling the columnPrint()
# promt user to specify which products are of interest by its index numbers and split the input and convert into list
commodity = [int(i) for i in input("Enter product numbers separated by spaces: ").split()]
commodity_names = [Product_list[i] for i in commodity]
print(f"selected products: {', '.join(map(str,commodity_names))} \n")   #print the selected Products


print("SELECT DATE RANGE BY NUMBER ...")
date_list=list({i[1] for i in records})
date_list.sort()                # sort the date_list
columndatePrint(date_list)      # calling the columndatePrint()
#print the start and end dates
print(f"Ealiest available date is: {datetime.strftime(date_list[0],'%Y-%m-%d')}")
print(f"Latest available date is: {datetime.strftime(date_list[-1],'%Y-%m-%d')}")
# promt user to specify which dates are of interest by its index numbers and split the input and convert into list
date = [int(i) for i in input("\nEnter start/end date numbers separated by a space: ").split()]  
date1 = [datetime.strftime(date_list[i],'%Y-%m-%d') for i in date]
print(f"Dates from  {''.join(map(str,date1[0]))} to {''.join(map(str,date1[1]))}") #print the selected start and end date


print("\nSELECT LOCATIONS BY NUMBER ...")
locations.sort()            #sort the locations
for (i, L) in enumerate(locations):     # map each loation with index number using enumerate()
    print(f"<{i}> {L}")
# promt user to specify which locations are of interest by its index numbers and split the input and convert into list
location = [int(i) for i in input(f"\nEnter location numbers separated by spaces: ").split()]
location1 = [locations[i] for i in location]
print(f"Selected locations: {', '.join(map(str,location1))}") #print the seelcted locations

#Create a list for user options
user_filter = list(filter(lambda i:i[0] in Product_list and (datetime.strptime(date1[0],'%Y-%m-%d')<=i[1]<=datetime.strptime(date1[1],'%Y-%m-%d')) and i[2] in location1,records ))
print(f"{len(user_filter)} records have been selected.")

'''---------------Debug----------

for i,r in enumerate(user_filter):
    print(f"<{i}> {r}")  
'''
# Create the dictionary for user options
user_dict = {}
for l in location1:
    user_dict[l]={}
    for k in commodity_names:
        user_dict[l].update({k:[]})
        user_dict[l][k] =[y[3] for y in user_filter if y[2]==l and y[0]==k]
    
# Traverse the dictionary and replace each list with the average of the prices in the list   
dict1 = {}
for loc in user_dict:
    dict1.update({loc:{}})
    for p in user_dict[loc]:
        dict1[loc].update({p:avg(user_dict[loc][p])})   #calling avg()

#	Create a title string for the graph        
graph1=[]
for l in location1:
    li_price=[dict1[l][product] for product in commodity_names]
    graph1.append(go.Bar(x= commodity_names, y=li_price , name =l))
layout= go.Layout(barmode='group')

#	update the figure layout by providing format y-axis values, b.	x and y axis titles and	a chart title
fig=go.Figure(data=graph1, layout= layout)
fig.update_layout(title=f"Produce Prices from {date1[0]} through {date1[1]}",xaxis_title="Product",yaxis_title="Average Price")

#plot the figure to the html file 
fig.update_layout(yaxis_tickformat= '$.2f')
py.plot(fig,filename="grouped-bar.html")