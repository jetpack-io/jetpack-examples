# Flask Hello

## Description
This example deploys a simple Flask Hello World service with Secrets using a Dockerfile

## How to Deploy
In this case, the secrets are contained within a `secrets.json` file. This file can be uploaded to the cluster as a secret using the `--mount-secret-file` flag.

To starte a development session, run: 
```
jetpack dev --mount-secret-file secrets.json --replicas=1
```

The file will be mounted to your container at `'/var/run/secrets/jetpack.io/secrets.json'`. 

## How to Test

```
curl localhost:8080/readsecrets

# {
#	"secretString": "Hello",
#	"secretNumber": 42
# }

```

