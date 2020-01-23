#python format_team_data.py team_init year

import os
import sys

import json

teams = {'angels' : 'LAA', 'astros' : 'HOU', 'athletics' : 'OAK', 'bluejays' : 'TOR', 'braves' : 'ATL', 'brewers' : 'MIL',
		'cardinals' : 'STL', 'cubs' : 'CHC', 'diamondbacks' : 'ARI', 'dodgers' : 'LAD', 'giants' : 'SFG', 'indians' : 'CLE',
		'mariners' : 'SEA', 'marlins' : 'FLA', 'mets' : 'NYM', 'yankees':'NYY', 'nationals':'WSN', 'orioles':'BAL', 
		'padres':'SDP', 'phillies':'PHI', 'pirates':'PIT', 'rangers':'TEX', 'rays':'TBR', 'reds':'CIN', 'redsox':'BOS',
		'rockies':'COL', 'royals':'KCR', 'tigers':'DET', 'twins':'MIN', 'whitesox':'CHW'}
		
with open('team_data2.txt') as readfile:
	data = json.load(readfile)
	
def populateField(team, year, parks):
	pos = int(year) - 2009
	
	set = data[team][pos][year]
	i = 0
	for game in parks[pos][str(year)]:
		if i >= len(set):
			break
			
		set[i]['field'] = game['venue']
		i+=1

		

def main():

	
#for team in data:
#for i in data[team]:
#for j in i:
#for x in i[j]:
#if x['BA'] == '':
#i[j].remove(x)
	
	team = str(sys.argv[1])
	year = int(sys.argv[2])
	
	url = 'teams_data_sep\\venues\\' + team + 'venues.json'
	
	with open(url) as park_file:
		parks = json.load(park_file)
	
	while year <= 2018:
		populateField(team, str(year), parks)
		year += 1
	
	with open('team_data2.txt', 'w') as outfile:
		json.dump(data, outfile)
		
main()