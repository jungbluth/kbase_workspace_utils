# KBase Workspace Utils

This is a standalone, installable Python package for downloading and uploading data using the KBase Workspace. You can get it with pip:

```py
pip install kbase_workspace_utils
```

In the Dockerfile of your KBase app or persistent ("dynamic") service, you can add a line like the following:

```
RUN pip install kbase_workspace_utils==0.0.1
```

In an app, it's recommended to lock the version of the package you install.

## Usage

### Setup

You need to set the environment variable `KBASE_WORKSPACE_URL` to a valid KBase workspace server (for example: `https://appdev.kbase.us/services/ws`).

### Download any object

To get any object, regardless of its type, use the `download` function

```py
from kbase_workspace_utils import download

download(reference, path=file_path)
```

Note that there must not be an existing file at the path that you provide.

### Download a Reads type to a fastq file

To download a workspace reference of a KBase "Reads" object to a fastq file, set the `type` options
to `"Reads"`:

```py
# Pass in a file path where you want the fastq to be saved
download(reference, path=fastq_file_path, type="Reads")
```

Note that the there must not be an existing file at the path that you provide.

### Download an Assembly type to fasta

To download an Assembly object to a fasta file, set the `type` option to `"Assembly"`

```py
download(reference, path=fasta_file_path, type="Assembly")
```

Note that there must not be an existing file at the path that you provide.

### Download a Genome type as a GFF file

To download a Genome type to a GFF file, set `type` to `"Genome"` and `format` to `"gff"`:

```py
download(reference, path=gff_file_path, type="Genome", format="gff")
```

Note that there must not be an existing file at the path that you provide.

### Download a Genome type as a Genbank file

To download a Genome type to a Genbank formatted file, set `type` to `"Genome"` and `format` to `"genbank"`

```py
from kbase_workspace_utils import download_genome

download_genome(reference, path=genbank_file_path, format="genbank", type="Genome")
```

Note that there must not be an existing file at the path that you provide.

## Development

You can use a `.env` file for env vars:

```sh
$ cp .env.example .env
```

Clone the repo, activate a virtualenv, and install dependenceis:

```sh
$ python -m venv env
$ source env/bin/activate
$ pip install --upgrade -r requirements.txt -r dev-requirements.txt
```

Then, run tests with:

```sh
$ make test
```

### Build the package

### Project anatomy

* The main package source code lives in `src/kbase_workspace_utils`
* Tests live in `src/kbase_workspace_utils/test`
