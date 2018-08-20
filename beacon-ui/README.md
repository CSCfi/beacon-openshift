## Beacon UI

This subdirectory contains relevant files for the Beacon UI, and is powered by AngularJS. Dependencies are included in this subdirectory.

### Configuration

The Beacon UI endpoints can be configured in `app/view/config.json` file. Currently they will default to:
```json
{
  "baseUrl": "https://beacon-search-beacon.rahtiapp.fi",
  "aggregatorUrl": "https://beacon-aggregator-beacon.rahtiapp.fi/q?"
}
```

### Run and Build

In the `app` folder one can start the application (for development purposes) using:

#### Run from command line


```
python -m SimpleHTTPServer 8080
```
or
```
python3 -m http.server 8080
```

#### Run from Apache Web Server

Create container for `beacon-ui`:
```
s2i build git@github.com:CSCfi/beacon-openshift.git \
    --context-dir=beacon-ui \
    centos/httpd-24-centos7 \
    beacon-ui
```

Run the created container:
```
docker run -p 8080:8080 beacon-ui
```

The application will be available at: `http://localhost:8080/app`
