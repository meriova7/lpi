import os
import sys
sys.path[0:0] = [os.path.join(sys.path[0], '../examples/sat')]
import sat


Dorothy = 0
Virginia = 1
George = 2
Howard = 3
mena = ['Dorothy','Virginia','George','Howard']
muzi = [George, Howard]
zeny = [Dorothy, Virginia]

def otec(x):
    return x+1
def matka(x):
    return 4+x+1
def syn(x):
    return 8+x+1
def dcera(x):
    return 12+x+1
def pb(x,y):
    return 16 + 4*x + y +1
def st(x,y):
    return 32 + 4*x + y +1
def ml(x,y):
    return 48 + 4*x + y +1

roly = ['otec','matka','syn','dcera']

with open('vstup.txt', 'w') as f:
    for o in zeny:
        f.write('{} 0 {} 0\n'.format(-otec(o), -syn(o)))

    for m in muzi:
        f.write('{} 0 {} 0\n'.format(-matka(m), -dcera(m)))
 
    for prem in [otec,syn]:
        for m in muzi:
            f.write('{} '.format(prem(m)))
        f.write('0 \n')
        for m in muzi:
            f.write('{} '.format(-prem(m)))
        f.write('0 \n')

    for m in muzi:
        f.write('{} {} 0\n'.format(-otec(m), -syn(m)))

    for prem in [matka,dcera]:
        for m in zeny:
            f.write('{} '.format(prem(m)))
        f.write('0 \n')
        for m in zeny:
            f.write('{} '.format(-prem(m)))
        f.write('0 \n')

    for z in zeny:
        f.write('{} {} 0\n'.format(-matka(z), -dcera(z)))

#t1: George a Dorothy su pokrv pribuzni
#t1 ->-(G_O ^ D_M)
#t1->(-G_O v -D_M)
#(-t1 v -G_O v -D_M)

#t2 Howard je starsi nez George
#t2->H_O ^ G_S
#-t2 v (H_O ^ G_S)
#-t2 v H_O
#-t2 v G_S

#t3 Virginia je mladsia nez Howard
#(t3->(V_M v V_D))
#(-t3 v V_M v V_D)

#t4 Virginia je starsia nez Dorothy
#(t4->(V_M ^ D_D))
#-t4 v (V_M ^ D_D)
#-t4 v V_M
#-t4 v D_D



    t1 = pb(George, Dorothy)
    t2 = st(Howard,George)
    t3 = ml(Virginia, Howard)
    t4 = st(Virginia, Dorothy)
    cleny = [Dorothy, Virginia, George, Howard]

    for i in range(len(cleny)):
        for j in range(i, len(cleny)):
            f.write('{} {} {} 0\n'.format(-pb(cleny[i], cleny[j]),-otec(cleny[i]), -matka(cleny[j])))
            f.write('{} {} 0\n'.format(pb(cleny[i], cleny[j]),otec(cleny[i])))
            f.write('{} {} 0\n'.format(pb(cleny[i], cleny[j]),matka(cleny[j])))
    for i in range(len(cleny)):
        for j in range(i, len(cleny)):
            f.write('{} {} 0\n'.format(-st(cleny[i], cleny[j]),otec(cleny[i])))
            f.write('{} {} 0\n'.format(-st(cleny[i], cleny[j]),syn(cleny[j])))
            f.write('{} {} {} 0\n'.format(st(cleny[i],cleny[j]),-matka(cleny[i]), -dcera(cleny[j])))
    for i in range(len(cleny)):
        for j in range(i, len(cleny)):
            f.write('{} {} {} 0\n'.format(-ml(cleny[i], cleny[j]),matka(cleny[i]),dcera(cleny[i])))
            f.write('{} {} {} 0\n'.format(-ml(cleny[i], cleny[j]),otec(cleny[j]), dcera(cleny[i])))
            f.write('{} {} {} 0\n'.format(ml(cleny[i], cleny[j]),-matka(cleny[i]),-otec(cleny[j])))
            f.write('{} {} 0\n'.format(ml(cleny[i], cleny[j]),-dcera(cleny[i])))

    tvrdenia = [t1,t2,t3,t4]

    for i in range(len(tvrdenia)):
        pomocne = tvrdenia[:]
        pomocne.pop(i)
        f.write('{} {} {} 0\n'.format(-pomocne[0],-pomocne[1],-pomocne[2]))
        f.write('{} {} {} 0\n'.format(pomocne[0],pomocne[1],pomocne[2]))
        
        
                
        
s, ries = sat.SatSolver().solve('vstup.txt','vystup.txt')

if not s:
    print('nema riesenie')
else:
    for i in ries:
        if i > 0 and i < 17:
            i -= 1
            print('{}: {}'.format(roly[i//4], mena[i%4]))
