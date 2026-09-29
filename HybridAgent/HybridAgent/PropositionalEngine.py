from KnowledgeBase import Rule
from Ontology import NOT


class PropositionalEngine:
    def __init__(self, facts, goal, blocking_rules, ground_rules):
        self.facts = facts
        self.goal = goal
        self.blocking_rules = blocking_rules
        self.ground_rules = ground_rules
        self.emergency = False
        self.door_open = False
        self.access = False
        self.time = False
        self.has_time = False

    def convert_to_CNF(self, rule):
        sentence = ("OR", [NOT(rule.conditions), rule.conclusion])
        cnf = self.cnf_form(sentence)
        if cnf[0] == "AND":
            return cnf[1]
        return cnf

    def cnf_form(self, proposition):
        if proposition[0] == "OR":
            or_clause = []
            clauses = []
            for clause in proposition[1]:
                new_clause = self.cnf_form(clause)
                if new_clause[0] != "AND":
                    or_clause += new_clause
                else:
                    clauses.append(new_clause)
            final = [or_clause]
            for clause in clauses:
                new = []
                for sentence in clause[1]:
                    for or_clause in final:
                        new_clause = or_clause + [sentence]
                        new.append(new_clause)
                final = new
            return ("AND", final)
        elif proposition[0] == "AND":
            final = []
            for clause in proposition[1]:
                sentences = self.cnf_form(clause)
                if sentences[0] == "AND":
                    final += sentences[1]
                else:
                    final += sentences
            return ("AND", final)
        return [proposition]

    def PL_Resolution(self, cnf):
        for clause in cnf:
            not_goal = NOT(self.goal)
            self.PL_Resolve(clause, not_goal)
            if len(clause) == 0:
                return True
            for fact in self.facts:
                self.PL_Resolve(clause[0], fact)
                if len(clause[0]) == 0:
                    return True
        return False

    def PL_Resolve(self, clause, fact):
        if fact[0] == "DoorOpen":
            self.door_open = True
        elif fact[0] == "Emergency":
            self.emergency = True
        elif fact in self.ground_rules:
            self.access = True
        if fact[0] == "Time":
            for sentence in clause:
                if sentence[0] == "NOT" and sentence[1][0] == "Time":
                    if sentence[1][1][0] <= int(fact[1][0]) <= sentence[1][1][1]:
                        self.time = True
                        clause.remove(sentence)
        else:
            not_fact = NOT(fact)
            if not_fact in clause:
                clause.remove(not_fact)

    def final_decision(self):
        new_ground = []
        for rule in self.ground_rules:
            new_ground.append((rule[0], self.goal[1]))
        clause = ("OR", new_ground)
        self.ground_rules = new_ground
        time = False
        for fact in self.facts:
            if fact[0] == "Time":
                time = True
                self.has_time = True
        new_blocking = []
        new_blocking.append((self.blocking_rules[0].conditions[0][0], [self.goal[1][1]]))
        new_blocking.append((self.blocking_rules[1].conditions[0][0], (self.blocking_rules[1].conditions[0][1][0], [self.goal[1][1]])))
        if time:
            new_blocking.append(self.blocking_rules[2].conditions[0])
        not_blocking_rules = []
        for rule in new_blocking:
            not_blocking_rules.append(NOT(rule))
        conditions = ("AND", not_blocking_rules + [clause])
        rule = Rule("Final", conditions, self.goal)
        cnf = self.convert_to_CNF(rule)
        return self.PL_Resolution(cnf)


