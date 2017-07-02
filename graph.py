import mysql.connector
from datetime import datetime
import plotly.plotly as py
import plotly
import plotly.graph_objs as go


def graph():
    number = 0
    inUserLoop = True
    while inUserLoop:
        number = input('Number of Era: ')
        if number.isdigit():
            number = int(number)
            inUserLoop = False
        else:
            print("Invalid Input")


    plotly.tools.set_credentials_file(username='edwardsainsbury', api_key='23d2jFb3YDBkl9sWe1Vx')

    cnx = mysql.connector.connect(user='root', password='mysql', host='127.0.0.1', database='signal')
    cursor = cnx.cursor()
    cursor.execute("SELECT MAX(era_no) FROM matches")
    latestEra = cursor.fetchone()[0]
    cursor.execute("SELECT MAX(player_one_id) FROM matches WHERE era_no = %s" % str(latestEra))
    highest_id = cursor.fetchone()[0]

    startEra = 0
    if number != 0:
        startEra = latestEra - number
    cursor.execute("SELECT MIN(player_one_id) FROM matches WHERE era_no = %s" % str(startEra+1))
    lowest_id = cursor.fetchone()[0]
    era_data = []
    counter = 0
    for x in range(startEra, latestEra):
        cursor.execute("SELECT player_one_id, score FROM matches WHERE  era_no = %s" % str(x+1))
        data = cursor.fetchall()
        id_array = {}
        print(str(((x+1 - startEra) / (latestEra - startEra)) * 100) + "%")

        for array in data:

            id_array.update({array[0]: 0}) if array[0] not in id_array else id_array
            id_array[array[0]] = array[1]
        era_data.append(id_array)
    # Create traces
    trace_array = []
    trace2_array = []

    # for x in range(lowest_id, highest_id+1):
    #     values = []
    #     era = []
    #     id_lines = []
    #     for y in range(len(era_data)):
    #         if x in era_data[y]:
    #             values.append(era_data[y][x])
    #             id_lines.append(x)
    #             era.append(y)
    #     trace_array.append(go.Scatter(x=era, y=values, mode='lines+markers', name=str(x)))
    #     trace2_array.append(go.Scatter(x=era, y=id_lines, mode='lines+markers', name=str(x)))

    eraNumber = []
    for i in range(startEra, latestEra):
        eraNumber.append(i)

    values = []
    trace3_array = []
    for x in range(9):
        values = []
        print(str(((x+1) / 9) * 100) + "%")
        counter += 1
        for eras in era_data:
            eraArray = []
            for y in eras:
                eraArray.append(eras[y])
            values.append(eraArray.count(x))
        trace3_array.append(go.Scatter(x=eraNumber, y=values, mode='lines+markers', name=str(x)))


    #py.offline.plot(trace_array, filename='EraScores.html')
    #py.offline.plot(trace2_array, filename='PlayerLongevity.html')
    py.plot(trace3_array, filename='Success')



    # cursor.execute("SELECT timestamp FROM matches")
    # times = cursor.fetchall()
    # diff_array = []
    # match_array = []
    # trace4_array = []
    # runningAverage = []
    # sum = 0
    # for x in range(len(times)-1):
    #     diff_array.append((times[x+1][0]-times[x][0]).total_seconds()/60)
    #     sum += (times[x+1][0]-times[x][0]).total_seconds()/60
    #     runningAverage.append(sum/(x+1))
    #     match_array.append(x)
    # trace4_array.append(go.Scatter(x=match_array, y=diff_array, mode='lines+markers', name='Time'))
    # trace4_array.append(go.Scatter(x=match_array, y=runningAverage, mode='lines+markers', name='Average'))
    # py.offline.plot(trace4_array, filename='MatchTime.html')
    # cnx.close()

graph()