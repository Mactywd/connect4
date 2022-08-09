board = [
	["","","","","","",""],
	["","","","","","",""],
	["","","","","","",""],
	["","","","","","",""],
	["","","","","","",""],
	["","","","","","",""],
]

def check_equality(a, b, c, d):
	return a == b and b == c and c == d and d != ''

def find_space(column):
	for i in range(5, -1, -1):
		if board[i][column] == "":
			return i
	return None

	

def check_winner(board):
	winner = ""
	# Horizontal and verical
	for i in range(6):
		for j in range(3):
			if check_equality( board[0+j][i], board[1+j][i], board[2+j][i], board[3+j][i] ):
				winner = board[0+j][i]
				strike = [[0+j, i], [3+j, i]]

			if check_equality( board[i][0+j], board[i][1+j], board[i][2+j], board[i][3+j] ):
				winner = board[i][0+j]
				strike = [[i, 0+j], [i, 3+j]]

		if check_equality( board[i][3], board[i][4], board[i][5], board[i][6] ):
			winner = board[i][3]
			strike = [[i, 3], [i, 6]]

	for i in range(3):
		if check_equality( board[0+i][6], board[1+i][6], board[2+i][6], board[3+i][6] ):
			winner = board[0+i][6]
			strike = [[0+i, 6], [3+i, 6]]

	# Diagonal
	for i in range(3):
		for j in range(4):
			if check_equality( board[i+3][j], board[i+2][j+1], board[i+1][j+2], board[i][j+3] ):
				winner = board[i][j+3]
				strike = [[i+3, j], [i, j+3]]

			if check_equality( board[i+3][j+3], board[i+2][j+2], board[i+1][j+1], board[i][j] ):
				winner = board[i][j]
				strike = [[i+3, j+3], [i, j]]

	if winner:
		return [winner, strike]

	for i in range(6):
		for j in range(7):
			if board[i][j] == "":
				return [False, False]

	return ["tie", "tie"]