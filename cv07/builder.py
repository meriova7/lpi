import tableau

class TableauBuilder(object):
    def build(self, signedFormulas):
        """ Vytvori a vrati uzavrete alebo uplne tablo pre zoznam oznacenych formul. """

        alphas = []
        betas = []
        branch = {}
        self.tabl = tableau.Tableau()
        lastNode = None
        closed = False
        for sf in signedFormulas:
            newNode = tableau.Node(sf)
            self.tabl.append(lastNode, newNode)
            lastNode = newNode
            if self.processNode(newNode,alphas,betas,branch):
                closed = True
        if not closed:
            self.expand(lastNode, alphas, betas, branch)
            # TODO 
        return self.tabl

    def processNode(self, node, alphas, betas, branch):
        if node.sf.getType() == tableau.ALPHA:
            alphas.append(node)
        else:
            betas.append(node)
        s = node.sf.f.toString()
        if s not in branch:
            branch[s] = [node]
        else:
            branch[s].append(node)
        for otherNode in branch[s]:
            if otherNode.sf.sign != node.sf.sign:
                node.close(otherNode)
                return True
        return False
    
    def expand(self, node, alphas, betas, branch):
        while alphas != []:
            newAlphas = []
            for nd in alphas:
                for sf in nd.sf.subf():
                    newNode = tableau.Node(sf,nd)
                    self.tabl.append(node,newNode)
                    if self.processNode(newNode, newAlphas, betas, branch):
                        return
                    node = newNode
            alphas = newAlphas
# vim: set sw=4 ts=8 sts=4 et :

