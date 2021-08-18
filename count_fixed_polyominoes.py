import argparse
import pprint

parser = argparse.ArgumentParser()
parser.add_argument("n", help="size of polyomino", type=int)
parser.add_argument("-p", "--verbose", action="store_true")
args = parser.parse_args()
n = args.n

def creategraph(n):
    thisdict = {}
    temp = n
    temp1 = (-n + 2)  
    for j in range(0, n):
        if (j == 0):
            for i in range(0, n):
                if (i==0):
                    thisdict[(i, j)] = [(i + 1, j),(i, j + 1)]    
                elif ((abs(i)+abs(j))==(n-1)):
                    thisdict[(i, j)] = [(i - 1, j)]
                else:
                    thisdict[(i, j)] = [(i - 1, j),(i + 1, j),(i, j + 1)]
            temp-=1
        elif (j == 1):
             for i in range((-n+2), temp):
                if ((abs(i)+abs(j)) == (n-1))and(i>=0):
                    thisdict[(i, j)] = [(i - 1, j), (i, j-1)]
                elif ((abs(i)+abs(j)) == (n-1))and(i<0):
                    thisdict[(i, j)] = [(i + 1, j)]
                elif (i<0):
                    thisdict[i, j] = [(i-1,j),(i+1,j),(i,j+1)]
                elif (i==0):
                    thisdict[(i, j)] = [(i-1,j),(i+1,j),(i,j-1),(i,j+1)]
                elif (i>0):
                    thisdict[i, j] = [(i-1,j),(i+1,j),(i,j+1),(i,j-1)]
             temp-=1
             temp1+=1
        elif (j == (n-1)):
            thisdict[(0,j)] = [0, (j-1)]
        else:
            for i in range (temp1, temp):
                if (((abs(i)+abs(j)) == (n-1))and(i>=0)):
                    thisdict[(i, j)] = [(i - 1, j),(i, j-1)]
                elif ((abs(i)+abs(j)) == (n-1))and(i<0):
                    thisdict[(i, j)] = [(i + 1, j),(i, j-1)]
                else:
                    thisdict[(i, j)] = [(i-1,j), (i+1, j),(i, j-1),(i, j+1)]
            temp-=1
            temp1+=1
    return thisdict

def isnotempty(untried):
    if untried:
        return True
    else:
        return False

def condition3(g,p,u,v):
    x = []
    for l in p:
        if (l != u):
            for f in g[l]:
                x.append(f)
    if v not in x:
        return True
    else:
        return False

def CountFixedPolyominoes(g,untried,n,p,c):
    while isnotempty(untried):
        u = untried.pop()
        p.append(u)
        if (len(p)==n):
            c+=1
        else:
            new_neighbors = set()
            for v in g[u]:
                if ((v not in untried)and(v not in p)and(condition3(g,p,u,v))): 
                    new_neighbors.add(v)
            new_untried = untried|new_neighbors
            c = CountFixedPolyominoes(g,new_untried,n,p,c)
        p.remove(u)
    return (c)

g = creategraph(n)
untried = {(0,0)}
p = []
c = 0
x = []

c= CountFixedPolyominoes(g,untried,n,p,c)

if args.verbose:
    pprint.pprint(g)
    print(c)
else:
    print(c)