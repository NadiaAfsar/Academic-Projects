# Graph Analyzer 

A Java console application for managing directed weighted graphs. Supports creation, addition, deletion, and editing of vertices and edges, with sorted output.

## 📖 Overview

This project provides a data structure for storing directed weighted graphs and a command-line interface to manipulate them. The implementation uses `HashMap` for storing vertices and edges, with manual sorting applied only when displaying the graph.

## ✨ Features

- Create empty graphs with unique 2-digit IDs.
- Add, delete, and edit vertices (unique 8-digit IDs, real weight).
- Add, delete, and edit directed edges (start/end vertices, real weight).
- Display graph information in sorted order (vertices by ID, edges by start then end).
- Gracefully handles invalid commands by printing `INVALID COMMAND`.
- Uses `HashMap` for average O(1) insertion, deletion, and lookup.

## 🕹️ Supported Commands

| Command | Description |
|---------|-------------|
| `NEW_GRAPH [GRAPH_ID]` | Creates a new empty graph. |
| `ADD_VERTEX [GRAPH_ID] [VERTEX_ID] [WEIGHT]` | Adds a vertex with the given weight. |
| `ADD_EDGE [GRAPH_ID] [START] [END] [WEIGHT]` | Adds a directed edge from START to END. |
| `DEL_VERTEX [GRAPH_ID] [VERTEX_ID]` | Deletes a vertex and all its incident edges. |
| `DEL_EDGE [GRAPH_ID] [START] [END]` | Deletes the edge from START to END. |
| `EDIT_VERTEX [GRAPH_ID] [VERTEX_ID] [WEIGHT]` | Updates the weight of a vertex. |
| `EDIT_EDGE [GRAPH_ID] [START] [END] [WEIGHT]` | Updates the weight of an edge. |
| `SHOW_GRAPH [GRAPH_ID]` | Prints the graph in a specific format. |

## 📥 Input / Output Format

### Input
- The first line contains an integer `q` (1 ≤ q ≤ 10⁶), the number of commands.
- Each of the next `q` lines contains one command in the format described above.

### Output
- For `SHOW_GRAPH`, the output is:
  ```
     [GRAPH_ID] [N] [M]
     [GRAPH_ID] [VERTEX_ID] [WEIGHT] // N lines, sorted by VERTEX_ID
     [GRAPH_ID] [START] [END] [WEIGHT] // M lines, sorted by START then END
- Weights are printed with exactly 6 decimal places.
- For any invalid command, the program prints `INVALID COMMAND`.

## 🧪 Example

**Input:**
```
11
NEW_GRAPH 10
ADD_VERTEX 10 10000000 0.5
ADD_VERTEX 10 10000001 0.5
ADD_VERTEX 10 10000002 0.5
ADD_VERTEX 10 10000003 0.8
ADD_VERTEX 10 10000004 2.7
ADD_EDGE 10 10000000 10000001 1.3
ADD_EDGE 10 10000003 10000002 5.8
EDIT_EDGE 10 10000000 10000001 1.2
DEL_VERTEX 10 10000003
SHOW_GRAPH 10
```
**Output:**
```
10 4 1
10 10000000 0.500000
10 10000001 0.500000
10 10000002 0.500000
10 10000004 2.700000
10 10000000 10000001 1.200000
```
