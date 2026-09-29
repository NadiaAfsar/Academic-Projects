# Quoridor AI Agent 🤖

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![AI](https://img.shields.io/badge/AI-Minimax%20%26%20Alpha--Beta-red.svg)]()
[![Game](https://img.shields.io/badge/Game-Quoridor-green.svg)]()

> A Python implementation of the board game **Quoridor** with an AI agent that uses **Minimax** and **Alpha-Beta pruning**. The project was developed as the second homework for an Artificial Intelligence course.

## 📖 Overview

Quoridor is a two-player abstract strategy game played on a 9×9 board. Each player has a pawn and 10 walls. The goal is to reach the opposite side of the board. On each turn, a player can either move their pawn one square (orthogonally) or place a wall to block the opponent. Walls cannot completely block all paths to the goal.

This project implements:
- A complete game engine with legal move generation, wall placement, and win detection.
- A human-vs-human mode.
- An AI agent that uses **Minimax** with **Alpha-Beta pruning** to choose the best move.
- A heuristic evaluation function based on shortest path distances and wall count.

## ✨ Features

- **Full Quoridor rules:** orthogonal moves, jump moves over the opponent, diagonal moves when blocked, and wall placement.
- **Wall validation:** walls cannot overlap, cross, or completely block a player's path.
- **AI Agent:** uses Alpha-Beta search with a configurable depth (default depth = 2).
- **Heuristic:** combines shortest path distance to goal for both players, center control, and remaining walls.
- **CLI Interface:** clear text-based board display with colored players and walls.
- **Statistics:** the AI reports the number of nodes visited and pruned during search.

## 🧠 AI Implementation

### Minimax and Alpha-Beta
- The AI uses **Minimax** with **Alpha-Beta pruning** to search the game tree.
- The search depth is configurable (currently set to 2 in `Alpha_Beta` function).
- The algorithm explores all legal actions: moves and wall placements.
- Alpha-Beta pruning significantly reduces the number of nodes evaluated.

### Heuristic Function
The heuristic evaluates a state from the perspective of the maximizing player:
