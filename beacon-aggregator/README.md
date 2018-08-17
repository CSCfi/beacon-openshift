# beacon-aggregator

This API is used to receive a Beacon variant call, which is then queued up in a task list and asynchronous GET requests are made to known beacons. The response is returned in `application/json` format as a stream. The query should conform to [Beacon 1.0 specification](https://github.com/ga4gh-beacon/specification/blob/master/beacon.md).

##### Endpoints
| Endpoint | Description |
| --- | --- |
| `/health` | Returns `HTTP 200` |
| `/q?` | Can be queried with various query parameters according to Beacon 1.0 specification. |

##### Example queries
```/q?assemblyId=GRCh37&referenceName=5&start=3000000&referenceBases=A&alternateBases=C```

```/q?assemblyId=GRCh38&referenceName=X&start=150000&referenceBases=TTG&alternateBases=GAC```

A succesful query requires an ELIXIR AAI access token stored into the cookies, which is sent to the Beacons in the headers as `{Authorization: Bearer <access_token>}`.

##### Environment variables in Openshift
The API requires some configuration variables stored as environment variables in Openshift. If no environment variables are found, defaults are used instead. Below is a table listing all used environment variables with their default values and a brief description.

| ENV | Default | Description |
| --- | --- | --- |
| `BEACON_LIST` | `beacons.txt` | Contains Beacon URLs line by line, see [beacons.txt](https://github.com/CSCfi/beacon-openshift/blob/master/beacon-aggregator/beacons.txt) for reference. |
| `HTTPS_ONLY` | `True` | Determines security level when making variant calls to Beacons. If set to `False` `http://` Beacons can be queried. |
| `APP_HOST` | `localhost` | Web server host address inside the Openshift container. This is not the same as the external URL. |
| `APP_PORT` | `8080` | Web server port inside the Openshift container. | 
