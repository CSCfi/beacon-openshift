# beacon-auth

This is an ELIXIR AAI Client API which authenticates the user at Beacon UI and stores an access token into the cookies to be used later in `beacon-aggregator` as means of authorization. Refer to [ELIXIR AAI Documentation](https://www.elixir-europe.org/services/compute/aai) for issues related to authentication.

##### Endpoints
| Endpoint | Description |
| --- | --- |
| `/app` | API index, redirects user to ELIXIR AAI Login on landing. |
| `/` | Callback URL to which user is returned to from ELIXIR AAI after authentication. User is redirected back to Beacon UI along with storing the access token to cookies at this phase. |

##### Example queries
```/app``` # Redirects user to ELIXIR AAI for authentication

##### Environment variables in Openshift
The API requires some configuration variables stored as environment variables in Openshift. If no environment variables are found, defaults are used instead. Below is a table listing all used environment variables with their default values and a brief description.

| ENV | Default | Description |
| --- | --- | --- |
| `APP_HOST` | `localhost` | Web server host address inside the Openshift container. This is not the same as the external URL. |
| `APP_PORT` | `8080` | Web server port inside the Openshift container. |
| `APP_DEBUG` | `False` | If set to `True`, Flask will print events into the Openshift terminal. |
| `COOKIE_SECRET` | `None` | Should be set to a random string. Used as a secret key for storing cookies. |
| `COOKIE_AGE` | `3600` | Cookie expiration time in seconds. |
| `COOKIE_SECURE` | `True` | Tells Flask to only set secure https cookies. |
| `COOKIE_DOMAIN` | `None` | Should point to wildcard subdomain level, as the APIs are served in subdomains in Openshift, e.g. `*.domain.org` |
| `SESSION_COOKIE_SECURE` | `True` | Tells Flask to only allow cookies if connection is secure (https). |
| `REDIRECT_URL` | `None` | Should point to Beacon UI index page. | 
| `CALLBACK_URL` | `None` | ELIXIR AAI Callback to `beacon-auth` `/`. |
| `CLIENT_ID` | `None` | Client service identifier. Acquired from ELIXIR AAI. |
| `CLIENT_SECRET` | `None` | Secret key for client service identifier. Acquired from ELIXIR AAI. |
