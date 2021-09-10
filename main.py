from ursina import *
from menu import MenuButton
from player import Player
from obstacle import Obstacle
from field import Field
from spawn_barrier import SpawnBarrier
from physics3d import *
from random import randint
from coin import Coin
from ursina.shaders import lit_with_shadows_shader
from star import Star

clear = False
musics = []
obstacles = []
coins = []
colliders = []
positions = ((-4,5,80),
			(0,5,80),
			(4,5,80))
jumps = []
jumps_right = []
jumps_left = []

def start():
	for i in main_menu.buttons:
		i.enabled = False
	player.start = True
	main_menu_music.fade_out(value=0, duration=.1, delay=0, curve=curve.in_expo) 
	game_music.play()

def restart():
	player.coins = 0
	player.eternal = True
	score_coins.color = color.white
	for i in main_menu.buttons:
		i.enabled = True
	player.start = False
	game_music.stop()
	for obstacle in obstacles:
		obstacle.eternal = False
	for collider in colliders:
		world.remove(collider)
	obstacles.clear()
	colliders.clear()
	camera.overlay.color = color.red
	player.position = player.origin_pos
	scene.clear()
	obs = Obstacle((0, 5, 80), (.7,.7,.7), 'obstacle', obstacle_texture, shader = lit_with_shadows_shader)
	obstacles.append(obs)
	colliders.append(MeshCollider(world, obs, mass=1))
	camera.overlay.animate_color(color.black, duration = 1, delay = .1)
	camera.rotation = camera.origin_rot
	camera.position = camera.origin_pos
	camera.fov = camera.origin_fov
	
def quit():
	application.resume()
	application.quit()

def pause():
	for i in pause_menu.buttons:
		i.enabled = True
	game_music.pause()
	application.pause()

def resume():
	application.resume()
	for i in pause_menu.buttons:
		i.enabled = False
	game_music.resume()
	try:
		game_music.volume = game_music.save_volume
	except:
		game_music.volume = .3

def set_mmm(): # Main Menu Music
	main_menu_music.volume = audio_menu.mmm_volume.value

def set_gm(): # Game Music
	game_music.save_volume = audio_menu.gm_volume.value

def set_fps():
	if player.show_fps == False:
		window.fps_counter.enabled = True
		video_menu.show_fps.text = 'FPS: ON'
		player.show_fps = True
	elif player.show_fps:
		window.fps_counter.enabled = False
		video_menu.show_fps.text = 'FPS: OFF'
		player.show_fps = False

def set_borderless():
	if window.borderless:
		window.borderless = False
		window.exit_button.enabled = False
		video_menu.borderless.text = 'Borderless: OFF'
	else:
		window.borderless = True
		window.exit_button.enabled = True
		video_menu.borderless.text = 'Borderless: ON'
def set_fullscreen():
	if window.fullscreen:
		window.fullscreen = False
		video_menu.fullscreen.text = 'Fullscreen: OFF'
	else:
		window.fullscreen = True
		video_menu.fullscreen.text = 'Fullscreen: ON'


def update():
	global obstacles
	global coins
	global clear
	global musics

	if player.start:
		if getattr(Obstacle, 'spawn'):
	
			obstacle_type = randint(1,3)
	
			if obstacle_type >= 2:
				random_pos = randint(1,3)
		
				if random_pos == 1:
					rand = randint(0,2)
					pos = (positions[rand],)
				if random_pos == 2:
					ran1 = randint(0,2)
					if ran1 == 0:
						ran2 = randint(1,2)
					if ran1 == 1:
						ran2 = randint(-1,0)
					if ran1 == 2:
						ran2 = randint(0,1)
					pos = (positions[ran1],positions[ran2])
				if random_pos >= 3:
					pos = (positions[0],positions[1],positions[2])
		
				for position in pos:
					do = randint(1,2)

					obstacles.append(Obstacle(position, (.7,.7,.7), 'obstacle', 'obstacle', lit_with_shadows_shader))
					colliders.append(MeshCollider(world, obstacles[-1], mass = 1))
					colliders[-1].scale = (1,1,1)
					if do == 1:
						coins.append(Coin(position, lit_with_shadows_shader, coin_texture))
						coins[-1].z += 2
						coins[-1].y -= 3
					setattr(Obstacle, 'spawn', False)
					obstacles[-1].run == False
					obstacles[-2].spawned = True
	
			if obstacle_type == 1:
				random_pos = randint(0,1)
				if random_pos == 0:
					pos = (positions[randint(0,2)],)
				if random_pos == 1:
					ran1 = randint(0,2)
					if ran1 == 0:
						ran2 = randint(1,2)
					if ran1 == 1:
						ran2 = randint(-1,0)
					if ran1 == 2:
						ran2 = randint(0,1)
					pos = (positions[ran1],positions[ran2])
				for position in pos:
					obstacles.append(Obstacle(position, (1.1,1,.7), 'cube', obstacle2_texture, lit_with_shadows_shader))
					colliders.append(MeshCollider(world, obstacles[-1], mass=1.5))
					colliders[-1].scale = (1.4,3,1)
					setattr(Obstacle, 'spawn', False)
					obstacles[-1].run == False
					obstacles[-2].spawned = True
	
		for obstacle in obstacles:
			if obstacle.z <= -100:
				obstacle.eternal = False
				obstacles.pop(obstacles.index(obstacle))
					
	
			for spawn_barrier in spawn_barriers:
				if obstacle.hit_info.hit and obstacle.hit_info.entity == player:
					restart()
					camera.overlay.animate_color(color.clear, duration = 1, delay = 3.5)
					main_menu_music.play()
					main_menu_music.volume = .3
	
				if obstacle.hit_info.hit and obstacle.hit_info.entity == spawn_barrier and obstacle.spawned == False:
					setattr(Obstacle, 'spawn', True)

	
			for coin in coins:
				if obstacle.run:
					coin.run = True
				if coin.z <= -100:
					coin.eternal = False
					coins.pop(coins.index(coin))
	
				if coin.hit_info.hit and coin.hit_info.entity == player and coin.hit:
					coin.hit = False
					player.coins += 1
					coin.x = 1000
					coin.visible = False
					Audio('sfx/pickup_coin2.mp3', volume = 1, eternal = True)
					score_coins.color = color.green
					score_coins.blink(value = color.white, duration = .1, delay = 0, interrupt = 'finish', curve = curve.linear)
					camera.fov += 4
					camera.change_fov = True
					a.blink(value = color.violet, duration = .1, delay = 0, interrupt = 'finish', curve = curve.linear)
	
		for collider in colliders:
			if round(collider.y) == -1:
				world.remove(collider)
				colliders.pop(colliders.index(collider))
			if round(collider.y) == 0 and collider.scale == (1.4,3,1):
				world.remove(collider)
				colliders.pop(colliders.index(collider))

		if 45 > round(player.coins) >= 25:
			camera.position = player.position
			camera.rotation = (0,0,0)

		if 75 > round(player.coins) >= 45:
			camera.position = Vec3(10,2,-8)
			camera.rotation_y = -20
			camera.fov = 90

		if round(player.coins) >= 75:
			camera.position = camera.origin_pos
			camera.rotation = camera.origin_rot
			camera.fov = camera.origin_fov
	
		score_coins.text = f'Coins: {round(player.coins)}'
	
		dt = time.dt
		world.doPhysics(dt)

		if musics[-1].playing == False and player.start:
			song = randint(1,6)
			musics.append(Audio(f'music/game_music_{song}', autoplay = False, volume = .3, eternal = True))
			musics[-1].play()
		if round(camera.fov) != round(camera.origin_fov) and camera.change_fov:
			if round(camera.fov) == round(camera.origin_fov):
				camera.change_fov = False
			camera.fov -= .5
	try:
		input(jumps[-1])
		jumps.pop(-1)
	except IndexError:
		print()


def input(key):

	if player.start:
		if key == 'a':
			if player.in_air == False:
				player.jump_left()
				scene.clear()
				a.blink(value = color.rgb(0,0,255), duration = .1, delay = 0, interrupt = 'finish', curve = curve.linear)
			elif player.in_air:
				jumps.append('a')
	
		if key == 'd':
			if player.in_air == False:
				player.jump_right()
				scene.clear()
				a.blink(value = color.rgb(230, 0, 255), duration = .1, delay = 0, interrupt = 'finish', curve = curve.linear)
			elif player.in_air:
				jumps.append('d')

		if key == 's':
			if player.in_air == False:
				player.jump_mid()
				scene.clear()
				a.blink(value = color.rgb(155, 60, 120), duration = .1, delay = 0, interrupt = 'finish', curve = curve.linear)
			elif player.in_air:
				jumps.append('s')
	
		if key == 'space':
			if player.in_air == False:
				player.jump()
				scene.clear()
				a.blink(value = color.rgb(300,0,0), duration = .1, delay = 0, interrupt = 'finish', curve = curve.linear)
			elif player.in_air:
				jumps.append('space')

		if key == 'escape':
			pause()

app = Ursina(title = 'Runner', borderless = True, fullscreen = True)

camera.overlay.color = color.black
camera.overlay.eternal = True
logo = Sprite(name='ursina_splash', parent=camera.ui, texture='ursina_logo', world_z=camera.overlay.z-1, scale=.1, color=color.clear, x = .3)
logo.animate_color(color.white, duration=3, delay=1, curve=curve.out_quint_boomerang)
logo2 = Sprite(name='B3CTOR_splash', parent=camera.ui, texture='assets/logo.png', world_z=camera.overlay.z-1, scale=.07, color=color.clear, x = -.3)
logo2.animate_color(color.white, duration=3, delay=1, curve=curve.out_quint_boomerang)
camera.overlay.animate_color(color.clear, duration=1, delay=4)
destroy(logo, delay=5)
destroy(logo2, delay=5)

def splash_input(key):
    destroy(logo)
    destroy(logo2)
    camera.overlay.animate_color(color.clear, duration=.25)


logo.input = splash_input

camera.y = 6
camera.rotation = Vec3(10,0,0)
camera.origin_pos = camera.position
camera.origin_rot = camera.rotation
camera.origin_fov = camera.fov

window.fps_counter.y -= .07

field_texture = load_texture('assets/field.png')
obstacle_texture = load_texture('assets/obstacle.png')
obstacle2_texture = load_texture('assets/obstacle2.png')
coin_texture = load_texture('assets/coin.png')

main_menu_music = Audio('music/main_menu.mp3', volume = .3, loop = True)
song = randint(1,6)
game_music = Audio(f'music/game_music_{song}', autoplay = False, volume = .3, eternal = True)
musics.append(game_music)

button_spacing = .075 * 1.25
menu_parent = Entity(parent = camera.ui, y = .15, eternal = True)
main_menu = Entity(parent = menu_parent, eternal = True)
settings_menu = Entity(parent = menu_parent, eternal = True)
pause_menu = Entity(parent = menu_parent, eternal = True)
video_menu = Entity(parent = menu_parent, eternal = True)
audio_menu = Entity(parent = menu_parent, eternal = True)
how_to_play_menu = Entity(parent = menu_parent, eternal = True)

state_handler = Animator({
    'main_menu' : main_menu,
    'settings_menu' : settings_menu,
    'pause_menu' : pause_menu,
    'video_menu' : video_menu,
    'audio_menu' : audio_menu,
    'how_to_play_menu' : how_to_play_menu,
    }
)

main_menu.buttons = [
    MenuButton('Play', on_click = start),
    MenuButton('Settings', on_click = Func(setattr, state_handler, 'state', 'settings_menu')),
    MenuButton('How To Play', on_click = Func(setattr, state_handler, 'state', 'how_to_play_menu')),
    MenuButton('Quit', on_click = Func(quit)),
]

for i, e in enumerate(main_menu.buttons):
	print(i)
	e.parent = main_menu
	e.eternal = True
	e.y = -i * button_spacing

pause_menu.buttons = [
	MenuButton('Resume', on_click = Func(resume), eternal = True, ignore_paused = True),
    MenuButton('Settings', on_click = Func(setattr, state_handler, 'state', 'settings_menu'), eternal = True, ignore_paused = True),
    MenuButton('Quit', on_click = Func(quit), eternal = True, ignore_paused = True)
]

for i, e in enumerate(pause_menu.buttons):
    e.parent = main_menu
    e.eternal = True
    e.y = -i * button_spacing
    e.enabled = False

settings_menu.video = MenuButton('Video', parent = settings_menu, y = 0, on_click = Func(setattr, state_handler, 'state', 'video_menu'), eternal = True),
settings_menu.audio = MenuButton('Audio', parent = settings_menu, y = -.09375, on_click = Func(setattr, state_handler, 'state', 'audio_menu'), eternal = True),
settings_menu.back = MenuButton('Back', parent = settings_menu, y = -.1875, on_click = Func(setattr, state_handler, 'state', 'main_menu'), eternal = True)

how_to_play_menu.howto = Sprite('assets/how_to_play.png', scale = .07, parent = how_to_play_menu, eternal = True)
how_to_play_menu.back = MenuButton('Back', parent = how_to_play_menu, y = -.4, on_click = Func(setattr, state_handler, 'state', 'main_menu'), eternal = True)

video_menu.show_fps = MenuButton('FPS: ON', parent = video_menu, y = 0, on_click = Func(set_fps), eternal = True)
video_menu.borderless = MenuButton('Borderless: ON', parent = video_menu, y = -.09375, on_click = Func(set_borderless), eternal = True)
video_menu.fullscreen = MenuButton('Fullscreen: ON', parent = video_menu, y = -.1875, on_click = Func(set_fullscreen), eternal = True)
video_menu.back = MenuButton('Back', parent = video_menu, y = -.375, on_click = Func(setattr, state_handler, 'state', 'settings_menu'), eternal = True)

audio_menu.mmm_volume = Slider(text = 'Main Menu Music Volume', ignore_paused = True, min = .1, max = 2, dynamic = True, value = .3, on_value_changed = set_mmm, parent = audio_menu, y = .15, x = -.2, eternal = True)
audio_menu.mmm_volume.knob.ignore_paused = True
audio_menu.mmm_volume.on_value_changed.ignore_paused = True
audio_menu.gm_volume = Slider(text = 'Game Music Volume', ignore_paused = True, min = .1, max = 2, dynamic = True, value = .3, on_value_changed = set_gm, parent = audio_menu, y = .05, x = -.2, eternal = True)
audio_menu.gm_volume.on_value_changed.ignore_paused = True
audio_menu.gm_volume.knob.ignore_paused = True
audio_menu.back = MenuButton('Back', parent = audio_menu, y = -.375, on_click = Func(setattr, state_handler, 'state', 'settings_menu'), eternal = True)

world = BulletWorld()
world.setGravity(Vec3(0, -9.81, 0))
window.color = color.black

spawn_barriers = [
	SpawnBarrier((0,-10,79)),
	SpawnBarrier((4,-10,79)),
	SpawnBarrier((-4,-10,79)),
]

sun = Sprite('assets/sun.png', z = 95, y = 2, eternal = True)
for i in range(100):
	star = Star(position = (randint(-50,50),randint(-30,30),70), texture = f'assets/stars/star{randint(1,8)}.png')

obs = Obstacle((0, 5, 80), (.7,.7,.7), 'obstacle', obstacle_texture, shader = lit_with_shadows_shader)
obstacles.append(obs)
colliders.append(MeshCollider(world, obs, mass=1))

fields = [
	Field((0,-1,45), field_texture, shader = lit_with_shadows_shader),
	Field((4,-1,45), field_texture, shader = lit_with_shadows_shader),
	Field((-4,-1,45), field_texture, shader = lit_with_shadows_shader)
]

for i in fields:
	BoxCollider(world, i, scale = i.scale/2)

player = Player(shader = lit_with_shadows_shader)
player.origin_pos = player.position
score_coins = Text(text = f'Coins: {player.coins}', eternal = True, position = (-.86,.47))

a = DirectionalLight(position = (0,10,70), rotation_x = 10, shadows=True, color = color.white, eternal = True)

for menu in (main_menu, video_menu, settings_menu, audio_menu):
	def animate_in_menu(menu=menu):
		for i, e in enumerate(menu.children):
			e.original_scale = e.scale
			e.scale -= .01
			e.animate_scale(e.original_scale, delay=i*.05, duration=.1, curve=curve.out_quad)

			e.alpha = 0
			e.animate('alpha', .7, delay=i*.05, duration=.1, curve=curve.out_quad)

			if hasattr(e, 'text_entity'):
				e.text_entity.alpha = 0
				e.text_entity.animate('alpha', 1, delay=i*.05, duration=.1)

	menu.on_enable = animate_in_menu

app.run()
	