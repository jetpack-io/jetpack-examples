# Is It Down Monitor

This app monitors a list of websites and checks if they are down. 
If any website is down, then it notifies a slack channel using a slack webhook.

The code in `jetpack_main.py` is deliberately written in a fashion
to exercise the remote-functions that jetpack's runtime enables. It is not
the optimal way to structure this app because of the high overhead in spinning 
up a remote process for such simple functionality.


## Setup steps

To run it, you'll need to create a slack webhook following the instructions 
at https://api.slack.com/messaging/webhooks. This will be assigned an url of
the form:
```
https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
```

Set this in `app/.env` as: 
```
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
```

## Testing

After running `jetpack dev`, you can test the monitor by running:

```bash
curl localhost:8080/poll_down_status
```

## Debugging
- Ensure the `jetpack-io` version in `requirements.txt` is the latest.
- There is a FastAPI endpoint which can trigger the cronjob functionality on-demand.
- There is a commented out line in `check_if_down` that randomly returns that a website is down.
- The logging is rather verbose.
