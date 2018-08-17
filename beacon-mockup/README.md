# beacon-mockup

This API is a simple Beacon mockup intended for testing the `beacon-aggregator` API and `beacon-ui`.


##### Endpoints
| Endpoint | Description |
| --- | --- |
| `/api/true` | Always responds true. |
| `/api/false` | Always responds false. |
| `/api/null` | Always responds null. |

##### Example queries
Endpoints take query parameters according to [Beacon 1.0 specification](https://github.com/ga4gh-beacon/specification/blob/master/beacon.md)

#### Example responses
Can be seen directly in [app.py](https://github.com/CSCfi/beacon-openshift/blob/master/beacon-mockup/app.py)
