#!/usr/bin/env python3

import asyncio
import aiohttp
from aiohttp import web
import json
import logging
import aiohttp_cors
import os

# Logging
FORMAT = '[%(asctime)s][%(name)s][%(process)d %(processName)s][%(levelname)-8s] (L:%(lineno)s) %(funcName)s: %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

routes = web.RouteTableDef()


@routes.get('/health')
async def health_check(request):
    """Answer age old question: is this API up."""
    LOG.info('hello')
    return web.HTTPOk()


def get_beacons():
    """Read beacon URLs from a file and return them in a list"""
    beacon_list = os.environ.get('BEACON_LIST', 'beacons.txt')
    beacons = []
    with open(beacon_list, 'r') as f:
        beacons = [line.strip() for line in f]
    return beacons  


@routes.get('/q')
async def query_string_endpoint(request):
    """Stream the response from the query and package it nicely."""

    # A COMPLETE LIST OF PARAMETERS
    '''
    q = {'referenceName': request.rel_url.query['referenceName'],
         'start': request.rel_url.query['start'],
         'end': request.rel_url.query['end'],
         'startMin': request.rel_url.query['startMin'],
         'startMax': request.rel_url.query['startMax'],
         'endMin': request.rel_url.query['endMin'],
         'endMax': request.rel_url.query['endMax'],
         'referenceBases': request.rel_url.query['referenceBases'],
         'alternateBases': request.rel_url.query['alternateBases'],
         'variantType': request.rel_url.query['variantType'],
         'assemblyId': request.rel_url.query['assemblyId'],
         'datasetIds': request.rel_url.query['datasetIds'],
         'includeDatasetResponses': request.rel_url.query['includeDatasetResponses']}
    '''

    resp = web.StreamResponse(status=200,
                              reason='OK',
                              headers={'Content-Type': 'application/json'})
    await resp.prepare(request)
    q = request.query_string  # query parameters, pass all
    tasks = []  # requests to-be-done are appended here
    BEACONS = get_beacons()  # list of beacon urls

    for beacon in BEACONS:
        task = asyncio.ensure_future(query(beacon, q))
        tasks.append(task)
        LOG.info(f'Making request to {beacon}')
    #try:
    await resp.write(b'[')
    for index, res in enumerate(asyncio.as_completed(tasks)):
        if index == len(tasks)-1:
            await resp.write(json.dumps(await res).encode('utf-8'))
            LOG.info('Last item has been processed')
        else:
            await resp.write(json.dumps(await res).encode('utf-8') + b',')
            LOG.info('Processing requests')
    await resp.write(b']')
    await resp.drain()
    await resp.write_eof()
    LOG.info('All requests have been completed')
    #except Exception as e:
    #    LOG.error(f'Something went bad: {e}')
    return resp


async def query(beacon, q):
    """Query the beacon endpoint."""
    access_token = None
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar) as session:
        #try:
        cookies = session.cookie_jar.filter_cookies(os.environ.get('COOKIE_DOMAIN', None))
        access_token = cookies['access_token'].value
        LOG.info(cookies.keys())
        '''for cookie in cookies:
            if cookie.key == 'access_token':
                access_token = cookie.value'''
        async with session.get(beacon,
                               params=q,
                               ssl=os.environ.get('HTTPS_ONLY', True),
                               headers={'Authorization': 'Bearer '+access_token}) as response:
            return await response.json()
        #except Exception as e:
        #    LOG.info(str(e))


def main():
    loop = asyncio.get_event_loop()
    server = web.Application(loop=loop)
    cors = aiohttp_cors.setup(server, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
    })
    server.router.add_routes(routes)
    for route in list(server.router.routes()):
        cors.add(route)
    web.run_app(server,
                host=os.environ.get('APP_HOST', 'localhost'),
                port=os.environ.get('APP_PORT', 5000))


if __name__ == '__main__':
    main()
