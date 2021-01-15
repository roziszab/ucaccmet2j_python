import json

# Open the csv file
with open('stations.csv') as file:
    headers = file.readline()
    csv_data = []
    for line in file:
        Location, State, Station = line.strip().split(',')
        csv_data.append({'Location': Location, "State": State, 'Station': Station})

# Find the code for Seattle
code_seattle = csv_data[1]['Station']
print(code_seattle)

# Load the precipitation file
with open('precipitation.json') as file:
    precipitation = json.load(file)

# Create a directory with only data from Seattle
seattle_prcp = []
for dict in precipitation:
    if code_seattle == dict['station']:
        seattle_prcp.append(dict.copy())
#print(seattle_prcp)

# Create a list of lists grouped by month
months = [[], [], [], [], [], [], [], [], [], [], [], []]
value = 0
for dict in seattle_prcp:
    for i in range(12):
        if f"-{i:02d}-" in dict['date']:
            months[i-1].append(dict['value'])
#print(months)

# Summarize the lists into one total variable
monthly_prcp = []
for list in months:
    monthly_prcp.append(sum(list))
#print(monthly_prcp)

# Save the monthly value into a json file
with open('seattlemonthly.json', 'w') as file:
    json.dump(monthly_prcp, file)
