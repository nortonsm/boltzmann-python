import pygame
import random
import math
import matplotlib.pyplot as plt

# -----------------
# Global variables
# -----------------
collision_count = 0
cumulative_counts = [0] * 9  # For coin counts 0..8

# --- Constants ---
WIDTH, HEIGHT = 800, 600   # Size of the Pygame window
FPS = 60                   # Frames per second
DISK_RADIUS = 40           # Radius of each disk
DISK_COUNT = 3             # Number of disks (balls)
MAX_COINS_PER_DISK = 4     # Maximum number of coins (energy units) per disk
SPEED_FACTOR = 5.0         # Speed factor for disks (1.0 = normal speed)
EPSILON = 1e-5             # Small value to avoid division by zero
N = 100                    # Print y-values every N collisions

# -----------------
# Disk class
# -----------------
class Disk:
    def __init__(self, x, y, vx, vy, radius, coin_count=0):
        self.x = x
        self.y = y
        self.vx = vx * SPEED_FACTOR  # Apply speed factor
        self.vy = vy * SPEED_FACTOR  # Apply speed factor
        self.radius = radius
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
        text_surface = font.render(str(self.coin_count), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text_surface, text_rect)


# -----------------
# Helper functions
# -----------------
def distance(disk1, disk2):
    """Euclidean distance between two disk centers."""
    dx = disk2.x - disk1.x
    dy = disk2.y - disk1.y
    return math.sqrt(dx*dx + dy*dy)

def handle_disk_collision(disk1, disk2):
    """
    Check if disks collide. If they do, perform elastic collision and coin exchange.
    Returns True if a collision actually happened, otherwise False.
    """
    dist = distance(disk1, disk2)
    if dist < disk1.radius + disk2.radius:
        # Avoid division by zero by adding a small epsilon
        dist = max(dist, EPSILON)

        # --- Simple elastic collision for equal masses ---
        nx = (disk2.x - disk1.x) / dist
        ny = (disk2.y - disk1.y) / dist
        v1n = disk1.vx * nx + disk1.vy * ny
        v2n = disk2.vx * nx + disk2.vy * ny

        disk1.vx += (v2n - v1n) * nx
        disk1.vy += (v2n - v1n) * ny
        disk2.vx += (v1n - v2n) * nx
        disk2.vy += (v1n - v2n) * ny

        # --- Coin exchange ---
        # Calculate coins moving from disk1 to disk2
        coins_moving_to_disk2 = 0
        for _ in range(disk1.coin_count):
            if random.random() < 0.5:
                coins_moving_to_disk2 += 1

        # Calculate coins moving from disk2 to disk1
        coins_moving_to_disk1 = 0
        for _ in range(disk2.coin_count):
            if random.random() < 0.5:
                coins_moving_to_disk1 += 1

        # Apply the changes simultaneously
        disk1.coin_count = disk1.coin_count - coins_moving_to_disk2 + coins_moving_to_disk1
        disk2.coin_count = disk2.coin_count - coins_moving_to_disk1 + coins_moving_to_disk2

        # Clamp coin counts
        disk1.coin_count = min(disk1.coin_count, MAX_COINS_PER_DISK)
        disk2.coin_count = min(disk2.coin_count, MAX_COINS_PER_DISK)

        return True
    return False


def update_plot(disks, lines, xdata, ydata, ax):
    """
    Recompute how many disks have 0..8 coins, update the
    global cumulative sums, update the lines, and redraw.
    """
    global collision_count, cumulative_counts

    # Count how many disks are in each coin state
    counts = [0] * (MAX_COINS_PER_DISK + 1)
    for d in disks:
        counts[d.coin_count] += 1

    # Update global cumulative sums
    for i in range(len(counts)):
        cumulative_counts[i] += counts[i]

    # Update the running average number of disks for each coin count
    for i in range(len(counts)):
        xdata[i].append(collision_count)
        avg = cumulative_counts[i] / collision_count
        ydata[i].append(avg)
        lines[i].set_xdata(xdata[i])
        lines[i].set_ydata(ydata[i])

    # Dynamically adjust the plot range
    ax.set_xlim(0, max(10, collision_count))
    ax.set_ylim(0, DISK_COUNT)  # Y-axis now goes from 0 to DISK_COUNT
    ax.relim()
    ax.autoscale_view(False, True, True)

    # Print y-values every N collisions
    if collision_count % N == 0:
        print(f"\nCollision # {collision_count}")
        for i in range(len(counts)):
            print(f"{i} coins: {ydata[i][-1]:.2f}")

    plt.draw()
    plt.pause(0.001)


def main():
    global collision_count  # we will assign to it here

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Disks with Coin Exchange")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont(None, 24)

    # Initialize disks with one disk having all coins and others having 0
    coin_distribution = [MAX_COINS_PER_DISK] + [0] * (DISK_COUNT - 1)
    disks = []
    for i in range(DISK_COUNT):
        x = random.randint(DISK_RADIUS, WIDTH - DISK_RADIUS)
        y = random.randint(DISK_RADIUS, HEIGHT - DISK_RADIUS)
        vx = random.uniform(-400, 400) * SPEED_FACTOR
        vy = random.uniform(-400, 400) * SPEED_FACTOR
        disk = Disk(x, y, vx, vy, DISK_RADIUS, coin_count=coin_distribution[i])
        disks.append(disk)

    # --- Matplotlib Setup for dynamic plotting ---
    plt.ion()
    fig, ax = plt.subplots()
    fig.canvas.manager.set_window_title("Running Average of Coin Counts")

    # We'll keep lines for coin counts 0..MAX_COINS_PER_DISK
    lines = []
    xdata = [[] for _ in range(MAX_COINS_PER_DISK + 1)]
    ydata = [[] for _ in range(MAX_COINS_PER_DISK + 1)]
    colors = [
        "tab:blue", "tab:orange", "tab:green", "tab:red", "tab:purple",
        "tab:brown", "tab:pink", "tab:gray", "tab:olive"
    ]
    labels = [f"{i} coins" for i in range(MAX_COINS_PER_DISK + 1)]
    for i in range(MAX_COINS_PER_DISK + 1):
        (line,) = ax.plot([], [], color=colors[i], label=labels[i])
        lines.append(line)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, DISK_COUNT)  # Y-axis now goes from 0 to DISK_COUNT
    ax.legend(loc="upper right")
    ax.set_xlabel("Collision Count")
    ax.set_ylabel("Running Average Number of Disks")

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update all disks
        for disk in disks:
            disk.update_position(dt)

        # Collision detection among disks
        for i in range(DISK_COUNT):
            for j in range(i + 1, DISK_COUNT):
                did_collide = handle_disk_collision(disks[i], disks[j])
                if did_collide:
                    collision_count += 1
                    update_plot(disks, lines, xdata, ydata, ax)

        screen.fill((0, 0, 0))
        for disk in disks:
            disk.draw(screen, font)

        pygame.display.flip()

    pygame.quit()
    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()