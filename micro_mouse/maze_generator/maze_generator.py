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
    try:
        with open(world_path, 'a') as file:
            file.write('\n' + generated_walls)
        print(f"Successfully added walls to the file: {world_path}")
    except Exception as e:
        print(f"An error occurred while adding walls to the file: {e}")


def wall_generation_logic(line_white_spaces, line_seen_chars, formated_generated_walls_str):
    if char == '|':
        formated_generated_walls_str += make_horizontal_wall(horizontal_start - ((line_number // 2) * horizontal_space),
                                                             vertical_start - (line_seen_chars // 3) * horizontal_space)

    elif char == 'o':
        if char_num != len(line) - 1 and line[char_num + 1] == '-':
            formated_generated_walls_str += make_vertical_wall(vertical_start - ((line_number // 2) * vertical_space),
                                                               horizontal_start - (
                                                                           line_seen_chars // 3) * vertical_space)

    elif char == ' ':
        line_seen_chars += 1
        line_white_spaces += 1

        if line_white_spaces == 3 and line[char_num + 1] != ' ':
            line_white_spaces = 0

        elif line_white_spaces == 4:
            line_seen_chars -= 1
            line_white_spaces = 0

    else:
        line_seen_chars += 1

    return line_white_spaces, line_seen_chars, formated_generated_walls_str


if __name__ == '__main__':
    with open(r'text_mazes/100.txt', 'r') as file:
        lines = file.readlines()

    # measurements based on the pre-created world
    board_x_size, board_y_size = 4, 4
    wall_length = 0.2

    maze_x, maze_y = len(lines) - 1 / 2, len(lines) - 1 / 2

    vertical_start = 1.6
    horizontal_start = 1.5

    vertical_space, horizontal_space = 0.2, 0.2

    formated_generated_walls_str = ""

    for line_number, line in enumerate(lines):
        line_seen_chars = 0
        line_white_spaces = 0

        for char_num, char in enumerate(line):
            line_white_spaces, line_seen_chars, formated_generated_walls_str = wall_generation_logic(
                line_white_spaces, line_seen_chars, formated_generated_walls_str
            )

    add_walls_2_world(formated_generated_walls_str, "../worlds/micro_mouse.wbt")
