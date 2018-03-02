import tdl
from input_handlers import handle_keys

SCREEN_WIDTH = 80
SCREEN_HEIGHT = 50


def main():
    player_x = int(SCREEN_WIDTH / 2)
    player_y = int(SCREEN_HEIGHT / 2)

    tdl.set_font('arial12x12.png', greyscale=True, altLayout=True)

    root_console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='Roguelike Tutorial Revised')
    con = tdl.Console(SCREEN_WIDTH, SCREEN_HEIGHT)

    while not tdl.event.is_window_closed():
        con.draw_char(player_x, player_y, '@', bg=None, fg=(255, 255, 255))
        root_console.blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0)
        tdl.flush()

        con.draw_char(player_x, player_y, ' ', bg=None)

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
            player_x += dx
            player_y -= dy

        if exit_action:
            return True

        if switch_fullscreen:
            tdl.set_fullscreen(not tdl.get_fullscreen())

        if user_input.key == 'ESCAPE':
            return True


if __name__ == '__main__':
    main()
