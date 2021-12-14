# Async Functions

## Description
This example deploys a FastAPI service with different endpoints that demonstrate Jetpack Functions

## Endpoints

1. `/diamond` runs a diamond workflow that runs one function function, fans out to run two functions in parallel, and then runs a fourth function after the fan out returns. This example demonstrates how to construct workflows with fan-out and fan-in patterns
2. `/fibonacci/{n}` runs a recursive fibonacci sequence using Jetpack functions. This demonstrates how workflows and functions can be chained. NOTE: we recommend testing this with small numbers, to avoid depleting too many resources in your namespace.
3. `/error` runs a Jetpack function that returns a Python Error. This shows how errors can be serialized and handled between function calls

## How to Deploy
`jetpack dev` to start a development session with port + log forwarding

## How to Test

```bash
curl localhost:8080/diamond

curl localhost:8080/fibonacci/{number}

curl localhost:8080/error

```