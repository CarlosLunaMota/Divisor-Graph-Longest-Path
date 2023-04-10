import time
import pulp

# Requires: sudo apt-get install coinor-cbc
#           sudo pip install pulp

"""
Divisor Graph Longest Path problem

Author:  Carlos Luna Mota
Version: 2023-04-05
License: The Unlicense
"""

# INPUT DATA ###################################################################

# Find the longest path on the divisor graph G = (V,A)
#
#   V = {1, 2, ..., N}
#   A = {(x,y) in VxV | x != y and max(x,y) % min(x,y) == 0}
#
N = 60

### MIXED INTEGER LINEAR PROGRAMMING MODEL #####################################

start = time.time() # Start timer

V = tuple(v for v in range(N+1))
A = tuple((x,y) for x in V for y in V
                if x != y and (min(x,y) == 0 or max(x,y) % min(x,y) == 0))
AA = list(str(a) for a in A)

# Create a binary variable for each arc:
X = pulp.LpVariable.dicts("arc", AA, lowBound=0, upBound=1, cat=pulp.LpInteger)

# Maximize the path length:
model  = pulp.LpProblem("Divisor_Graph_Longest_Path", pulp.LpMaximize)
model += pulp.lpSum([X[a] for a in AA])

# Conservation constraints: (Outdegree == Indegree)
for v in V:
    model += (pulp.lpSum([X[str(a)] for a in A if a[0]==v]) ==
              pulp.lpSum([X[str(a)] for a in A if a[1]==v]), f"Cons({v})")

# Outdegree of depot:
model += (pulp.lpSum([X[str(a)] for a in A if a[0]==0]) == 1.0, "Out(0)")

# Outdegree of the other nodes:
for v in V[1:]:
    model += (pulp.lpSum([X[str(a)] for a in A if a[0]==v]) <= 1.0, f"Out({v})")

# Subtours of length 2:
for (v,w) in A:
    if v < w:
        model += (X[str((v,w))] + X[str((w,v))] <= 1, f"Subtour([{v},{w}])")

# Iteartive generation of subtour elimination constraints:
UNSOLVED = True
while UNSOLVED:

    # Solve:
    model.solve(pulp.PULP_CBC_CMD(msg=0))
    UNSOLVED = False

    # Post-process solution:
    solution = [a for a in A if X[str(a)].value() == 1.0]
    path     = [0]
    while len(path) <= len(solution):
        v = path[-1]
        w = [j for (i,j) in solution if i==v][0]
        path.append(w)

        # If a subtour is found: generate a new cut and solve again 
        if w == 0 and len(path) <= len(solution):
            print(f"Adding Subtour({path[:-1]})")
            UNSOLVED = True
            model += (pulp.lpSum([X[str(a)] for a in A
                                 if a[0] in path and a[1] in path])
                                 <= len(path)-2, f"Subtour({path[:-1]})")
            break

end = time.time() # Stop timer

### OUTPUT #####################################################################

print(f"\nDivisor Graph Longest Path for [1, ..., {N}]")
print(f"Path of length {len(path)-2} found in {round(end-start,2)} seconds:")
print(path[1:-1])

################################################################################
