#!/usr/bin/env python3

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
            'source': config.get('files', 'f_mimtitles')}
    conf_named = namedtuple("Config", conf.keys())(*conf.values())
    return conf_named


def db_init(hostname, username, password, database):
    """Connect to database and return connection object."""
    db = pymysql.connect(host=hostname,
                         user=username,
                         passwd=password,
                         db=database)
    return db


def generate_omim_list(omimfile):
    """
    Generate dictionary of genotype id-name key-value pairs.

    :omimfile: path to mimTitles.txt
    """
    omimlist = {}
    with open(omimfile) as file:
        for line in file:
            # Clean up lines and pick first occurrence of titles
            lineparts = line.strip().split('\t')
            genotype_id = 'OMIM:' + lineparts[1]
            genotype_name = lineparts[2].split(';')[0]
            omimlist[genotype_id] = genotype_name
    return omimlist


def add_genotypes(db, omimlist):
    """
    Update genotype names to database according to genotype IDs.

    :db: database connection object
    :omimlist: list of titles from generate_omim_list()
    """
    cur = db.cursor()
    timestart = time.time()

    # Tracking variables for terminal
    i = 0
    updates = 0

    try:
        for item in omimlist:
            cur.execute('UPDATE annotations SET genotype=%s '
                        'WHERE disease_id=%s AND genotype IS NULL;',
                        (omimlist[item], item,))
            i += 1
            if i == 1000:
                updates += i
                i = 0
                db.commit()
                run_time = round(time.time()-timestart, 2)
                sys.stdout.write("{0}/{1}  genotype titles updated. Total runtime: {2} s.\r".format(str(updates),
                                                                                                    str(len(omimlist),
                                                                                                    run_time)))
                sys.stdout.flush()
    except Exception as e:
        print(str(e))
    finally:
        db.commit()  # Last commit for less than 1000 items
        cur.connection.close()
        print('DONE: Runtime: %.2f' % round(time.time()-timestart, 2) + ' s.\n')
    return


def parse_arguments(arguments):
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('config',
                        help='path to configuration file.')
    return parser.parse_args(arguments)


def main(arguments=None):
    """Run updater."""
    # Get configuration variables and initiate db connection
    args = parse_arguments(arguments)
    config = get_conf(args.config)
    db = db_init(config.host,
                 config.user,
                 config.passwd,
                 config.db)
    # Start the update process
    omimlist = generate_omim_list(config.source)
    add_genotypes(db, omimlist)


if __name__ == '__main__':
    main()
