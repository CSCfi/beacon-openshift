#!/usr/bin/env python3.4

import pymysql
import argparse
from configparser import ConfigParser
from collections import namedtuple


def get_conf(path):
    """Return configuration variables in dictionary."""
    config = ConfigParser()
    config.read(path)
    conf = {'host': config.get('database', 'host'),
            'user': config.get('database', 'user'),
            'passwd': config.get('database', 'passwd'),
            'db': config.get('database', 'db'),
            'source': config.get('files', 'f_genes')}
    conf_named = namedtuple("Config", conf.keys())(*conf.values())
    return conf_named


def db_init(hostname, username, password, database):
    """Connect to database and return connection object."""
    db = pymysql.connect(host=hostname,
                         user=username,
                         passwd=password,
                         db=database)
    return db


def pop(db, source):
    """Populate database table genes with gene data.

    :db: database connection object
    :source: source file containing data to be inserted
    """
    cur = db.cursor()

    with open(source, 'r') as file:
        collection = {}
        next(file)  # skip header
        for line in file:
            id = line.strip().split('\t')[0]
            gene = line.strip().split('\t')[1]

            if gene not in collection:
                collection[id] = gene

        for k, v in collection.items():
            params = [k, v]

            try:
                cur.execute('INSERT INTO genes '
                            'VALUES (%s, %s);',
                            params)
            except IndexError:
                continue

        db.commit()
    cur.connection.close()
    return


def parse_arguments(arguments):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('config',
                        help='path to configuration file.')
    return parser.parse_args(arguments)


def main(arguments=None):
    """Run database populator."""
    # Get configuration variables and initiate db connection
    args = parse_arguments(arguments)
    config = get_conf(args.config)
    db = db_init(config.host,
                 config.user,
                 config.passwd,
                 config.db)

    # populate database with sourcefile
    pop(db, config.source)


if __name__ == '__main__':
    main()
