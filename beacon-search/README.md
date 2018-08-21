## Beacon Search

This is a prototype suggestion API that can be used to find relevant disease-gene-variant relations. The database behind this API has been aggregated with data extracted from [HPO](https://hpo.jax.org/app/), [NCBI ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) and [OMIM](https://omim.org/), all data used in this prototype suggestion API can be found from the providers' respective documentation pages. The database creation scripts will be released at a later date.

### Endpoints
| Endpoint | Description |
| --- | --- |
| `/` | Greets user with the name of the service. |
| `/api?` | Multipurpose API endpoint serving disease and gene discovery services. Examples below. |
| `/autocomplete?` | Autocomplete API endpoint which suggests diseases and genes as user types in characters. |

#### Example Queries

* `/api?type=disease&query=Alzheimer` - will use default pagination settings;
* `/api?type=gene&query=APOE,GRCh38` - will use default pagination settings;
* `/api?type=gene&query=APOE,GRCh38&page=1&resultsPerPage=20`  - custom pagination request;
* `/autocomplete?q=Migraine`.

#### Example Responses

Response for `/api?type=disease&query=<disease>`:
```
{
  "pagination": {
    "currentPage": int,
    "totalPages": int,
    "totalResults": int
  },
  "results": [
    {
      "gene": string,
      "genotype_id": string,
      "genotype_name": string,
      "phenotype_id": string,
      "phenotype_name": string
    }
  ]
}
```

Response for `/api?type=gene&query=<gene>,<assembly>`:

```
{
  "pagination": {
    "currentPage": int,
    "totalPages": int,
    "totalResults": int
  },
  "results": [
    {
      "accession": string,
      "accession_ver": string,
      "alt": string,
      "assembly": string,
      "chr": string,
      "chrpos": string,
      "ref": string
    }
  ]
}
```

Response for `/autocomplete?q=<keyword>`:

```
[
  {
    "name": string,
    "relatedGenes": int,
    "type": "disease",
    "variations": int
  },
  {
    "name": string,
    "type": "gene",
    "variations": int
  }
]
```

#### Environment Variables
The API requires some configuration variables stored as environment variables in Openshift. If no environment variables are found, defaults are used instead. Below is a table listing all used environment variables with their default values and a brief description.

| ENV | Default | Description |
| --- | --- | --- |
| `APP_HOST` | `localhost` | Web server host address inside the Openshift container. This is not the same as the external URL. |
| `APP_PORT` | `8080` | Web server port inside the Openshift container. |
| `APP_DEBUG` | `False` | If set to `True`, Flask will print events into the Openshift terminal. |
| `DB_HOST` | `localhost` | Database hostname. |
| `DB_USER` | `root` | Database username with sufficient permissions. |
| `DB_PASS` | `root` | Password for `DB_USER`. |
| `DB_NAME` | `hpo` | Database name that contains relevant tables. |


### Run and Build

#### Run from the command line

The application can be run as (the application will default to the environment variable values specified above):

```
pip install -r requirements.txt
python app.py
```

##### Build using s2i

Create container for `beacon-search`
```
s2i build git@github.com:CSCfi/beacon-openshift.git \
    --context-dir=beacon-search \
    centos/python-35-centos7 \
    beacon-search
```

Run the created container:
```
docker run -p 8080:8080 beacon-search
```
