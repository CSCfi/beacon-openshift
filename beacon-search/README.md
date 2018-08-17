# beacon-search

This is a prototype suggestion API that can be used to find relevant disease-gene-variant relations. The database behind this API has been aggregated with data extracted from [HPO](https://hpo.jax.org/app/), [NCBI ClinVar](https://www.ncbi.nlm.nih.gov/clinvar/) and [OMIM](https://omim.org/), all data used in this prototype suggestion API can be found from the providers' respective documentation pages. The database creation scripts will be released at a later date.


##### Endpoints
| Endpoint | Description |
| --- | --- |
| `/` | Greets user with the name of the service. |
| `/api?` | Multipurpose API endpoint serving disease and gene discovery services. Examples below. |
| `/autocomplete?` | Autocomplete API endpoint which suggests diseases and genes as user types in characters. |

##### Example queries
```/api?type=disease&query=Alzheimer```

```/api?type=gene&query=APOE,GRCh38```  # Will use default pagination settings

```/api?type=gene&query=APOE,GRCh38&page=1&resultsPerPage=20```  # Custom pagination request

```/autocomplete?q=Migraine```

##### Example responses
```
/api?type=disease&query=<disease>

[
  {
    "gene": string,
    "genotype_id": string,
    "genotype_name": string,
    "phenotype_id": string,
    "phenotype_name": string
  }
]
```

```
/api?type=gene&query=<gene>,<assembly>

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

```
/autocomplete?q=<keyword>

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

##### Environment variables in Openshift
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
