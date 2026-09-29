from Ontology import NOT


def is_variable(term):
    if isinstance(term, str):
        return term.startswith("x_") or term.startswith("y_") or term.startswith("r_") or term.startswith("p_")
    return False


def is_variable2(term):
    if isinstance(term, str):
        return term == "x" or term == "y" or term == "r" or term == "p"
    return False


class Rule:
    def __init__(self, name, conditions, conclusion):
        self.name = name
        self.conditions = conditions
        self.conclusion = conclusion

    def __str__(self):
        s = ""
        for i in range(len(self.conditions)):
            condition = self.conditions[i]
            if condition[0] == "NOT":
                s += f"{condition[0]} ({condition[1][0]}{condition[1][1]})"
            else:
                s += f"{condition[0]}{condition[1]}"
            if i < len(self.conditions) - 1:
                s += " and "
        s += f" --> "
        if self.conclusion[0] == "NOT":
            s += f"{self.conclusion[0]} ({self.conclusion[1][0]}{self.conclusion[1][1]})"
        else:
            s += f"{self.conclusion[0]}{self.conclusion[1]}"
        return s

    def extract_variables(self):
        variables = []
        # arguments in conditions
        for condition in self.conditions:
            args = None
            if condition[0] == "NOT":
                args = condition[1][1]
            else:
                args = condition[1]
            for arg in args:
                if is_variable2(arg):
                    variables.append(arg)
        # arguments in conclusion
        args = None
        if self.conclusion[0] == "NOT":
            args = self.conclusion[1][1]
        else:
            args = self.conclusion[1]
        for arg in args:
            if is_variable2(arg):
                variables.append(arg)
        return variables


class KnowledgeBase:
    def __init__(self):
        self.ground_rules = []
        self.facts = []
        self.rules = []
        self.blocking_rules = []
        self.granting_rules = []
        self.initialize_default_rules()

    def initialize_default_rules(self):
        # Blocking Rules
        self.blocking_rules = [
            Rule("EmergencyRule",
                 [("Emergency", ["r"])],
                 ("NOT", ("CanAccess", ["x", "r"]))),
            Rule("DoorClosedRule",
                 [("NOT", ("DoorOpen", ["r"]))],
                 ("NOT", ("CanAccess", ["x", "r"]))),
            Rule("TimeRule",
                 [("NOT", ("Time", [9, 15]))],
                 ("NOT", ("CanAccess", ["x", "r"])))
        ]

        # Granting Rules
        self.granting_rules = [
            # managerial
            Rule("DeanRule",
                 [("Dean", ["x"])],
                 ("PossibleAccessViaDean", ["x", "r"])),
            Rule("OfficeRule",
                 [("Professor", ["x"]), ("Office", ["x", "r"])],
                 ("PossibleAccessViaOffice", ["x", "r"])),
            # projects and education
            Rule("ProjectRule",
                 [("Student", ["x"]), ("MemberOf", ["x", "p"]),
                  ("ProjectRoom", ["p", "r"]), ("HasID", ["x"])],
                 ("PossibleAccessViaProject", ["x", "r"])),
            Rule("SupervisionRule",
                 [("Student", ["x"]), ("Mentor", ["y", "x"]),
                  ("InRoom", ["y", "r"])],
                 ("PossibleAccessViaSupervision", ["x", "r"])),
            # security
            Rule("SecureLabRule",
                 [("HasID", ["x"]), ("IsSecureLab", ["r"]),
                  ("PassedSafetyCourse", ["x"])],
                 ("PossibleAccessViaSecureLab", ["x", "r"]))
        ]

        self.rules = self.blocking_rules + self.granting_rules
        for rule in self.granting_rules:
            self.ground_rules.append(rule.conclusion)

    def add_fact(self, pre, predicate, entities):
        if pre == "NOT":
            fact = ("NOT", (predicate, entities))
        else:
            fact = (predicate, entities)
        if (NOT(fact) in self.facts) or (predicate == "Professor" and ("Student", entities) in self.facts) or (predicate == "Student" and ("Professor", entities) in self.facts):
            raise ValueError("This fact causes contradiction")
        self.facts.append(fact)

