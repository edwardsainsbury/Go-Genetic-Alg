import math

## The number of spots per side of the board
## This code allows for an nxn board
boardsize = 19
## Value determining whether the player wants to quit or not
gameon = 1
## Lists of groups that have been removed from the board via capture,
## held in these varaibles in case, when all captures have been
## completed, the board resembles a previous game state and
## the move is invalid.  In that case, the groups are restored
## from these varaibles.
restore_o = []
restore_x = []


## Generates blank game states
def initalize():
    gs = []
    for i in range(0, boardsize):
        gs.append([])
        for j in range(0, boardsize):
            gs[i].append('-')
    return gs


## Provides an ascii display of the Go board
def printboard(gs):
    global boardsize
    for row in gs:
        rowprint = ''
        for element in row:
            rowprint += element
            rowprint += ' '
        print(rowprint)


## Returns a list of the board positions surrounding the
## passed group.
def gperm(group):
    permimeter = []
    global boardsize
    hit = 0
    loss = 0
    ## Adds permimeter spots below
    ## Works by looking from top to bottom, left to right,
    ## at each posisition on the board.  When a posistion
    ## is hit that is in the given group, I set hit = 1.
    ## Then, at the next position that is not in that group,
    ## or if the end of the column is reached, I set loss = 1.
    ## That point is the first point below a point in that group,
    ## so it is part of the permieter of that group.
    i = 0
    j = 0
    while i < boardsize:
        j = 0
        hit = 0
        while j < boardsize:
            if [i, j] in group:
                hit = 1
            elif (hit == 1) & ([i, j] not in group):
                loss = 1
            if (hit == 1) & (loss == 1):
                permimeter.append([i, j])
                hit = 0
                loss = 0
            j += 1
        i += 1
    ## Adds permimeter spots to the right
    i = 0
    j = 0
    while i < boardsize:
        j = 0
        hit = 0
        while j < boardsize:
            if [j, i] in group:
                hit = 1
            elif (hit == 1) & ([j, i] not in group):
                loss = 1
            if (hit == 1) & (loss == 1):
                permimeter.append([j, i])
                hit = 0
                loss = 0
            j += 1
        i += 1
    ## Adds permimeter spots above
    i = 0
    j = boardsize - 1
    while i < boardsize:
        j = boardsize - 1
        hit = 0
        while j >= 0:
            if [i, j] in group:
                hit = 1
            elif (hit == 1) & ([i, j] not in group):
                loss = 1
            if (hit == 1) & (loss == 1):
                permimeter.append([i, j])
                hit = 0
                loss = 0
            j -= 1
        i += 1
    ## Adds permimeter spots to the left
    i = 0
    j = boardsize - 1
    while i < boardsize:
        j = boardsize - 1
        hit = 0
        while j >= 0:
            if [j, i] in group:
                hit = 1
            elif (hit == 1) & ([j, i] not in group):
                loss = 1
            if (hit == 1) & (loss == 1):
                permimeter.append([j, i])
                hit = 0
                loss = 0
            j -= 1
        i += 1
    return permimeter


## Returns a string that describes the game state
def readable(gs):
    readthis = ''
    readthis += '<<'
    for row in gs:
        for element in row:
            readthis += element
    readthis += '>>'
    return readthis


## Counts the territory captured by each player
def count():
    global gsc
    global non_groups
    global o_points
    global x_points
    global boardsize

    ## Creates a list of groups (non_groups) of empty positions.
    for i in range(0, boardsize):
        for j in range(0, boardsize):
            if gsc[j][i] == '-':
                new = 1
                for group in non_groups:
                    if [i, j] in gperm(group):
                        group.append([i, j])
                        new = 0
                if new == 1:
                    non_groups.append([[i, j]])
    concat('-')

    o_points = 0
    x_points = 0

    ## Gives a point to the each player for every pebble they have
    ## on the board.
    for group in o_groups:
        o_points += len(group)
    for group in x_groups:
        x_points += len(group)

    ## The permimeter of these empty positions is here considered,
    ## and if every position in the permimeter of a non_group is
    ## one player or the other, that player gains a number of points
    ## equal to the length of that group (the number of positions
    ## that their pieces enclose).
    for group in non_groups:
        no = 0
        for element in gperm(group):
            if gsc[element[1]][element[0]] != 'o':
                no = 1
        if no == 0:
            o_points += len(group)

    for group in non_groups:
        no = 0
        for element in gperm(group):
            if gsc[element[1]][element[0]] != 'x':
                no = 1
        if no == 0:
            x_points += len(group)


## Checks for capture, and removes the captured pieces from the board
def capture(xoro,opponent):
    global o_groups
    global x_groups
    global gsf
    global restore_o
    global restore_x
    global edited
    if xoro == 'o':
        groups = x_groups
        otherplayer = 'o'
    else:
        groups = o_groups
        otherplayer = 'x'

    ## Checks to see, for each group of a particular player,
    ## whether any of the board positions in the
    ## perimeter around that group are held by the other player.
    ## If any position is not held by the other player,
    ## the group is not captured, and is safe.  Otherwise,
    ## the group is removed.  But we haven't tested this yet
    ## to see if this would return the board to a previous
    ## state, so we save the removed groups with the restore lists.
    for group in groups:
        safe = 0
        for element in gperm(group):
            if gsf[element[1]][element[0]] != otherplayer:
                safe = 1
        if safe != 1:
            edited = 1

            if opponent:
                #print('Would result in opponent capture')
                return 0
            else:
                if xoro == 'o':
                    restore_x.append(group)
                else:
                    restore_o.append(group)
            try:
                groups.remove(group)
            except:
                pass

    # Sets gsf given the new captures
    gsf = initalize()
    for group in o_groups:
        for point in group:
            gsf[point[1]][point[0]] = 'o'
    for group in x_groups:
        for point in group:
            gsf[point[1]][point[0]] = 'x'
    return 1


## Checks to see if the new game state, created by the most recent
## move, returns the board to a previous state.  If not, then
## gsc is set as this new state, and gsp is set as what gsc was, and
## the new game state is stored in gscache.  The function returns 1
## if the move is valid, 0 otherwise.
def goodmove():
    global gscache
    global gsc
    global gsp
    global gsf
    if readable(gsf) not in gscache:
        gsp = []
        gsc = []
        for element in gsf:
            gsp.append(element)
            gsc.append(element)
        gscache += readable(gsf)
        return 1
    else:
        return 0


## Checks if any groups contain the same point;
## if so, joins them into one group
def concat(xoro):
    global o_groups
    global x_groups
    global non_groups
    if xoro == 'o':
        groups = o_groups
    elif xoro == 'x':
        groups = x_groups
    else:
        groups = non_groups
    i = 0
    ## currentgroups and previousgroups are used to compare the number
    ## of groups before this nest of whiles to the number after.  If
    ## The number is the same, then nothing needed to be concatinated,
    ## and we can move on.  If the number is different, two groups
    ## were concatinated, and we need to run through this nest again
    ## to see if any other groups need to be joined together.
    currentgroups = len(groups)
    previousgroups = currentgroups + 1
    ## Checks if the positions contained in any group are to be
    ## found in any other group.  If so, all elements of the second are
    ## added to the first, and the first is deleted.
    while previousgroups != currentgroups:
        while i < len(groups) - 1:
            reset = 0
            j = i + 1
            while j < len(groups):
                k = 0
                while k < len(groups[i]):
                    if groups[i][k] in groups[j]:
                        for element in groups[j]:
                            if element not in groups[i]:
                                groups[i].append(element)
                        groups.remove(groups[j])
                        reset = 1
                    if reset == 1:
                        break
                    k += 1
                j += 1
            if reset == 1:
                i = -1
            i += 1
        previousgroups = currentgroups
        currentgroups = len(groups)


## Adds point xy to a group if xy is in the
## perimeter of an existing group, or creates
## new group if xy is not a part of any existing group.
def addpoint(xy, xoro):
    global o_groups
    global x_groups
    if xoro == 'o':
        groups = o_groups
    else:
        groups = x_groups
    new = 1
    for group in groups:
        if xy in gperm(group):
            group.append(xy)
            new = 0
    if new == 1:
        groups.append([xy])

def removepoint(xy, xoro):
    global o_groups
    global x_groups
    #global completedMoves
    if xoro == 'o':
        groups = o_groups
    else:
        groups = x_groups
    for group in groups:
        if xy in group:
            group.remove(xy)
            new = 0



## Lets the player select a move.
def selectmove(xoro, move):
    global boardsize
    global gsf
    global gsc
    valid = 1


    '''
    while minihold == 1:


        #pp = input('Place or pass (l/a)? ')
        #if pp == 'a':
        if round(output[362]) == 1:
            return 'pass'
        elif round(output[362]) == 0:
            minihold = 0
            ## This try...except ensures that the user
            ## inputs only numbers
            error = 0





            try:
                x = int(input('x: '))
            except ValueError:
                error = 1
            try:
                y = int(input('y: '))
            except ValueError:
                error = 1
            if error == 1:
                minihold = 1
                print('invalid')

        else:
            print('invalid')
    '''
    x = move[0]
    y = move[1]
    ## Ensures that the input is on the board
    if (x > boardsize) | (x < 0) | (y > boardsize) | (y < 0):
        #print('invalid')
        valid = 0
    elif gsc[y][x] != '-':
        #print('invalid')
        valid = 0
    #middle
    elif x < 18 and y < 18 and x > 0 and y > 0:
        if (gsc[y+1][x] != xoro and gsc[y+1][x] != '-') and (gsc[y][x+1] != xoro and gsc[y][x+1] != '-') and (gsc[y][x-1] != xoro and gsc[y][x-1] != '-') and (gsc[y-1][x] != xoro and gsc[y-1][x] != '-'):
            # print('invalid')
            valid = 0
    #right edge
    elif x == 18 and y < 18 and y > 0:
        if (gsc[y+1][x] != xoro and gsc[y+1][x] != '-') and (gsc[y][x-1] != xoro and gsc[y][x-1] != '-') and (gsc[y-1][x] != xoro and gsc[y-1][x] != '-'):
            # print('invalid')
            valid = 0
    #bottom edge
    elif x < 18 and y == 18 and x > 0:
        if (gsc[y][x+1] != xoro and gsc[y][x+1] != '-') and (gsc[y][x-1] != xoro and gsc[y][x-1] != '-') and (gsc[y-1][x] != xoro and gsc[y-1][x] != '-'):
            # print('invalid')
            valid = 0
    # left edge
    elif y < 18 and x == 0 and y > 0:
        if (gsc[y+1][x] != xoro and gsc[y+1][x] != '-') and (gsc[y][x+1] != xoro and gsc[y][x+1] != '-') and (gsc[y-1][x] != xoro and gsc[y-1][x] != '-'):
            # print('invalid')
            valid = 0
    #top edge
    elif x < 18  and x > 0 and y == 0:
        if (gsc[y+1][x] != xoro and gsc[y+1][x] != '-') and (gsc[y][x+1] != xoro and gsc[y][x+1] != '-') and (gsc[y][x-1] != xoro and gsc[y][x-1] != '-'):
            # print('invalid')
            valid = 0
    #bottom right
    elif x == 18 and y == 18:
        if (gsc[y][x-1] != xoro and gsc[y][x-1] != '-') and (gsc[y-1][x] != xoro and gsc[y-1][x] != '-'):
            # print('invalid')
            valid = 0
    #top right
    elif x == 18 and y == 0:
        if (gsc[y+1][x] != xoro and gsc[y+1][x] != '-') and (gsc[y][x-1] != xoro and gsc[y][x-1] != '-'):
            # print('invalid')
            valid = 0
    #top left
    elif x == 0 and y == 0:
        if (gsc[y+1][x] != xoro and gsc[y+1][x] != '-') and (gsc[y][x+1] != xoro and gsc[y][x+1] != '-'):
            # print('invalid')
            valid = 0
    #bottom left
    elif x == 0 and y == 18:
        if (gsc[y][x+1] != xoro and gsc[y][x+1] != '-')  and (gsc[y-1][x] != xoro and gsc[y-1][x] != '-'):
            # print('invalid')
            valid = 0
    else:
        hold = 0


    ## Places the piece on the 'future' board, the board
    ## used to test if a move is valid
    if valid:
        if xoro == 'o':
            gsf[y][x] = 'o'
        else:
            gsf[y][x] = 'x'

    return [x, y], valid


## The 'turn,' in which a player makes a move,
## the captures caused by that piece are made,
## the validity of the move is checked, and
## the endgame status is checked.
def turn(output):
    global xoro
    global notxoro
    global player1_pass
    global player2_pass
    global gameover
    #global completedMoves

    numbers = []
    hold = 1
    counter = 0

    for x in range(len(output[0:362])):
        numbers.append(x)

    sortedNumbers = [x for y, x in sorted(zip(output, numbers), reverse=True)]

    #print('place for ' + xoro)
    while hold == 1 and counter < 362:

        ## By calling selectmove(), the player
        ## is given the option of whether to place
        ## a piece or to pass, and where to place
        ## that piece.


        if sortedNumbers[counter] == 361 or counter == 361:
            if xoro == 'o':
                player1_pass = 1
            else:
                player2_pass = 1
            hold = 0
        ## If the player doesn't pass...
        else:

            #if sortedNumbers[counter] in completedMoves:
            #    counter += 1
            #    continue




            move = [0, 0]
            move[0] = sortedNumbers[counter] % 19
            move[1] = math.floor(sortedNumbers[counter] / 19)
            # print(move)
            xy, valid = selectmove(xoro, move)

            if not valid:
                counter +=1
                continue


            if xoro == 'o':
                player1_pass = 0
            else:
                player2_pass = 0


            ## The new piece is added to its group,
            ## or a new group is created for it.
            addpoint(xy, xoro)
            ## Groups that have been connected by
            ## the this placement are joined together
            concat(xoro)
            minihold = 1
            ## Edited is a value used to check
            ## whether any capture is made.  capture()
            ## is called as many times as until no pieces
            ## are capture (until edited does not change
            ## to 1)
            #edited = 0
            #while minihold == 1:
            #    restore_o = []
             #   restore_x = []
            allowedmove = capture(notxoro, True)
            if not allowedmove:
                removepoint(xy, xoro)
                gsf[move[1]][move[0]] = '-'
                counter +=1
                continue
            nocapture = capture(xoro, False)

            ## Checks to see if the move, given all the
            ## captures it causes, would return the board
            ## to a previous game state.
            if goodmove() == 1:
                hold = 0
            ## If the move is invalid, the captured groups need
            ## to be returned to the board, so we use
            ## the groups stored in the restore lists to
            ## restore the o_ and x_groups lists.
            else:
                #print('invalid move - that returns to board to a previous state')
                '''
                for group in restore_o:
                    o_groups.append(group)
                for group in restore_x:
                    x_groups.append(group)
                '''
        #print(counter)
        counter +=1
    #completedMoves.append(counter)
    if (player1_pass == 1) & (player2_pass == 1):
        gameover = 1


## Called to start a game
def playgo(playerone, playertwo):
    ## Either 'o' or 'x', determines who's turn it is
    global xoro
    ## The opposite of xoro, determines who's turn it is not
    global notxoro
    ## Game State Current, the current layout of the board
    ## This value is two-dimensional list, the higher dimension being
    ## lists representing the rows and the lower dimension being
    ## strings representing individual positions on the board.
    ## These strings are either '-', 'o', or 'x'
    global gsc
    ## 0 or 1, determins whether the current game is ongoing or ended
    global gameover
    ## Game State Future, same setup as gsc, used for testing the
    ## waters of a new move, to see if that move is valid, before
    ## gsc is edited to reflect that move
    global gsf
    ## Two-dimensional lists, the higher dimension being groups, the
    ## lower dimension being lists of board positions in a particular
    ## group
    global o_groups
    global x_groups
    ## Groups of empty positions
    global non_groups
    ## String containing all the game states encountered in a particular
    ## game, used to check validity of moves
    global gscache
    ## 0 or 1, for whether the player has passed their turn or not
    global player1_pass
    global player2_pass
    ## Integer value reflecting the score of a player
    global o_points
    global x_points
    #global completedMoves
    #completedMoves = []
    ## Creates a blank game state - a blank board
    gsc = initalize()
    gsf = initalize()
    ## Sets initial values
    o_groups = []
    x_groups = []
    non_groups = []
    gscache = ''
    player1_pass = 0
    player2_pass = 0
    gameover = 0
    o_points = 0
    x_points = 0
    counter = 0
    ## Gives players turns until the end of the game
    ## (that is, until both players pass, one after
    ## the other)
    while gameover != 1 and counter < 1000:

        ## Set it as o-player's turn
        xoro = 'o'
        notxoro = 'x'

        print('Turn ' + str(counter) + ' ' + xoro)

        output = playerone.result(gsctonet(gsc, True))
        turn(output)
        #printboard(gsc)
        counter += 1

        if gameover == 1:
            break

        ## Sets it as x-player's turn
        xoro = 'x'
        notxoro = 'o'

        #print()
        print('Turn ' + str(counter) + ' ' + xoro)

        output = playertwo.result(gsctonet(gsc, False))
        turn(output)

        #printboard(gsc)
        #print()
        counter += 1

    ## Counts the score of both players
    count()
    #print()
    print('final board:')
    #print()
    printboard(gsc)
    #print()
    print('o points: ', str(o_points))
    print('x points: ', str(x_points))
    ## Determines the winner
    if counter == 1000:
        o_points = x_points
    if o_points > x_points:
        print('o wins')
        return 2
    elif x_points > o_points:
        print('x wins')
        return 0
    else:
        print('tie')
        return 1


## Finally something that is not a function!
## This while loop will start new games for as
## long as the user choses to.
'''
while gameon == 1:
    playgo()
    hold = 1
    while hold == 1:
        yn = input('play again (y/n)? ')
        if yn == 'n':
            gameon = 0
            hold = 0
        elif yn == 'y':
            hold = 0
        else:
            print('invalid')

'''

def gsctonet(gsc, first):
    global player1_pass
    global player2_pass
    output = []
    for x in range(19):
        for y in range(19):
            if gsc[x][y] == 'o':
                output.append(2)
            elif gsc[x][y] == 'x':
                output.append(0)
            else:
                output.append(1)

    if first:
        output.append(1)
    else:
        output.append(0)
    if player1_pass or player2_pass:
        output.append(1)
    else:
        output.append(0)


    return output

