#!/usr/bin/env python3.4

import pymysql
import time
import argparse
from configparser import ConfigParser
from collections import namedtuple
from lxml import etree


# global tracker that checks if xml-parser is inside a specific element
inelem = [False, None]


def fast_iter(context, func, genes, keys, triggers, db):
    """
    Parse through an XML file and fires processing functions for elements.

    :context: XML file
    :func: process_element() function
    :genes: list of genes that are being searched for
    :keys: mutation descriptions
    :triggers: parsing trigger tags
    :db: database connection object
    """
    start = time.time()  # runtime start
    timestamp_file = time.strftime('%d-%m-%Y_%H-%M-%S')
    timestamp_pretty = time.strftime('%d.%m.%Y %H:%M:%S')

    print('INFO: PROCESS STARTED at ' + str(timestamp_pretty) + '\n')
    i = 0  # iterator counter

    for event, elem in context:
        i += 1
        func(event, elem, genes, keys, triggers, db)
        elem.clear()
        for ancestor in elem.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
    del context

    print('INFO: ' + str(i) + ' xml elements read, runtime: %.2f' % round(time.time()-start, 2) + ' s.')
    print('INFO: PROCESS ENDED at ' + str(time.strftime('%d.%m.%Y %H:%M:%S')))


def process_element(event, elem, genes, keys, triggers, db):
    """
    Process XML elements and insert genetic mutations into database if they are found.

    :event: XML start and end tag fires an event
    :elem: XML tag for current element
    :genes: list of genes that are searched from <Title>
    :keys: mutation descriptions
    :triggers: parsing trigger tags
    :db: database connection object
    """
    global inelem

    # opening tag :trigger_start: found with :gene: inside, start reading
    if event is 'start' and triggers['start'] in elem.tag:
        try:
            for gene in genes:
                if gene[1] in elem.text:
                    inelem = [True, gene]
        except Exception:
            pass

    # closing tag :trigger_end: found, stop reading
    if inelem[0] is True and event is 'end' and triggers['end'] in elem.tag:
        inelem = [False, None]

    # reading lines from element
    if inelem[0] is True and 'SequenceLocation' in elem.tag:
        if triggers['vcf'] in elem.attrib:

            # write variables to dictionary and insert them
            results = {row[0]: row[1] for row in elem.attrib.items() if row[0] in keys}
            insert_to_db(db, inelem[1][0], results)


def insert_to_db(db, entrez, items):
    """Insert received items into database.

    :db: database connection object
    :entrez: gene identifier
    :items: mutation description
    """
    params = [entrez,
              items['Accession'],
              items['AssemblyAccessionVersion'],
              items['Assembly'],
              items['Chr'],
              items['positionVCF'],
              items['referenceAlleleVCF'],
              items['alternateAlleleVCF']]

    cur = db.cursor()
    cur.execute('INSERT IGNORE INTO changes '
                'VALUES (%s, %s, %s, %s, %s, %s, %s, %s);',
                params)
    db.commit()
    cur.close()


def gene_catalogue(db):
    """Get list of genes from database."""
    cur = db.cursor()
    cur.execute('SELECT entrez, gene '
                'FROM genes;')
    results = cur.fetchall()

    # format into single list
    genes = []
    for item in results:
        genes.append([item[0], item[1]])
    return genes


def get_conf(path):
    """Return configuration variables in dictionary."""
    config = ConfigParser()
    config.read(path)

    conf = {'host': config.get('database', 'host'),
            'user': config.get('database', 'user'),
            'passwd': config.get('database', 'passwd'),
            'db': config.get('database', 'db'),
            'file': config.get('files', 'f_mutations')}

    conf_named = namedtuple("Config", conf.keys())(*conf.values())

    return conf_named


def db_init(hostname, username, password, database):
    """Connect to database and return connection object."""
    db = pymysql.connect(host=hostname,
                         user=username,
                         passwd=password,
                         db=database)

    return db


def main(arguments=None):
    """Run XML parser and database populator."""
    # arguments
    args = parse_arguments(arguments)

    # database
    config = get_conf(args.config)
    db = db_init(config.host,
                 config.user,
                 config.passwd,
                 config.db)

    # path to xml file
    file = config.file

    # list of genes
    genes = gene_catalogue(db)

    # constants for parsing
    keys = ['Assembly',
            'AssemblyAccessionVersion',
            'Accession',
            'Chr',
            'positionVCF',
            'referenceAlleleVCF',
            'alternateAlleleVCF']
    triggers = {'start': 'Title',
                'end': 'ClinVarSet',
                'seq': 'SequenceLocation',
                'vcf': 'positionVCF'}

    # open xml file, start parsing
    context = etree.iterparse(file, events=('start', 'end'))
    fast_iter(context,
              process_element,
              genes,
              keys,
              triggers,
              db)


def parse_arguments(arguments):
    """Parse arguments from command line."""
    parser = argparse.ArgumentParser(description='Parses ClinVar XML for '
                                     'chromosome mutation HGVS markers '
                                     'and inserts them into a MySQL database')

    parser.add_argument('config',
                        help='Path to config.ini')

    return parser.parse_args(arguments)


if __name__ == '__main__':
    main()
