#print(__doc__)
# Raul and Vedant
# SPIS 2020
# ML Project
# Predictions for player databases
# Title: Game Genie


# Concept by: Nelle Varoquaux <nelle.varoquaux@gmail.com>
#         	  Alexandre Gramfort <alexandre.gramfort@inria.fr>
# License: BSD

# Imports the following modules in order to establish a graph
import matplotlib.pyplot as plt
import csv
import pandas as pd
import random




def pickGame():
	'''
	Selects the game based on user input to display its data
	'''
	listGames = ["Civ_VI", "CSGO", "Destiny2", "DOTA_2", "FM_2020","Garry's_Mod", "GTA_V", "PUBG", "RainbowSixSiege", "Rocket_League", "TF2", "Warframe"]
	print(listGames)
	game = input("Enter the name of a game: ")
	if game in listGames:
		return game
	else:
		print("Game is not in the list")
		return pickGame()

def dataPoints(game):
	'''
	Opens, reads, and prints day and player data from the csv file
	'''
	pd.read_csv(game + '.txt')
	dataFile = game + '.txt'

	# Opens the csv file
	# Accounts for any errors in the file
	with open(dataFile, 'r') as csvfile:
		
		# Begins to read the csv file 
		# Skips the column headers
		pointreader = csv.reader(csvfile)
		next(pointreader)
		
		# Loops through each row of the csv file 
		# Displays date/time and number of players
		for row in pointreader:
			print(row[0], row[1] + " players")
	

		


#dataPoints()


def graph(game):
	'''
	Creates a graph based on recorded data and predictive data 
	'''
	# Creates a list for the x and y coordinates
	x = []
	y = []
	
	# Begins after the csv file has been processed
	# Each value is a day after recorded data
	i = 1
	n = int(input('How many days would you like me to predict? '))
	
	# Creates a list of potential events which would affect the behavior of the predictive model, each in their different ways
	events = ['normal', 'server failure', 'game changing update']
	
	# Creates a list multiNum containing the number of days that correspond to each event in events list occurring
	multiNum = [int(n * 0.98), int(n * 0.005), int(n* 0.015)]
	c = sum([[s] * n for s, n in zip(events, multiNum)], [])
	
	# Opens the csv file to read it
	# Distinguishes between date/time and player count
	with open('data/' + game + '.txt','r') as csvfile:
		
		# Reads csv file and splits up data between axis, with a comma acting as the boundary 
		plots = csv.reader(csvfile, delimiter=',')
		next(csv.reader(csvfile))
		
		# For each row of data in plots, append the time and day values to list x, with the number of concurrent players per day being appended to list y
		for row in plots:
			x.append((row[0]))
			y.append(int(row[1]))
		
		# Loops as long as the given day does not pass the total number of days specififed
		while i < n:
			
			# Certain behavoir triggers based on the event the computer randomly chose
			randEvent = random.choice(c)
			print(randEvent)
			if randEvent == 'normal':
				x.append(str(i) + ' days after data')
				y.append(y[-1] * random.uniform(0.97, 1.03))
			if randEvent == 'game changing update':
				x.append(str(i) + ' days after data')
				y.append(y[-1] * random.uniform(0.97, 1.03))
			if randEvent == 'server failure':
				x.append(str(i) + " days after data")
				y.append(y[-1] * 0.15)
				# Prevents the program from plotting points that are dependent from the server failure
				# 'Recovery' state allows the program to plot reasonable points again
				x.append('recovery')
				y.append(y[-2])
			
			# Increases to indicate the next day after recorded data
			i += 1
		
		# Plots the data (both from the csv file along with the predictive model); Labels each axis, title, and legend, and sets a boundary line defining where the original csv data ends and the prediction begins
		plt.plot(y, label='') #x parameter was taken out
		plt.axvline(x = len(x) - n, ymin = 0, ymax = 1, label = 'start of prediction', color = 'red')
		plt.xlabel('Days After Launch')
		plt.ylabel('Concurrent Players')
		plt.title('Number of Concurrent Players per Day in\n' + game)
		plt.legend()
		plt.show()

# Calls the function 'graph'
graph(pickGame())
