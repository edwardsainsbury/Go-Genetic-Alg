import math
import os
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


def encode(path):
    file = open(path, 'rb')
    data = []
    i = 0
    bytestring = file.read()[:1000]
    for byte in bytestring:

        if byte == b"":
            break
        i += 1
        data.append(byte)
    start_length = len(data)
    match_array = ''
    x = 0
    while x < len(data) - 1:
        #print(x)
        if data[x] == data[x+1]:
            match_array += '1'
            data.pop(x+1)
        else:
            match_array+='0'
            x += 1
        x += 1
    if len(data) % 2 == 1:
        match_array+='0'
    #print(len(match_array))
    #print(len(data))
    print('Start length: ' + str(start_length))
    end_length = len(data) + len(match_array)/8
    print('End length: ' + str(end_length))
    print('Compression: ' + str((start_length-end_length)/start_length*100))
    if end_length > start_length:
        print('Can not compress file')
        raise Exception
    else:
        filename = path[:path.find('.')]
        new_file = open(filename + '1.edzipa', 'wb')
        new_file.write(bytes(data))
        new_file = open(filename + '1.edzipb', 'wb')
        b_data = []
        for x in range(math.ceil(len(match_array)/8)):
            if len(match_array[x*8:8*x+8]) == 8:
                b_data.append(int(match_array[x*8:8*x+8], 2))
            else:
                b_data.append(int((match_array[x * 8:8 * x + 8]).ljust(8, '0'), 2))

        new_file.write(bytes(b_data))
        new_file.close()

def decode(path):
    filename = path
    file = open(filename + '.edzipa', 'rb')
    bytestring = file.read()
    file = open(filename + '.edzipb', 'rb')
    bytestring2 = file.read()
    bytestring3 = ''

    for byte in bytestring2:
        string = "{0:b}".format(byte).rjust(8, '0')

        bytestring3 += string
    data = []
    recreate = []
    main_array_index = 0
    for x in range(len(bytestring3)):
        if bytestring3[x] == '1':
            recreate.append(bytestring[main_array_index])
            recreate.append(bytestring[main_array_index])
            main_array_index += 1
        else:
            recreate.append(bytestring[main_array_index])
            recreate.append(bytestring[main_array_index + 1])
            main_array_index += 2

        if main_array_index >= len(bytestring):
            break
    while main_array_index < len(bytestring):
        recreate.append(bytestring[main_array_index])
        main_array_index += 1

    file = open(filename[:len(filename)-1] + '.edzipa', 'wb')

    file.write(bytes(recreate))
    file.close()
    print("Recreated: " + str(len(recreate)))


encode('duck.bmp')
#decode('duck1')
ones = '1'
lenth  = 10
for x in range(lenth):
    print('Level: ' + str(x))
    try:
        encode('duck'+ones+'.edzipa')
        os.remove('duck' + ones + '.edzipa')
    except:
        print('Max level reached')
        break
    ones += '1'
for _ in range(x):
    decode('duck'+ones)
    ones -= '1'
'''
encode('duck1.edzipa')
os.remove('duck1.edzipa')
encode('duck11.edzipa')
os.remove('duck11.edzipa')
encode('duck111.edzipa')
os.remove('duck111.edzipa')
encode('duck1111.edzipa')
os.remove('duck1111.edzipa')

decode('duck11111')
decode('duck1111')
decode('duck111')
decode('duck11')
decode('duck1')
'''