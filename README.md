# beacon-openshift

This repository contains scripts intended to be run in Openshift environment. The subdirectories can be directly loaded into containers via webhooks. The contents of the subdirectories are briefly described below, and in more detail inside the respective subdirectories.

### APIs

##### beacon-search [>>](https://github.com/CSCfi/beacon-openshift/tree/master/beacon-search)
Prototype suggestion API to find relevant variants related to diseases and genes.

##### beacon-auth [>>](https://github.com/CSCfi/beacon-openshift/tree/master/beacon-auth)
ELIXIR AAI client API for storing access token to be used in beacon-aggregator.

##### beacon-aggregator [>>](https://github.com/CSCfi/beacon-openshift/tree/master/beacon-aggregator)
Master Beacon API endpoint that queries known beacons and combines the results into a single response.

##### beacon-mockup [>>](https://github.com/CSCfi/beacon-openshift/tree/master/beacon-mockup)
Mockup Beacon APIs used in testing software operability.

### UI

##### beacon-ui [>>](https://github.com/CSCfi/beacon-openshift/tree/master/beacon-ui/app)
User interface for looking up disease-gene-variant relations and creating variant calls to beacons. Is powered by the APIs listed above.


### Other

##### Related Information
[ELIXIR Beacon implementation study](https://www.elixir-europe.org/about-us/implementation-studies/beacons)

[GA4GH Beacon project](https://beacon-project.io/)

[Beacon 1.0 Specification](https://github.com/ga4gh-beacon/specification/blob/master/beacon.md)

[Beacon 1.0 API]() # To be published
