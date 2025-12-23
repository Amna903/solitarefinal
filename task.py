import pygame
from moviepy.editor import VideoFileClip
from PIL import Image, ImageSequence

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 1480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game with GIF and Video")

# Load GIF directly using Pillow
gif_path = '/Users/amanmalik/Downloads/A World That Does Not Exist_ _ via Tumblr on We Heart It.gif'
im = Image.open(gif_path)
gif_frames = [pygame.image.fromstring(frame.tobytes(), frame.size, frame.mode) for frame in ImageSequence.Iterator(im)]

# Load MP4 video using MoviePy and set to loop
video_path = '/Users/amanmalik/Downloads/f3f18afa5e01261a23e045b803f02a5a.mp4'
video = VideoFileClip(video_path).loop()

# Player settings
player_pos = [50, 50]
player_color = (255, 0, 0)
player_size = 10

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement logic
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
    if keys[pygame.K_UP]:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, player_color, (*player_pos, player_size, player_size))
    
    # Display GIF frame by frame
    gif_index = (pygame.time.get_ticks() // 100) % len(gif_frames)
    screen.blit(gif_frames[gif_index], (100, 100))

    # Display MP4 video frame by frame
    video_frame = video.get_frame((pygame.time.get_ticks() / 1000) % video.duration)  # Loop the video
    video_frame_surface = pygame.surfarray.make_surface(video_frame.swapaxes(0, 1))
    screen.blit(video_frame_surface, (300, 100))

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
