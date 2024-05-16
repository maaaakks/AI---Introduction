from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave), # Either one or the other
    Not(And(AKnight, AKnave)), # Not both

    Implication(AKnave, Not(AKnight)), # If it's a Knave then A lie -> A Knight can't be a Knave
    Implication(AKnight, And(AKnight, AKnave)) # If it's an Knight A don't lie -> AKnight and AKnave
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    And(Or(AKnight, AKnave),Or(BKnight, BKnave)), # Both must be a Knave or a Knight
    Not(And(AKnave, BKnave)),  # Both cannot be Knaves
    Not(And(AKnight, BKnight)),  # Both cannot be Knights
    
    Implication(AKnave, Not(And(BKnave, AKnave))),  # If A is a Knave, then A lies
    Implication(AKnight, And(AKnave, BKnave))   # If A is a Knight (which is impossible), then A and B are both Knaves
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    And(Or(AKnight, AKnave),Or(BKnight, BKnave)), # Both must be a Knave or a Knight
    
    Implication(AKnight, BKnight),  # If A is a Knight then both are Knights
    Implication(AKnave, Not(BKnave)),  # If A is a Knave then B is not a Knave
    
    Implication(BKnight, AKnave), # If B is a Knight then A is a Knave
    Implication(BKnave, Not(AKnight)) # If B is a Knave then A is not a Knight
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.

# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    And(Or(AKnight, AKnave),Or(BKnight, BKnave), Or(CKnight, CKnave)), # A, B, C must be a Knave or a Knight
    
    Implication(BKnight, And( # If B is a Knight, A said "i am a knave"
        Implication(AKnight, AKnave), # paradoxe
        Implication(AKnave, Not(AKnave)), # paradoxe
        CKnave, # C is a knave
    )),
    
    Implication(BKnave, CKnight), # If B is a Knave C must be a Knight but we don't know about A (Maybe A said nothing)
    
    Implication(CKnight, AKnight), # If B is a Knight A must be a Knight
    Implication(CKnave, AKnave), # If C is a Knave A must be a Knave
)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
