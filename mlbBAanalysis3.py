#python mlbBAanalysis.py
import json

import sys

import os
from decimal import Decimal

import csv

with open('team_data2.txt') as readfile:
	data = json.load(readfile)

teams = ['LAA', 'HOU', 'OAK', 'TOR', 'ATL', 'MIL','STL', 'CHC', 'ARI',  'LAD', 'SFG', 'CLE',
		'SEA', 'FLA', 'NYM', 'NYY', 'WSN', 'BAL', 'SDP', 'PHI', 'PIT', 'TEX', 'TBR', 'CIN', 'BOS',
		'COL', 'KCR', 'DET','MIN', 'CHW']
		


def gameBA(pos, team, park):
	
	year = str(pos + 2009)
	
	BA = 0
	count = 0
	for game in data[team][pos][year]:
		if game['field'] == park:
			BA += float(game['BA'])
			count += 1
	
	if count == 0:
		return None
		
	else:
		return BA/count
	
def populatefileBP():
	club = ['club']
	pos = 0
	while pos+2009 <=2018:
		fields = []
		
		for team in teams:
			findBP(team, pos, fields)
			
		fields.sort()
		year = str(pos+2009)
		
		url = 'ballpark_data\\mlb_' + year + '.csv'
		with open(url, 'w+') as csv_file:
			writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
			writer.writerow(club + fields)
		pos += 1
		
def returnBP(team, ballparks, pos, year):
#	for team in teams:
	line = []
	for bp in ballparks:
		if bp == 'club':
			line.append(team)
			continue
		
		count = 0
		sum_BA = 0
		for game in data[team][pos][year]:
			if bp == game['field']:
				count += 1
				sum_BA += float(game['BA'])
		if count == 0:
			line.append(None)
		else:
			line.append(round(sum_BA/count, 3))
	return line

def populatefileBA(year):
	pos = int(year) - 2009
	url = 'ballpark_data\\mlb_' + year + '.csv'
	with open(url) as file:
		temp = file.readline()
	temp = temp.strip('\n')
	temp = temp.split('"')
	bps = []
	for x in temp:
		if x != ',' and x != '':
			bps.append(x)

	for team in teams:
		line = returnBP(team, bps, pos, year)

		with open(url, 'a', newline='') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(line)

def findFields(url):
	fields = []
	with open(url) as file:
		csv_reader = csv.DictReader(file, delimiter=',')
		for row in csv_reader:
			for x in row:
				fields.append(x)
			break
	fields.remove('club')
	return fields
	
def findTotal(url, park):
	with open(url) as file:
		csv_reader = csv.DictReader(file, delimiter=',')
		count = 0
		sum = 0
		for row in csv_reader:
			x = row[park]
			if x != '':
				sum += float(x)
				count += 1
		return round(sum/count, 3)

def findBP(team, pos, fields):
	wrong = [str(pos+2009)]
	
	for game in data[team][pos][str(pos+2009)]:
		if game['field'] not in fields:
			fields.append(game['field'])
			
		if game['field'] == '':
			wrong.append(team + game['game'])
	if len(wrong) > 1:
	 print(wrong)
		
def main():
	#ARI_GM1 = data['ARI'][0]['2009'][0]
	year = 2010
	while year <= 2018:
		url = 'ballpark_data\\mlb_' + str(year) + '.csv'
		fields = findFields(url)
		line = ['Total']
		for park in fields:
			line.append(findTotal(url, park))
			
		with open(url, 'a', newline='') as csv_file:
			writer = csv.writer(csv_file)
			writer.writerow(line)
		year += 1
		
main()
		