#!/usr/bin/env python3.4


from flask import Flask, jsonify, request
from flask_cors import CORS
import pymysql
import logging
import os


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


@app.route("/api")
def api():
    """
    This function implements query string type search for the API

    --explain how it works--
    """

    query = {}
    assemblies = ['GRCh37', 'GRCh38']

    # Query for Diseases
    if request.args.get('disease'):
        query['disease'] = request.args.get('disease')
    
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
    elif request.args.get('gene') and request.args.get('assembly'):  # Query for Genes
        query['gene'] = request.args.get('gene')
        query['assembly'] = request.args.get('assembly')
    
        if query['gene'] and any(a in query['assembly'] for a in assemblies):
            try:
                cur = db_cursor()
                cur.execute('SELECT chr, chrpos, ref, alt, assembly, accession, accession_ver '
                            'FROM changes WHERE entrez=(SELECT entrez FROM genes WHERE gene=%s) '
                            'AND assembly=%s ORDER BY chrpos;', (query['gene'], query['assembly'],))
                results = cur.fetchall()
                if len(results) == 0:
                    return jsonify({'http': 404, 'msg': 'gene not found'})
                else:
                    return jsonify(results)
            except Exception as e:
                logging.info('ERROR IN /api?gene=' + query['gene'] + '&assembly=' + query['assembly'] + 
                            ' :: ' + str(e))
            finally:
                cur.connection.close()
        else:
            return jsonify({'http': 400, 'msg': 'Missing gene, or incorrect assembly.'})
    else:
        return jsonify({'http': 400, 'msg': 'Invalid query string combinations.'})


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
