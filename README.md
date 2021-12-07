# Jetpack Examples

This repo contains example services and functions for running with Jetpack.

1. **01-py-flask-hello** - A simple "Hello World" flask example 
2. **02-py-flask-hello-buildpacks** - Same example as 01, but using buildpacks instead of dockerfiles
3. **03-py-async-jobs** - Shows various examples using the @function decorator from the Jetpack SDK to launch remote functions
4. **04-py-scheduled-jobs** - Shows how to schedule a function to run later with the Jetpack SDK
5. **05-py-cron-job** - Demonstrates how to schedule a recurring job in the cluster

## Deploying Examples:

If you have the Jetpack CLI and access to a Kubernetes Cluster, you can deploy and test the examples using `jetpack dev`.
