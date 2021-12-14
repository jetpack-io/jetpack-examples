# Flask Hello

## Description
This example deploys a simple Flask Hello World service using a Buildpack. The Jetpack CLI will automatically attempt to build the project using a Buildpack if a Dockerfile is not detected.

A Procfile must be provided to specify what command the container should run on launch. 

## How to Deploy
`jetpack dev` to start a development session with port + log forwarding

## How to Test

```bash
curl localhost:8080/

# <h1>Hello! You are currently in development</h1>

```