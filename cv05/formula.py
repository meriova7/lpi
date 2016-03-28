import cnf

class Formula(object):
    def __init__(self, subs = []):
        self.m_subf = subs
    def subf(self):
        return self.m_subf
    def eval(self, i):
        return False
    def toString(self):
        return "INVALID"
    def __str__(self):
        return self.toString()
    def __repr__(self):
        return self.__class__.__name__ + '(' + ','.join([ repr(f) for f in self.subf()]) + ')'

    def toCnf(self):
        """ Vrati reprezentaciu formuly v CNF tvare. """
        # TODO
        return cnf.Cnf()

class Variable(Formula):
    def __init__(self, name):
        Formula.__init__(self)
        self.name = name
    def eval(self, i):
        return i[self.name]
    def toString(self):
        return self.name
    def __repr__(self):
        return "Variable(%r)" % (self.name,)

class Negation(Formula):
    def __init__(self, orig):
        Formula.__init__(self, [orig])
    def originalFormula(self):
        return self.subf()[0]
    def eval(self, i):
        return not self.originalFormula().eval(i)
    def toString(self):
        return "-%s" % (self.originalFormula().toString())

class Disjunction(Formula):
    def __init__(self, subs):
        Formula.__init__(self, subs)
    def eval(self, i):
        return any(f.eval(i) for f in self.subf())
    def toString(self):
        return '(' + '|'.join(f.toString() for f in self.subf()) + ')'

class Conjunction(Formula):
    def __init__(self, subs):
        Formula.__init__(self, subs)
    def eval(self, i):
        return all(f.eval(i) for f in self.subf())
    def toString(self):
        return '(' + '&'.join(f.toString() for f in self.subf()) + ')'

class BinaryFormula(Formula):
    def __init__(self, left, right, connective = ''):
        Formula.__init__(self, [left, right])
        self.connective = connective
    def leftSide(self):
        return self.subf()[0]
    def rightSide(self):
        return self.subf()[1]
    def toString(self):
        return '(%s%s%s)' % (self.leftSide().toString(), self.connective, self.rightSide().toString())

class Implication(BinaryFormula):
    def __init__(self, left, right):
        BinaryFormula.__init__(self, left, right, '=>')
    def eval(self, i):
        return (not self.leftSide().eval(i)) or self.rightSide().eval(i)

class Equivalence(BinaryFormula):
    def __init__(self, left, right):
        BinaryFormula.__init__(self, left, right, '<=>')
    def eval(self, i):
        return self.leftSide().eval(i) == self.rightSide().eval(i)

# vim: set sw=4 ts=4 sts=4 et :
