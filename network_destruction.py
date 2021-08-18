import argparse

parser = argparse.ArgumentParser()
parser.add_argument("num_nodes",type=int, help="number of nodes you want to delete")
parser.add_argument("input_file",type=str, help="name of input file")
parser.add_argument("-c", "--parametros", action="store_true")
parser.add_argument("-r", "--RADIUS",type = int, help="aktina")
args = parser.parse_args()

txt_choice = args.input_file
num_nodes = args.num_nodes
r = args.RADIUS


def creategraph(txt_choice):
    thisdict = {}
    with open(txt_choice) as f:
        for line in f:
            parts = line.split()
            thisdict.setdefault(int(parts[0]),[]).append(int(parts[1]))
            thisdict.setdefault(int(parts[1]),[]).append(int(parts[0]))
    return (thisdict)

def find_famous(thisdict):
    max = -1
    for i in thisdict:
        plithos = len(thisdict[i])
        if (plithos > max) or (plithos==max and i<removable):
            removable = i 
            max = plithos
    return removable
      

def vaccinate(node,thisdict):
    thisdict.pop(node)
    for j in thisdict:
        if node in thisdict[j]:
            thisdict[j].remove(node)


def famousness(thisdict,num_nodes):
    for i in range(0,num_nodes):
        diashmos = find_famous(thisdict)
        print (diashmos, len(thisdict[diashmos]))
        vaccinate(diashmos,thisdict)


def ball(graph,node,r,thita):
    counter = 0
    visited = []
    queue = []
    results = []
    queue.append(-1)
    visited.append(node)
    queue.append(node)
    while queue:
        s = queue.pop(0)
        if (s == -1):
            counter += 1
            if (counter > r):
                return results
            if len(queue)==0:
                return results
            queue.append(-1)
            s = queue.pop(0)
        for neighbor in graph[s]:
            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)
                if thita: 
                    if (counter == r):
                        results.append(neighbor)
                else:
                    if (counter <= r):
                        results.append(neighbor)
    return results

def collective_influence(graph,i,r):
    ci = 0
    for j in ball(graph,i,r,True):
        ci += (len(graph[j])-1)
    ci = (ci * (len(graph[i])-1))
    return ci

def find_ci_max(graph,r,sunolikesepirroes):
    sunoliki_epirroi = -1
    max_ci_node = -1
    for i in graph:
        c = sunolikesepirroes[i]
        if (c > sunoliki_epirroi) or (c==sunoliki_epirroi and i<max_ci_node) :
            sunoliki_epirroi = c
            max_ci_node = i
    return max_ci_node


def sumup(graph,r,num_nodes):
    sunolikesepirroes = {}
    for i in graph:
        sunolikesepirroes[i] = collective_influence(graph,i,r)
    for j in range (0,num_nodes):
        t = find_ci_max(graph,r,sunolikesepirroes)
        print(t,sunolikesepirroes[t])
        b = ball(graph, t, r + 1, False)
        vaccinate(t,graph)
        for i in b:
            sunolikesepirroes[i]= collective_influence(graph,i,r)

grafos=creategraph(txt_choice)


if args.parametros:
    famousness(grafos,num_nodes)
elif not args.parametros:
    sumup(grafos,r,num_nodes)
    



