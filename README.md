# Asymmetrical Coin Exchange Algorithm (Original Implementation)

This document describes the original coin exchange algorithm used in the simulation. **The interaction is asymmetrical** because the order in which disks are processed affects the outcome of the energy exchange.

---

## Interaction Logic

### Key Steps:
1. **Disk1's coins are processed first**:  
   For each coin in Disk1, there is a 50% chance it will move to Disk2.  
   These transferred coins are immediately added to Disk2's count.  

2. **Disk2's coins are processed second**:  
   For each coin in Disk2 (including those just received from Disk1), there is a 50% chance it will move to Disk1.  

This creates an asymmetry: Disk2's coin transfers are influenced by the coins it received from Disk1 earlier in the same interaction.

---

## Code Snippet: Asymmetrical Implementation

```python
# --- Coin exchange (original asymmetrical version) ---
total_coins_disk1 = disk1.coin_count
total_coins_disk2 = disk2.coin_count

# For disk1's coins:
coins_moving_to_disk2 = 0
for _ in range(total_coins_disk1):
    if random.random() < 0.5:
        coins_moving_to_disk2 += 1
disk1.coin_count -= coins_moving_to_disk2
disk2.coin_count += coins_moving_to_disk2  # Disk2 updated FIRST

# For disk2's coins:
coins_moving_to_disk1 = 0
for _ in range(total_coins_disk2):
    if random.random() < 0.5:
        coins_moving_to_disk1 += 1
disk2.coin_count -= coins_moving_to_disk1
disk1.coin_count += coins_moving_to_disk1  # Disk1 updated SECOND
