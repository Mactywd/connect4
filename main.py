import config
from config import check_winner, find_space
import pygame
import ai
import sys

pygame.init()

players = ['Y', 'R']
curr_player = 0


# Pygame vars
w, h = 700, 600
display_w, display_h = 1050, 650
display = pygame.display.set_mode((display_w, display_h))
screen = pygame.Surface((w, h))

bkg_col = pygame.Color('#4287f5')
grid_col = pygame.Color('#ffffff')
yellow = pygame.Color('#ffff00')
red = pygame.Color('#ff0000')
hover_col = pygame.Color((200, 200, 200, 100))
font = pygame.font.SysFont('ubuntu', 40)

turn_1 = sys.argv[1]
turn_2 = sys.argv[2]
curr_turn = 0

# Logistic functions



def print_board():
	board_toprint = [["","","","","","",""], ["","","","","","",""],	["","","","","","",""],	["","","","","","",""],	["","","","","","",""],	["","","","","","",""],]
	for l, line in enumerate(config.board):
		for s, slot in enumerate(line):
			if config.board[l][s] == '':
				board_toprint[l][s] = ' '
			else:
				board_toprint[l][s] = config.board[l][s]
	
		print(board_toprint[l])
	print('\n')

def player_turn(row, col):
	global curr_player
	config.board[row][col] = players[curr_player]
	curr_player = int(not curr_player)
	

def ai_turn():
	global curr_player
	print(players[curr_player])
	ai.ai(players[curr_player])
	curr_player = int(not curr_player)

def game_ended():
	global end_message, end_obj, winner_obj, winner, strike
	winner, strike = check_winner(config.board)
	if winner:
		if winner == 'tie':
			end_message = "Pareggio!"
		else:
			end_message = " ha vinto"
			color = yellow if winner == 'Y' else red
			winner = 'Giallo' if winner == 'Y' else 'Rosso'
			winner_obj = font.render(winner, True, color)

		end_obj = font.render(end_message, True, (255, 255, 255))

# Pygame rendering functions

def draw_board():
	for i in range(7):
		for j in range(6):
			pygame.draw.circle(screen, grid_col, (w/7*i+w/14, h/6*j+h/12), h/14)

def draw_hover():
	x, _y = pygame.mouse.get_pos()
	col = (x-25) // (w//7)
	rect = pygame.Surface((w//7,h), pygame.SRCALPHA)
	rect.fill(hover_col)
	screen.blit(rect, (w//7*col,0))


def draw_player(row, col, p_color):
	player = players[curr_player]
	x = w / 7 * col + w / 14
	y = h / 6 * row + h / 12
	radius = h / 14

	pygame.draw.circle(screen, p_color, (x, y), radius)

def draw_end_line(strike):
	start = [strike[0][0]*w/7+w/14, strike[0][1]*h/6+h/12]
	end = [strike[1][0]*w/7+w/14, strike[1][1]*h/6+h/12]

	start = start[::-1]
	end = end[::-1]

	color = yellow if config.board[strike[0][0]][strike[0][1]] == 'Y' else red

	pygame.draw.line(screen, color, start, end, 10)
	# print('drawn at start: {}     end: {}'.format(start, end))


# Pygame mainloop
def mainloop():
	global end_message, end_obj, winner_obj, winner, curr_player, curr_turn
	player_clicked = False
	end_message = ""
	while True:
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				return True
			elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
				if not end_message:
					col = (pygame.mouse.get_pos()[0]-25) // (w//7)
					row = find_space(col)
					if row is not None:
						player_clicked = True


						
		if not end_message:
			if curr_turn == 0:
				if turn_1 == 'player':
					if player_clicked:
						player_turn(row, col)
						player_clicked = False
						if not end_message:
							curr_turn = 1
						game_ended()
				elif turn_1 == 'ai':
					ai_turn()
					if not end_message:
						curr_turn = 1
					game_ended()

			elif curr_turn == 1:
				if turn_2 == 'player':
					if player_clicked:
						player_turn(row, col)
						player_clicked = False
						if not end_message:
							curr_turn = 0
						game_ended()

				elif turn_2 == 'ai':
					ai_turn()
					if not end_message:
						curr_turn = 0

					game_ended()


		screen.fill(bkg_col)
		display.fill(bkg_col)
		draw_board()

		for i in range(6):
			for j in range(7):
				if config.board[i][j] == 'Y':
					draw_player(i, j, yellow)
				elif config.board[i][j] == 'R':
					draw_player(i, j, red)
		
		if not end_message:
			draw_hover()
		else:
			blit_x = w+25+(display_w-w)/2-end_obj.get_width()/2
			if end_message != 'Pareggio!':
				display.blit(winner_obj, (w+25+(display_w-w)/2-end_obj.get_width()/2-winner_obj.get_width()/2, display_h/2-winner_obj.get_height()/2))
				blit_x = w+25+(display_w-w)/2-end_obj.get_width()/2+winner_obj.get_width()/2

				draw_end_line(strike)

			display.blit(end_obj, (blit_x, display_h/2-end_obj.get_height()/2))

		display.blit(screen, (25, 25))
		pygame.display.flip()

if mainloop():
	pygame.quit()


#####################################################################





def console_board_play():
	while True:
		print_board()
		col = int(input('Enter the column: '))
		row = find_space(col)
		if row == -1:
			print("That column is full! Try again")
			continue

		make_move(row, col)
		curr_player = int(not curr_player)

		end = check_winner(board)
		if end:
			print_board()
			if end == "tie":
				print("It's a tie!")
			else:
				print("The winner is " + end)

			break
