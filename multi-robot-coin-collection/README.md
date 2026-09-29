# Multi-Robot Coin Collection in a 3D Grid

A Java implementation of an algorithm to plan paths for multiple rectangular robots to collect the maximum number of coins in a 3D grid environment, respecting movement constraints and avoiding collisions.

## 📖 Problem Overview

This project is the second phase of an Algorithm Design course assignment. The goal is to guide a set of robots to collect as many coins as possible from a 3D grid (a rectangular box). Each robot is a rectangular prism with integer dimensions. The environment is a 3D grid where each cell (a unit cube) may contain a coin (1) or be empty (0).

**Rules:**
- All robots start at specified initial positions (determined by their order).
- In each time step, a robot can either:
  - Move to an adjacent cell (up, down, left, right, forward, backward) – one unit per move.
  - Move from the top surface of a layer to the bottom surface of the same layer? Actually the description says: "move from the top surface of the layer to the bottom surface of it" – but the code seems to just move in 3D with Manhattan distance.
- No rotation is allowed.
- Robots cannot collide (they cannot occupy the same cell at the same time).
- The goal is to maximize the total number of coins collected by all robots.

## 🧠 Algorithm

The solution uses **recursive backtracking with pruning** to explore all possible sequences of coin collection.

**Key components:**
- **State representation:**
  - `notCollected`: a linked list of coins not yet collected.
  - `robotsRemained`: a linked list of remaining movement points for each robot (initially a maximum value based on grid dimensions).
  - `lastCells`: a linked list of the current positions of the robots.
  - `index`: the index of the robot whose turn it is to move (round-robin).
- **Pruning:**
  - If the current collected count + number of remaining coins ≤ best found so far, prune.
  - Early exit if all coins are collected or if the theoretical maximum (max * robotsNum) is reached.
- **Movement and coin collection:**
  - For the current robot, try to move to any uncollected coin.
  - The distance (Manhattan) is subtracted from the robot's remaining movement points.
  - If the robot reaches the coin (distance ≤ remaining), the coin is collected, and the robot's position updates to the coin's position.
  - If the robot runs out of movement points after collecting, it is removed from the rotation.
  - Otherwise, the next robot's turn.
- **Backtracking:** All changes are undone after each recursive call to explore other possibilities.
- **Optimization:** Coins are sorted by their sum of coordinates (Manhattan distance from origin) to encourage collecting closer coins first.

The algorithm uses a custom doubly linked list (`MyLinkedList`) for efficient removals and additions during backtracking.

## 📥 Input Format
```
n x y z
c111 c112 ... c11x
c121 ...
...
(Total of z * y * x integers, each 0 or 1)
```

- **n**: number of robots.
- **x, y, z**: dimensions of the 3D grid (length, width, height).
- Then the grid is given layer by layer (z layers), each layer as y rows of x integers. `1` means a coin is present, `0` means empty.

**Note:** The code uses 1-based indexing for coordinates.

## 📤 Output Format

- A single integer: the maximum number of coins that can be collected by all robots.

