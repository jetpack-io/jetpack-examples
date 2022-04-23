Jetpack Email Send Example
==========================

This sample demonstrates running a Python FastAPI web server that fans out email sends to parallel Kubernetes jobs.


How to Use
----------

1. Download the Jetpack CLI:

   ```sh
   curl https://get.jetpack.io/ -fsSL | bash
   ```

2. Login to the Jetpack CLI to get access to the free trial cluster:

   ```sh
   jetpack auth login
   ```

   You'll be prompted to login through Google, GitHub, or email/password.

3. Start the sample on Jetpack's free trial Kubernetes cluster:

   ```sh
   jetpack dev
   ```

   This console won't return so it can stream logs from the Python app.

4. Browse to the app:

   http://localhost:8080/

   Fill in a bunch of emails, and push send.

5. See the Kubernetes jobs that ran:

   ```sh
   kubectl get jobs
   ```

6. Once you're done, remove the sample from the cluster:

   ```sh
   jetpack down
   ```


Browsing the Code
-----------------

Notice how main.py calls `send_brochure()` imported from send.py. In send.py, notice the `@jetroutine` attribute over the `async def send_email(...):` function. With this attribute in place, the Jetpack runtime will split the monolith into two separate container instances, allowing them to scale independently. In this case, a single web server can fan out to many email send jobs, asynchronously harvesting the results. The monolith becomes a distributed system with Jetpack.


License
-------

MIT, Copyright Jetpack.io
