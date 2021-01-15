import json

# Open the csv file
with open('stations.csv') as file:
    headers = file.readline()
    csv_data = []
    for line in file:
        Location, State, Station = line.strip().split(',')
        csv_data.append({'Location': Location, "State": State, 'Station': Station})

# Creating a directory of the locations and define codes and states
d = {}
for dict in csv_data:
    d[dict['Location']] = {'station':dict['Station'], 'state':dict['State']}

# Load the precipitation file
with open('precipitation.json') as file:
    precipitation = json.load(file)

##create a list with area codes
codes = []
for dict in d:
    codes.append(d[dict]['station'])

## Add the lists of monthly precipitations into the defined directory.
for item in codes:
    location_prcp = []
    for dict in precipitation: # Filter by location
        if item == dict['station']:
            location_prcp.append(dict.copy())
    months = [[], [], [], [], [], [], [], [], [], [], [], []]
    for dict in location_prcp: # Create a list of lists, where every list is one month
        for i in range(12):
            if f"-{i+1:02d}-" in dict['date']:
                months[i].append(dict['value'])
    monthly_prcp = []
    for list in months: # Summarise the months into one integer
        monthly_prcp.append(sum(list))
    for dict in d: # Add the list of monthly integers into the dictionary
        if d[dict]['station'] == item:
            d[dict]['totalMonthlyPrecipitation'] = monthly_prcp

# Calculating relative monthly prcp, total prcp per location and defining and calculating yearly total prcp
yearly_total = 0
for dict in d:
    total = sum(d[dict]['totalMonthlyPrecipitation'])
    d[dict]['relativeMonthlyPrecipitation'] = [x / total for x in d[dict]['totalMonthlyPrecipitation']]
    d[dict]['totalYearlyPrecipitation'] = total
    yearly_total += total

# Calculate realtive yearly prcp per location
for dict in d:
    d[dict]['relativeYearlyPrecipitation'] = d[dict]['totalYearlyPrecipitation'] / yearly_total

# Save the dictionary into a json file
with open('result.json', 'w') as file:
    json.dump(d, file, indent = 4)
