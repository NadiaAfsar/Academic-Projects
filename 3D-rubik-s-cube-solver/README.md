# 3D Rubik's Cube Solver using Search Algorithms

A Python implementation of various uninformed and informed search algorithms to solve a 3D Rubik's cube of arbitrary dimensions (x × y × z). This project was developed as the first homework for an Artificial Intelligence course.

## 📖 Overview

The goal is to find a sequence of moves that transforms a randomly scrambled cube into a solved state, where each face has a uniform color. The cube is represented as a flat string of color characters, and moves rotate a slice (layer) of the cube.

The project implements several classic AI search algorithms, both blind and heuristic, and compares their performance in terms of **nodes expanded** and **execution time**.

## ✨ Implemented Algorithms

### Uninformed (Blind) Search
- **Breadth-First Search (BFS)**
- **Depth-First Search (DFS)**
- **Uniform Cost Search (UCS)**
- **Depth-Limited Search (DLS)**
- **Iterative Deepening Search (IDS)**

### Informed (Heuristic) Search
- **Greedy Best-First Search (GBFS)**
- **A\*** 
- **Weighted A\*** (with adjustable weight)
- **Iterative Deepening A\* (IDA\*)**
- **Recursive Best-First Search (RBFS)**

## 🧠 Heuristic Function

The heuristic `get_heuristic` estimates the number of misplaced stickers. It counts how many colored stickers are not on their correct face. The heuristic is **admissible** (never overestimates the true cost) and **consistent** (monotonic), making it suitable for A* and its variants.

The heuristic is updated incrementally during moves (`heuristic_move`) to avoid recomputing from scratch.

## 📂 Project Structure

- `3D-rubik's-cube-solver.py` – Main source file containing all classes and algorithms.
  - `Cuby`: Represents a single small cube (cubie) with its coordinates and face colors.
  - `Cube`: Manages the overall cube state, dimensions, movable slices, and expected solved state.
  - `State`, `StateWithDepth`, `HeuristicState`, `AStarState`, `RBFSState`: Wrapper classes for search nodes.
  - Search functions: `BFS`, `DFS`, `UCS`, `DLS`, `IDS`, `GBFS`, `WAStar`, `AStar`, `IDAStar`, `RBFS`.
  - Helper functions: `move`, `heuristic_move`, `generate_random`, `get_position`, `get_heuristic`, `print_state`, `print_moves`.
