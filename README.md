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

## Problem Generator

`problem_generator.py` is a Python 3 module to generate random problems.

## Verify Witness

`verifier.py` is a module that takes in a TCSP and an assignment to
the variables, and verifies whether the assignment is a solution to the TCSP.

## Preprocessing

`preprocessing.py` contains the implementation of some constraint propagation
preprocessing algorithms.

## Solver

`exact_solver.py` has a general TCSP solver implementation.

## Genetic

`genetic_direct.py` and `genetic_meta.py` contain random, walking, and genetic
algorithms for solving TCSP.
