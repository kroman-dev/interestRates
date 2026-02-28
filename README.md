# interestRates

## Multi-Curve Bootstrap with Automatic Differentiation
A Python implementation of the bootstrapping methodology described in
the seminal paper by F. M. Ametrano and M. Bianchetti (2013)[1].

## Overview
This repository partially reproduces the results from "Everything You Always
Wanted to Know About Multiple Interest Rate Curve Bootstrapping but Were
Afraid to Ask". The implementation approaches curve construction as a
numerical optimization problem.

## Key Features
- Optimization-based bootstrapping: Formulated as a nonlinear least squares problem
- Solvers: Implementation of Gauss-Newton and Levenberg-Marquardt algorithms
- Automatic differentiation: Using dual numbers for accurate derivative computation [2]
- Multi-curve framework: Support for multiple interest rate curves (OIS, LIBOR, etc.)


**References:**
1) F. M. Ametrano and M. Bianchetti, Everything You Always Wanted to Know 
About Multiple Interest Rate Curve Bootstrapping but Were Afraid 
to Ask (April 2013).

2) Darbyshire, J.H.M., 2022. Pricing and Trading Interest Rate 
Derivatives 2022: A Practical Guide to Swaps. Aitch & Dee Limited.


