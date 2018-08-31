#!/usr/bin/env python3.4


from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import logging
import os
import math

# Logging
logging.basicConfig(filename='api.log',
                    format='%(asctime)s %(message)s',
                    datefmt='%d-%M-%Y %H:%M:%S',
                    level=logging.INFO)

# Initialize web app
application = Flask(__name__)
CORS(application)


@app.route("/")
def hello():
    """Greet user with service name."""
    return "\nBeacon 2.0 API\n"


def http_error(status, message):
    """Return HTTP error status code and message."""
    response = jsonify({'message': message})
    response.status_code = status
    return response


def create_pagination(page, results_per_page, total_results):
    """Create pagination to filter results to manageable amounts."""
    pagination = {}

    # For UI
    pagination['page'] = page
    pagination['total_results'] = total_results
    pagination['total_pages'] = math.ceil(total_results / results_per_page)

    # For database
    pagination['limit'] = results_per_page
    pagination['offset'] = (page - 1) * results_per_page

    return pagination


@app.route("/api")
def api():
    """Serve multipurpose API endpoint.

    Example disease query:
    /api?type=disease&query=Alzheimer

    Example gene query:
    /api?type=gene&query=APOE,GRCh38&page=1&resultsPerPage=30
    """
    query = {}
    assemblies = ['GRCh37', 'GRCh38']  # Currently supported assemblies

    # Query for diseases
    # Query string should be at least 3 characters long to limit results
    if request.args.get('type') == 'disease' and len(request.args.get('query')) > 3:
        query['disease'] = request.args.get('query')
        try:
            cur = db_cursor()
            results = ''

            # Get number of results for pagination
            cur.execute('SELECT COUNT(*) AS total_results '
                        'FROM annotations WHERE disease LIKE %s;',
                        ('%' + query['disease'] + '%',))
            total_results = cur.fetchall()[0]['total_results']

            if total_results > 0:

                # Create guide for UI to operate pagination
                pagination = create_pagination(page=int(request.args.get('page', 1)),
                                               results_per_page=int(request.args.get('resultsPerPage', 30)),
                                               total_results=total_results)

                # Finally make the actual query for diseases
                cur.execute('SELECT disease AS phenotype_name, '
                            'hpo_id AS phenotype_id, '
                            'disease_id AS genotype_id, genotype AS genotype_name, gene '
                            'FROM annotations WHERE disease LIKE %s LIMIT %s OFFSET %s;',
                            ('%' + query['disease'] + '%', pagination['limit'], pagination['offset'],))

                results = cur.fetchall()

                response = {'pagination': {'totalResults': pagination['total_results'],
                                           'currentPage': pagination['page'],
                                           'totalPages': pagination['total_pages']},
                            'results': results}

                return jsonify(response)
            else:
                return http_error(404, 'Disease not found')

        except Exception as e:
            logging.info('ERROR IN /api?disease=' + query['disease'] + ' :: ' + str(e))
        finally:
            cur.connection.close()

    # Query for genes
    elif request.args.get('type') == 'gene':

        # Break query params from &query=gene,assembly
        params = request.args.get('query').split(',')
        query['gene'] = params[0]
        query['assembly'] = params[1]

        if query['gene'] and any(a in query['assembly'] for a in assemblies):
            try:
                cur = db_cursor()
                results = ''

                # Get number of results for pagination
                cur.execute('SELECT COUNT(*) AS total_results '
                            'FROM changes WHERE entrez=(SELECT entrez FROM genes WHERE gene=%s) '
                            'AND assembly=%s ORDER BY chrpos;', (query['gene'], query['assembly'],))
                total_results = cur.fetchall()[0]['total_results']

                if total_results > 0:

                    # Create guide for UI to operate pagination
                    pagination = create_pagination(page=int(request.args.get('page', 1)),
                                                   results_per_page=int(request.args.get('resultsPerPage', 30)),
                                                   total_results=total_results)

                    # Finally make the actual query for genes
                    cur.execute('SELECT chr, chrpos, ref, alt, assembly, accession, accession_ver '
                                'FROM changes WHERE entrez=(SELECT entrez FROM genes WHERE gene=%s) '
                                'AND assembly=%s ORDER BY chrpos LIMIT %s OFFSET %s;',
                                (query['gene'], query['assembly'], pagination['limit'], pagination['offset'],))
                    results = cur.fetchall()

                    # Combine pagination settings with the query results
                    response = {'pagination': {'totalResults': pagination['total_results'],
                                               'currentPage': pagination['page'],
                                               'totalPages': pagination['total_pages']},
                                'results': results}

                    return jsonify(response)
                else:
                    return http_error(404, 'Gene not found')

            except Exception as e:
                logging.info('ERROR IN /api?gene=' + query['gene'] + '&assembly=' + query['assembly'] +
                             ' :: ' + str(e))
            finally:
                cur.connection.close()
        else:
            return http_error(400, 'Missing gene or incorrect assembly')
    else:
        return http_error(400, 'Invalid query parameters')


@app.route("/autocomplete")
def autocomplete():
    """Suggest matching results for input keywords."""
    # Initialize autocomplete variables
    diseases = ''
    genes = ''
    results = []

    if request.args.get('q'):
        keyword = request.args.get('q')
        try:
            # Search for diseases
            cur = db_cursor()
            cur.execute('SELECT DISTINCT(disease) AS name, '
                        'COUNT(DISTINCT(a.gene)) AS relatedGenes, '
                        'COUNT(*) AS variations, '
                        '"disease" AS type '
                        'FROM annotations a INNER JOIN changes c '
                        'ON a.entrez=c.entrez '
                        'WHERE a.disease LIKE %s '
                        'GROUP BY a.disease;',
                        ('%' + keyword + '%',))
            diseases = cur.fetchall()

            # Search for genes
            cur.execute('SELECT DISTINCT(gene) AS name, '
                        'COUNT(*) AS variations, '
                        '"gene" AS type '
                        'FROM genes g, changes c '
                        'WHERE g.entrez=c.entrez '
                        'AND g.gene LIKE %s '
                        'GROUP BY gene;',
                        ('%' + keyword + '%',))
            genes = cur.fetchall()

            # Add results from queries to the response if results were found
            if len(diseases) != 0:
                results = results + diseases
            if len(genes) != 0:
                results = results + genes

            if len(results) == 0:
                return http_error(404, 'No matches with keyword')
            else:
                return jsonify(results)
        except Exception as e:
            logging.info('ERROR IN /autocomplete :: ' + str(e))
    else:
        return http_error(400, 'Missing query parameter ?q=')


def db_init():
    """Connect to a database."""
    try:
        db = pymysql.connect(host=os.environ.get('DB_HOST', 'localhost'),
                             user=os.environ.get('DB_USER', 'root'),
                             passwd=os.environ.get('DB_PASS', 'root'),
                             db=os.environ.get('DB_NAME', 'hpo_2018_05'))
        return db
    except Exception as e:
        logging.info('ERROR IN db_init() :: ' + str(e))


def db_cursor():
    """Return database cursor."""
    try:
        return db_init().cursor(pymysql.cursors.DictCursor)
    except Exception as e:
        logging.info('ERROR IN db_cursor() :: ' + str(e))


def main():
    """Start the web server."""
    application.run(host=os.environ.get('APP_HOST', 'localhost'),
                    port=os.environ.get('APP_PORT', 8080),
                    debug=os.environ.get('APP_DEBUG', False))


if __name__ == '__main__':
    main()
