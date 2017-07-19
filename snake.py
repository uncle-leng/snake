import pygame
from pygame.locals import *
import random, sys

fps = 20
window_height = 480
window_width = 640
cell_size = 10

assert window_height % cell_size == 0
assert window_width % cell_size == 0

cell_height = int(window_height / cell_size)
cell_width = int(window_width /  cell_size)

white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
yellow = (255, 255, 0)

up = 'up'
down = 'down'
left = 'left'
right = 'right'

head = 0

def main():
	global fps_lock, display_surface, font
	pygame.init()
	fps_lock = pygame.time.Clock()
	display_surface = pygame.display.set_mode((window_width, window_height))
	font = pygame.font.SysFont('arial', 18)
	pygame.display.set_caption('snake')
	show_start()
	while True:
		run_game()
		game_over()

def run_game():
	start_x = random.randint(5, cell_width - 6)
	start_y = random.randint(5, cell_height - 6)

	init_snake = [
		{'x': start_x, 'y': start_y},
		{'x': start_x - 1, 'y': start_y},
		{'x': start_x - 2, 'y': start_y}
	]

	direction = right
	apple = get_random_location()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
			elif event.type == KEYDOWN:
				if (event.key == K_LEFT and direction != right):
					direction = left
				elif (event.key == K_RIGHT and direction != left):
					direction = right
				elif (event.key == K_UP and direction != down):
					direction = up
				elif (event.key == K_DOWN and direction != up):
					direction = down
				elif event.key == K_ESCAPE:
					terminate()

		if init_snake[head]['x'] == -1 or init_snake[head]['x'] == cell_width or init_snake[head]['y'] == -1 or init_snake[head]['y'] == cell_height:
			return

		for snake_body in init_snake[1:]:
			if snake_body['x'] == init_snake[head]['x'] and snake_body['y'] == init_snake[head]['y']:
				return

		if init_snake[head]['x'] == apple['x'] and init_snake[head]['y'] == apple['y']:
			apple = get_random_location()
		else:
			del init_snake[-1]

		if direction == up:
			new_head = {'x': init_snake[head]['x'], 'y': init_snake[head]['y']-1}
		elif direction == down:
			new_head = {'x': init_snake[head]['x'], 'y': init_snake[head]['y']+1}
		elif direction == left:
			new_head = {'x': init_snake[head]['x']-1, 'y': init_snake[head]['y']}
		elif direction == right:
			new_head = {'x': init_snake[head]['x']+1, 'y': init_snake[head]['y']}
		init_snake.insert(0, new_head)

		display_surface.fill(black)
		draw_grid()
		draw_snake(init_snake)
		draw_apple(apple)
		draw_score(len(init_snake) - 3)
		pygame.display.update()
		fps_lock.tick(fps)

def terminate():
	pygame.quit()
	sys.exit()

def get_random_location():
	return {'x': random.randint(0, cell_width-1), 'y': random.randint(0, cell_height-1)}

def draw_grid():
	for i in range(window_width, cell_size):
		pygame.draw.line(display_surface, white, (i, 0), (i, window_height))
	for j in range(window_height, cell_size):
		pygame.draw.line(display_surface, white, (0, j), (window_width, j))

def draw_snake(snake):
	for each in snake:
		x = each['x'] * cell_size
		y = each['y'] * cell_size
		snakerect = pygame.Rect(x, y, cell_size, cell_size)
		pygame.draw.rect(display_surface, white, snakerect)
		snake_inner = pygame.Rect(x-4, y-4, cell_size-8, cell_size-8)
		pygame.draw.rect(display_surface, blue, snake_inner)

def draw_apple(apple):
	x = apple['x'] * cell_size
	y = apple['y'] * cell_size
	applerect = pygame.Rect(x, y, cell_size, cell_size)
	pygame.draw.rect(display_surface, green, applerect)

def draw_score(score):
	score_surface = font.render("Score : %s" % score, True, white)
	scorerect = score_surface.get_rect()
	scorerect.topleft = (window_width-200, 10)
	display_surface.blit(score_surface, scorerect)

def draw_press_msg():
	press_surface = font.render('Press any key to play !', True, yellow)
	pressrect = press_surface.get_rect()
	pressrect.topleft = (window_width - 200, window_height - 30)
	display_surface.blit(press_surface, pressrect)

def key_press():
	if len(pygame.event.get(QUIT)) > 0:
		terminate()
	key_up_events = pygame.event.get(KEYUP)
	if len(key_up_events) == 0:
		return None
	if key_up_events[0].key == K_ESCAPE:
		terminate()
	return key_up_events[0].key

def show_start():
	display_surface.fill(black)
	title_font = pygame.font.SysFont('arial', 100)
	title_surface = title_font.render('Snake ! ', True, white)
	titlerect = title_surface.get_rect()
	titlerect.center = (window_width / 2, window_height / 2)
	display_surface.blit(title_surface, titlerect)

	draw_press_msg()
	pygame.display.update()

	while True:
		if key_press():
			pygame.event.get()
			return

def game_over():
	game_over_font = pygame.font.SysFont('arial.ttf', 50)
	game_surface = game_over_font.render('Game ', True, blue)
	over_surface = game_over_font.render('Over ', True, green)
	gamerect = game_surface.get_rect()
	overrect = over_surface.get_rect()
	gamerect.midtop = (window_width / 2, window_height / 2-gamerect.height-10)
	overrect.midtop = (window_width / 2, window_height / 2)
	display_surface.blit(game_surface, gamerect)
	display_surface.blit(over_surface, overrect)
	draw_press_msg()
	pygame.display.update()
	pygame.time.wait(500)
	key_press()

	while True:
		if key_press():
			pygame.event.get()
			return

if __name__ == "__main__":
	main()




































