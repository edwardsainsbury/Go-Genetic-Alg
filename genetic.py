import random
import go
import itertools
import mysql.connector
from datetime import datetime
import ast

#player class
class Player:

    def __init__(self, depth, height, inputs, output, id, weights, parentone, parenttwo):
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
            weights.append([[round(random.random(), 4) for _ in range(inputs)] for _ in range(height)])
            for x in range(depth - 1):
                weights.append([[round(random.random(), 4)for _ in range(height)] for _ in range(height)])
            weights.append([[round(random.random(), 4)for _ in range(height)] for _ in range(output)])
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
    do_load = 1
    if do_load:
        arrayOfPlayers, numberOfPlayersCreated, startEra = load()
    else:
        arrayOfPlayers, numberOfPlayersCreated, startEra = startNew(numberOfPlayersPerRound)

    for i in range(startEra, numberOfEra, 1):
        print('Era: ' + str(i+1))
        wins = []

        for x in range(numberOfPlayersPerRound):
            wins.append(0)

        matches = list(itertools.permutations(range(numberOfPlayersPerRound), 2))
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
                             "  `player_weights_1` mediumtext NOT NULL,"
                             "  `player_weights_2` mediumtext NOT NULL,"
                             "  `player_weights_3` mediumtext NOT NULL,"
                             "  `player_weights_4` mediumtext NOT NULL,"
                             "  PRIMARY KEY (`timestamp`)"
                             ") ENGINE=InnoDB")

        for x in range(0, int(len(wins)/4), 2):
            newPlayers.append(reproduce(arrayOfPlayers[sortedNumbers[x]], arrayOfPlayers[sortedNumbers[x+1]], numberOfPlayersCreated))
            newPlayers.append(Player(3, 363, 363, 362, numberOfPlayersCreated+2, [], 999, 999))
            newPlayers.append(arrayOfPlayers[sortedNumbers[x]])
            newPlayers.append(arrayOfPlayers[sortedNumbers[x+1]])
            for player in newPlayers:
                insertPlayer(player)
            numberOfPlayersCreated += 2
        arrayOfPlayers = newPlayers

#Create new players from the best players
def reproduce(playerone, playertwo, numberOfPlayers):
    playeroneweights = []
    playertwoweights = []

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
                if random.random() < 1 / (len(playertwoweights)*len(playertwoweights[x])*len(playertwo.weights[x][y])):
                    newweights[-1] = round(random.random(), 4)
            newnewweights.append(newweights)
        allnewweights.append(newnewweights)

    playerone.numchildren += 1
    playertwo.numchildren += 1
    return Player(3, 363, 363, 362, numberOfPlayers+1, allnewweights, playerone.id, playertwo.id)

#load players at end of most recent era
def load():
    arrayOfPlayers = []

    #numberOfPlayersCreated = numberOfPlayersPerRound?
    cnx = mysql.connector.connect(user='root', password='mysql', host='127.0.0.1', database='test')
    cursor = cnx.cursor()
    #need a query that returns the current era from the matches table
    cursor.execute("SELECT MAX(era_no) FROM matches")
    currentEra = cursor.fetchone()[0]
    currentEra = 0 if currentEra is None else currentEra

    # need a query that finds the highest id number in the players table
    cursor.execute("SELECT MAX(player_id) FROM players")
    numberOfPlayersCreated = cursor.fetchone()[0]
    #need to delete matches at the srart of the era
    cursor.execute("DELETE FROM matches WHERE era_no = %s" % currentEra)
    cnx.commit()
    #load players from players table
    cursor.execute("SELECT player_id, parent_one_id, parent_two_id, player_weights_1, "
                             "player_weights_2, player_weights_3, player_weights_4 FROM players ")
    playerData = cursor.fetchall()
    for player in playerData:
        arrayOfPlayers.append(Player(3, 363, 363, 362, player[0], [ast.literal_eval(player[3]), ast.literal_eval(player[4]), ast.literal_eval(player[5]), ast.literal_eval(player[6])], player[1], player[2]))
    cnx.close()
    return arrayOfPlayers, numberOfPlayersCreated, currentEra

#Create new players
def startNew(numberOfPlayersPerRound):
    cnx = mysql.connector.connect(user='root', password='mysql', host='127.0.0.1', database='test')
    arrayOfPlayers = []
    cnx.cursor().execute("DROP TABLE if exists `matches`")
    cnx.cursor().execute("CREATE TABLE `matches` ("
                         "  `timestamp` time(6) NOT NULL, "
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
                         "  `player_weights_1` mediumtext NOT NULL ,"
                         "  `player_weights_2` mediumtext NOT NULL,"
                         "  `player_weights_3` mediumtext NOT NULL,"
                         "  `player_weights_4` mediumtext NOT NULL,"
                         "  PRIMARY KEY (`timestamp`)"
                         ") ENGINE=InnoDB")
    cnx.close()
    for x in range(numberOfPlayersPerRound):
        arrayOfPlayers.append(Player(3, 363, 363, 362, str(x + 1), [], 999, 999))
        insertPlayer(arrayOfPlayers[x])

    return arrayOfPlayers, numberOfPlayersPerRound, 0

#Function that inserts new player into database
def insertPlayer(player):
    cnx = mysql.connector.connect(user='root', password='mysql', host='127.0.0.1', database='test')
    add_player = ("INSERT INTO `players`"
                  "(timestamp, player_id, parent_one_id, parent_two_id, player_weights_1, player_weights_2, player_weights_3, player_weights_4)"
                  "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
    data_player = (str(datetime.now()), str(player.id), str(player.parentone), str(player.parenttwo), str(player.weights[0]),
                   str(player.weights[1]), str(player.weights[2]), str(player.weights[3]))
    cnx.cursor().execute(add_player, data_player)
    cnx.commit()
    cnx.close()

handler()
