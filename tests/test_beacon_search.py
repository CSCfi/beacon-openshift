import unittest

from unittest import mock

from beacon_search.app import create_pagination, app


class TestSearchAPI(unittest.TestCase):
    """Test beacon-search API functions and endpoints."""

    def setUp(self):
        """Execute this method on start."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        """Execute this method after each test."""
        pass

    # FUNCTION TESTS

    def test_pagination_function(self):
        """Test creation of pagination."""
        assert create_pagination(1, 10, 100) == {'page': 1,
                                                 'total_pages': 10,
                                                 'total_results': 100,
                                                 'limit': 10,
                                                 'offset': 0}

    def test_pagination_error(self):
        """Test failure of pagination."""
        with self.assertRaises(TypeError):
            create_pagination(1)

    # ENDPOINT TESTS

    def test_health(self):
        """Test health check."""
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_api_400(self):
        """Test HTTP 400: Bad request."""
        response = self.app.get('/api?incorrectQueryParameter=someValue', follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    @mock.patch('beacon_search.app.db_cursor')
    def test_api_disease_200(self, mock_cursor):
        """Test successful disease search."""
        mock_cursor.return_value = mock_cur = mock.MagicMock()
        mock_cur.fetchall.return_value = [{'total_results': 1}]
        response = self.app.get('/api?type=disease&query=someDisease', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    @mock.patch('beacon_search.app.db_cursor')
    def test_api_gene_200(self, mock_cursor):
        """Test successful gene search."""
        mock_cursor.return_value = mock_cur = mock.MagicMock()
        mock_cur.fetchall.return_value = [{'total_results': 1}]
        response = self.app.get('/api?type=gene&query=someGene,GRCh38', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_api_gene_400(self):
        """Test HTTP 400: Bad request. For type: gene."""
        with self.assertRaises(IndexError):
            self.app.get('/api?type=gene&query=someGene', follow_redirects=True)

    @mock.patch('beacon_search.app.db_cursor')
    def test_api_disease_404(self, mock_cursor):
        """Test HTTP 404: Not found. For type: disease."""
        mock_cursor.return_value = mock_cur = mock.MagicMock()
        mock_cur.fetchall.return_value = [{'total_results': 0}]
        response = self.app.get('/api?type=disease&query=nonExistantDisease', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    @mock.patch('beacon_search.app.db_cursor')
    def test_api_gene_404(self, mock_cursor):
        """Test HTTP 404: Not found. For type: gene."""
        mock_cursor.return_value = mock_cur = mock.MagicMock()
        mock_cur.fetchall.return_value = [{'total_results': 0}]
        response = self.app.get('/api?type=gene&query=nonExistantGene,GRCh38', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    @mock.patch('beacon_search.app.db_cursor')
    def test_autocomplete_404(self, mock_cursor):
        """Test HTTP 404: Not found."""
        mock_cursor.return_value = mock_cur = mock.MagicMock()
        mock_cur.fetchall.return_value = ''
        response = self.app.get('/autocomplete?q=nonExistantKeyword', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    @mock.patch('beacon_search.app.db_cursor')
    def test_autocomplete_400(self, mock_cursor):
        """Test HTTP 400: Bad request."""
        response = self.app.get('/autocomplete', follow_redirects=True)
        self.assertEqual(response.status_code, 400)

    @mock.patch('beacon_search.app.db_cursor')
    def test_autocomplete_200(self, mock_cursor):
        """Test successful autocomplete."""
        mock_cursor.return_value = mock_cur = mock.MagicMock()
        mock_cur.fetchall.return_value = [{'something': 'anything'}]
        response = self.app.get('/autocomplete?q=existingKeyword', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
