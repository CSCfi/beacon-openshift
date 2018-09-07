## Resources for Beacon Search API

This directory contains an automated [luigi](https://github.com/spotify/luigi) workflow, which creates a database and populates it with relevant data, that the Beacon Search API may serve.

#### Data Ownership Declaration
The database is aggregated with data extracted from a handful of open source services.

##### [Human Phenotype Ontologies](https://hpo.jax.org/app/)
* HPO IDs;
* HPO Terms (phenotype names);
* OMIM IDs (genotype names);
* Disease-gene relations.

##### [National Center for Biotechnology Information](https://www.ncbi.nlm.nih.gov/clinvar/)
* Chromosomal variants;
* Variant-gene relations.

##### [Online Mendelian Inheritance in Man](https://omim.org/)
* OMIM Titles (genotype names).

(Optional resource, this data requires individual access permissions)

#### Requirements
* Python3.4+
* Running MySQL server;

#### Setup
Install required python libraries.
```
cd resources
pip3 install -r requirements.txt
```
In one terminal start the luigi daemon.
```
luigid
```
In another terminal run the workflow.
```
cd resources
luigi --module BeaconUpdater CreateDatabaseDump --config config.ini
```
**NOTICE:** This workflow may take 4-6 hours to complete and generates a database with more than a million rows (~70 MB .sql).
#### Workflow Tasks
The workflow consists of several tasks that it must completed. Tasks are processed in order, and the system checks for completed tasks before moving onto next tasks. The process can be followed from the terminal you run the `luigi` command from, or from the luigi GUI that is served at `localhost:8082`.

Workflow steps:
* 1: Create a new database with name according to current month and year;
* 2: Download gene list from HPO;
* 3: Parse gene list and insert entries into the database;
* 4: Download annotation list from HPO (containing disease-gene relations);
* 5: Parse annotation list and insert entries into the database;
* 6: Download chromosomal variant list from NCBI ClinVar;
* 7: Parse chromosomal variant list and insert entries into the database;
* 8: _OPTIONAL STEP: Parse OMIM Titles (genotypes according to OMIM IDs) to database (requires permissions and datafile from OMIM)_;
* 9: Generate database dump file that can be used in a database container for the Beacon Search API.
