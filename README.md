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

Two environment variables are requiredc to be set:
* `KBASE_ENV`: one of "appdev", "ci", or "prod"
* `KB_AUTH_TOKEN`: an authentication token

### Download any object

To get any object, regardless of its type, use the `download_obj` function

```py
from kbase_workspace_utils import download

obj = download_obj(ref=ws_reference)
```

The return value will be a dictionary of data representing the object.

### Download a Reads to a fastq file

To download a workspace reference of a KBase "Reads" object to a fastq file, use the `download_reads` function.

```py
from kbase_workspace_utils import download_reads

# Pass in a file path where you want the fastq to be saved
download_reads(ref=ws_reference, path=fastq_file_path)
```

This will return the full path of the downloaded file, with the original filename from the workspace.

Note that the there must not be an existing file at the path that you provide.

### Download an Assembly to a fasta file

To download an Assembly object to a fasta file, use `download_assembly` and pass in a parent directory:

```py
from kbase_workspace_utils import download_assembly

path = download_assembly(ref=ws_reference, file_dir=file_directory)
```

This will return the full path of the downloaded file, with the original filename from the workspace.

Note that there must not be an existing file at the path that you provide.

### Download a Genome type as a GFF or Genbank file

To download a Genome to a file, use the `download_genome` function.

To specify the format -- GFF or Genbank -- set the `format` arg to "gff" or "Genbank. It defaults to "Genbank".

```py
from kbase_workspace_utils import download_genome

path = download_genome(ref=ws_reference, file_dir=directory, format="gff")
```

Will return the full path of the downloaded file, with the original filename from the workspace.

Note that there must not be an existing file at the path that you provide.

## Development

You can use a `.env` file for env vars. Set `KB_AUTH_TOKEN` and `KBASE_ENV` to one of "ci", 
"appdev", or "prod".

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

TODO -- setup.py, bdist_wheel, etc

### Project anatomy

* The main package source code lives in `src/kbase_workspace_utils`. See `src/kbase_workspace_utils/__init__.py` for a list of all exported functions.
* Tests live in `src/kbase_workspace_utils/test`
