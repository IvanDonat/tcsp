# TCSP - Temporal Constraint Satisfaction Problem

TSCP is a constraint satisfaction problem in which variables represent time
points and temporal information is represented by a set of unary and binary
constraints.

We associate a TCSP with a graph, involving:
- a set of variables `X_1 to X_n`, having continuous domains
- a set of constraints, each of which is represented by a set of intervals

A unary constraint `T_i` restricts the domain of a variable `X_i` to a
given set of intervals.

A binary constraint `T_{ij}` constraints the values for the distance of
`X_j - X_i` to a set of intervals.

We represent this with a directed constraint graph, where nodes represent
variables and an edge `i -> j` specifies a constraint `T_{ij}`.

We also introduce `X_0 = 0` for simplicity, so unary constraints are
represented by `T_{0i}`.

## Input

The input to this program is given by `stdin`.
First line should contain the number of nodes (we will label them `0 <= i < n`).
For simplicity we assume `X_0 = 0`.

The second line should contain the number of edges.
Each following line should be in the format `i j N (a_{i} b_{i})^N`.
In other words, the `i -> j`, followed by a number of intervals,
and then the intervals in order.
