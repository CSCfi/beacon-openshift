#!/usr/bin/env python3
"""Master Beacon API endpoint that queries known beacons and combines the results into a single response."""

import json
import logging
import os

import asyncio
import aiohttp
import aiohttp_cors
import uvloop

from aiohttp import web

# Logging
FORMAT = '[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s] (L:%(lineno)s) %(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

# Collect API endpoints
routes = web.RouteTableDef()
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


@routes.get('/health')
async def health_check(request):
    """Return HTTP 200."""
    return web.HTTPOk()


def get_beacons():
    """Read beacon URLs from a file and return them in a list."""
    # Look for a file containing beacon URLs line by line
    # defaults to beacons.txt if no value is given in ENV
    beacon_list = os.environ.get('BEACON_LIST', 'beacons.txt')
    beacons = []

    # Parse beacon URLs from file into a list for easy iteration
    with open(beacon_list, 'r') as f:
        beacons = [line.strip() for line in f]

    return beacons


@routes.get('/q')
async def query_string_endpoint(request):
    """Stream the response from the query and package it nicely."""
    # Prepare websocket for responding
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    q = request.query_string  # query parameters, pass all
    tasks = []  # requests to-be-done are appended here
    BEACONS = get_beacons()  # list of beacon urls

    # Iterate over beacon URLs and queue requests to them
    for beacon in BEACONS:
        # Get access token from cookies
        access_token = request.cookies['access_token'] if 'access_token' in request.cookies else None
        # Bundle queries together
        task = asyncio.ensure_future(query(beacon, q, access_token, ws))
        tasks.append(task)
        LOG.info(f'Queueing request to {beacon} with params={q}')

    # Prepare and initiate coroutines
    await asyncio.gather(*tasks)

    # Finally close the websocket connection
    await ws.close()
    LOG.info('All requests have been completed')

    return ws


async def query(beacon, q, access_token, ws):
    """Query the beacon endpoint."""
    headers = {'User-Agent': 'ELIXIR Beacon Aggregator 1.0'}
    if access_token:
        headers.update({'Authorization': 'Bearer ' + access_token})

    # Create a new session for querying a beacon
    async with aiohttp.ClientSession() as session:
        try:
            # Send a GET request to beacon with authorized access token
            async with session.get(beacon,
                                   params=q,
                                   ssl=os.environ.get('HTTPS_ONLY', True),
                                   headers=headers) as response:
                LOG.info(f'Made request to {beacon} with params={q}')

                # Check that response status is 200 before sending websocket message
                # filters e.g. 504 time-outs
                if response.status == 200:
                    # Return the response asynchronously when it arrives
                    result = await response.json()
                    # Send result to websocket client
                    return await ws.send_str(json.dumps(result))
                else:
                    # Send error to websocket client
                    return await ws.send_str(json.dumps(str({"beaconUrl": beacon,
                                                             "queryParams": q,
                                                             "responseStatus": response.status})))
        except Exception as e:
            LOG.info(str(e))


def init():
    """Initialise server."""
    server = web.Application()
    # Set this to the domain of the GUI to only allow requests from that source
    DOMAIN = os.environ.get('CORS_ALLOWED_DOMAIN', 'localhost:8000')
    cors = aiohttp_cors.setup(server, defaults={
        DOMAIN: aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })
    server.router.add_routes(routes)
    for route in list(server.router.routes()):
        cors.add(route)
    return server


def main():
    """Start the web server."""
    web.run_app(init(),
                host=os.environ.get('APP_HOST', 'localhost'),
                port=os.environ.get('APP_PORT', 8080))


if __name__ == '__main__':
    main()
