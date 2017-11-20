def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

def groups(string):
    x = 0
    all_array = []
    y = 1
    while x + y < len(string):
        bit = string[x]
        bit_array = []
        bit_array.append(bit)
        y = 1
        while y < len(string) - x:
            next_bit = string[x+y]
            if bit == next_bit:
                bit_array.append(bit)
            else:
                x += 1
                break
            y += 1
            #x += 1
        #x += 1
        all_array.append(bit_array)
    return all_array



print(numberToBase(10,4))

#file = open('test.txt', 'wb')
#file.write(b'1')
#file.write(b'2')
#file.write(b'3')
#file.write(b'4')
#file.close()
file = open('test.txt', 'rb')
bytes = []
while True:

    byte = file.read(1)
    if byte == b'':
        break
    else:
        bytes.append(int.from_bytes(byte, byteorder='little'))

sums = 0
for x in range(len(bytes)):
    sums += bytes[x] << 8 * (len(bytes) - x)

quad_string = numberToBase(sums, 4)
print('hello')
group = groups(quad_string)
first_array = []
second_array = []

for number in quad_string:
    if number == 0:
        first_array
    elif number == 1:
        print('hello')
    elif number == 2:
        print('hello')
    else:
        print('hello')