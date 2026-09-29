# Hybrid Agent for Access Control using FOL and Propositional Logic 🤖🔐

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![AI](https://img.shields.io/badge/AI-FOL%20%26%20Propositional%20Logic-red.svg)]()
[![Knowledge Representation](https://img.shields.io/badge/Knowledge%20Representation-Hybrid%20Agent-green.svg)]()

> A Python implementation of a hybrid reasoning agent that combines **First-Order Logic (FOL)** and **Propositional Logic** to decide whether a person can access a specific room. The agent uses forward chaining with unification for FOL grounding, and resolution for propositional inference. It handles blocking rules (e.g., emergency, door closed, working hours) and granting rules (e.g., dean, professor, project member, supervision, secure lab) to produce a final access decision.

## 📖 Project Overview

This project was developed as the third homework for an Artificial Intelligence course. The goal is to design an intelligent agent that can reason about complex organizational rules and environmental conditions to grant or deny access to rooms. The agent uses a two-layer architecture:

1. **FOL Layer (Grounding):** Uses forward chaining and unification to convert general FOL rules into ground facts specific to the query.
2. **Propositional Layer (Decision):** Uses propositional resolution to check blocking rules and granting rules, and returns a final `True`/`False` decision.

The system also provides **explainability** by printing the inference path (which rules fired and how the conclusion was reached).

## ✨ Features

- **FOL Forward Chaining:** Implements unification, occurs check, and variable standardization.
- **Propositional Resolution:** Converts rules to CNF and applies resolution to derive the goal.
- **Blocking Rules:** Emergency, door closed, and working hours (time-based).
- **Granting Rules:** Dean, professor office, project membership, supervision, secure lab.
- **Contradiction Detection:** `add_fact` raises an error if a fact contradicts existing facts (e.g., both `Professor` and `Student` for the same person).
- **Input Validation:** Only predefined predicates and correct number of arguments are accepted.
- **Explainability:** Prints generated ground facts and the final reasoning steps.
- **Time Handling:** The blocking rule `NOT Time(start, end) -> NOT CanAccess` is implemented with a working-hour check.

## 🧠 Architecture

### 1. FOL Layer (`FOLEngine.py`)
- **Unification:** `unify`, `unify_var`, `occur_check`.
- **Standardization:** Renames variables in rules to avoid collisions.
- **Forward Chaining:** `FOL_FC_Ask` iteratively applies granting rules to derive new ground facts until no new facts can be generated.
- **Substitution:** Applies substitutions to conditions and conclusions.

### 2. Propositional Layer (`PropositionalEngine.py`)
- **CNF Conversion:** `convert_to_CNF`, `cnf_form`.
- **Resolution:** `PL_Resolution`, `PL_Resolve`.
- **Final Decision:** `final_decision` builds a combined rule from blocking and granting rules and applies resolution to determine if access is allowed.

### 3. Knowledge Base (`KnowledgeBase.py`)
- **Rules:** `Rule` class for conditions and conclusion.
- **Facts:** List of ground facts.
- **Default Rules:** Blocking and granting rules are initialized in `initialize_default_rules`.
- **Contradiction Check:** `add_fact` raises `ValueError` on contradictions.

### 4. Ontology (`Ontology.py`)
- **Predicates:** Valid predicates and their expected arguments.
- **Validation:** `Predicate.validate` and `Predicate.split_proposition`.
- **Negation:** `NOT` function for logical negation.

