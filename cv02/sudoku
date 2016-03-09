import sys
import os
sys.path[0:0] = [os.path.join(sys.path[0], '../examples/sat')]

import sat

class SudokuSolver():

    def solve(self,sudoku):
        def q(r,s,c):
            return 9*9 * r + 9 * s + c
        vstup = open("sudoku.txt","w")
        ######riadky
        for r in range(9):
            for s in range(9):
                if sudoku[r][s] == 0:
                    for c in range(1,10):
                        vstup.write('{} '.format(q(r,s,c)))
                else:
                    vstup.write('{} '.format(q(r,s,sudoku[r][s])))
                vstup.write('0\n')
                
        for r in range(9):
            for s in range(9):
                for c1 in range(1,10):
                    for c2 in range(1,10):
                        if (c1 != c2):
                            vstup.write('{} {} 0\n'.format(-q(r,s,c1),-q(r,s,c2)))
        for r in range(9):
            for s1 in range(9):
                for s2 in range(9):
                    for c in range(1,10):
                        if (s1 != s2):
                            vstup.write('{} {} 0\n'.format(-q(r,s1,c),-q(r,s2,c)))
        ######stlpce
        for r in range(9):
            for s in range(9):
                for c in range(1,10):
                    vstup.write('{} '.format(q(r,s,c)))
                vstup.write('0\n')
        for r in range(9):
            for s in range(9):
                for c1 in range(1,10):
                    for c2 in range(1,10):
                        if c1 != c2:
                            vstup.write('{} {} 0\n'.format(-q(r,s,c1),-q(r,s,c2)))
        for r in range(9):
            for s1 in range(9):
                for s2 in range(9):
                    for c in range(1,10):
                        if (s1 != s2):
                            vstup.write('{} {} 0\n'.format(-q(s1,r,c),-q(s2,r,c)))
        #### 3*3
        for r1 in range(9):
            for r2 in range(9):
                for s1 in range(9):
                    for s2 in range(9):
                        for c in range(1,10):
                            if (r1//3 == r2//3 and s1//3 == s2//3 and q(r1,s2,c) != q(r2,s1,c)):
                                vstup.write('{} {} 0\n'.format(-q(r1,s2,c),-q(r2,s1,c)))


                    
        vstup.close()
        solver = sat.SatSolver()
        splnene, riesenie = solver.solve("sudoku.txt","sudoku_out.txt")
##        print(splnene,riesenie)
        
        
        if not splnene:
            nuly = []
            for i in range(9):
                nuly.append([0]*9)
            return nuly
        else: #malo riesenie, dekodujem
            for x in riesenie:
                if x > 0:
                   r,s,cislo = (x-1)//81,(x-1)%81//9,x%9
                   cislo+=1
                   sudoku[r][s] = cislo
                    
            return sudoku

