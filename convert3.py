#import plotly as py
#import plotly.graph_objs as go


def ten_to_base(base_ten_num, base):
    """ Takes a number of base ten and converts it to another number of a base
    between base 2 and base 36. Base_ten_num and base are taken as integers. The
    number of place values are determined and added to the ending_num string,
    which is returned. Bases larger than 10 are handled with capital letters.
    Negative numbers and decimals are not handled."""
    current_power = 0
    # continues to add 1 to current_power until current_power+1 is the number of
    # places in the converted number.
    while base ** (current_power+1) < base_ten_num:
        current_power += 1

    # inital value
    ending_num = ""

    # finds each place value
    while current_power >= 0:
        # floor division by place value. Base ** current_power is the value of
        # 1 in that place value, so base_ten_num divided by the power with no
        # remainder is that place value
        current_value = base_ten_num // base ** current_power

        # updates values for next loop
        base_ten_num -= current_value * base ** current_power
        current_power -= 1

        # Assigns a character to the place value. Values larger than 10 are
        # assigned alpha characters with unicode. A's unicode value is 65 and it
        # is worth 10, so 55 is added to get the unicode value. The values
        # progress from there. Current_value is always a string after the if
        # statement.
        if current_value > 9:
            current_value = chr(current_value + 55)
        else:
            current_value = str(current_value)

        # Adds the value's character to the number's string
        ending_num += current_value

    return ending_num


#file = open('duck.bmp', 'rb')
file = open('grief-and-loss.jpg', 'rb')
data = []
i = 0
bytestring = file.read()
for byte in bytestring:

    if byte == b"":
        break
    i += 1
    data.append(byte)
start_length = len(data)
match_array = []
x = 0
while x < len(data) - 1:
    if data[x] == data[x+1]:
        match_array.append(1)
        data.pop(x+1)
    else:
        match_array.append(0)
    x += 1

print(len(match_array))
print(len(data))
print('Start length: ' + str(start_length))
print('End length: ' + str(len(data) + (len(match_array)/8)))
'''

binary_string = ''
for number in data:
    converted = "{0:b}".format(number)
    binary_string += converted
zeros = binary_string.count('0')
ones = binary_string.count('1')


if ones > zeros:
    highest = '1'
    second_highest = '0'
else:
    highest = '0'
    second_highest = '1'



binary_string = ''
for number in data:
    converted = "{0:b}".format(255 - number)
    binary_string += converted
zeros_flip = binary_string.count('0')
ones_flip = binary_string.count('1')


if ones_flip > zeros_flip:
    highest_flip = '1'
    second_highest_flip = '0'
else:
    highest_flip = '0'
    second_highest_flip = '1'

most_array = []
least_array = []
most_array_flip = []
least_array_flip = []
score = []
score_flip = []
standard = []
axis = []
prediction = []
prediction_flip = []
running_ones = 0
running_zeros = 0
running_delim = 0
running_new = []
running_ones_flip = 0
running_zeros_flip = 0
running_delim_flip = 0
running_new_flip = []
for x in range(int(len(data)/5)):
    number = data[x]
    binary_string = "{0:b}".format(number)
    print(binary_string)
    #print((x+1)*100/len(data))
    axis.append(x)
    for bit in binary_string:

        if bit == highest:
            most_array.append(0)
        else:
            most_array.append(1)
            least_array.append(0)
    most_array.append(1)
    least_array.append(1)
    running_ones += binary_string.count('1')
    running_zeros += binary_string.count('0')
    running_delim += 1

    if x % 1 == 0:
        standard.append((x+1)*8)
        score.append(len(most_array) + len(least_array))
        prediction.append(ones + 2*(len(data) + zeros))
        running_new.append(running_delim + running_ones + running_zeros)


    binary_string = "{0:b}".format(255 - number)
    print(binary_string)
    # print((x+1)*100/len(data))

    for bit in binary_string:

        if bit == highest_flip:
            most_array_flip.append(0)
        else:
            most_array_flip.append(1)
            least_array_flip.append(0)
    most_array_flip.append(1)
    least_array_flip.append(1)

    running_ones_flip += binary_string.count('1')
    running_zeros_flip += binary_string.count('0')
    running_delim_flip += 1
    if x % 1 == 0:
        score_flip.append(len(most_array_flip) + len(least_array_flip))
        prediction_flip.append(ones_flip + 2 * (len(data) + zeros_flip))
        running_new_flip.append(running_ones_flip + running_zeros_flip + running_delim_flip)


score = []
axis = []
normal = []
for x in range(255):
    axis.append(x)
    bin_string = ten_to_base(x, 3)
    score.append(2*len(bin_string) + 2)
    normal.append(8)

trace_array = []
#trace_array.append(go.Scatter(x=axis, y=score, mode='lines+markers', name='score'))
#trace_array.append(go.Scatter(x=axis, y=normal, mode='lines+markers', name='score'))
#trace_array.append(go.Scatter(x=axis, y=score_flip, mode='lines+markers', name='scoreflip'))
#trace_array.append(go.Scatter(x=axis, y=standard, mode='lines+markers', name='normal'))
#trace_array.append(go.Scatter(x=axis, y=running_new, mode='lines+markers', name='new'))
#trace_array.append(go.Scatter(x=axis, y=running_new_flip, mode='lines+markers', name='newflip'))
#trace_array.append(go.Scatter(x=axis, y=prediction, mode='lines+markers', name='score'))
#trace_array.append(go.Scatter(x=axis, y=prediction_flip, mode='lines+markers', name='score'))
#py.offline.plot(trace_array, filename='EraScores.html')
'''