#!/usr/bin/env python3.4

import pymysql
import sys
import time
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
            'source': config.get('files', 'f_annotations')}
    conf_named = namedtuple("Config", conf.keys())(*conf.values())
    return conf_named


def db_init(hostname, username, password, database):
    """Connect to database and return connection object."""
    db = pymysql.connect(host=hostname,
                         user=username,
                         passwd=password,
                         db=database)
    return db


def estimate(source):
    """Estimate runtime."""
    print('Calculating number of lines in file.')
    i = 0
    with open(source) as file:
        for line in file:
            i += 1
    print(str(i) + ' lines in file. Estimated insertion time for file: %.2f' % round(i*0.0003) + ' s.\n')


def populate(db, source):
    """Populate database table annotations with disease informations."""
    cur = db.cursor()
    timestart = time.time()
    i = 0
    j = 0
    with open(source) as file:
        next(file)  # skip header
        for line in file:
            # remove \t and \n from string and format string to list
            params = line.strip().split('\t')

            # avoid empty lines
            try:
                # first NULL is index, second NULL is genotype placeholder
                cur.execute('INSERT INTO annotations '
                            'VALUES (NULL, %s, %s, %s, %s, %s, NULL);',
                            params)
                i += 1
            except IndexError:
                continue

            # log progress to console
            if i == 1000:
                db.commit()  # commit 1000 lines at once
                i = 0
                j += 1
                sys.stdout.write(str(j) + 'k lines inserted. Total runtime: %.2f' % round(time.time()-timestart, 2) + ' s.\r')
                sys.stdout.flush()
        db.commit()  # final commit for less than 1000 lines
    cur.connection.close()
    return '\nDone'


def parse_arguments(arguments):
    """Parse arguments from command line."""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('config',
                        help='path to configuration file.')
    return parser.parse_args(arguments)


def main(arguments=None):
    """Run database populator."""
    # configuration and database connection
    args = parse_arguments(arguments)
    config = get_conf(args.config)
    db = db_init(config.host,
                 config.user,
                 config.passwd,
                 config.db)
    # run process
    estimate(config.source)
    populate(db, config.source)


if __name__ == '__main__':
    main()
