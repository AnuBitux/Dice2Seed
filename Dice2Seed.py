#!/usr/bin/env python3

import hashlib
import binascii

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# Checks if string is binary
def check_bin(string):
    # every char will be checked if it is in the string '01'
    t = '01'
    if all(char in t for char in string):
        return True
    else:
        return False


# Checks if string contains the results of dice rolls (1 to 6)
def check_dice(string):
    # every char will be checked if it is in the string '01'
    t = '123456'
    if all(char in t for char in string):
        return True
    else:
        return False


# Converts string made by numbers from 1 to 6 to a binary string
def six_to_bin(string):
    binstr = ''
    for diceres in string:
        nn = int(diceres)
        binnn = nn % 2
        cc = str(binnn)
        binstr += cc
    return binstr


# Converts string with 0 and 1 to hexadecimal
def binToHexa(n):
    bnum = int(n)
    temp = 0
    mul = 1
    # counter to check group of 4
    count = 1
    # char array to store hexadecimal number
    hexaDeciNum = ['0'] * 100
    # counter for hexadecimal number array
    i = 0
    while bnum != 0:
        rem = bnum % 10
        temp = temp + (rem * mul)
        # check if group of 4 completed
        if count % 4 == 0:
            # check if temp < 10
            if temp < 10:
                hexaDeciNum[i] = chr(temp + 48)
            else:
                hexaDeciNum[i] = chr(temp + 55)
            mul = 1
            temp = 0
            count = 1
            i = i + 1
        # group of 4 is not completed
        else:
            mul = mul * 2
            count = count + 1
        bnum = int(bnum / 10)
    # check if at end the group of 4 is not completed
    if count != 1:
        hexaDeciNum[i] = chr(temp + 48)
    # check at end the group of 4 is completed
    if count == 1:
        i = i - 1
    return hexaDeciNum[i]


# Intro
print(color.YELLOW + 'Welcome to Dice2Seed!' + color.END)
print('This tool generates a 24 words mnemonic seed from entropy obtained rolling a dice')
print('Entropy can be pasted by the user (in binary or as the result of dice rolls) or can be inserted tracking the result of dice rolls\n')

# Define size of entropy
tour3 = True
while tour3:
    print(color.GREEN + 'How much entropy do you want? (128, 160, 192, 224, 256 bits)' + color.END)
    bits = int(input())
    if bits == 128 or bits == 160 or bits == 192 or bits == 224 or bits == 256:
        tour3 = False
    else:
        print(color.RED + 'Unallowed input, type 128, 160, 192, 224 or 256!' + color.END)
bytes = int(bits / 8)

# Stores the binary string
dicestr = ''
print(color.GREEN + '\nDo you want to paste entropy or the result of previous dice rolls?(y/n)' + color.END)
print('Unless this tool will help you tracking dice rolls')
tour0 = 1
ans = ''    # decides if the user pastes key or wants to track dice rolls
while tour0:
    ans = input()
    if ans == 'y' or ans == 'Y' or ans == 'n' or ans == 'N':
        tour0 = 0
    else:
        print(color.RED + 'Unaccepted answer! Only type y for yes or n for no' + color.END)

# User wants to paste the key
if ans == 'y' or ans == 'Y':
    tour = 1
    while tour:
        is_bin = False
        is_dice = False
        dicestr = input(f'Paste your string now with Ctrl + Shift + V\nnote that it must be {bits} digits long\n')
        if len(dicestr) != bits:
            print(color.RED + f'Entropy has to be {bits} digits long' + color.END)
        else:
            is_bin = check_bin(dicestr)
            is_dice = check_dice(dicestr)
            if is_bin:
                print(color.GREEN + 'String accepted!' + color.END)
                tour = 0
            elif is_dice:
                dicestr = six_to_bin(dicestr)
                print(color.GREEN + 'String accepted and converted to binary!' + color.END)
                tour = 0
            else:
                print(color.RED + 'String is not binary or is not the result of dice rolls!' + color.END)
                print(color.YELLOW + 'It has to contain only 0 and 1 or only numbers from 1 to 6' + color.END)

# user wants to track dice rolls
elif ans == 'n' or ans == 'N':
    # input result of dice rolls
    print(color.GREEN + "Let's go! It may take a while" + color.END)
    print('Simply type the result of each time you roll your dice')
    dicerolls = 0
    while dicerolls < bits:
        res = input(f'insert {dicerolls +1} number: ')
        if res.isdigit():
            res = int(res)
            if res > 6 or res < 1 or res == '':
                print(color.RED + 'Unallowed input! Only six faces dices are supported' + color.END)
            else:
                res = res % 2
                res = str(res)
                dicestr += res
                dicerolls += 1
        else:
            print(color.RED + 'Unallowed input!' + color.END)


# Converting dicestr into mnemonic seed
tmp_bin = dicestr
# convert string with 0 and 1 to hex and to binary
bin_list = []
start = 0
part = 4
while start < len(tmp_bin): # Splitting string in 4 digits parts
    bin_list.append(tmp_bin[start: start + part])
    start += part
# convert list with four 0 and 1 digits to list with hexadecimal letters
hex_list = []
for bn in bin_list:
    hex_list.append(binToHexa(bn))
hex_ent = ''.join(hex_list)    # creates hexadecimal string of entropy

tmp_bin = binascii.unhexlify(hex_ent)  # binary of entropy
tmp_hex = binascii.hexlify(tmp_bin)   # hexadecimal of entropy

str_hash = hashlib.sha256(tmp_bin).hexdigest()   # hashing binary of entropy

# Converting hash to binary
int_hash = int(str_hash, base=16)
bin_hash = str(bin(int_hash))[2:]

# Length of checksum is 1 bit every 32 of the mnemonic
checksum_length = int((len(dicestr))/32)
checksum = bin_hash[0:checksum_length]  # Getting first digits of hash (4 to 8 depending on entropy)
# Adding checksum to entropy
binary_seed = (bin(int(tmp_hex, 16))[2:].zfill(bytes * 8) + bin(int(str_hash, 16))[2:].zfill(256)[: bytes * 8 // 32])

# Obtaining the indexes of the words
# Each index is 11 bits long. Adding a bit to every 32 gives 33 bits. 11 will always fit in a 33 multiple
# Dividing the seed in 11 bits long indexes
index_list = []
start = 0
part = 11
while start < len(binary_seed):
    index_list.append(binary_seed[start: start + part])
    start += part

# Converting binary indexes to integer
index_list_int = []
b = 0
while b < len(index_list):
    index_list_int.append(int(index_list[b], 2))
    b += 1

# Choose language
print(color.GREEN + 'Choose your mnemonic seed language' + color.END)
print(' 1 -> Engligh')
print(' 2 -> Japanese')
print(' 3 -> Korean')
print(' 4 -> Spanish')
print(' 5 -> Chinese simplified')
print(' 6 -> Chinese traditional')
print(' 7 -> French')
print(' 8 -> Italian')
print(' 9 -> Czech')
print('10 -> Portuguese')

tour2 = 1
while tour2:
    print('Insert the number corresponding to the desired language')
    lang = input()
    if lang.isdigit():
        lang = int(lang)
        if lang < 1 or lang > 10:
            print(color.RED + 'Unallowed input!' + color.END)
        else:
            tour2 = 0
    else:
        print(color.RED + 'Unallowed input!' + color.END)

print('==========')
# Opening file corresponding to language
if lang == 1:
    f = open('Wordlists/b39en', 'r')
    print(color.DARKCYAN + 'Language: English' + color.END)
elif lang == 2:
    f = open('Wordlists/b39jp', 'r')
    print(color.DARKCYAN + 'Language: Japanese' + color.END)
elif lang == 3:
    f = open('Wordlists/b39kr', 'r')
    print(color.DARKCYAN + 'Language: Korean' + color.END)
elif lang == 4:
    f = open('Wordlists/b39es', 'r')
    print(color.DARKCYAN + 'Language: Spanish' + color.END)
elif lang == 5:
    f = open('Wordlists/b39cn', 'r')
    print(color.DARKCYAN + 'Language: Chinese simplified' + color.END)
elif lang == 6:
    f = open('Wordlists/b39cn2', 'r')
    print(color.DARKCYAN + 'Language: Chinese traditional' + color.END)
elif lang == 7:
    f = open('Wordlists/b39fr', 'r')
    print(color.DARKCYAN + 'Language: French' + color.END)
elif lang == 8:
    f = open('Wordlists/b39it', 'r')
    print(color.DARKCYAN + 'Language: Italian' + color.END)
elif lang == 9:
    f = open('Wordlists/b39cz', 'r')
    print(color.DARKCYAN + 'Language: Czech' + color.END)
elif lang == 10:
    f = open('Wordlists/b39pr', 'r')
    print(color.DARKCYAN + 'Language: Portuguese' + color.END)

# Access list to obtain words corresponding to indexes
mnemonic = []
w = 0
while w < len(index_list_int):
    f.seek(0)
    for i, line in enumerate(f):
        if i == index_list_int[w]:
            mnemonic.append(line.strip('\n'))
    w += 1

mnemonic_clean = ' '.join(mnemonic)
print('==========')
print(color.DARKCYAN + mnemonic_clean + color.END)
print('==========')
print(color.BLUE + 'Made by the AnuBitux Team!' + color.END)
print('==========')
