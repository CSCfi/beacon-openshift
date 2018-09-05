## Beacon Mockup

This API is a simple Beacon mockup intended for testing the `beacon-aggregator` API and `beacon-ui`.

### Endpoints
| Endpoint | Description |
| --- | --- |
| `/api/true` | Always responds true. |
| `/api/false` | Always responds false. |
| `/api/null` | Always responds null. |

#### Example Queries
Endpoints take query parameters according to [Beacon 1.0 specification](https://github.com/ga4gh-beacon/specification/blob/master/beacon.md)

#### Example Responses
Example for `true` response can be seen directly in [app.py](https://github.com/CSCfi/beacon-openshift/blob/master/beacon-mockup/app.py#L17-L62)

### Run and Build

#### Run from the command line

The application can be run as:

```
pip install -r requirements.txt
python app.py
```

##### Build using s2i

Create container for `beacon-mockup`
```
s2i build git@github.com:CSCfi/beacon-openshift.git \
    --context-dir=beacon_mockup \
    centos/python-35-centos7 \
    beacon_mockup
```

Run the created container:
```
docker run -p 8080:8080 beacon_mockup
```
