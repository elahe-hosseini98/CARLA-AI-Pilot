def make_horizontal_wall(x_start, y_start):
    return f"""
    Wall {{
      translation {x_start} {y_start} 0
      rotation 0 0 1 1.5708
      size 0.01 0.2 0.1
    }}
    """


def make_vertical_wall(x_start, y_start):
    return f"""
        Wall {{
          translation {x_start} {y_start} 0
          size 0.01 0.2 0.1
        }}
        """


def add_walls_2_world(generated_walls, world_path):
    ...


if __name__ == '__main__':
    with open(r'text_mazes/100.txt', 'r') as file:
        lines = file.readlines()

    board_x_size, board_y_size = 4, 4
    wall_length = 0.2

    maze_x, maze_y = len(lines) - 1 / 2, len(lines) - 1 / 2

    vertical_start = 1.6
    horizontal_start = 1.5

    vertical_space, horizontal_space = 0.2, 0.2

    generated_walls = ""

    for line_number, line in enumerate(lines):
        seen_chars = 0
        null_chars = 0

        for char_num, char in enumerate(line):
            if char == '|':
                generated_walls += make_horizontal_wall(horizontal_start-((line_number//2)*horizontal_space),
                                                        vertical_start-(seen_chars//3)*horizontal_space)

            elif char == 'o':
                if char_num != len(line)-1 and line[char_num + 1] == '-':
                    generated_walls += make_vertical_wall(vertical_start-((line_number//2)*vertical_space),
                                                          horizontal_start-(seen_chars//3)*vertical_space)

            elif char == ' ':
                seen_chars += 1
                null_chars +=  1

                if null_chars == 3 and line[char_num + 1] != ' ':
                    null_chars = 0

                elif null_chars == 4:
                    seen_chars -= 1
                    null_chars = 0

            else: seen_chars += 1

    add_walls_2_world(generated_walls, "../worlds/micro_mouse.wbt")
