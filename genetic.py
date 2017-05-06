import random
import go
import itertools
import mysql.connector
from datetime import datetime





class Player:

    def __init__(self, depth, height, inputs, output, id, weights):
        self.depth = depth
        self.height = height
        self.input = inputs
        self.output = output
        self.id = id.rjust(3,'0')
        self.numchildren = 0
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



def handler():
    numberOfEra = 100
    arrayOfPlayers = []
    runningScores = []
    numberOfPlayersPerRound = 4
    numberOfPlayersCreated = numberOfPlayersPerRound
    cnx = mysql.connector.connect(user='root', password='mysql',
                                  host='127.0.0.1',
                                  database='test')
    cnx.cursor().execute("DROP TABLE if exists `matches`")
    cnx.cursor().execute("CREATE TABLE `matches` ("
                         "  `timestamp` time NOT NULL, "
                         "  `era_no` int(3) NOT NULL ,"
                         "  `turn_no` int(2) NOT NULL,"
                         "  `player_one_id` int(3) NOT NULL,"
                         "  `player_two_id` int(3) NOT NULL,"
                         "  `player_one_winner` bool NOT NULL,"
                         "  `draw` bool NOT NULL,"
                         "  `no_moves` int(3) NOT NULL,"
                         "  PRIMARY KEY (`timestamp`)"
                         ") ENGINE=InnoDB")


    for x in range(numberOfPlayersPerRound):
        arrayOfPlayers.append(Player(3, 363, 363, 362, str(x), []))

    '''
    f = open('record.txt', 'w')
    f.close()
    '''
    for i in range(numberOfEra):
        print('Era: ' + str(i+1))
        wins = []
        for x in range(numberOfPlayersCreated):
            wins.append(0)


        matches = list(itertools.permutations(range(len(wins)), 2))
        winner = 2
        for x in range(len(matches)):
            print('Match:' + str(x+1))
            winner, moves = go.playgo(arrayOfPlayers[matches[x][0]], arrayOfPlayers[matches[x][1]])
            add_match = ("INSERT INTO `matches`"
                        "(timestamp, era_no, turn_no, player_one_id, player_two_id, player_one_winner, draw, no_moves) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
            if winner == 2:
             #   data_turn = (str(i+1).rjust(3,'0'),str(x).rjust(2,'0'),arrayOfPlayers[matches[x][0]].id,
              #              arrayOfPlayers[matches[x][1]].id,True,False)
                wins[matches[x][0]] += 1
            #elif winner == 1:

            elif winner == 0:
             #   data_turn = (str(i + 1).rjust(3,'0'), str(x).rjust(2,'0'), arrayOfPlayers[matches[x][0]].id,
              #              arrayOfPlayers[matches[x][1]].id, False, False)
                wins[matches[x][1]] += 1
            data_match = (str(datetime.now()) ,str(i + 1).rjust(3, '0'), str(x).rjust(2, '0'), arrayOfPlayers[matches[x][0]].id,
                arrayOfPlayers[matches[x][1]].id, winner == 2 or winner == 1, winner == 1, str(moves))
            cnx.cursor().execute(add_match, data_match)
            cnx.commit()
        print(wins)
        runningScores.append(wins)
        numbers = []
        playerids = []
        for x in range(len(wins)):
            numbers.append(x)
            playerids.append(arrayOfPlayers[x].id)
        '''
        with open('record.txt', 'a+') as f:
            for item in wins:
                f.write("%s " % item)
            f.write('\n')
            for item in playerids:
                f.write("%s " % item)
            f.write('\n')
        '''
        sortedNumbers = [x for y, x in sorted(set(zip(wins, numbers)), reverse=True)]
        newPlayers = []
        d = open('weights.txt', 'w')
        d.close()

        for x in range(0, int(len(wins)/4), 2):

            newPlayers.append(reproduce(arrayOfPlayers[sortedNumbers[x]], arrayOfPlayers[sortedNumbers[x+1]]),numberOfPlayersCreated)
            newPlayers.append(Player(3, 363, 363, 362, numberOfPlayersCreated+2, []))
            newPlayers.append(arrayOfPlayers[sortedNumbers[x]])
            newPlayers.append(arrayOfPlayers[sortedNumbers[x+1]])
            numberOfPlayersCreated += 2
            with open('weights.txt', 'a+') as d:
                for item in arrayOfPlayers[sortedNumbers[x]].weights:
                    for seconditem in item:
                        for thirditem in seconditem:
                            d.write("%s " % thirditem)
                d.write('\n')
                for item in arrayOfPlayers[sortedNumbers[x+1]].weights:
                    for seconditem in item:
                        for thirditem in seconditem:
                            d.write("%s " % thirditem)
                d.write('\n')
        arrayOfPlayers = newPlayers



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
    return Player(3, 363, 363, 362,numberOfPlayers+1, allnewweights)


handler()

