# Symmetrical Interaction

## Interaction Logic

### Key Steps:
1. **Calculate all coin movements first**:  
   - Determine how many coins will move from Disk1 to Disk2.  
   - Determine how many coins will move from Disk2 to Disk1.  

2. **Apply the changes simultaneously**:  
   - Update the coin counts for both disks at the same time.  

This ensures that the exchange is fair and independent of the order in which disks are processed.

---

## Code Snippet: Symmetrical Implementation

```python
# --- Coin exchange (updated symmetrical version) ---
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
