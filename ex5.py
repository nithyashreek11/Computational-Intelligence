# ex5.py
# Simple Wumpus World

rooms = {
    1: [2, 3],
    2: [1, 4],
    3: [1, 4],
    4: [2, 3]
}

wumpus = 4
player = 1

print("Player starts in Room", player)

for room in rooms[player]:
    if room == wumpus:
        print("Stench detected! Wumpus nearby.")

move = int(input("Enter next room: "))

if move == wumpus:
    print("Game Over! Wumpus ate you.")
else:
    print("Safe Room.")
