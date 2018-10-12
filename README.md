## Beacon Openshift

[![Build Status](https://travis-ci.org/CSCfi/beacon-openshift.svg?branch=master)](https://travis-ci.org/CSCfi/beacon-openshift)
[![Coverage Status](https://coveralls.io/repos/github/CSCfi/beacon-openshift/badge.svg?branch=master)](https://coveralls.io/github/CSCfi/beacon-openshift?branch=master)

This repository contains scripts intended to be run in [Openshift](https://www.openshift.com/) environment.
The subdirectories can be directly loaded into containers via webhooks or build as images using [s2i - source to image](https://github.com/openshift/source-to-image).

The contents of the subdirectories are briefly described below, and in more detail inside the respective subdirectories.

---

### APIs

APIs can be explored as OpenAPI 3.0 specification in: [Swagger Editor](http://editor.swagger.io/?url=https://raw.githubusercontent.com/CSCfi/beacon-openshift/master/beacon-search-apis.yaml)

* [beacon_search](https://github.com/CSCfi/beacon-openshift/tree/master/beacon_search) - Prototype suggestion API to find relevant variants related to diseases and genes;
* [beacon_aggregator](https://github.com/CSCfi/beacon-openshift/tree/master/beacon_aggregator) - Master Beacon API endpoint that queries known beacons and combines the results into a single response;
* [beacon_auth](https://github.com/CSCfi/beacon-openshift/tree/master/beacon_auth) - ELIXIR AAI client API for storing access token to be used in beacon-aggregator;

For testing purposes we provide: [beacon_mockup](https://github.com/CSCfi/beacon-openshift/tree/master/beacon_mockup) (a mockup Beacon APIs used in testing software operability). We recommend the use of [Beacon 1.0 Web Server](https://github.com/CSCfi/beacon-python) that implements the [Beacon 1.0 Specification](https://github.com/ga4gh-beacon/specification/blob/master/beacon.md).


### UI

* [beacon-ui](https://github.com/CSCfi/beacon-openshift/tree/master/beacon-ui/app) - User interface for looking up disease-gene-variant relations and creating variant calls to beacons. Is powered by the APIs listed above.

### Build and Deployment

#### OpenShift Installation

Following the instructions from [Creating an Application using the Web Console](https://docs.openshift.com/container-platform/3.9/dev_guide/application_lifecycle/new_app.html#using-the-web-console-na):
1. Create a new vanilla python image from the catalogue.
2. On advanced options set git repository URL and select proper subdirectory for context dir.
3. Click on create to pull source to image, container is automatically built and set up.

#### Manual Installation

##### Method 1

You can also build the containers manually with using [Creating an Application From Source Code](https://docs.openshift.com/container-platform/3.9/dev_guide/application_lifecycle/new_app.html#specifying-source-code).


##### Method 2

Environment variables can be set with [s2i](https://github.com/openshift/source-to-image) on creation (refer to the documentation).

e.g. Create container for `beacon-mockup`
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

Similar steps can be followed for `beacon-aggregator` (requires `centos/python-36-centos7` base image), `beacon_search`, `beacon_auth` and `beacon-ui` (requires `centos/httpd-24-centos7`).

### Running Tests

You can run tests manually with:
```
pytest
```

Or run automatically (builds test environment, runs tests, checks flake8).
```
tox
```

### Related Information

* [ELIXIR Beacon implementation study](https://www.elixir-europe.org/about-us/implementation-studies/beacons)
* [GA4GH Beacon project](https://beacon-project.io/)
* [Beacon 1.0 Specification](https://github.com/ga4gh-beacon/specification/blob/master/beacon.md)
* [Beacon 1.0 Web Server](https://github.com/CSCfi/beacon-python) - implementing the Beacon 1.0 specification
