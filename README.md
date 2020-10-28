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

## STP - Simple Temporal Problem

An STP is a TCSP in which all constraints specify a single interval.

We associate such a problem with a `distance graph` `(V, E_d)`, where `V`
consists of the same nodes as the constraint network, and each edge is
labelled by a weight `a_{ij}`, representing `X_j - X_i <= a_{ij}`.

## Input

The input to the solver program is given by `stdin`.
First line should contain the number of nodes (we will label them `0 <= i < n`)
and the number of edges.
For simplicity we assume `X_0 = 0`.

Each following line should be in the format `i j n (a_{i} b_{i})^n`.
In other words, the `i -> j`, followed by a number of intervals,
and then the intervals in order.

For an STP, simply say `n=1`.

## Problem Generator

`generate_problems.py` is a Python 3 script to generate random problems.

## Verify Witness

`verify_witness.py` is a program that takes in a TCSP and an assignment to
the variables, and verifies whether the assignment is a solution to the TCSP.

The input consists of the input as a TCSP, followed by an additonal line
consisting of `n` integers, specifying `X = (X_0, X_1, ..., X_n)`.
