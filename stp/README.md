# STP - Simple Temporal Problem

A STP is a TCSP in which all constraints specify a single interval.

In such a network, each edge `i -> j` is labeled by an interval `[ a_{ij} , b_{ij} ]`,
which represents the constraint `a_{ij} <= X_j - X_i <= b_{ij}`.

We associate a STP with a `distance graph` `(V, E_d)`, where `V` is the same as the nodes
in the constraint network, and each edge is labelled by a weight `a_{ij}`, representing
`X_j - X_i <= a_{ij}`.


## Input

The input to this program is given by `stdin`.
First line should contain the number of nodes (we will label them `0 <= i < n`).
For simplicity we assume `X_0 = 0`.

The second line should contain the number of edges.
Each following line should be in the format `i j a_{ij} b_{ij}`.
