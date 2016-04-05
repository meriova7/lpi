import cnf,copy

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
#---
    def toCnf(self):
        return cnf.Cnf([cnf.Clause([cnf.Literal(self.name)])])

class Negation(Formula):
    def __init__(self, orig):
        Formula.__init__(self, [orig])
    def originalFormula(self):
        return self.subf()[0]
    def eval(self, i):
        return not self.originalFormula().eval(i)
    def toString(self):
        return "-%s" % (self.originalFormula().toString())
    def toCnf(self):
        if isinstance(self.originalFormula(), Variable):
            return cnf.Cnf([cnf.Clause([cnf.Literal.Not(self.originalFormula().name)])])
        #opravena cast
        
        else:
            disj = Disjunction([])
            for clauses in self.originalFormula().toCnf():
                literal = 0
                pom = True
                konj = Conjunction([])
                while pom:
                    if literal == len(clauses):
                        pom = False
                    elif clauses[literal].neg:
                        konj.m_subf.append(Variable(clauses[literal].name))
                        literal +=1
                    else:
                        konj.m_subf.append(Negation(Variable(clauses[literal].name)))
                        literal += 1

                disj.m_subf.append(konj)
        return disj.toCnf()
        
class Disjunction(Formula):
    def __init__(self, subs):
        Formula.__init__(self, subs)
    def eval(self, i):
        return any(f.eval(i) for f in self.subf())
    def toString(self):
        return '(' + '|'.join(f.toString() for f in self.subf()) + ')'

    def toCnf(self):
         c = cnf.Cnf()
         subCnfs = [x.toCnf() for x in self.subf()]
         def doProduct(i, cls):
            if i >= len(subCnfs):
                c.append(copy.deepcopy(cls))
                return
            for subCl in subCnfs[i]:
                cls.extend(subCl) #pridame z itej subCnf jtu klauzu
                doProduct(i+1, cls)#zavolame sa na dalsiu subCnf
                cls[-len(subCl):] = [] #odstranime prave pridane
         doProduct(0, cnf.Clause())
         return c

class Conjunction(Formula):
    def __init__(self, subs):
        Formula.__init__(self, subs)
    def eval(self, i):
        return all(f.eval(i) for f in self.subf())
    def toString(self):
        return '(' + '&'.join(f.toString() for f in self.subf()) + ')'

    def toCnf(self):
        c = cnf.Cnf()  #prazdna cnf
        for st in self.subf(): #prejdem podformuly
            sfcnf = st.toCnf() #skonvertujem na cnf
            c.extend(sfcnf) #pridam vsetky klauzi do vyslednej
        return c
    
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
    def toCnf(self):
        return Disjunction([Negation(self.leftSide()),self.rightSide()]).toCnf()

class Equivalence(BinaryFormula):
    def __init__(self, left, right):
        BinaryFormula.__init__(self, left, right, '<=>')
    def eval(self, i):
        return self.leftSide().eval(i) == self.rightSide().eval(i)

    def toCnf(self):
        return Conjunction([Implication(self.leftSide(), self.rightSide()),
                            Implication(self.rightSide(), self.leftSide())]).toCnf()

# vim: set sw=4 ts=4 sts=4 et :
