from typing import Union, List, Dict, Optional

# --- Term classes ---
class Term:
    def occurs(self, var: 'Variable') -> bool:
        raise NotImplementedError

    def substitute(self, subs: Dict['Variable', 'Term']) -> 'Term':
        raise NotImplementedError

class Variable(Term):
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Variable) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.name

    def occurs(self, var: 'Variable') -> bool:
        return self == var

    def substitute(self, subs: Dict['Variable', Term]) -> Term:
        return subs.get(self, self)

class Constant(Term):
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        return isinstance(other, Constant) and self.name == other.name

    def __repr__(self):
        return self.name

    def occurs(self, var: 'Variable') -> bool:
        return False

    def substitute(self, subs: Dict[Variable, Term]) -> Term:
        return self

class Function(Term):
    def __init__(self, name: str, args: List[Term]):
        self.name = name
        self.args = args

    def __eq__(self, other):
        return isinstance(other, Function) and self.name == other.name and self.args == other.args

    def __repr__(self):
        return f"{self.name}({', '.join(map(str, self.args))})"

    def occurs(self, var: 'Variable') -> bool:
        return any(arg.occurs(var) for arg in self.args)

    def substitute(self, subs: Dict[Variable, Term]) -> Term:
        return Function(self.name, [arg.substitute(subs) for arg in self.args])

# --- Unification ---
def unify(x: Term, y: Term, subs: Optional[Dict[Variable, Term]] = None) -> Optional[Dict[Variable, Term]]:
    if subs is None:
        subs = {}

    x = x.substitute(subs)
    y = y.substitute(subs)

    if x == y:
        return subs

    if isinstance(x, Variable):
        if x.occurs(y):
            return None  # Occurs check failed
        subs[x] = y
        return subs

    if isinstance(y, Variable):
        if y.occurs(x):
            return None
        subs[y] = x
        return subs

    if isinstance(x, Function) and isinstance(y, Function) and x.name == y.name and len(x.args) == len(y.args):
        for a, b in zip(x.args, y.args):
            subs = unify(a, b, subs)
            if subs is None:
                return None
        return subs

    return None  # Cannot unify

if __name__ == "__main__":
    # Variables
    x = Variable('x')
    y = Variable('y')

    # Constants
    John = Constant('John')

    # Functions
    knows = lambda *args: Function('knows', list(args))
    mother = lambda arg: Function('mother', [arg])

    term1 = knows(John, x)
    term2 = knows(y, mother(y))

    result = unify(term1, term2)
    
    print("1BM23CS304 : Sarim Ali")

    if result:
        print("Unifier:")
        for var, val in result.items():
            print(f"  {var} -> {val}")
    else:
        print("Cannot unify")
