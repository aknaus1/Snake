import pygame
import time
import random

# SET SNAKE_SHAPE to the desired shape options: "circle" or "square"
SNAKE_SHAPE = "circle"

pygame.init()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 102)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (102, 0, 102)
orange = (255, 165, 0)

SNAKE_BLOCK = 20
FOOD_COLOR = white

# Constant screen size
DIS_WIDTH = SNAKE_BLOCK * 60
DIS_HEIGHT = SNAKE_BLOCK * 40

# Load background image
background_image = pygame.image.load("../assets/background.jpg")
background_rect = background_image.get_rect()

dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake')
pygame.display.set_icon(background_image)

# Clock to control the speed of the game
clock = pygame.time.Clock()

font_style = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 25)

def random_color():
    return (random.randint(25, 255), random.randint(25, 255), random.randint(25, 255))

# Function to display text messages
def message(msg, color, x_displace=0, y_displace=0):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(DIS_WIDTH / 2 + x_displace, DIS_HEIGHT / 2 + y_displace))
    dis.blit(mesg, text_rect)

# Function to display table
def display_table(data, headers=True, row_headers=True, table_border=True, cell_border=True, height=DIS_HEIGHT, width=DIS_WIDTH, center_x=DIS_WIDTH//2, center_y=DIS_HEIGHT//2):
    # Calculate dimensions of the table
    num_rows = len(data)
    num_cols = len(data[0])

    # Calculate cell width and height
    cell_width = width // num_cols
    cell_height = height // num_rows

    # Function to draw cell borders
    def draw_cell_border(x, y, width, height):
        pygame.draw.rect(dis, white, (x, y, width, height), 1)

    # Function to draw table border
    def draw_table_border(x, y, width, height):
        pygame.draw.rect(dis, white, (x, y, width, height), 3)

    # Function to draw text in cell
    def draw_text(text, x, y, type="body"):
        if type == "header":
            mesg = font_style.render(text, True, blue)
        else:
            mesg = font_style.render(text, True, yellow)
        text_rect = mesg.get_rect(center=(x + cell_width // 2, y + cell_height // 2))
        dis.blit(mesg, text_rect)

    # Draw data cells
    for row_index, row in enumerate(data):
        for col_index, cell in enumerate(row):
            x = center_x - width // 2 + col_index * cell_width
            y = center_y - height // 2 + row_index * cell_height

            if cell_border:
                draw_cell_border(x, y, cell_width, cell_height)
            
            if headers and row_index == 0:
                draw_text(cell, x, y, "header")
            elif row_headers and col_index == 0:
                draw_text(cell, x, y, "header")
            else:
                draw_text(cell, x, y, "body")

    # Draw table border
    if table_border:
        # draw_table_border(0, 0, width, height)
        draw_table_border(center_x - width // 2, center_y - height // 2, width, height)


# Function to load high scores
def load_high_score(difficulty):
    try:
        with open(f"../high_scores/highscore_{difficulty}.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Function to save high scores
def save_high_score(score, difficulty):
    with open(f"../high_scores/highscore_{difficulty}.txt", "w") as file:
        file.write(str(score))

# Function to display the main menu
def display_menu():
    menu = True
    while menu:
        dis.blit(background_image, (0, 0))
        message("Welcome to Snake Game", white, 0, -200)
        message("Press 1 for Easy", green, 0, -50)
        message("Press 2 for Medium", green, 0, 0)
        message("Press 3 for Hard", green, 0, 50)
        message("Press C for Controls Information", green, 0, 100)
        message("Press H to view High Scores", green, 0, 150)
        message("Press Q to Quit", red, 0, 200)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_1:
                    return "easy"
                elif event.key == pygame.K_2:
                    return "medium"
                elif event.key == pygame.K_3:
                    return "hard"
                elif event.key == pygame.K_c:
                    display_controls_info()
                elif event.key == pygame.K_h:
                    display_high_scores()

# Function to display player selection
def display_player_selection():
    player_selection = True
    while player_selection:
        dis.blit(background_image, (0, 0))
        message("Select Number of Players", white, 0, -200)
        message("Press 1 for 1 Player", green, 0, -50)
        message("Press 2 for 2 Players", green, 0, 0)
        message("Press M to return to Menu", red, 0, 150)
        message("Press Q to Quit", red, 0, 200)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_m:
                    return 'menu'
                elif event.key == pygame.K_1:
                    return 1
                elif event.key == pygame.K_2:
                    return 2

# Function to display high scores
def display_high_scores():
    dis.fill(white)
    high_scores = True
    while high_scores:
        dis.blit(background_image, (0, 0))
        message("High Scores", green, 0, -300)

        # Load high scores for all difficulties
        easy_1_high_score = load_high_score("easy_1")
        easy_2_high_score = load_high_score("easy_2")
        medium_1_high_score = load_high_score("medium_1")
        medium_2_high_score = load_high_score("medium_2")
        hard_1_high_score = load_high_score("hard_1")
        hard_2_high_score = load_high_score("hard_2")

        # Display high scores in a table format
        high_score_data = [
            ["Difficulty", "1 Player", "2 Player"],
            ["Easy", str(easy_1_high_score), str(easy_2_high_score)],
            ["Medium", str(medium_1_high_score), str(medium_2_high_score)],
            ["Hard", str(hard_1_high_score), str(hard_2_high_score)]
        ]
        display_table(high_score_data, headers=True, row_headers=True, table_border=True, cell_border=True, height=DIS_HEIGHT//2, width=DIS_WIDTH//2)

        message("Press M to return to Menu", red, 0, 300)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    return
                
# Function to display controls information
def display_controls_info():
    info = True
    while info:
        dis.blit(background_image, (0, 0))
        message("Controls", white, 0, -200)
        message("Use arrow keys to move the snake", green, 0, -100)
        message("Press P to pause the game", green, 0, -50)
        message("Press any key to return to Menu", red, 0, 150)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                info = False

# Function to handle the pause functionality
def pause_game():
    message("Paused", red, 0, -100)
    message("Press P to resume the game", green, 0, 0)
    message("Press M to return to Menu", red, 0, 50)
    message("Press Q to Quit", red, 0, 100)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Resume game if 'p' key is pressed again
                    return "resume"
                elif event.key == pygame.K_m:  # Return to menu if 'm' key is pressed
                    return "menu"
                elif event.key == pygame.K_q:  # Quit game if 'q' key is pressed
                    pygame.quit()
                    quit()

def draw_food(foods):
    for food in foods:
        if SNAKE_SHAPE == "circle":
            pygame.draw.circle(dis, food[2], [food[0] + SNAKE_BLOCK // 2, food[1] + SNAKE_BLOCK // 2], SNAKE_BLOCK // 2)
        elif SNAKE_SHAPE == "square":
            pygame.draw.rect(dis, food[2], [food[0], food[1], SNAKE_BLOCK, SNAKE_BLOCK])
        else:
            raise ValueError("Invalid SNAKE_SHAPE value. Use 'circle' or 'square'.")

def draw_snake(player):
    snake_list = player["snake_list"]
    snake_color = player["snake_color"]
    for i, segment in enumerate(snake_list):
        if SNAKE_SHAPE == "circle":
            if i == 0 or i == len(snake_list) - 1:
                pygame.draw.circle(dis, snake_color, segment.center, SNAKE_BLOCK // 2)
            if i > 0 and i < len(snake_list) - 1:
                pygame.draw.rect(dis, snake_color, segment)
            if i > 0 and len(snake_list) > 1:
                    temp_x1, temp_y1 = snake_list[i - 1].x, snake_list[i - 1].y
                    if abs(snake_list[i].x - snake_list[i - 1].x) == SNAKE_BLOCK:
                        temp_x1 += (snake_list[i].x - snake_list[i - 1].x) / 2
                    elif abs(snake_list[i].y - snake_list[i - 1].y) == SNAKE_BLOCK:
                        temp_y1 += (snake_list[i].y - snake_list[i - 1].y) / 2
                    pygame.draw.rect(dis, snake_color, pygame.Rect(temp_x1, temp_y1, SNAKE_BLOCK, SNAKE_BLOCK))
        elif SNAKE_SHAPE == "square":
            pygame.draw.rect(dis, snake_color, segment)
        else:
            raise ValueError("Invalid SNAKE_SHAPE value. Use 'circle' or 'square'.")
        
def add_snake_head(snake_list, length_of_snake, x1, y1):
    snake_head = pygame.Rect(x1, y1, SNAKE_BLOCK, SNAKE_BLOCK)
    snake_list.append(snake_head)
    if len(snake_list) > length_of_snake:
        del snake_list[0]

def add_snake_head_to_player(player):
    snake_head = pygame.Rect(player["x1"], player["y1"], SNAKE_BLOCK, SNAKE_BLOCK)
    player["snake_list"].append(snake_head)
    if len(player["snake_list"]) > player["length_of_snake"]:
        del player["snake_list"][0]

    player["snake_head"] = snake_head

def new_player(difficulty, snake_color):
    player = {
        "x1": round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK,
        "y1": round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK,
        "x1_change": 0,
        "y1_change": 0,
        "snake_list": [],
        "length_of_snake": 0,
        "snake_color": snake_color,
    }

    if difficulty == "easy":
        player["snake_speed"] = 10
        player["length_of_snake"] = 1
    elif difficulty == "medium":
        player["snake_speed"] = 20
        player["length_of_snake"] = 2
    else:
        player["snake_speed"] = 30
        player["length_of_snake"] = 3
    
    return player

def check_collision_w_self(player, difficulty):
    if player["x1_change"] == 0 and player["y1_change"] == 0:
        return False
    snake_head = player["snake_head"]
    for segment in player["snake_list"][:-1]:
        if snake_head.colliderect(segment):
            return True
    return False

def check_collision_w_others(players, player, difficulty):
    snake_head = player["snake_head"]
    for other in players:
        if other is not player:
            for segment in other["snake_list"]:
                if snake_head.colliderect(segment):
                    other["length_of_snake"] += player["length_of_snake"] // 5
                    return True
    return False

def check_collision_w_food(foods, player):
    snake_head = player["snake_head"]
    for food in foods:
        if snake_head.colliderect(food[0], food[1], SNAKE_BLOCK, SNAKE_BLOCK):
            foods.remove(food)
            foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
            foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
            foods.append((foodx, foody, random_color()))
            player["length_of_snake"] += 1
            return True
    return False

def update_player_position(player):
    if player["x1"] >= DIS_WIDTH:
        player["x1"] = -player["x1_change"]
    elif player["x1"] < 0:
        player["x1"] = DIS_WIDTH - SNAKE_BLOCK - player["x1_change"]
    
    if player["y1"] >= DIS_HEIGHT:
        player["y1"] = -player["y1_change"]
    elif player["y1"] < 0:
        player["y1"] = DIS_HEIGHT - SNAKE_BLOCK - player["y1_change"]

    player["x1"] += player["x1_change"]
    player["y1"] += player["y1_change"]

def update_delta(player, direction):
    if direction == "left":
        player["x1_change"] = -SNAKE_BLOCK
        player["y1_change"] = 0
    elif direction == "right":
        player["x1_change"] = SNAKE_BLOCK
        player["y1_change"] = 0
    elif direction == "up":
        player["y1_change"] = -SNAKE_BLOCK
        player["x1_change"] = 0
    elif direction == "down":
        player["y1_change"] = SNAKE_BLOCK
        player["x1_change"] = 0

def key_pressed(players, key):
        if key == pygame.K_LEFT:
            update_delta(players[0], "left")
        elif key == pygame.K_RIGHT:
            update_delta(players[0], "right")
        elif key == pygame.K_UP:
            update_delta(players[0], "up")
        elif key == pygame.K_DOWN:
            update_delta(players[0], "down")

        player = players[1] if len(players) > 1 else players[0]

        if key == pygame.K_a:
            update_delta(player, "left")
        elif key == pygame.K_d:
            update_delta(player, "right")
        elif key == pygame.K_w:
            update_delta(player, "up")
        elif key == pygame.K_s:
            update_delta(player, "down")
            
        
# Function to run the game loop
def gameLoop(difficulty, number_of_players):
    number_of_food = number_of_players * 10

    game_over = False
    game_close = False

    players = []
    snake_colors = [blue, red, green, yellow]
    for i in range(number_of_players):
        player = new_player(difficulty, snake_colors[i] if i < len(snake_colors) else blue)
        players.append(player)

    foods = []
    for _ in range(number_of_food):
        foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
        foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
        foods.append((foodx, foody, random_color()))

    high_score = load_high_score(difficulty + "_" + str(number_of_players))

    # Variables for background animation
    bg_x = 0
    bg_speed = 1

    while not game_over:

        while game_close:
            dis.blit(background_image, (0, 0))
            message("You Lost!", red, 0, -100)
            message("Press C to Play Again", green, 0, -50)
            message("Press M to return to Menu", green, 0, 0)
            message("Press Q to Quit", red, 0, 50)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        quit()
                    if event.key == pygame.K_c:
                        gameLoop(difficulty)
                    if event.key == pygame.K_m:
                        return "menu"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]:
                    key_pressed(players, event.key)
                elif event.key == pygame.K_p:
                    pause_result = pause_game()
                    if pause_result == "menu":
                        return "menu"
                    elif pause_result == "resume":
                        pass

        # Update the background
        dis.blit(background_image, (bg_x, 0))
        dis.blit(background_image, (bg_x - background_rect.width, 0))

        bg_x += bg_speed
        if bg_x >= background_rect.width:
            bg_x = 0
        
        for player in players:
            update_player_position(player)

        draw_food(foods)

        for player in players:
            add_snake_head_to_player(player)
            draw_snake(player)

        pygame.display.update()

        for i, player in enumerate(players):
            if number_of_players == 1:
                if check_collision_w_self(player, difficulty) or check_collision_w_others(players, player, difficulty):
                    # game_close = True
                    players[i] = new_player(difficulty, player["snake_color"])
                    break
            else:
                if check_collision_w_others(players, player, difficulty):
                    # game_close = True
                    players[i] = new_player(difficulty, player["snake_color"])
                    break
            check_collision_w_food(foods, player)

        for player in players:
            # Update high score if needed
            if player["length_of_snake"] - player["snake_speed"] / 10 > high_score:
                high_score = int(player["length_of_snake"] - player["snake_speed"] / 10)
                save_high_score(high_score, difficulty + "_" + str(number_of_players))

            clock.tick(player["snake_speed"])
    return "menu"

# Main function
def main():
    while True:
        selected_difficulty = display_menu()
        number_of_players = display_player_selection()
        if selected_difficulty != "menu":
            game_result = gameLoop(selected_difficulty, number_of_players)
            if game_result == "menu":
                continue

if __name__ == "__main__":
    main()
