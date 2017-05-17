#CONFIGURATION FILE
#GAME RULE

#LAYOUT OF THE BONUSES ON THE BOARD
# 0 : start
# 1 : normal tile
# 2 : double letter
# 3 : triple letter
# 4 : double word
# 5 : triple word
LAYOUT = [
[5,1,1,2,1,1,1,5,1,1,1,2,1,1,5],
[1,4,1,1,1,3,1,1,1,3,1,1,1,4,1],
[1,1,4,1,1,1,2,1,2,1,1,1,4,1,1],
[2,1,1,4,1,1,1,2,1,1,1,4,1,1,2],
[1,1,1,1,4,1,1,1,1,1,4,1,1,1,1],
[1,3,1,1,1,3,1,1,1,3,1,1,1,3,1],
[1,1,2,1,1,1,2,1,2,1,1,1,2,1,1],
[5,1,1,2,1,1,1,0,1,1,1,2,1,1,5],
[1,1,2,1,1,1,2,1,2,1,1,1,2,1,1],
[1,3,1,1,1,3,1,1,1,3,1,1,1,3,1],
[1,1,1,1,4,1,1,1,1,1,4,1,1,1,1],
[2,1,1,4,1,1,1,2,1,1,1,4,1,1,2],
[1,1,4,1,1,1,2,1,2,1,1,1,4,1,1],
[1,4,1,1,1,3,1,1,1,3,1,1,1,4,1],
[5,1,1,2,1,1,1,5,1,1,1,2,1,1,5]
]

#DICTIONARIES
#FRENCH
french = [] #total length must be 102
for i in range(15):
	french.append('E')
for i in range(9):
	french.append('A')
for i in range(8):
	french.append('I')
for i in range(6):
	french.append('N')
	french.append('O')
	french.append('R')
	french.append('S')
	french.append('T')
	french.append('U')
for i in range(5):
	french.append('L')
for i in range(3):
	french.append('D')
	french.append('M')
for i in range(2):
	french.append('G')
	french.append('B')
	french.append('C')
	french.append('P')
	french.append('F')
	french.append('H')
	french.append('V')
	french.append('*')
french.append('J')
french.append('Q')
french.append('K')
french.append('W')
french.append('X')
french.append('Y')
french.append('Z')

#choose current dictionary
DICTIONARY = french

#POINTS
french_points = {
'*': 0,
'A' : 1,
'B' : 3,
'C' : 3,
'D' : 2,
'E' : 1,
'F' : 4,
'G' : 2,
'H' : 4,
'I' : 1,
'J' : 8,
'K' : 10,
'L' : 1,
'M' : 2,
'N' : 1,
'O' : 1,
'P' : 3,
'Q' : 8,
'R' : 1,
'S' : 1,
'T' : 1,
'U' : 1,
'V' : 4,
'W' : 10,
'X' : 10,
'Y' : 10,
'Z' : 10
}

#CHHOOSE RULE FOR POINTS
POINTS = french_points