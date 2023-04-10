# Divisor Graph Longest Path

A Mixed Integer Linear Programming implementation of the Divisor Graph Longest Path problem.

Implemented using the PuLP Python library to call the COIN-OR CBC solver.

---

This arc-based model uses an artificial depot (node "0") and then looks for the longest tour that starts and ends in that node.

**Variables:**

$x_{ij} \in \{0,1\} \qquad \forall\quad i \neq j \quad\text{ s.t. }\quad i=0 \quad\text{ or }\quad j=0 \quad\text{ or }\quad i|j \quad\text{ or }\quad j|i$

**Constraints:**

$\sum_j x_{ij} \quad = \quad \sum_{j} x_{ji} \qquad \forall\quad i = 0..N \qquad\qquad$ (outdegree(i) = indegree(i))

$x_{ij} + x_{ji} \quad \leq \quad 1 \qquad \forall\quad i \neq j \qquad\qquad$ (subtours of size 2)

$\sum_j x_{ij} \quad \leq \quad 1 \qquad \forall\quad i = 1..N \qquad\qquad$ (outdegree(i) ≤ 1)

$\sum_j x_{0j} \quad = \quad 1 \qquad\qquad$  (outdegree(0) = 1)

The implementation also adds subtour elimination constraints for subtours of arbitrary size iteratively:

 * Solve the problem
 * If the solution has a subtour: add the corresponding subtour elimination constraint and start again
 * Otherwise: print the solution

--- ---

Inspired by this discussion: https://twitter.com/elprofefriki/status/1633138512491937792
