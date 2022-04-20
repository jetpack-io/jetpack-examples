# Async Functions

## Description
This example deploys a container which launches a CronJob. The CronJob in this example will check and print the latest Bitcoin price every 10 minutes

## How to Deploy
`jetpack up` to deploy the image + CronJob to your namespace 

## How to Test
The job won't run for **10** minutes. In 10 minutes, you can see the results by running:
```bash
kubectl logs <name-of-the-job-pod>
```
To get the list of pods related to `py-cron-job` in your namespace, you can run: 
```bash
kubectl get pods -l app.kubernetes.io/instance=py-async-jobs
```
