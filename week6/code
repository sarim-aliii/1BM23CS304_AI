from itertools import product

# ----------------- Propositional Logic Symbols -----------------
class Symbol:
    def __init__(self, name):
        self.name = name

    def __invert__(self):  # ~P
        return Not(self)

    def __and__(self, other):  # P & Q
        return And(self, other)

    def __or__(self, other):  # P | Q
        return Or(self, other)

    def __rshift__(self, other):  # P >> Q (implication)
        return Or(Not(self), other)

    def __eq__(self, other):  # P == Q (biconditional)
        return And(Or(Not(self), other), Or(Not(other), self))

    def eval(self, model):
        return model[self.name]

    def symbols(self):
        return {self.name}

    def __repr__(self):
        return self.name


class Not:
    def __init__(self, operand):
        self.operand = operand

    def eval(self, model):
        return not self.operand.eval(model)

    def symbols(self):
        return self.operand.symbols()

    def __repr__(self):
        return f"~{self.operand}"


class And:
    def __init__(self, left, right):
        self.left, self.right = left, right

    def eval(self, model):
        return self.left.eval(model) and self.right.eval(model)

    def symbols(self):
        return self.left.symbols() | self.right.symbols()

    def __repr__(self):
        return f"({self.left} & {self.right})"


class Or:
    def __init__(self, left, right):
        self.left, self.right = left, right

    def eval(self, model):
        return self.left.eval(model) or self.right.eval(model)

    def symbols(self):
        return self.left.symbols() | self.right.symbols()

    def __repr__(self):
        return f"({self.left} | {self.right})"


# ----------------- Truth Table Entailment -----------------
def tt_entails(kb, alpha, show_table=False):
    symbols = sorted(list(kb.symbols() | alpha.symbols()))
    if show_table:
        print_truth_table(kb, alpha, symbols)
    return tt_check_all(kb, alpha, symbols, {})


def tt_check_all(kb, alpha, symbols, model):
    if not symbols:  # all symbols assigned
        if kb.eval(model):  # KB is true
            return alpha.eval(model)
        else:
            return True  # if KB is false, entailment holds
    else:
        P, rest = symbols[0], symbols[1:]

        model_true = model.copy()
        model_true[P] = True
        result_true = tt_check_all(kb, alpha, rest, model_true)

        model_false = model.copy()
        model_false[P] = False
        result_false = tt_check_all(kb, alpha, rest, model_false)

        return result_true and result_false


# ----------------- Truth Table Printer -----------------
def print_truth_table(kb, alpha, symbols):
    header = symbols + ["KB", "Query"]
    print(" | ".join(f"{h:^5}" for h in header))
    print("-" * (7 * len(header)))

    for values in product([False, True], repeat=len(symbols)):
        model = dict(zip(symbols, values))
        kb_val = kb.eval(model)
        alpha_val = alpha.eval(model)
        row = [str(model[s]) for s in symbols] + [str(kb_val), str(alpha_val)]
        print(" | ".join(f"{r:^5}" for r in row))
    print()


# ----------------- Example -----------------
P = Symbol("P")
Q = Symbol("Q")

# KB: P → Q
kb = P | Q & P
# Query: Q
alpha = Q | P

print("Knowledge Base:", kb)
print("Query:", alpha)
print()
result = tt_entails(kb, alpha, show_table=True)
print("Does KB entail Query?", result)
