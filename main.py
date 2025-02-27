import pygame
import random
from queue import PriorityQueue

# Maze generation with loops
def generate_maze(width, height, loop_probability=0.2):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    stack = [(1, 1)]
    maze[1][1] = 0

    while stack:
        x, y = stack[-1]
        directions = [(x+2, y), (x-2, y), (x, y+2), (x, y-2)]
        random.shuffle(directions)

        for nx, ny in directions:
            if 0 < nx < width-1 and 0 < ny < height-1 and maze[ny][nx]:
                maze[ny][nx] = 0
                maze[(ny + y) // 2][(nx + x) // 2] = 0
                stack.append((nx, ny))
                break
        else:
            stack.pop()

    # Add loops to the maze
    for y in range(1, height-1):
        for x in range(1, width-1):
            if maze[y][x] == 1:
                neighbors = 0
                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    if maze[y + dy][x + dx] == 0:
                        neighbors += 1
                if neighbors >= 2 and random.random() < loop_probability:
                    maze[y][x] = 0

    return maze

# A* Pathfinding Algorithm
def a_star(maze, start, end):
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: abs(start[0] - end[0]) + abs(start[1] - end[1])}

    while not open_set.empty():
        _, current = open_set.get()

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < len(maze[0]) and 0 <= neighbor[1] < len(maze) and maze[neighbor[1]][neighbor[0]] == 0:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + abs(neighbor[0] - end[0]) + abs(neighbor[1] - end[1])
                    open_set.put((f_score[neighbor], neighbor))

    return None

# Pygame Setup
pygame.init()
width, height = 1200, 900
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

maze_width, maze_height = 51, 41  # Larger maze
maze = generate_maze(maze_width, maze_height, loop_probability=0.2)  # Add loops
player_pos = (1, 1)
ai_pos = (maze_width-2, maze_height-2)
exit_pos = (maze_width-2, maze_height-2)

# Game Loop
running = True
ai_move_counter = 0  # Slow down AI movement
while running:
    screen.fill((0, 0, 0))

    # Draw Maze
    for y in range(maze_height):
        for x in range(maze_width):
            if maze[y][x]:
                pygame.draw.rect(screen, (255, 255, 255), (x*20, y*20, 20, 20))

    # Draw Player Bot, AI Opponent, and Exit
    pygame.draw.rect(screen, (0, 255, 0), (player_pos[0]*20, player_pos[1]*20, 20, 20)) #green
    pygame.draw.rect(screen, (255, 0, 0), (ai_pos[0]*20, ai_pos[1]*20, 20, 20)) #red
    pygame.draw.rect(screen, (0, 0, 255), (exit_pos[0]*20, exit_pos[1]*20, 20, 20)) #draw

    # Player Bot Movement
    player_path = a_star(maze, player_pos, exit_pos)
    if player_path and len(player_path) > 1:
        player_pos = player_path[1]

    # AI Opponent Movement (Slower)
    ai_move_counter += 1
    if ai_move_counter % 1 == 0:  # AI moves every 5 frames
        ai_path = a_star(maze, ai_pos, player_pos)
        if ai_path and len(ai_path) > 1:
            ai_pos = ai_path[1]

    # Check Win/Lose Conditions
    if player_pos == exit_pos:
        print("Player Bot Wins!")
        running = False
    if player_pos == ai_pos:
        print("AI Opponent Wins!")
        running = False
    
    pygame.display.flip()
    clock.tick(3)  # Adjust speed of the game

pygame.quit()