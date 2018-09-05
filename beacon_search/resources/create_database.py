#!/usr/bin/env python3.4

import pymysql
import argparse
import time
from configparser import ConfigParser
from collections import namedtuple


def get_conf(path):
    """Return configuration variables in dictionary."""
    config = ConfigParser()
    config.read(path)
    conf = {'host': config.get('database', 'host'),
            'user': config.get('database', 'user'),
            'passwd': config.get('database', 'passwd')}
    conf_named = namedtuple("Config", conf.keys())(*conf.values())
    return conf_named


def db_init(hostname, username, password):
    """Connect to database and return connection object."""
    db = pymysql.connect(host=hostname,
                         user=username,
                         passwd=password)
    return db


def db_create(db, dbname, confile):
    """Create new database according to year and month.

    :db: database connection object
    :dbname: database name
    :confile: path to config.ini
    """
    try:
        cur = db.cursor()
        sql = '''
                CREATE DATABASE IF NOT EXISTS dbname;
                USE dbname;

                CREATE TABLE annotations (
                    id INT NOT NULL AUTO_INCREMENT,
                    disease_id VARCHAR(32),
                    gene VARCHAR(16),
                    entrez INT,
                    hpo_id VARCHAR(16),
                    disease VARCHAR(128),
                    genotype VARCHAR(128),
                    PRIMARY KEY (id)
                );

                CREATE TABLE genes (
                    entrez INT NOT NULL,
                    gene VARCHAR(16) NOT NULL,
                    PRIMARY KEY (entrez)
                );

                CREATE TABLE changes (
                    entrez INT NOT NULL,
                    accession VARCHAR(32),
                    accession_ver VARCHAR(32),
                    assembly VARCHAR(16),
                    chr VARCHAR(16),
                    chrpos VARCHAR(32),
                    ref VARCHAR(8192),
                    alt VARCHAR(8192),
                    FOREIGN KEY (entrez) REFERENCES genes (entrez)
                );
              '''
        # put :dbname: into :sql:
        sql = sql.replace('dbname', dbname, 2)
        sql.rstrip()  # remove new lines "\n"
        cur.execute(sql)
    except Exception as e:
        print(str(e))
    else:
        # write dbname to config.ini
        f = open(confile, 'r')
        lines = f.readlines()
        f.close()
        f = open(confile, 'w')
        for line in lines:
            if 'db=' in line:
                f.write('db=' + dbname + '\n')
            else:
                f.write(line)
    finally:
        db.commit()
        cur.connection.close()


def parse_arguments(arguments):
    """Parse arguments from command line."""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('config',
                        help='path to configuration file.')
    return parser.parse_args(arguments)


def main(arguments=None):
    """Run database creation."""
    # configuration and database connection
    args = parse_arguments(arguments)
    config = get_conf(args.config)
    db = db_init(config.host,
                 config.user,
                 config.passwd)
    # generate database name according to month and year and start creation
    dbname = 'hpo_' + time.strftime('%Y_%m')
    db_create(db, dbname, args.config)


if __name__ == '__main__':
    main()
