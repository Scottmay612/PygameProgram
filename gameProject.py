import pygame
import random

"""
In this project, I used Gemini AI to help 
me with syntax or to brainstorm ideas.
No code was directly copied from Gemini.
"""

# Initialize game.
pygame.init()

# Set screen dimensions and create screen.
HEIGHT = 400
WIDTH = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set fps and clock speed.
clock = pygame.time.Clock()
fps = 60

# Store white as a variable.
white = (255,255,255)

# Text: "You Died"
font = pygame.font.SysFont(None, 32)
text_spike = "You Died"
text_spike_surface = font.render(text_spike, True, white)
text_spike_rect = text_spike_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Text: "Don't touch the spikes.."
text_warning = "Don't touch the spikes.."
text_warning_surface = font.render(text_warning, True, white)
text_warning_rect = text_warning_surface.get_rect(center=(WIDTH // 2, HEIGHT - 100))

# Text: "This room does nothing"
text_nothing = "This room does nothing"
text_nothing_surface = font.render(text_nothing, True, white)
text_nothing_rect = text_nothing_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Assign colors to each room.
left_color = ((255,0,0))
right_color = ((80,130,40))

# Create dimensions for main rectangle.
rect_width = 20
rect_height = 40
rect_color = (24,100,12)
rect_x = WIDTH // 2
rect_y = 50
rect_bottom = rect_y + rect_height

# Create dimensions (and color) for the walls.
wall_color = (50,50,50)
wall_width = 15
lower_wall_bound = HEIGHT // 2 - rect_height + 1.5 * rect_height
upper_wall_bound = HEIGHT // 2 - rect_height

# Make for walls for all four sides of the screen.
walls = [
    pygame.Rect(0, 0, WIDTH, wall_width), # Top wall
    pygame.Rect(0, HEIGHT - wall_width, WIDTH, wall_width), # Bottom wall
    pygame.Rect(WIDTH - wall_width, 0, wall_width, HEIGHT), # Right wall
    pygame.Rect(0, 0, wall_width, HEIGHT), # Left wall
    ]

# Make doors for the left and right sides of the screen.
doors = [
    pygame.Rect(0, HEIGHT // 2 - rect_height, wall_width, 
                1.5 * rect_height), # Left door
    pygame.Rect(WIDTH - wall_width, HEIGHT // 2 - rect_height, 
                wall_width, 1.5 * rect_height) # Right door
]

# Declare a list of random colors.
rand_colors = []

# Fill the rand_colors list with 10 different random colors.
for i in range(0, 11):
    color = (random.randint(0,255), random.randint(0,255),random.randint(0,255))
    rand_colors.append(color)

# Function will make a rectangle with random dimensions.
def make_rand_rect():
    rand_height = random.randint(0,100)
    rand_width = random.randint(0,100)
    rand_x = random.randint(0, WIDTH)
    rand_y = random.randint(0, HEIGHT)
    return pygame.Rect(rand_x, rand_y, rand_width, rand_height)

# Function displays the four walls on the edges of the screen.
def display_walls():
    for wall in walls:
        pygame.draw.rect(screen, wall_color, wall)

# Make 10 random rectangles and add them to the rand_rects list.
rand_rects = []
for i in range(0,11):
    rand_rects.append(make_rand_rect())

# Label dimensions for each triangle.
side_length = 15
tri_x = wall_width
tri_y = wall_width

# Create as many triangles as will fit in the screen and add their point 
# coordinates to the list.
triangles = []
while tri_x < WIDTH - wall_width:

    # Moves the x coordinate over each time so that they are all in a row.

    """
    AI helped me learn how to make triangles in a row.
    I did not copy any code. I just learned about it and 
    implemented it in a way that worked for what I am doing.
    """
    points = ((tri_x,tri_y), (tri_x + side_length, tri_y), 
              ((tri_x + side_length / 2), tri_y * 3))
    
    tri_x += side_length

    # Add the points to the list.
    triangles.append(points)

# Shows which room is currently being used.
right_room = False
main_room = True
left_room = False

# Boolean for if you touched the spikes or not in the left room.
you_died = False

# Boolean for if the game is running or not.
running = True

while running:
    # Save the velocity in vel.
    time_elapsed = clock.tick(fps) / 1000 # AI showed me how to do this.
    velocity = 200
    vel = velocity * time_elapsed


    # Instantiate your movable rectangle as box.
    box = pygame.Rect(rect_x, rect_y, rect_width, rect_height)

    # Assign names to each wall.
    top_wall = walls[0]
    bottom_wall = walls[1]
    right_wall = walls[2]
    left_wall = walls[3]

    # Check events for if they click the X button.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Run this if the main room is active.
    if main_room:

        # Make the screen white.
        screen.fill(white)

        # Display the walls.
        display_walls()

        # Draw the random rectangles and delete them if the box runs into them.
        for i, rect in enumerate(rand_rects):
            pygame.draw.rect(screen, rand_colors[i], rect)
            if box.colliderect(rect):

                # Delete both the rectangle and its color from their lists.
                del rand_colors[i]
                del rand_rects[i]
        
        # Draw each of the doors.
        for door in doors:
            pygame.draw.rect(screen, white, door)

        # Change to the left room if the user goes out the left door.
        pygame.draw.rect(screen, rect_color, box)
        if rect_x < 0:
            main_room = False
            left_room = True
            rect_x = WIDTH

        # Change to the right room if the user goes out the right door.
        elif rect_x > WIDTH:
            main_room = False
            right_room = True
            rect_x = 0

    # Run this if the left room is active.
    elif left_room:
        screen.fill(left_color)
        for wall in walls:
            pygame.draw.rect(screen, wall_color, wall)

        for door in doors:
            pygame.draw.rect(screen, left_color, door)

        for i, tri in enumerate(triangles):
            pygame.draw.polygon(screen, (0,0,0), tri)
            rand_tri = random.randint(0, len(triangles))
        
        # If the box hits the triangles, you_died changes to true.
        if box.y < wall_width * 4:
            you_died = True

        if you_died:
            # Display "You died" if spikes are touched.
            screen.blit(text_spike_surface, text_spike_rect)
        else: 
            # Display warning if the spikes haven't been touched yet.
            screen.blit(text_warning_surface, text_warning_rect)

        # Draw the box on the screen.
        pygame.draw.rect(screen, rect_color, box)

        # Change to main room if go through right door.
        if rect_x > WIDTH:
            left_room = False
            main_room = True
            rect_x = 0

        # Change to right room if go through left door.
        if rect_x < 0:
            right_room = True
            left_room = False
            rect_x = WIDTH

    # Run this if the right room is active.
    elif right_room:
        # Fill the room with green (right_color).
        screen.fill(right_color)

        # Display message.
        screen.blit(text_nothing_surface, text_nothing_rect)

        # Display walls.
        for wall in walls:
            pygame.draw.rect(screen, wall_color, wall)

        # Display doors.
        for door in doors:
            pygame.draw.rect(screen, right_color, door)

        # Draw the box on the screen.
        pygame.draw.rect(screen, rect_color, box)
        
        # Change to main room if go through left door.
        if rect_x < 0:
            right_room = False
            main_room = True
            rect_x = WIDTH
        
        # Change to left room if go through right door.
        elif rect_x > WIDTH:
            left_room = True
            right_room = False
            rect_x = 0

    # Find all the keys getting pressed.
    keys = pygame.key.get_pressed()

    # Create a separate variable for the bottom of the rectangle.
    rect_bottom = rect_y + rect_height

    # Move left.
    if keys[pygame.K_LEFT]:

        # Move if you're not touching the wall or you're in the doorway.
        if (not box.colliderect(left_wall) or 
           (rect_y > upper_wall_bound and rect_bottom < lower_wall_bound)):
            rect_x -= vel

    # Move right.
    if keys[pygame.K_RIGHT]:

        # Move if you're not touching the wall or you're in the doorway.
        if (not box.colliderect(right_wall) or 
           (rect_y > upper_wall_bound and rect_bottom < lower_wall_bound)):
                rect_x += vel

    # Move up if not touching the wall.
    if keys[pygame.K_UP] and rect_y > wall_width:
        rect_y -= vel

    # Move down if not touching the wall.
    if keys[pygame.K_DOWN] and rect_bottom < HEIGHT - wall_width:
        rect_y += vel

    # Refresh the game.
    pygame.display.flip()