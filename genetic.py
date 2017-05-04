import random
import go
import itertools
from multiprocessing.dummy import Pool as ThreadPool

class Player:

    def __init__(self, depth, height, inputs, output, id, weights):
        self.depth = depth
        self.height = height
        self.input = inputs
        self.output = output
        self.id = id
        self.numchildren = 0

        # Change weights order to work backwards
        if len(weights) == 0:
            weights.append([[round(random.random(),4) for x in range(inputs)] for y in range(height)])
        # self.weights.append([[1 for x in range(input)] for y in range(height)])
            for x in range(depth - 1):
                weights.append([[round(random.random(),4)for x in range(height)] for y in range(height)])
                # self.weights.append([[1 for x in range(height)] for y in range(height)])
            weights.append([[round(random.random(),4)for x in range(height)] for y in range(output)])
            # self.weights.append([[1 for x in range(height)] for y in range(output)])
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

#test = Player(2, 20, 361, 361)

# print(test.weights[0])
# print(test.weights[1])
# print(test.weights[2])
#inputs = []
#for x in range(361):
#    inputs.append(1)
#outputs = test.result(inputs)
#max = 0
#for x in range(361):
#    if outputs[x] > max:
#        i = x
#        max = outputs[x]
#print(i, max)


def handler():
    numberOfEra = 100
    arrayOfPlayers = []
    runningScores = []
    numberOfPlayers = 4

    for x in range(numberOfPlayers):
        newPlayer = Player(3, 363, 363, 362, str(x), [])
        arrayOfPlayers.append(newPlayer)

    f = open('record.txt', 'w')
    f.close()

    for i in range(numberOfEra):
        print('Era: ' + str(i+1))
        wins = []
        for x in range(numberOfPlayers):
            wins.append(0)


        matches = list(itertools.permutations(range(len(wins)), 2))
        winner = 1
        '''
        firstOpponent = []
        secondOpponent = []
        for x in range(len(matches)):
            firstOpponent.append(arrayOfPlayers[matches[x][0]])
            secondOpponent.append(arrayOfPlayers[matches[x][1]])

        pool = ThreadPool(8)
        winner = pool.starmap(go.playgo, zip(firstOpponent, secondOpponent))
        pool.close()
        pool.join()
        '''
        for x in range(len(matches)):
            print('Match:' + str(x+1))
            winner = go.playgo(arrayOfPlayers[matches[x][0]], arrayOfPlayers[matches[x][1]])
            if winner == 2:
                wins[matches[x][0]] += 1
            elif winner == 0:
                wins[matches[x][1]] += 1

        print(wins)
        runningScores.append(wins)
        numbers = []
        playerids = []
        for x in range(len(wins)):
            numbers.append(x)
            playerids.append(arrayOfPlayers[x].id)

        with open('record.txt', 'a+') as f:
            for item in wins:
                f.write("%s " % item)
            f.write('\n')
            for item in playerids:
                f.write("%s " % item)
            f.write('\n')

        sortedNumbers = [x for y, x in sorted(set(zip(wins, numbers)), reverse=True)]
        newPlayers = []
        d = open('weights.txt', 'w')
        d.close()

        for x in range(0, int(len(wins)/4), 2):
            if arrayOfPlayers[sortedNumbers[x]].id > arrayOfPlayers[sortedNumbers[x+1]].id:
                newPlayers.append(reproduce(arrayOfPlayers[sortedNumbers[x]], arrayOfPlayers[sortedNumbers[x+1]]))
                newPlayers.append(reproduce(arrayOfPlayers[sortedNumbers[x]], arrayOfPlayers[sortedNumbers[x+1]]))
                newPlayers.append(arrayOfPlayers[sortedNumbers[x]])
                newPlayers.append(arrayOfPlayers[sortedNumbers[x+1]])
            else:
                newPlayers.append(reproduce(arrayOfPlayers[sortedNumbers[x+1]], arrayOfPlayers[sortedNumbers[x]]))
                newPlayers.append(reproduce(arrayOfPlayers[sortedNumbers[x+1]], arrayOfPlayers[sortedNumbers[x]]))
                newPlayers.append(arrayOfPlayers[sortedNumbers[x+1]])
                newPlayers.append(arrayOfPlayers[sortedNumbers[x]])
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



def reproduce(playerone, playertwo):
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
    if len(playerone.id) ==1:
        newid = playerone.id+'00'+str(playerone.numchildren)+playertwo.id+'00'+str(playertwo.numchildren)
    elif playerone.numchildren>9 and playertwo.numchildren > 9 :
        newid = playerone.id[0] + '0' + str(playerone.numchildren) + playertwo.id[0] + '0' + str(playertwo.numchildren)
    elif playertwo.numchildren > 9:
        newid = playerone.id[0] + '00' + str(playerone.numchildren) + playertwo.id[0] + '0' + str(playertwo.numchildren)
    elif playerone.numchildren > 9:
        newid = playerone.id[0] + '0' + str(playerone.numchildren) + playertwo.id[0] + '00' + str(playertwo.numchildren)
    else:
        newid = playerone.id[0] + '00' + str(playerone.numchildren) + playertwo.id[0] + '00' + str(playertwo.numchildren)
    return Player(3, 363, 363, 362,newid, allnewweights)



'''
    firstMoveInput = []
    gameWon = 0
    for x in range(19*19+1):
        #add 1 as first player flag
        firstMoveInput.append(1)
    # Add 0 as pass flag
    firstMoveInput.append(0)
    input = firstMoveInput
    counter = 0
    while gameWon == 0 and counter < 100:
        #print('Turn', counter)
        output, forfeit1, gameWon = turn(playerOne, input, True)
        output[361] = 0
        input, forfeit2, gameWon = turn(playerTwo, output, False)
        input[361] = 1
        if forfeit1 and forfeit2 is True:
            gameWon = True
        counter += 1
        print(input)
    print('Game Over')
'''


'''
def turn(player, input, first):
    result = player.result(input)
    numbers = []
    for x in range(len(result)):
        numbers.append(x)

    sortedNumbers = [x for y, x in sorted(zip(result, numbers))]
    sortedResult = [y for y, x in sorted(zip(result, numbers))]


    for x in range(361):
        if sortedNumbers[x] == 362:
            return input, True, False
        gameWon, input, legal = moveIsLegal(sortedNumbers[x], input, first)
        if legal:
            break

    if legal is True and gameWon is False:
        return input, False, gameWon

        #check if the next highest value is acceptable

def moveIsLegal(i, input, first):
    #legal move
    #cant move, already piece there
    #cant lay piece as would be taken
    #has taken other players piece



    #moves are exhasuted add points to deterine winner


    if input[i] == 1:
        if first:
            input[i] = 2
        else:
            input[i] = 0
        return False, input, True
    else:
        return False, input, False
'''



handler()

