import KnowledgeBase
from collections import deque


class FOLEngine:
    def __init__(self, kb):
        self.kb = kb
        self.grounded_facts = []
        self.inference_path = []
        self.standardization_counter = {}

    def unify(self, x, y, substitution=None):
        if substitution is None:
            substitution = {}

        if substitution is False:
            return False
        elif x == y:
            return substitution
        # if x is a variable
        elif KnowledgeBase.is_variable(x):
            return self.unify_var(x, y, substitution)
        # if y is a variable
        elif KnowledgeBase.is_variable(y):
            return self.unify_var(y, x, substitution)
        elif isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)):
            if len(x) != len(y):
                return False
            for t1, t2 in zip(x, y):
                substitution = self.unify(t1, t2, substitution)
            return substitution
        else:
            return False

    def unify_var(self, var, x, substitution):
        if var in substitution:
            return self.unify(substitution[var], x, substitution)
        elif x in substitution:
            return self.unify(var, substitution[x], substitution)
        elif self.occur_check(var, x, substitution):
            return False
        else:
            substitution[var] = x
            return substitution

    def occur_check(self, var, x, substitution):
        if var == x:
            return True

        # if x is a variable
        elif isinstance(x, str) and x.islower():
            if x in substitution:
                return self.occur_check(var, substitution[x], substitution)
            else:
                return False

        elif isinstance(x, (list, tuple)):
            for sub in x:
                if self.occur_check(var, sub, substitution):
                    return True
            return False

        else:
            return False

    def standardize_variables(self, rule):
        all_vars = rule.extract_variables()

        substitution = {}
        for var in all_vars:
            # Update counter for this variable type
            if var not in self.standardization_counter:
                self.standardization_counter[var] = 0

            # Generate new unique variable name
            new_var = f"{var}_{self.standardization_counter[var]}"
            substitution[var] = new_var
            self.standardization_counter[var] += 1

        # Apply substitution to create fresh rule
        fresh_conditions = []
        for condition in rule.conditions:
            if condition[0] == "NOT":
                pred, args = condition[1]
                fresh_args = []
                for arg in args:
                    new_arg = substitution[arg]
                    fresh_args.append(new_arg)
                fresh_conditions.append(("NOT", (pred, fresh_args)))
            else:
                pred, args = condition
                fresh_args = []
                for arg in args:
                    new_arg = substitution[arg]
                    fresh_args.append(new_arg)
                fresh_conditions.append((pred, fresh_args))

        if rule.conclusion[0] == "NOT":
            pred, args = rule.conclusion[1]
            fresh_args = []
            for arg in args:
                new_arg = substitution[arg]
                fresh_args.append(new_arg)
            fresh_conclusion = ("NOT", (pred, fresh_args))
        else:
            pred, args = rule.conclusion
            fresh_args = []
            for arg in args:
                new_arg = substitution[arg]
                fresh_args.append(new_arg)
            fresh_conclusion = (pred, fresh_args)

        # Return fresh rule (as a tuple since it's temporary)
        return {
            'name': rule.name,
            'conditions': fresh_conditions,
            'conclusion': fresh_conclusion,
            'substitution': substitution
        }

    def find_matching_substitutions(self, rule, facts):
        substitutions = []
        conditions = rule["conditions"]
        queue = deque()
        queue.append(({}, 0))
        while len(queue) > 0:
            substitution, index = queue.pop()
            for fact in facts:
                new_subs = self.unify(conditions[index], fact, substitution.copy())
                if new_subs:
                    if index + 1 == len(conditions):
                        substitutions.append(new_subs)
                    else:
                        queue.append((new_subs, index + 1))
        return substitutions

    def subst(self, substitution, proposition, room):
        if proposition[0] == "NOT":
            pred, args = proposition[1]
        else:
            pred, args = proposition
        new_args = []
        for arg in args:
            try:
                new_arg = substitution[arg]
            except KeyError:
                new_arg = room
            new_args.append(new_arg)
        if proposition[0] == "NOT":
            return ("NOT", (pred, new_args))
        return (pred, new_args)

    def subst_rule(self, sub, rule, room):
        new_conditions = []
        for condition in rule["conditions"]:
            new_condition = self.subst(sub, condition, room)
            new_conditions.append(new_condition)
        new_conclusion = self.subst(sub, rule["conclusion"], room)
        return KnowledgeBase.Rule(rule["name"], new_conditions, new_conclusion)

    def FOL_FC_Ask(self, room):
        rules = self.kb.granting_rules
        while True:
            new = []
            for rule in rules:
                standardized_rule = self.standardize_variables(rule)
                matching_substitutions = self.find_matching_substitutions(standardized_rule, self.kb.facts)
                for sub in matching_substitutions:
                    q_prime = self.subst(sub, standardized_rule["conclusion"], room)
                    if not ((q_prime in new) or (q_prime in self.kb.facts)):
                        new.append(q_prime)
                        new_rule = self.subst_rule(sub, standardized_rule, room)
                        # -----------------------------------
                        print(f"New proposition generated: {new_rule}")
                        # -----------------------------------
            if len(new) == 0:
                return
            self.kb.facts += new



