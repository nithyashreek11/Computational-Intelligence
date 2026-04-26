import random

class WumpusWorld:
    def __init__(self, size, total_points):
        self.size = size
        self.total_points = total_points
        self.grid = [["" for _ in range(size)] for _ in range(size)]
        self.agent_pos = [0, 0]
        self.score = total_points
        self.wumpus_alive = True
        self.arrow = 1
        self.initialize_world()

    # -----------------------------
    # Initialize World
    # -----------------------------
    def initialize_world(self):
        cells = [(i, j) for i in range(self.size) for j in range(self.size)]
        cells.remove((0, 0))  # Remove start

        # Place Wumpus
        self.wumpus = random.choice(cells)
        cells.remove(self.wumpus)

        # Place Gold
        self.gold = random.choice(cells)
        cells.remove(self.gold)

        # Place Pits (20%)
        pit_count = int(0.2 * self.size * self.size)
        self.pits = random.sample(cells, pit_count)

    # -----------------------------
    # Display Grid (only if size <=5)
    # -----------------------------
    def display_world(self):
        if self.size <= 5:
            print("\nWorld State:")
            cell_number = 1
            for i in range(self.size):
                for j in range(self.size):
                    content = ""
                    if [i, j] == self.agent_pos:
                        content = "A"
                    elif (i, j) == self.wumpus and self.wumpus_alive:
                        content = "W"
                    elif (i, j) == self.gold:
                        content = "G"
                    elif (i, j) in self.pits:
                        content = "P"
                    else:
                        content = str(cell_number)

                    print(f"{content:3}", end=" ")
                    cell_number += 1
                print()
        print("Score:", self.score)

    # -----------------------------
    # Sensors
    # -----------------------------
    def get_sensors(self):
        x, y = self.agent_pos
        sensors = []

        # Glitter
        if (x, y) == self.gold:
            sensors.append("Glitter")

        # Adjacent cells
        adjacent = self.get_adjacent(x, y)

        # Stench
        if self.wumpus_alive and self.wumpus in adjacent:
            sensors.append("Stench")

        # Breeze
        for pit in self.pits:
            if pit in adjacent:
                sensors.append("Breeze")
                break

        return sensors

    def get_adjacent(self, x, y):
        adj = []
        if x > 0: adj.append((x-1, y))
        if x < self.size-1: adj.append((x+1, y))
        if y > 0: adj.append((x, y-1))
        if y < self.size-1: adj.append((x, y+1))
        return adj

    # -----------------------------
    # Actions
    # -----------------------------
    def move(self, direction):
        x, y = self.agent_pos
        self.score -= 1

        if direction == "up" and x > 0:
            self.agent_pos[0] -= 1
        elif direction == "down" and x < self.size-1:
            self.agent_pos[0] += 1
        elif direction == "left" and y > 0:
            self.agent_pos[1] -= 1
        elif direction == "right" and y < self.size-1:
            self.agent_pos[1] += 1
        else:
            print("Bump!")
            return "Bump"

        return "Moved"

    def grab(self):
        if tuple(self.agent_pos) == self.gold:
            print("Gold grabbed! You win!")
            self.score += 100
            return "Win"
        else:
            print("No gold here.")
            return "No"

    def shoot(self):
        if self.arrow == 0:
            print("No arrows left!")
            return

        self.score -= 10
        self.arrow -= 1

        if self.wumpus_alive and self.wumpus in self.get_adjacent(*self.agent_pos):
            self.wumpus_alive = False
            print("Scream! Wumpus killed!")
        else:
            print("Missed!")

    # -----------------------------
    # Check Death
    # -----------------------------
    def check_status(self):
        pos = tuple(self.agent_pos)

        if pos in self.pits:
            print("Fell into a pit! Game Over.")
            return "Dead"

        if pos == self.wumpus and self.wumpus_alive:
            print("Wumpus ate you! Game Over.")
            return "Dead"

        if self.score < 0:
            print("Score below zero. You died.")
            return "Dead"

        return "Alive"


# ==============================
# MAIN PROGRAM
# ==============================

size = int(input("Enter grid size (4/5/6): "))
total_points = int(input("Enter total points: "))
actions_limit = int(input("Enter number of actions allowed: "))

world = WumpusWorld(size, total_points)

for step in range(actions_limit):
    world.display_world()
    sensors = world.get_sensors()
    print("Sensors:", sensors)

    action = input("Enter action (up/down/left/right/grab/shoot/no): ")

    if action in ["up", "down", "left", "right"]:
        world.move(action)
    elif action == "grab":
        result = world.grab()
        if result == "Win":
            break
    elif action == "shoot":
        world.shoot()
    elif action == "no":
        print("No action taken.")

    status = world.check_status()
    if status == "Dead":
        break

print("Final Score:", world.score)
