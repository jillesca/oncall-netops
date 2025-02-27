# grafana-to-langgraph-proxy

The script is a simple wrapper that takes a webhook from Grafana as input and creates a `POST` request to the langgraph API server.

Here you can see the basic components needed to trigger a background run in the Langgraph API server.

```bash
curl http://<LANGGRAPH_SERVER>/runs \
  --request POST \
  --header 'Accept: */*' \
  --header 'Content-Type: application/json' \
  --data '{
    "assistant_id": "oncall-netops",
    "input": {
      "incident_description": "Can you check the interfaces on device cat8000v-0 are working correctly, I'\''m afraid ISIS is not working"
    },
    "on_completion": "keep",
    "on_disconnect": "continue",
    "after_seconds": 1
  }'
```

The `on_completion` field is important to be able to see the run on the threads, otherwise you won't see the result of the operation in the langgraph GUI.
