# Jetpack Examples

This repo contains example services and functions for running with Jetpack.

1. **01-py-flask-hello** - Start a Flask API in Jetpack: no kubernetes yaml required. 
2. **02-py-flask-secrets** - Same Flask API, includes mounted secret file
3. **03-py-async-jobs** - Shows various examples using the @function decorator from the Jetpack SDK to launch remote functions
4. **04-py-scheduled-jobs** - Shows how to schedule a function to run later with the Jetpack SDK
5. **05-py-cron-job** - Demonstrates how to schedule a recurring job in the cluster

## Deploying Examples:

1. Install the Jetpack CLI:

   ```
   curl https://get.jetpack.io/ -fsSL | bash
   ```

2. Clone this repo to your local machine:

   ```
   git clone https://github.com/jetpack-io/jetpack-examples
   ```

3. Switch to an example repo:

   ```
   cd jetpack-examples/01-py-flask-hello
   ```

4. Login to the Jetpack CLI for free:

   ```
   jetpack auth login
   ```

5. Spin up the sample for free in the Jetpack trial cluster:

   ```
   jetpack dev
   ```

6. When you finish with a sample, stop the resources in Kubernetes:

   ```
   jetpack down
   ```

## Documentation

For more documentation on Jetpack, you can visit: https://docs.jetpack.io/
