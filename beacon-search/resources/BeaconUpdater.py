import luigi
import logging
import urllib
import gzip
import shutil
import time
import os
from configparser import ConfigParser
from collections import namedtuple

import update_genes
import update_annotations
import update_mutations
import create_database
import add_genotypes

# Set up logging
logging.basicConfig(filename='BeaconUpdater.log',
                    format='%(asctime)s %(message)s',
                    datefmt='%d-%M-%Y %H:%M:%S',
                    level=logging.INFO)


def get_conf(path_to_config):
    """Return configuration variables in dictionary."""
    config = ConfigParser()
    config.read(path_to_config)
    conf = {'user': config.get('database', 'user'),
            'passwd': config.get('database', 'passwd'),
            'db': config.get('database', 'db'),
            'url_genes': config.get('urls', 'genes'),
            'url_annotations': config.get('urls', 'annotations'),
            'url_mutations': config.get('urls', 'mutations'),
            'file_genes': config.get('files', 'f_genes'),
            'file_annotations': config.get('files', 'f_annotations'),
            'file_mutations': config.get('files', 'f_mutations'),
            'file_mimtitles': config.get('files', 'f_mimtitles')}
    conf_named = namedtuple("Config", conf.keys())(*conf.values())
    return conf_named


def download_file(url, dst):
    """Download a file.

    :url: filehost
    :dst: destination file
    """
    return urllib.request.urlretrieve(url, dst)


class CreateNewDatabase(luigi.Task):
    """Create new database for following tasks."""

    config = luigi.Parameter()

    def run(self):
        """Run database creation script."""
        create_database.main([self.config])
        with self.output().open('w') as f:
            f.write(str(self))
        return

    def output(self):
        """Write process completed to trigger next task."""
        return luigi.LocalTarget('luigi_process_dump/CreateNewDatabase.txt')


class GetSourceFile_Genes(luigi.Task):
    """Download gene list."""

    config = luigi.Parameter()

    def requires(self):
        """Wait for previous step to complete."""
        return CreateNewDatabase(config=self.config)

    def run(self):
        """Download gene list."""
        c = get_conf(self.config)
        download_file(c.url_genes, c.file_genes)
        with self.output().open('w') as f:
            f.write(str(self))
        return

    def output(self):
        """Write process completed to trigger next task."""
        return luigi.LocalTarget('luigi_process_dump/GetSourceFile_Genes.txt')


class ParseGenesIntoDatabase(luigi.Task):
    """Parse genes-list and insert them into database."""

    config = luigi.Parameter()

    def requires(self):
        """Wait for previous step to complete."""
        return GetSourceFile_Genes(config=self.config)

    def run(self):
        """Run parse and inserts."""
        update_genes.main([self.config])
        with self.output().open('w') as f:
            f.write(str(self))
        return

    def output(self):
        """Write process completed to trigger next task."""
        return luigi.LocalTarget('luigi_process_dump/ParseGenesIntoDatabase.txt')


class GetSourceFile_Annotations(luigi.Task):
    """Download disease information."""

    config = luigi.Parameter()

    def requires(self):
        """Wait for previous step to complete."""
        return ParseGenesIntoDatabase(config=self.config)

    def run(self):
        """Download disease list."""
        c = get_conf(self.config)
        download_file(c.url_annotations, c.file_annotations)
        with self.output().open('w') as f:
            f.write(str(self))
        return

    def output(self):
        """Write process completed to trigger next task."""
        return luigi.LocalTarget('luigi_process_dump/GetSourceFile_Annotations.txt')


class ParseAnnotationsIntoDatabase(luigi.Task):
    """Parse disease-list and insert them into database."""

    config = luigi.Parameter()

    def requires(self):
        """Wait for previous step to complete."""
        return GetSourceFile_Annotations(config=self.config)

    def run(self):
        """Run parse and inserts."""
        update_annotations.main([self.config])
        with self.output().open('w') as f:
            f.write(str(self))
        return

    def output(self):
        """Write process completed to trigger next task."""
        return luigi.LocalTarget('luigi_process_dump/ParseAnnotationsIntoDatabase.txt')


class GetSourceFile_Mutations(luigi.Task):
    """Download mutations list."""

    config = luigi.Parameter()

    def requires(self):
        """Wait for previous step to complete."""
        return ParseAnnotationsIntoDatabase(config=self.config)

    def run(self):
        """Download and unzip file packed file."""
        print('NOTICE: Downloading and unzipping a very large XML file. '
              'This step may take a few minutes to complete.')
        c = get_conf(self.config)
        # Always download the latest version
        date_latest = time.strftime('%Y-%m')
        url = c.url_mutations.replace('DATEOFLATESTBUILD', date_latest, 1)
        download_file(url, c.file_mutations + '.gz')
        with open(c.file_mutations, 'wb') as f_out, gzip.open(c.file_mutations + '.gz', 'rb') as f_in:
            shutil.copyfileobj(f_in, f_out)
        with self.output().open('w') as f:
            f.write(str(self))
        return

    def output(self):
        """Write process completed to trigger next task."""
        return luigi.LocalTarget('luigi_process_dump/GetSourceFile_Mutations.txt')


class ParseMutationsIntoDatabase(luigi.Task):
    """Parse mutations-list into database."""

    config = luigi.Parameter()

    def requires(self):
        """Wait for previous step to complete."""
        return GetSourceFile_Mutations(config=self.config)

    def run(self):
        """Run parse and inserts."""
        print('NOTICE: Parsing a very large XML file into MySQL. '
              'This step may take up to 4 hours to complete.')
        update_mutations.main([self.config])
        with self.output().open('w') as f:
            f.write(str(self))
        return

    def output(self):
        """Write process completed to trigger next task."""
        return luigi.LocalTarget('luigi_process_dump/ParseMutationsIntoDatabase.txt')


class AddGenotypesIfAvailable(luigi.Task):
    """Parse genotypes-list into database."""

    # This step is optional and requires data access permission
    # to mimTitles.txt from OMIM

    config = luigi.Parameter()

    def requires(self):
        """Wait for previous step to complete."""
        return ParseMutationsIntoDatabase(config=self.config)

    def run(self):
        """Run parse and inserts."""
        print('OPTIONAL: Looking for file containing OMIM titles from config.ini.')
        c = get_conf(self.config)
        if os.path.exists(c.file_mimtitles):
            print('INFO: File was found, commencing updates, this step may take 1-2 hours to complete.')
            add_genotypes.main([self.config])
        else:
            print('WARNING: File was not found. Consider applying for data access from https://omim.org/.')
        with self.output().open('w') as f:
            f.write(str(self))
        return

    def output(self):
        """Write process completed to trigger next task."""
        return luigi.LocalTarget('luigi_process_dump/AddGenotypesIfAvailable.txt')


class CreateDatabaseDump(luigi.Task):
    """Create database dump from the database and inserts created in previous tasks."""

    config = luigi.Parameter()

    def requires(self):
        """Wait for previous step to complete."""
        return AddGenotypesIfAvailable(config=self.config)

    def run(self):
        """Start dumping process."""
        c = get_conf(self.config)
        cmd = "mysqldump -u " + c.user + " -p" + c.passwd + " " + c.db + " > " + c.db + '.sql'
        os.system(cmd)
        with self.output().open('w') as f:
            f.write(str(self))
        return

    def output(self):
        """Write process completed to finish task workflow."""
        return luigi.LocalTarget('luigi_process_dump/CreateDatabaseDump.txt')
