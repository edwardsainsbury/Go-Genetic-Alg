import random
import go
import itertools
import mysql.connector
from datetime import datetime

#player class
class Player:

    def __init__(self, depth, height, inputs, output, id, weights,parentone,parenttwo):
        self.depth = depth
        self.height = height
        self.input = inputs
        self.output = output
        self.id = id
        self.numchildren = 0
        self.parentone = parentone
        self.parenttwo = parenttwo
        # Change weights order to work backwards
        if len(weights) == 0:
            weights.append([[round(random.random(),4) for x in range(inputs)] for y in range(height)])
            for x in range(depth - 1):
                weights.append([[round(random.random(),4)for x in range(height)] for y in range(height)])
            weights.append([[round(random.random(),4)for x in range(height)] for y in range(output)])
        self.weights = weights

    def result(self, inputArray):
        nodeOutput = [inputArray]
        # nodeOutput.append(inputArray)
        for x in range(self.depth+1):
            outputArray = []
            for y in range(len(self.weights[x])):
                output = 0
                for z in range(len(self.weights[x][y])):
                    output += self.weights[x][y][z]*nodeOutput[x][z]
                outputArray.append(output)
            nodeOutput.append(outputArray)
        return nodeOutput[-1]

#main script to run
def handler():
    numberOfEra = 100
    runningScores = []
    numberOfPlayersPerRound = 4
    do_load = 0
    if do_load:
        arrayOfPlayers, numberOfPlayersCreated, startEra = load()
    else:
        arrayOfPlayers, numberOfPlayersCreated, startEra = startNew(numberOfPlayersPerRound)

    for i in range(startEra, 1, numberOfEra):
        print('Era: ' + str(i+1))
        wins = []
        for x in range(numberOfPlayersPerRound):
            wins.append(0)

        matches = list(itertools.permutations(range(numberOfPlayersPerRound), 2))
        winner = 2
        cnx = mysql.connector.connect(user='root', password='mysql', host='127.0.0.1', database='test')
        for x in range(len(matches)):
            print('Match:' + str(x+1))
            winner, moves = go.playgo(arrayOfPlayers[matches[x][0]], arrayOfPlayers[matches[x][1]])
            add_match = ("INSERT INTO `matches`"
                        "(timestamp, era_no, match_no, player_one_id, player_two_id, player_one_winner, draw, no_moves) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            if winner == 2:
                wins[matches[x][0]] += 1
            elif winner == 0:
                wins[matches[x][1]] += 1
            data_match = (str(datetime.now()), str(i+1), str(x+1), arrayOfPlayers[matches[x][0]].id,
                arrayOfPlayers[matches[x][1]].id, winner == 2 or winner == 1, winner == 1, str(moves))
            cnx.cursor().execute(add_match, data_match)
            cnx.commit()
        cnx.close()
        print(wins)
        runningScores.append(wins)
        numbers = []
        playerids = []

        for x in range(len(wins)):
            numbers.append(x)
            playerids.append(arrayOfPlayers[x].id)
        sortedNumbers = [x for y, x in sorted(set(zip(wins, numbers)), reverse=True)]
        newPlayers = []
        #Drop table, undecided if this is required
        cnx = mysql.connector.connect(user='root', password='mysql', host='127.0.0.1', database='test')
        cnx.cursor().execute("DROP TABLE if exists `players`")
        cnx.cursor().execute("CREATE TABLE `players` ("
                             "  `timestamp` time(2) NOT NULL, "
                             "  `player_id` int(3) NOT NULL,"
                             "  `parent_one_id` int(3) NOT NULL,"
                             "  `parent_two_id` int(3) NOT NULL,"
                             "  `layer_one_weights` mediumtext NOT NULL ,"
                             "  `layer_two_weights` mediumtext NOT NULL,"
                             "  `layer_three_weights` mediumtext NOT NULL,"
                             "  PRIMARY KEY (`timestamp`)"
                             ") ENGINE=InnoDB")
        for x in range(0, int(len(wins)/4), 2):
            newPlayers.append(reproduce(arrayOfPlayers[sortedNumbers[x]], arrayOfPlayers[sortedNumbers[x+1]],numberOfPlayersCreated))
            insertPlayer(newPlayers[0], newPlayers[0].parentone, newPlayers[0].parenttwo)
            newPlayers.append(Player(3, 363, 363, 362, numberOfPlayersCreated+2, [], 999, 999))
            insertPlayer(newPlayers[1], newPlayers[0].parentone, newPlayers[0].parenttwo)
            newPlayers.append(arrayOfPlayers[sortedNumbers[x]])
            insertPlayer(newPlayers[2], newPlayers[0].parentone, newPlayers[0].parenttwo)
            newPlayers.append(arrayOfPlayers[sortedNumbers[x+1]])
            insertPlayer(newPlayers[3], newPlayers[0].parentone, newPlayers[0].parenttwo)
            numberOfPlayersCreated += 2
        arrayOfPlayers = newPlayers

#Create new players from the best players
def reproduce(playerone, playertwo, numberOfPlayers):
    playeroneweights = []
    playertwoweights = []
    newweights = []
    for x in range(len(playerone.weights)):
        playeroneweights.append(playerone.weights[x])
        playertwoweights.append(playertwo.weights[x])
    allnewweights = []
    for x in range(len(playertwoweights)):
        newnewweights = []
        for y in range(len(playertwoweights[x])):
            newweights = []
            for z in range(len(playertwo.weights[x][y])):
                if random.random() > 0.5:
                    newweights.append(playertwo.weights[x][y][z])
                else:
                    newweights.append(playerone.weights[x][y][z])
                if random.random() < 1 /(len(playertwoweights)*len(playertwoweights[x])*len(playertwo.weights[x][y])) :
                    newweights[-1] = round(random.random(),4)
            newnewweights.append(newweights)
        allnewweights.append(newnewweights)

    playerone.numchildren += 1
    playertwo.numchildren += 1
    return Player(3, 363, 363, 362,numberOfPlayers+1, allnewweights, playerone.id, playertwo.id)

#load players at end of most recent era
def load():
    arrayOfPlayers = []
    #need a query that finds the highest id number in the players table
    #numberOfPlayersCreated = numberOfPlayersPerRound?
    cnx = mysql.connector.connect(user='root', password='mysql', host='127.0.0.1', database='test')
    #need a query that returns the current era from the matches table
#    currentEra =
    #need a query that returns the latest match
#    completedMatches =

    #load players from players table
    #need query to return weights for each platyer
    #need to shape weights into the right order and shape
#    weights =
    for x in range(numberOfPlayersPerRound):
        arrayOfPlayers.append(Player(3, 363, 363, 362, str(x), []))
    return arrayOfPlayers, numberOfPLayersCreated, startEra

#Create new players
def startNew(numberOfPlayersPerRound):
    cnx = mysql.connector.connect(user='root', password='mysql', host='127.0.0.1', database='test')
    arrayOfPlayers = []
    numberOfPlayersCreated = numberOfPlayersPerRound
    cnx.cursor().execute("DROP TABLE if exists `matches`")
    cnx.cursor().execute("CREATE TABLE `matches` ("
                         "  `timestamp` time(2) NOT NULL, "
                         "  `era_no` int(3) NOT NULL ,"
                         "  `match_no` int(2) NOT NULL,"
                         "  `player_one_id` int(3) NOT NULL,"
                         "  `player_two_id` int(3) NOT NULL,"
                         "  `player_one_winner` bool NOT NULL,"
                         "  `draw` bool NOT NULL,"
                         "  `no_moves` int(3) NOT NULL,"
                         "  PRIMARY KEY (`timestamp`)"
                         ") ENGINE=InnoDB")
    cnx.cursor().execute("DROP TABLE if exists `players`")
    cnx.cursor().execute("CREATE TABLE `players` ("
                         "  `timestamp` time(2) NOT NULL, "
                         "  `player_id` int(3) NOT NULL,"
                         "  `parent_one_id` int(3) NOT NULL,"
                         "  `parent_two_id` int(3) NOT NULL,"
                         "  `layer_one_weights` mediumtext NOT NULL ,"
                         "  `layer_two_weights` mediumtext NOT NULL,"
                         "  `layer_three_weights` mediumtext NOT NULL,"
                         "  PRIMARY KEY (`timestamp`)"
                         ") ENGINE=InnoDB")
    cnx.close()
    for x in range(numberOfPlayersPerRound):
        arrayOfPlayers.append(Player(3, 363, 363, 362, str(x + 1), [], 999, 999))
        insertPlayer(arrayOfPlayers[x], arrayOfPlayers[x].parentone, arrayOfPlayers[x].parenttwo)

    return arrayOfPlayers, numberOfPlayersPerRound, 0

#Function that insserts new player into database
def insertPlayer(player, parent_one_id, parent_two_id):
    cnx = mysql.connector.connect(user='root', password='mysql', host='127.0.0.1', database='test')
    add_player = ("INSERT INTO `players`"
                  "(timestamp, player_id, parent_one_id, parent_two_id, layer_one_weights, layer_two_weights, layer_three_weights)"
                  "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    data_player = (str(datetime.now()), str(player.id), str(parent_one_id), str(parent_two_id), str(player.weights[0]),
                   str(player.weights[1]), str(player.weights[2]))
    cnx.cursor().execute(add_player, data_player)
    cnx.commit()
    cnx.close()

handler()

