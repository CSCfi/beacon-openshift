from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
import asynctest
from beacon_aggregator.app import init, main
from unittest import mock
from aiohttp import web


class AppTestCase(AioHTTPTestCase):
    """Test for Web app.

    Testing web app endpoints.
    """

    async def get_application(self):
        """Retrieve web Application for test."""
        return init()

    @unittest_run_loop
    async def test_health(self):
        """Test the info endpoint.

        The status should always be 200.
        """
        resp = await self.client.request("GET", "/health")
        assert 200 == resp.status


class TestBasicFunctionsApp(asynctest.TestCase):
    """Test App Base.

    Testing basic functions from web app.
    """

    def setUp(self):
        """Initialise fixtures."""
        pass

    def tearDown(self):
        """Remove setup variables."""
        pass

    @mock.patch('beacon_aggregator.app.web')
    def test_main(self, mock_webapp):
        """Should start the webapp."""
        main()
        mock_webapp.run_app.assert_called()

    def test_init(self):
        """Test init type."""
        server = init()
        self.assertIs(type(server), web.Application)
