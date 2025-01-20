# Uniform Probability Redistribution Algorithm

This document describes the **Uniform Probability Redistribution Algorithm** used in the simulation. Unlike the previous approaches, this algorithm ensures that all possible energy redistributions between two disks are equally likely during a collision. This approach eliminates any bias introduced by the order of processing and ensures that the system evolves toward the correct Boltzmann distribution.

---

## Interaction Logic

### Key Steps:
1. **Calculate Total Energy**:  
   - The total energy (coins) of the two disks is calculated as `total_coins = disk1.coin_count + disk2.coin_count`.

2. **Generate All Possible Redistributions**:  
   - All valid ways to redistribute the total energy between the two disks are generated.  
   - A redistribution is valid if neither disk exceeds the maximum allowed coins (`MAX_COINS_PER_DISK`).

3. **Randomly Select a Redistribution**:  
   - One of the possible redistributions is selected with **uniform probability**.

4. **Apply the Selected Redistribution**:  
   - The selected redistribution is applied to the two disks, updating their coin counts.

---

## Code Snippet: Uniform Probability Redistribution

```python
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

        # --- Uniform probability coin exchange ---
        total_coins = disk1.coin_count + disk2.coin_count

        # Generate all possible redistributions of coins between the two disks
        possible_redistributions = []
        for coins_in_disk1 in range(total_coins + 1):
            coins_in_disk2 = total_coins - coins_in_disk1
            if coins_in_disk1 <= MAX_COINS_PER_DISK and coins_in_disk2 <= MAX_COINS_PER_DISK:
                possible_redistributions.append((coins_in_disk1, coins_in_disk2))

        # Randomly select one of the possible redistributions
        selected_redistribution = random.choice(possible_redistributions)

        # Apply the selected redistribution
        disk1.coin_count, disk2.coin_count = selected_redistribution

        return True
    return False
