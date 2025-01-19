import pygame
import random
import math

# --- Constants ---
WIDTH, HEIGHT = 800, 600   # Size of the window
FPS = 60                   # Frames per second
DISK_RADIUS = 40           # Radius of each disk
DISK_COUNT = 6

# For demonstration, we won't actually draw 8 small "coin" circles inside,
# but we'll keep track of them in a list. You can add more advanced graphics later.
MAX_COINS_PER_DISK = 8

# --- Disk Class ---
class Disk:
    def __init__(self, x, y, vx, vy, radius, coin_count=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        # Instead of a count, you could store e.g. self.coins = ["coin"] * coin_count
        # if you need to manage them individually. For now a count is enough.
        self.coin_count = coin_count
    
    def update_position(self, dt):
        """Move the disk, bounce off the walls if hitting edges."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Check for collision with left/right walls
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vx = -self.vx
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.vx = -self.vx
        
        # Check for collision with top/bottom walls
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vy = -self.vy
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy = -self.vy

    def draw(self, screen, font):
        """Draw the disk and the coin count on top."""
        pygame.draw.circle(screen, (0, 128, 255), (int(self.x), int(self.y)), self.radius)
        
        # Draw the number of coins
        text_surface = font.render(str(self.coin_count), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text_surface, text_rect)

def distance(disk1, disk2):
    """Euclidian distance between two disk centers."""
    dx = disk2.x - disk1.x
    dy = disk2.y - disk1.y
    return math.sqrt(dx*dx + dy*dy)

def handle_disk_collision(disk1, disk2):
    """Check if disks collide. If they do, perform elastic collision and coin exchange."""
    dist = distance(disk1, disk2)
    if dist < disk1.radius + disk2.radius:
        # --- Simple elastic collision for equal masses ---
        # 1) Find the collision normal
        nx = (disk2.x - disk1.x) / dist
        ny = (disk2.y - disk1.y) / dist

        # 2) Project velocities onto normal
        v1n = disk1.vx * nx + disk1.vy * ny
        v2n = disk2.vx * nx + disk2.vy * ny

        # 3) Swap the normal components (like 1D elastic collision along that normal)
        disk1.vx += (v2n - v1n) * nx
        disk1.vy += (v2n - v1n) * ny
        disk2.vx += (v1n - v2n) * nx
        disk2.vy += (v1n - v2n) * ny

        # --- Coin exchange: for each coin in total, flip a coin to move it or not ---
        # For clarity, let's treat each disk's coin_count as if each "coin" is processed individually
        total_coins_disk1 = disk1.coin_count
        total_coins_disk2 = disk2.coin_count

        # We'll handle them all from the perspective of disk1 first
        # Then from the perspective of disk2. Another approach is to actually keep
        # coin arrays, but here's a simplified logic:
        
        # For disk1's coins:
        coins_moving_to_disk2 = 0
        for _ in range(total_coins_disk1):
            if random.random() < 0.5:
                coins_moving_to_disk2 += 1
        disk1.coin_count -= coins_moving_to_disk2
        disk2.coin_count += coins_moving_to_disk2
        
        # For disk2's coins:
        coins_moving_to_disk1 = 0
        for _ in range(total_coins_disk2):
            if random.random() < 0.5:
                coins_moving_to_disk1 += 1
        disk2.coin_count -= coins_moving_to_disk1
        disk1.coin_count += coins_moving_to_disk1
        
        # You could clamp coin counts to the max if needed:
        disk1.coin_count = min(disk1.coin_count, MAX_COINS_PER_DISK)
        disk2.coin_count = min(disk2.coin_count, MAX_COINS_PER_DISK)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Disks with Coin Exchange")
    clock = pygame.time.Clock()

    # Prepare a font for drawing coin counts
    font = pygame.font.SysFont(None, 24)

    # --- Create 6 disks ---
    # - 4 disks start with 1 coin each
    # - 2 disks start with 2 coins each
    # We have to ensure total 8 coins across them.
    disks = []
    coin_distribution = [1, 1, 1, 1, 2, 2]  # 4 disks with 1 coin, 2 with 2 coins

    for i in range(DISK_COUNT):
        # Random initial position (with some padding so they start inside the box)
        x = random.randint(DISK_RADIUS, WIDTH - DISK_RADIUS)
        y = random.randint(DISK_RADIUS, HEIGHT - DISK_RADIUS)

        # Random velocity
        vx = random.uniform(-200, 200)
        vy = random.uniform(-200, 200)

        # Create the disk
        disk = Disk(x, y, vx, vy, DISK_RADIUS, coin_count=coin_distribution[i])
        disks.append(disk)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # dt in seconds
        
        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # --- Update all disks ---
        for disk in disks:
            disk.update_position(dt)
        
        # --- Collision detection among disks ---
        # We'll do a naive all-pairs check for 6 disks (that’s only 15 checks).
        for i in range(DISK_COUNT):
            for j in range(i + 1, DISK_COUNT):
                handle_disk_collision(disks[i], disks[j])
        
        # --- Draw everything ---
        screen.fill((0, 0, 0))  # black background
        for disk in disks:
            disk.draw(screen, font)
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
