# KBase Workspace Utils

This is a standalone, installable Python package for downloading and uploading data using the KBase Workspace. You can get it with pip using the Anaconda registry:

```py
pip install -i https://pypi.anaconda.org/kbase/simple kbase-workspace-utils==0.0.2
```

## Usage and API

### Setup

Two environment variables are required to be set:
* `KBASE_ENV`: one of "appdev", "ci", or "prod"
* `KB_AUTH_TOKEN`: a KBase authentication token

### Download any object

To get any workspace object, regardless of its type, use the `download_obj` function

```py
from kbase_workspace_utils import download_obj

obj = download_obj(ref=ws_reference)
```

The return value will be a dictionary of data representing the object.

### Download Reads to a fastq file

To download a workspace reference of a KBase "Reads" object to a fastq file, use the `download_reads` function.

```py
from kbase_workspace_utils import download_reads

# Pass in a file path where you want the fastq to be saved
paths = download_reads(ref=ws_reference, save_dir=directory_to_save_file)
```

This will return an array of file paths according to the following rules:

* If the reads are single ended, then you will get one filepath of `ws_obj_name.single.fastq`
* If the reads are paired ends and interleaved, then you will get one filepath of `ws_obj_name.paired.interleaved.fastq`
* If the reads are paired ends and not interleaved, then you will get two filepaths, one of `ws_obj_name.paired.fwd.fastq` for left reads and one of `ws_obj_name.paired.rev.fastq` for right reads.

### Download an Assembly to a fasta file

To download an Assembly object to a fasta file, use `download_assembly` and pass in a parent directory:

```py
from kbase_workspace_utils import download_assembly

path = download_assembly(ref=ws_reference, save_dir=directory_to_save_file)
```

This will return the full path of the downloaded file, with the original name of the object from the workspace and the `.fasta` extension.

This also works on legacy ContigSet types.

### Get the Assembly reference from a Genome object

Use the `get_assembly_from_genome` function to get the assembly (or ContigSet) reference from a Genome object:

```py
from kbase_workspace_utils import get_assembly_from_genome

assembly_ref = get_assembly_from_genome(genome_ref)
```

The return value will be a reference path with the format `genome_ref;assembly_ref`. You can use `download_assembly(assembly_ref)` to get the fasta file.

### Download a Genome type as a GFF or Genbank file

> This is not implemented yet

To download a Genome to a file, use the `download_genome` function.

To specify the format -- GFF or Genbank -- set the `format` arg to "gff" or "Genbank. It defaults to "Genbank".

```py
from kbase_workspace_utils import download_genome

path = download_genome(ref=ws_reference, save_dir=directory, format="gff")
```

Will return the full path of the downloaded file, with the original object name from the workspace.

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

### Build the conda package

Install conda and conda-build, then run:

```py
$ python setup.py sdist
$ anaconda upload -u kbase dist/*.tar.gz
```

### Project anatomy

* The main package source code lives in `src/kbase_workspace_utils`. See `src/kbase_workspace_utils/__init__.py` for a list of all exported functions.
* Tests live in `src/kbase_workspace_utils/test`
