# Converting lab 4 to use Google Cloud Storage

In this lab you'll convert the **_extract_** and **_load_** processes from lab 4 away from relying on local file storage between processes to relying on a shared remote file store (specifically, Google Cloud Storage). The first _extract_ step has already been converted in class on Monday. In this lab we will convert the second and third steps.

You will need:
* A **command line terminal**. On Mac, this will just be the Terminal app. On Windows, this could be Ubuntu, Power Shell, or an Anaconda Terminal. It could be stand-alone, or integrated into your code editor.
* A **working version of `conda` or `poetry`** on the command line.
* A **code editor** for editing Python files.

To get started:
1. Clone this repository into a folder on your local machine
2. In a terminal, use `cd` to get into the folder for the repository
3. Ensure that you have an environment created and activated
4. Install the necessary packages:
   * `google-cloud-storage` -- the Google Cloud Storage client package for Python
   * `requests`
   * `sqlalchemy`
   * `pandas`
   * `psycopg2-binary` -- For Conda, psycopg2-binary is available via the `conda-forge` channel, so make sure you have the it added as a package source (in a terminal, run: `conda config --add channels conda-forge`). You can see what channel owns a particular package using [the search at anaconda.org](https://anaconda.org/search?q=psycopg2-binary).

```bash
conda create -n lab05
conda activate lab05
conda install requests google-cloud-storage sqlalchemy pandas psycopg2-binary
```

**OR**

```bash
poetry init
poetry shell
poetry add requests google-cloud-storage sqlalchemy pandas psycopg2-binary
```

From there, follow Google's [documentation](https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python) for setting up a service account, and generating keys. When you get to the point of setting `GOOGLE_APPLICATION_CREDENTIALS`, see the section below on _Environment Variables_.

## Environment Variables

Conda has a neat feature where you can [use it to set environment variables](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#setting-environment-variables). This is nice for when you have to switch between different environments. However, you want to be careful if you export your environment to a yml file.

For poetry, we'll need an additional tool to allow us to set environment variables within our environment. There are several tools that make this possible, but a reliable one that will work across platforms is [python-dotenv](https://github.com/theskumar/python-dotenv). You _can_ use `dotenv` with Conda as well.

### Using `dotenv` to manage environment variables

Install the package into your environment by running the following in a terminal:

```bash
poetry install python-dotenv
```

**OR (optional)**

```bash
conda install python-dotenv
```

The `dotenv` package allows you to define project-specific environment variables in a file named _.env_. Now, instead of running `export GOOGLE_APPLICATION_CREDENTIALS=...`, create a file named _.env_ within your project folder, add a line `GOOGLE_APPLICATION_CREDENTIALS=...` replacing the ellipses (`...`) with the path to your credentials key file.

To use `dotenv`, at the top of your scripts, add the following:

```python
from dotenv import load_dotenv
load_dotenv()
```

### Using `conda` to manage environment variables

To set an environment variable in Conda, you can use a command of the following format:

```bash
conda env config vars set var=value
```

For example, once you have the path to your Google application credentials, you can set it as a variable in your environment with:

```bash
conda env config vars set GOOGLE_APPLICATION_CREDENTIALS=...
```

(replace the ellipses with your path).

## Stretch goals

* Notice that in each of the extract scripts we are performing the following steps:
  1. making a request to an HTTP source,
  2. saving the response content to a file, and
  3. uploading that file content to Google Cloud Storage

  In this case, we can write a function to encapsulate the above logic. Create a function named `http_to_gcs`, and update the extract scripts to use that function. You can put the function in a new module named _pipeline_tools.py_ in the same folder as your scripts, and then in the import blocks of the extract scripts, add the line:

  ```python
  from pipeline_tools import http_to_gcs
  ```

  Your function could have the following signature:

  ```python
  def http_to_gcs(
      request_method: str,
      request_url: str,
      request_data: dict,
      request_files: dict,
      gcs_bucket_name: str,
      gcs_blob_name: str):
      ...
  ```
* What if the expected files aren't available in GCS? Write a [`try`/`except` block](https://realpython.com/python-exceptions/) that can handle this case.
