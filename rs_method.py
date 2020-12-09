# Enter the input in variables as either a,b,c,d,p,q,r,s
# For 'not' operation use symbol '~' in the propositional expression
# For 'and' operation use symbol '&' in the propositional expression
# For 'or' operation use symbol '|' in the propositional expression
# For '->' operation use symbol '>>' in the propositional expression
# For '<->' operation use symbol '<<' in the propositional expression
# Example Propositional Expression: (((~a | (b >> p)) & (a | b)) >> b)

# This is an important class where the primary evaluation of the expression to be a tautology or not is done
# It also initializes the various classes which are required for the evaluation of the expression
class Expression:
    def __invert__(self):
        return Negation(self)

    def __and__(self, other):
        return Conjunction(self, other)

    def __or__(self, other):
        return Disjunction(self, other)

    def __rshift__(self, other):
        return Implication(self, other)

    def __lshift__(self, other):
        return Iff(self, other)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.eq(other)

    # This evaluation function iteratively breaks the expression into two parts
    # until only operands are left and no operators are exit in the lhs and rhs
    # And continuously searches if the condition for tautology is met
    def evaluation_function(self, lhs, rhs):
        while True:
            found = True
            for exp in lhs:
                if exp in rhs:                  # check for exit condition if the exp or operand in lhs is also present in rhs
                    return None
                x = isinstance(exp, Operand)    # check for operator presence
                if not x:
                    lhs.remove(exp)
                    tup = exp._t_lhs(lhs, rhs)  # construct new lhs and rhs
                    if len(tup) > 1:
                        v = self.evaluation_function(*tup[1])
                        if v is not None:
                            return v
                    lhs, rhs = tup[0]           # assign new lhs and rhs
                    found = False
                    break
            for exp in rhs:
                if exp in lhs:                  # check for exit condition if the exp or operand in rhs is also present in lhs
                    return None
                x = isinstance(exp, Operand)    # check for operator presence
                if not x:
                    rhs.remove(exp)
                    tup = exp._t_rhs(lhs, rhs)  # construct new lhs and rhs
                    if len(tup) > 1:
                        v = self.evaluation_function(*tup[1])
                        if v is not None:
                            return v
                    lhs, rhs = tup[0]           # assign new lhs and rhs
                    found = False
                    break
            if found:
                return "expression is not tautology"    # exit condition if no tautology condition satisfied

    def _evaluation_function(self):
        return self.evaluation_function([], [self])


# The class and the functions in the class are made to form a binary expression
# i.e. expression containing two operands and one operator
# for the different operation such as conjunction, disjunction, implication, if and only if
# and also initializing the lhs and rhs children.
class Bin_Op(Expression):
    def __init__(self, lhs_child, rhs_child):
        self.lhs_child = lhs_child
        self.rhs_child = rhs_child

    def __str__(self):
        return '(' + str(self.lhs_child) + ' ' + self.op + ' ' + str(self.rhs_child) + ')'

    def eq(self, other):
        return self.lhs_child == other.lhs_child and self.rhs_child == other.rhs_child

# This class and the function are responsible for breaking
# the expression into two parts whenever a conjunction occurs in the expression
# and assigning it to the respective branch left or right depending on the side it was found on.
class Conjunction(Bin_Op):
    op = '^'

    def _t_lhs(self, lhs, rhs):
        print("Conjunction of {} and {}".format(self.lhs_child, self.rhs_child))
        return (lhs + [self.lhs_child, self.rhs_child], rhs),

    def _t_rhs(self, lhs, rhs):
        print("Conjunction of {} and {}".format(self.lhs_child, self.rhs_child))
        return (lhs, rhs + [self.lhs_child]), (lhs, rhs + [self.rhs_child])

# This class and the function are responsible for breaking
# the expression into two parts whenever a implication occurs in the expression
# and assigning it to the respective branch left or right depending on the side it was found on.
class Implication(Bin_Op):
    op = '->'

    def _t_lhs(self, lhs, rhs):
        print("Implication of {} and {}".format(self.lhs_child, self.rhs_child))
        return (lhs + [self.rhs_child], rhs), (lhs, rhs + [self.lhs_child])

    def _t_rhs(self, lhs, rhs):
        print("Implication of {} and {}".format(self.lhs_child, self.rhs_child))
        return (lhs + [self.lhs_child], rhs + [self.rhs_child]),

# This class and the function are responsible for breaking
# the expression into two parts whenever a IFF occurs in the expression
# and assigning it to the respective branch left or right depending on the side it was found on.
class Iff(Bin_Op):
    op = '<->'

    def _t_lhs(self, lhs, rhs):
        print("Iff of {} and {}".format(self.lhs_child, self.rhs_child))
        return (lhs + [self.lhs_child, self.rhs_child], rhs), (lhs, rhs + [self.lhs_child, self.rhs_child])

    def _t_rhs(self, lhs, rhs):
        print("Iff of {} and {}".format(self.lhs_child, self.rhs_child))
        return (lhs + [self.lhs_child], rhs + [self.rhs_child]), (lhs + [self.rhs_child], rhs + [self.lhs_child])

# This class and the function are responsible for removing
# the negation that occurs in the expression
# and assigning it to the respective branch left or right depending on the side it was found on.
class Negation(Expression):
    def __init__(self, child):
        self.child = child

    def __str__(self):
        return '~' + str(self.child)

    def eq(self, other):
        return self.child == other.child

    def _t_lhs(self, lhs, rhs):
        print("Negation of {}".format(self.child))
        return (lhs, rhs + [self.child]),

    def _t_rhs(self, lhs, rhs):
        print("Negation of {}".format(self.child))
        return (lhs + [self.child], rhs),

# This class and the function are responsible for breaking
# the expression into two parts whenever a disjunction occurs in the expression
# and assigning it to the respective branch left or right depending on the side it was found on.
class Disjunction(Bin_Op):
    op = 'V'

    def _t_lhs(self, lhs, rhs):
        print("Disjunction of {} and {}".format(self.lhs_child, self.rhs_child))
        return (lhs + [self.lhs_child], rhs), (lhs + [self.rhs_child], rhs)

    def _t_rhs(self, lhs, rhs):
        print("Disjunction of {} and {}".format(self.lhs_child, self.rhs_child))
        return (lhs, rhs + [self.lhs_child, self.rhs_child]),

# Class for Initializing and evaluating the variables used in the expression
class Operand(Expression):
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return str(self.name)

    __repr__ = __str__

    def eq(self, other):
        return self.name == other.name

# Intializing the variables that will be used in the expression
a = Operand('a')
b = Operand('b')
c = Operand('c')
d = Operand('d')
p = Operand('p')
q = Operand('q')
r = Operand('r')
s = Operand('s')

# The rs_method function that is used to call the tautology evaluation function
def rs_method(e):
    print("Formula: ", e)
    result = e._evaluation_function()
    if result == None:                             # If the result returned by the function is None then it is tautology
        print("\nThe Given Propositional Expression is a Tautology")
    else:                                          # If the result returned by the function is not None then it is NOT tautology
        print("\nThe Given Propositional Expression is NOT a Tautology")


# Below is the code to accept the input expression from the user
# it will prompt to enter the expression until the user provides
# an expression which is as per the guidelines
flag = True
while flag:
    print("Enter the input in variables as either a,b,c,d,p,q,r,s")
    print("For 'not' operation use symbol '~' in the propositional expression")
    print("For 'and' operation use symbol '&' in the propositional expression")
    print("For 'or' operation use symbol '|' in the propositional expression")
    print("For '->' operation use symbol '>>' in the propositional expression")
    print("For '<->' operation use symbol '<<' in the propositional expression")
    print("Example Propositional Expression: (((~a | (b >> p)) & (a | b)) >> b)")
    input_string = input("Please enter the input Propositional Expression as per above guidelines:")

    try:
        input_string = input_string.lower()
        e = eval(input_string)
        print(e)
        rs_method(e)
        flag = False
    except NameError:
        print("\nPlease enter a valid Propositional Expression!\n")
