# Async Functions

## Description
Jetroutines are code hints that tell the Jetpack Runtime how to separate the monolith into lots of microservices. When Jetpack deploys the project, it creates separate containers for the regular app and scheduled jobs when needed to run `jetroune` annotated functions.

This example deploys a FastAPI service with an endpoint that schedules a job. Developers can specify the delay and message they want to test with as a JSON request body

This example demonstrates how you can schedule tasks to run later. For tasks that you want to run on a recurring basis, see `05-py-cron-job` in the examples repo

## Endpoints

`POST /delay` -- Schedules a task to run after a delay, which will then print a provided message to it's logs. The request body should be a JSON object with the following fields:
* `delay`: int -- how much time in seconds to wait before running the job
* `message`: string -- the message you want the function to print

## How to Deploy
`jetpack dev` to start a development session with port + log forwarding

## How to Test
```bash
# Schedule a message 
curl -X POST localhost:8080/delay \
   -H 'Content-Type: application/json' \
   -d '{"delay": 10,"message":"Hello!"}'
```

Once the task runs, you can see the message by running: 
```bash
kubectl logs <name-of-the-job-pod>
```
To get the full list of pods running in your namespace, you can run 
```bash
kubectl get pods 
```