import pygame
import time
import random

# SET SNAKE_SHAPE to the desired shape options: "circle" or "square"
SNAKE_SHAPE = "circle"

pygame.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

SNAKE_BLOCK = 20
SNAKE_COLOR = blue
FOOD_COLOR = white
NUMBER_OF_FOOD = 10

# Constant screen size
DIS_WIDTH = SNAKE_BLOCK * 60
DIS_HEIGHT = SNAKE_BLOCK * 40

# Load background image
background_image = pygame.image.load("background.jpg")
background_rect = background_image.get_rect()

dis = pygame.display.set_mode((DIS_WIDTH, DIS_HEIGHT))
pygame.display.set_caption('Snake')
pygame.display.set_icon(pygame.image.load("background.jpg"))

# Clock to control the speed of the game
clock = pygame.time.Clock()

font_style = pygame.font.SysFont(None, 50)
small_font = pygame.font.SysFont(None, 25)

# Function to display text messages
def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    text_rect = mesg.get_rect(center=(DIS_WIDTH / 2, DIS_HEIGHT / 2 + y_displace))
    dis.blit(mesg, text_rect)

# Function to load high scores
def load_high_score(difficulty):
    try:
        with open(f"highscore_{difficulty}.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

# Function to save high scores
def save_high_score(score, difficulty):
    with open(f"highscore_{difficulty}.txt", "w") as file:
        file.write(str(score))

# Function to display the main menu
def display_menu():
    menu = True
    while menu:
        dis.blit(background_image, (0, 0))
        message("Welcome to Snake Game", white, -200)
        message("Press 1 for Easy", green, -50)
        message("Press 2 for Medium", green, 0)
        message("Press 3 for Hard", green, 50)
        message("Press C for Controls Information", green, 100)
        message("Press H to view High Scores", green, 150)
        message("Press Q to Quit", red, 200)
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

# Function to display high scores
def display_high_scores():
    high_scores = True
    while high_scores:
        dis.blit(background_image, (0, 0))
        message("High Scores", white, -200)

        # Load and display high scores for all difficulties
        easy_high_score = load_high_score("easy")
        medium_high_score = load_high_score("medium")
        hard_high_score = load_high_score("hard")

        message(f"Easy: {easy_high_score}", green, -100)
        message(f"Medium: {medium_high_score}", green, -50)
        message(f"Hard: {hard_high_score}", green)

        message("Press M to return to Menu", red, 200)
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
        message("Controls", white, -200)
        message("Use arrow keys to move the snake", green, -100)
        message("Press P to pause the game", green, -50)
        message("Press any key to return to Menu", red, 150)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                info = False

# Function to handle the pause functionality
def pause_game():
    message("Paused", red, 0)
    message("Press P to resume the game", green, 50)
    message("Press M to return to Menu", red, 100)
    message("Press Q to Quit", red, 150)
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
            pygame.draw.circle(dis, FOOD_COLOR, [food[0] + SNAKE_BLOCK // 2, food[1] + SNAKE_BLOCK // 2], SNAKE_BLOCK // 2)
        elif SNAKE_SHAPE == "square":
            pygame.draw.rect(dis, FOOD_COLOR, [food[0], food[1], SNAKE_BLOCK, SNAKE_BLOCK])
        else:
            raise ValueError("Invalid SNAKE_SHAPE value. Use 'circle' or 'square'.")

def draw_snake(snake_list):
    for i, segment in enumerate(snake_list):
        if SNAKE_SHAPE == "circle":
            if i == 0 or i == len(snake_list) - 1:
                pygame.draw.circle(dis, SNAKE_COLOR, segment.center, SNAKE_BLOCK // 2)
            if i > 0 and i < len(snake_list) - 1:
                pygame.draw.rect(dis, SNAKE_COLOR, segment)
            if i > 0 and len(snake_list) > 1:
                    temp_x1, temp_y1 = snake_list[i - 1].x, snake_list[i - 1].y
                    if abs(snake_list[i].x - snake_list[i - 1].x) == SNAKE_BLOCK:
                        temp_x1 += (snake_list[i].x - snake_list[i - 1].x) / 2
                    elif abs(snake_list[i].y - snake_list[i - 1].y) == SNAKE_BLOCK:
                        temp_y1 += (snake_list[i].y - snake_list[i - 1].y) / 2
                    pygame.draw.rect(dis, SNAKE_COLOR, pygame.Rect(temp_x1, temp_y1, SNAKE_BLOCK, SNAKE_BLOCK))
        elif SNAKE_SHAPE == "square":
            pygame.draw.rect(dis, SNAKE_COLOR, segment)
        else:
            raise ValueError("Invalid SNAKE_SHAPE value. Use 'circle' or 'square'.")
        
# Function to run the game loop
def gameLoop(difficulty):
    game_over = False
    game_close = False

    x1 = DIS_WIDTH / 2
    y1 = DIS_HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 0

    foods = []
    for i in range(NUMBER_OF_FOOD):
        foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
        foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
        foods.append((foodx, foody))

    high_score = load_high_score(difficulty)

    if difficulty == "easy":
        snake_speed = 10
        Length_of_snake = 1
    elif difficulty == "medium":
        snake_speed = 20
        Length_of_snake = 2
    else:
        snake_speed = 30
        Length_of_snake = 3

    # Variables for background animation
    bg_x = 0
    bg_speed = 1

    while not game_over:

        while game_close:
            dis.blit(background_image, (0, 0))
            message("You Lost!", red, -100)
            message("Press C to Play Again", green, -50)
            message("Press M to return to Menu", green, 0)
            message("Press Q to Quit", red, 50)
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
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_result = pause_game()
                    if pause_result == "menu":
                        return "menu"
                    elif pause_result == "resume":
                        pass

        if x1 >= DIS_WIDTH:
            x1 = -x1_change
        elif x1 < 0:
            x1 = DIS_WIDTH - SNAKE_BLOCK - x1_change

        if y1 >= DIS_HEIGHT:
            y1 = -y1_change
        elif y1 < 0:
            y1 = DIS_HEIGHT - SNAKE_BLOCK - y1_change

        x1 += x1_change
        y1 += y1_change

        dis.blit(background_image, (bg_x, 0))
        dis.blit(background_image, (bg_x - background_rect.width, 0))

        bg_x += bg_speed
        if bg_x >= background_rect.width:
            bg_x = 0

        draw_food(foods)

        snake_head = pygame.Rect(x1, y1, SNAKE_BLOCK, SNAKE_BLOCK)
        snake_List.append(snake_head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        draw_snake(snake_List)

        pygame.display.update()

        for food in foods:
            if snake_head.colliderect(food[0], food[1], SNAKE_BLOCK, SNAKE_BLOCK):
                foods.remove(food)
                foodx = round(random.randrange(0, DIS_WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
                foody = round(random.randrange(0, DIS_HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
                foods.append((foodx, foody))
                Length_of_snake += 1

        # Update high score if needed
        if Length_of_snake - snake_speed / 10 > high_score:
            high_score = int(Length_of_snake - snake_speed / 10)
            save_high_score(high_score, difficulty)

        clock.tick(snake_speed)
    return "menu"

# Main function
def main():
    while True:
        selected_difficulty = display_menu()
        if selected_difficulty != "menu":
            game_result = gameLoop(selected_difficulty)
            if game_result == "menu":
                continue

if __name__ == "__main__":
    main()
