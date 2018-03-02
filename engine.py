import tdl

from entity import Entity
from input_handlers import handle_keys
from map_utils import GameMap, make_map
from render_functions import clear_all, render_all

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50


def main():
    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 'BASIC'
    fov_light_walls = True
    fov_radius = 10

    colors = {
        'dark_wall': (0, 0, 100),
        'dark_ground': (50, 50, 150),
        'light_wall': (130, 110, 50),
        'light_ground': (200, 180, 50)
    }

    player = Entity(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), '@', (255, 255, 255))
    npc = Entity(int(SCREEN_WIDTH / 2 - 5), int(SCREEN_HEIGHT / 2), '@', (255, 255, 0))

    entities = [npc, player]

    tdl.set_font('arial12x12.png', greyscale=True, altLayout=True)

    root_console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='Roguelike Tutorial Revised')
    con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)

    game_map = GameMap(map_width, map_height)
    make_map(game_map, max_rooms, room_min_size, room_max_size, map_width, map_height, player)

    fov_recompute = True

    while not tdl.event.is_window_closed():
        if fov_recompute:
            game_map.compute_fov(player.x, player.y, fov=fov_algorithm, radius=fov_radius, light_walls=fov_light_walls)

        render_all(con, entities, game_map, fov_recompute, root_console, SCREEN_WIDTH, SCREEN_HEIGHT, colors)
        tdl.flush()

        clear_all(con, entities)

        fov_recompute = False

        for event in tdl.event.get():
            if event.type == 'KEYDOWN':
                user_input = event
                break
        else:
            user_input = None

        if not user_input:
            continue

        action = handle_keys(user_input)

        move = action.get('move')
        exit_action = action.get('exit')
        switch_fullscreen = action.get('switch_fullscreen')

        if move:
            dx, dy = move
            if game_map.walkable[player.x + dx, player.y + dy]:
                player.move(dx, dy)
                fov_recompute = True

        if exit_action:
            return True

        if switch_fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        if user_input.key == 'ESCAPE':
            return True


if __name__ == '__main__':
    main()
