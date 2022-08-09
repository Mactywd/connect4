import config
from config import check_winner, find_space
import random
from math import inf as infinity

scores = []
player_c = ''
ai_c = ''

def ai(ai_play):
	global scores
	if ai_play == 'Y':
		ai_c = 'Y'
		player_c = 'R'

	elif ai_play == 'R':
		ai_c = 'R'
		player_c = 'Y'

	scores = {
		ai_c: 10,
		player_c: -10,
		'tie': 0
	}


	board = config.board
	maxval = -infinity
	best_slot = []
	for c in range(7):
		r = find_space(c)
		if r is not None:		
			board[r][c] = ai_c
			val = minimax(board, False, 4, -infinity, infinity)
			board[r][c] = ''
			if val > maxval:
				maxval = val
				best_slot = [[r, c]]
			elif val == maxval:
				best_slot.append([r, c])
	move = random.choice(best_slot)
	board[move[0]][move[1]] = ai_c



def minimax(board, is_maximizing, depth, alpha, beta):
	end_res = check_winner(board)
	if end_res != [False, False]:
		print(end_res)
	if end_res[0]:
		return scores[end_res[0]]
	if depth == 0:
		return 0

	if is_maximizing:
		max_score = -infinity
		for c in range(7):
			r = find_space(c)
			if r is not None:
				board[r][c] = ai_c
				score = minimax(board, False, depth-1, alpha, beta)
				board[r][c] = ''
				max_score = max(score, max_score)
				alpha = max(alpha, score)
				if beta <= alpha:
					break
		return max_score

	else:
		min_score = infinity
		for c in range(7):
			r = find_space(c)
			if r is not None:
				board[r][c] = player_c
				score = minimax(board, True, depth-1, alpha, beta)
				board[r][c] = ''
				min_score = min(score, min_score)
				beta = min(beta, score)
				if beta <= alpha:
					break
		return min_score
