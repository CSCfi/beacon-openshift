#!usr/bin/env python3.4


from flask import Flask, jsonify, request
from flask_cors import CORS

'''This is a simple mock-up service with no configurations.'''

# Initialize web app
app = Flask(__name__)
CORS(app)


@app.route("/api/true")
def mock_true():
    """Return truthy response."""
    return jsonify({'beaconId': 'Always True',
                    'apiVersion': '1.0.0',
                    'exists': True,
                    'error': None,
                    'alleleRequest': {'referenceName': request.args.get('referenceName'),
                                      'start': request.args.get('start'),
                                      'startMin': request.args.get('startMin'),
                                      'startMax': request.args.get('startMax'),
                                      'end': request.args.get('end'),
                                      'endMin': request.args.get('endMin'),
                                      'endMax': request.args.get('endMax'),
                                      'referenceBases': request.args.get('referenceBases'),
                                      'alternateBases': request.args.get('alternateBases'),
                                      'variantType': request.args.get('variantType'),
                                      'assemblyId': request.args.get('assemblyId'),
                                      'datasetIds': request.args.get('datasetIds'),
                                      'includeDatasetResponses': request.args.get('includeDatasetsResponses')},
                    'datasetAlleleResponses': [{'datasetId': 'EGAD000000000011',
                                                'exists': True,
                                                'frequency': 0.01,
                                                'variantCount': 1,
                                                'callCount': 3000,
                                                'sampleCount': 1200,
                                                'note': 'Mockup dataset 1',
                                                'externalUrl': 'https://beacon-ui-beacon.rahtiapp.fi/',
                                                'info': {'accessType': 'PUBLIC'},
                                                'error': None},
                                                {'datasetId': 'EGAD000000000012',
                                                 'exists': True,
                                                 'frequency': 0.00123,
                                                 'variantCount': 1,
                                                 'callCount': 15000,
                                                 'sampleCount': 8500,
                                                 'note': 'Mockup dataset 2',
                                                 'externalUrl': 'https://beacon-ui-beacon.rahtiapp.fi/',
                                                 'info': {'accessType': 'REGISTERED'},
                                                 'error': None},
                                                {'datasetId': 'EGAD000000000013',
                                                 'exists': True,
                                                 'frequency': 0.00076,
                                                 'variantCount': 1,
                                                 'callCount': 1400,
                                                 'sampleCount': 500,
                                                 'note': 'Mockup dataset 3',
                                                 'externalUrl': 'https://beacon-ui-beacon.rahtiapp.fi/',
                                                 'info': {'accessType': 'PUBLIC'},
                                                 'error': None}]})


@app.route("/api/false")
def mock_false():
    """Return falsy response."""
    return jsonify({'beaconId': 'Always False',
                    'apiVersion': '1.0.0',
                    'exists': False,
                    'error': None,
                    'alleleRequest': {'referenceName': request.args.get('referenceName'),
                                      'start': request.args.get('start'),
                                      'startMin': request.args.get('startMin'),
                                      'startMax': request.args.get('startMax'),
                                      'end': request.args.get('end'),
                                      'endMin': request.args.get('endMin'),
                                      'endMax': request.args.get('endMax'),
                                      'referenceBases': request.args.get('referenceBases'),
                                      'alternateBases': request.args.get('alternateBases'),
                                      'variantType': request.args.get('variantType'),
                                      'assemblyId': request.args.get('assemblyId'),
                                      'datasetIds': request.args.get('datasetIds'),
                                      'includeDatasetResponses': request.args.get('includeDatasetsResponses')},
                    'datasetAlleleResponses': [{'datasetId': 'EGAD000000000002',
                                                'exists': False,
                                                'frequency': 0,
                                                'variantCount': 0,
                                                'callCount': 0,
                                                'sampleCount': 0,
                                                'note': 'Mockup dataset',
                                                'externalUrl': None,
                                                'info': {'accessType': 'PUBLIC'},
                                                'error': None}]})


@app.route("/api/null")
def mock_null():
    """Return null response."""
    return jsonify({'beaconId': 'Always Null',
                    'apiVersion': '1.0.0',
                    'exists': None,
                    'error': None,
                    'alleleRequest': {'referenceName': request.args.get('referenceName'),
                                      'start': request.args.get('start'),
                                      'startMin': request.args.get('startMin'),
                                      'startMax': request.args.get('startMax'),
                                      'end': request.args.get('end'),
                                      'endMin': request.args.get('endMin'),
                                      'endMax': request.args.get('endMax'),
                                      'referenceBases': request.args.get('referenceBases'),
                                      'alternateBases': request.args.get('alternateBases'),
                                      'variantType': request.args.get('variantType'),
                                      'assemblyId': request.args.get('assemblyId'),
                                      'datasetIds': request.args.get('datasetIds'),
                                      'includeDatasetResponses': request.args.get('includeDatasetsResponses')},
                    'datasetAlleleResponses': [{'datasetId': 'EGAD000000000000',
                                                'exists': None,
                                                'frequency': 0,
                                                'variantCount': 0,
                                                'callCount': 0,
                                                'sampleCount': 0,
                                                'note': 'Mockup dataset',
                                                'externalUrl': None,
                                                'info': {'accessType': 'PUBLIC'},
                                                'error': None}]})


if __name__ == "__main__":
    """Start the web server."""
    app.run(host='0.0.0.0', port=8080)
