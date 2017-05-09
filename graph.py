import mysql.connector

import plotly as py
import plotly.graph_objs as go


def graph():
    py.tools.set_credentials_file(username='edwardsainsbury', api_key='oFb4d2SzuUZdkMArQbaB')

    cnx = mysql.connector.connect(user='root', password='mysql', host='127.0.0.1', database='test2')
    cursor = cnx.cursor()
    cursor.execute("SELECT MAX(era_no) FROM matches")
    latest_era = cursor.fetchone()[0]
    cursor.execute("SELECT GREATEST(MAX(player_one_id), MAX(player_two_id)) FROM matches")
    highest_id = cursor.fetchone()[0]
    era_data = []
    for x in range(latest_era):
        cursor.execute("SELECT player_one_id, player_two_id, player_one_winner, draw FROM matches WHERE  era_no = %s" % str(x+1))
        data = cursor.fetchall()
        id_array = {}
        for array in data:
            id_array.update({array[0]: 0}) if array[0] not in id_array else id_array
            id_array.update({array[1]: 0}) if array[1] not in id_array else id_array
            if array[2] == 1 and array[3] == 0:
                id_array[array[0]] += 1
            elif array[2] == 0 and array[3] == 0:
                id_array[array[1]] += 1
        era_data.append(id_array)
    # Create traces
    trace_array = []
    trace2_array = []
    for x in range(highest_id):
        values = []
        era = []
        id_lines = []
        for y in range(len(era_data)):
            if x in era_data[y]:
                values.append(era_data[y][x])
                id_lines.append(x)
                era.append(y)
        trace_array.append(go.Scatter(x=era, y=values, mode='lines+markers', name=str(x)))
        trace2_array.append(go.Scatter(x=era, y=id_lines, mode='lines+markers', name=str(x)))
    py.offline.plot(trace_array, filename='EraScores.html')
    py.offline.plot(trace2_array, filename='PlayerLongevity.html')
    cnx.close()

graph()