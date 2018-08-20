## Beacon Aggregator

This API is used to receive a Beacon variant call, which is then queued up in a task list and asynchronous GET requests are made to known beacons. The response is returned in `application/json` format as a stream. The query should conform to [Beacon 1.0 specification](https://github.com/ga4gh-beacon/specification/blob/master/beacon.md).

### Endpoints
| Endpoint | Description |
| --- | --- |
| `/health` | Returns `HTTP 200` |
| `/q?` | Can be queried with various query parameters according to Beacon 1.0 specification. |

#### Example Queries
The variant format is enforced in the `beacon-ui` input field using a custom regex `/^([XY0-9]+) \: (\d+) ([ATCGN]+) \> ([ATCGN]+)$/i`.
A valid query would look like:
 * `1 : 1000 A > C`;
 * `1 : 2947887 C > T`;
 * `X : 389476 CAT > TAG`.

Actual API calls:
* `/q?assemblyId=GRCh37&referenceName=1&start=1000&referenceBases=A&alternateBases=C`
* `/q?assemblyId=GRCh38&referenceName=1&start=2947887&referenceBases=C&alternateBases=T`
* `/q?assemblyId=GRCh38&referenceName=X&start=389476&referenceBases=CAT&alternateBases=TAG`


A succesful query requires an ELIXIR AAI access token stored into the cookies, which is sent to the Beacons in the headers as `{Authorization: Bearer <access_token>}`.

### Environment Variables
The API requires some configuration variables stored as environment variables. If no environment variables are found, defaults are used instead. Below is a table listing all used environment variables with their default values and a brief description.

| ENV | Default | Description |
| --- | --- | --- |
| `BEACON_LIST` | `beacons.txt` | Contains Beacon URLs line by line, see [beacons.txt](https://github.com/CSCfi/beacon-openshift/blob/master/beacon-aggregator/beacons.txt) for reference. |
| `HTTPS_ONLY` | `True` | Determines security level when making variant calls to Beacons. If set to `False` `http://` Beacons can be queried. |
| `APP_HOST` | `localhost` | Web server host address inside the Openshift container. This is not the same as the external URL. |
| `APP_PORT` | `8080` | Web server port inside the Openshift container. |

### Run and Build

#### Run from the command line

The application can be run as (the application will default to the environment variable values specified above):

```
pip install -r requirements.txt
python app.py
```

##### Build using s2i

Create container for `beacon-search`
```
s2i build git@github.com:CSCfi/beacon-openshift.git --context-dir=beacon-search centos/python-35-centos7 beacon-search
```

Run the created container:
```
docker run -p 8080:8080 beacon-search
```
