#!/usr/bin/env python3.4


from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import pymysql
import logging
import os
import math


logging.basicConfig(filename='api.log',
                    format='%(asctime)s %(message)s',
                    datefmt='%d-%M-%Y %H:%M:%S',
                    level=logging.INFO)


app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    """
    This function is used to check if service is online
    Function: Greets the user with service name when visiting base URL
    """
    return "\nBeacon 2.0 API\n"


def create_pagination(page, results_per_page, total_results):

    pagination = {}

    # FOR UI
    pagination['page'] = page
    pagination['total_results'] = total_results
    pagination['total_pages'] = math.ceil(total_results / results_per_page)

    # FOR MYSQL
    pagination['limit'] = results_per_page
    pagination['offset'] = (page - 1) * results_per_page

    return pagination


@app.route("/api")
def api():
    """
    This function implements query string type search for the API

    Example disease query:
    /api?type=disease&query=Alzheimer

    Example gene query:
    /api?type=gene&query=APOE,GRCh38&page=1&resultsPerPage=20
    """

    query = {}
    assemblies = ['GRCh37', 'GRCh38']

    # Query for Diseases
    if request.args.get('type') == 'disease':
        query['disease'] = request.args.get('query')
    
        if len(query['disease']) > 3:
            try:
                cur = db_cursor()
                cur.execute('SELECT disease AS phenotype_name, '
                            'hpo_id AS phenotype_id, '
                            'disease_id AS genotype_id, genotype AS genotype_name, '
                            'gene '
                            'FROM annotations WHERE disease LIKE %s;',
                            ('%' + query['disease'] + '%',))
                results = cur.fetchall()

                if len(results) == 0:
                    return jsonify({'http': 404, 'msg': 'disease not found'})
                else:
                    return jsonify(results)
            except Exception as e:
                logging.info('ERROR IN /api?disease=' + query['disease'] + ' :: ' + str(e))
            finally:
                cur.connection.close()
        else:
            return jsonify({'http': 400, 'msg': 'Disease name must be at least 4 characters long.'})
    elif request.args.get('type') == 'gene':

        # Break query params from &query=gene,assembly
        params = request.args.get('query').split(',')
        query['gene'] = params[0]
        query['assembly'] = params[1]
    
        if query['gene'] and any(a in query['assembly'] for a in assemblies):
            try:
                cur = db_cursor()

                # GET NUMBER OF RESULTS FOR PAGINATION
                cur.execute('SELECT COUNT(*) AS total_results '
                            'FROM changes WHERE entrez=(SELECT entrez FROM genes WHERE gene=%s) '
                            'AND assembly=%s ORDER BY chrpos;', (query['gene'], query['assembly'],))

                # CREATE PAGINATION GUIDE
                pagination = create_pagination(page=int(request.args.get('page', 1)),
                                            results_per_page=int(request.args.get('resultsPerPage', 20)),
                                            total_results=cur.fetchall()[0]['total_results'])

                # MAKE THE ACTUAL QUERY FOR RESULTS
                cur.execute('SELECT chr, chrpos, ref, alt, assembly, accession, accession_ver '
                            'FROM changes WHERE entrez=(SELECT entrez FROM genes WHERE gene=%s) '
                            'AND assembly=%s ORDER BY chrpos LIMIT %s OFFSET %s;',
                            (query['gene'], query['assembly'], pagination['limit'], pagination['offset'],))
                results = cur.fetchall()

                response = {'pagination': {'totalResults': pagination['total_results'],
                                        'currentPage': pagination['page'],
                                        'totalPages': pagination['total_pages']},
                            'results': results}

                if len(results) == 0:
                    return jsonify({'http': 404, 'msg': 'gene not found'})
                else:
                    return jsonify(response)
            except Exception as e:
                logging.info('ERROR IN /api?gene=' + query['gene'] + '&assembly=' + query['assembly'] + 
                            ' :: ' + str(e))
            finally:
                cur.connection.close()
        else:
            return jsonify({'http': 400, 'msg': 'Missing gene, or incorrect assembly.'})
    else:
        return jsonify({'http': 400, 'msg': 'Invalid query string combinations.'})


@app.route("/autocomplete")
def autocomplete():
    """
    This endpoint serves an autocomplete field and returns
    related information
    """

    diseases = ''
    genes = ''
    results = []

    if request.args.get('q'):
        keyword = request.args.get('q')
        try:
            # SEARCH FOR DISEASES
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

            # SEARCH FOR GENES
            cur.execute('SELECT DISTINCT(gene) AS name, '
                        'COUNT(*) AS variations, '
                        '"gene" AS type '
                        'FROM genes g, changes c '
                        'WHERE g.entrez=c.entrez '
                        'AND g.gene LIKE %s '
                        'GROUP BY gene;',
                        ('%' + keyword + '%',))
            genes = cur.fetchall()

            # ADD RESULTS TO RESPONSE LIST IF RESULTS WERE FOUND
            if len(diseases) != 0:
                results = results + diseases
            if len(genes) != 0:
                results = results + genes

            if len(results) == 0:
                return jsonify({'http': 404, 'msg': 'keyword not found'})
            else:
                return jsonify(results)
        except Exception as e:
            logging.info('ERROR IN /autocomplete :: ' + str(e))
    else:
        return jsonify({'http': 400, 'msg': 'Missing parameter ?q='})


def db_init():
    """
    This function returns a database connection object
    """

    try:
        db = pymysql.connect(host=os.environ.get('DB_HOST', 'localhost'),
                             user=os.environ.get('DB_USER', 'root'),
                             passwd=os.environ.get('DB_PASS', 'root'),
                             db=os.environ.get('DB_NAME', 'hpo'))
        return db
    except Exception as e:
        logging.info('ERROR IN db_init() :: ' + str(e))


def db_cursor():
    """
    This function returns a database cursor from db_init()
    """

    try:
        return db_init().cursor(pymysql.cursors.DictCursor)
    except Exception as e:
        logging.info('ERROR IN db_cursor() :: ' + str(e))


def main():
    """
    This function runs the application
    """
    app.run(host=os.environ.get('APP_HOST', 'localhost'),
            port=os.environ.get('APP_PORT', 8080),
            debug=os.environ.get('APP_DEBUG', False))


if __name__ == '__main__':
    main()
