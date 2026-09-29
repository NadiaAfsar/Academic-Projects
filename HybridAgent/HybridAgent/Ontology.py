def NOT(proposition):
    if proposition[0] == "OR":
        new_pros = []
        for pro in proposition[1]:
            new_pros.append(NOT(pro))
        return ("AND", new_pros)
    elif proposition[0] == "AND":
        new_pros = []
        for pro in proposition[1]:
            new_pros.append(NOT(pro))
        return ("OR", new_pros)
    elif proposition[0] == "NOT":
        return proposition[1]
    return ("NOT", proposition)


class Predicate:
    PREDICATES = {
        'Student': ['person'],
        'Professor': ['person'],
        'Dean': ['person'],
        'HasID': ['person'],
        'PassedSafetyCourse': ['person'],
        'IsSecureLab': ['room'],
        'MemberOf': ['person', 'project'],
        'ProjectRoom': ['project', 'room'],
        'Mentor': ['professor', 'student'],
        'Office': ['professor', 'room'],
        'InRoom': ['person', 'room'],
        'DoorOpen': ['room'],
        'Emergency': ['room'],
        'CanAccess': ['person', 'room'],
        'Time': ['hour']
    }

    @staticmethod
    def validate(predicate_name, entities):
        if predicate_name not in Predicate.PREDICATES:
            raise ValueError(f"Predicate {predicate_name} not defined")

        expected_entities = len(Predicate.PREDICATES[predicate_name])
        if len(entities) != expected_entities:
            raise ValueError(f"Predicate {predicate_name} expects {expected_entities} arguments, got {len(entities)}")

        return True

    @staticmethod
    def split_proposition(proposition):
        pre = ""
        if proposition.startswith("NOT"):
            pre = "NOT"
            proposition = proposition.split("NOT ")[1]
        split1 = proposition.split('(')
        if len(split1) != 2:
            raise ValueError("Invalid Input")
        predicate = split1[0]
        split2 = split1[1].split(')')
        if len(split2) != 2:
            raise ValueError("Invalid Input")
        args = split2[0].split(',')
        for i in range(len(args)):
            args[i] = args[i].strip()
            if args[i] == "":
                raise ValueError("Invalid Input")
        return pre, predicate, args
