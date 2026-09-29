from FOLEngine import FOLEngine
from Ontology import Predicate
from KnowledgeBase import KnowledgeBase
from PropositionalEngine import PropositionalEngine


def main():
    kb = KnowledgeBase()
    facts_count = int(input("number of facts: "))
    for _ in range(facts_count):
        fact = input()
        pre, predicate, args = Predicate.split_proposition(fact)
        if Predicate.validate(predicate, args):
            kb.add_fact(pre, predicate, args)
    query = input()
    pre, predicate, args = Predicate.split_proposition(query)
    if Predicate.validate(predicate, args):
        query = (predicate, args)
    fol_engine = FOLEngine(kb)
    # add ground facts
    print("Phase 1: First-Order Logic Inference (FOL Grounding)")
    fol_engine.FOL_FC_Ask(query[1][1])
    print("------------------------------------------------------")
    print("Phase 2: Checking Constraints (Propositional Logic)")
    if not (("Emergency", [query[1][1]]) in kb.facts):
        kb.facts.append(("NOT", ("Emergency", [query[1][1]])))
    if not (("DoorOpen", [query[1][1]]) in kb.facts):
        kb.facts.append(("NOT", ("DoorOpen", [query[1][1]])))
    propositional_engine = PropositionalEngine(kb.facts, query, kb.blocking_rules, kb.ground_rules)
    # final decision
    decision = propositional_engine.final_decision()
    if propositional_engine.door_open:
        print("The door is open")
    else:
        print("The door is not open")
    if propositional_engine.emergency:
        print("The room is emergency")
    else:
        print("The room is not emergency")
    if propositional_engine.has_time:
        if propositional_engine.time:
            print("It is working hour")
        else:
            print("It isn't working hour")
    blocking_str = ""
    if propositional_engine.door_open and not propositional_engine.emergency and propositional_engine.time:
        blocking_str = "No blocking rule found, "
    else:
        blocking_str = "Blocking rule found, "
    access_str = ""
    if propositional_engine.access:
        access_str = "and at least one permission is active."
    else:
        access_str = "and no permission is active."
    print(f"Conclusion: {blocking_str}{access_str}")
    print(f"Final Result: {decision}")


main()