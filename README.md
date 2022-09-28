# tap-stackoverflow-sampledata

`tap-stackoverflow-sampledata` is a Singer tap for the Stack Overflow xml dump files avaiable at [Archieve.org](https://archive.org/details/stackexchange).  This tap is inteded to be use to test Singer targets and or seed a source system with enough data to sufficently test a source to target pipleline.  

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

You will need to install the tap directly from the GitHub repository.  Here is the command to use

```bash
pipx install git+https://github.com/BuzzCutNorman/tap-stackoverflow-sampledata.git
```

### Meltano CLI

You will need to do the following in while in a Meltano project folder

```bash
meltano add --custom extractor tap-stackoverflow-sampledata.git
```
You shoud see the custom extractor wizard start up that should look similar to the example below.  The first quesitons is what namespace would you like to use for this extractor.  This will be the name of the venv created in the `./.meltano/extractor` folder to house the extractor.  Please accecpt the default by pressing the enter key.  
```
Specify the plugin's namespace, which will serve as the:
- identifier to find related/compatible plugins
- default database schema (`load_schema` extra),
  for use by loaders that support a target schema

Hit Return to accept the default: plugin name with underscores instead of dashes

(namespace) [tap_stackoverflow_sampledata]: 
```


Next you will be were can pip find the tap so it can install it at the prompt 
```
(pip_url) [tap-stackoverflow-sampledata]:
```
Paste in the following and hit enter
```bash
git+https://github.com/BuzzCutNorman/tap-stackoverflow-sampledata.git
```

You will be asked to specify the exectuable name.  if the prompt looks like the following go ahead and hit enter since it is correct.
```
(executable) [tap-stackoverflow-sampledata]:
```

Here are the the capabilities of this tap.
```bash
catalog,discover
```
copy the above list and paste it into the prompt that looks like the following and hit enter.
```
(capabilities) [[]]:
```

You are almost there.  Just one more item to add.  That is the settings which are as follows
```bash
stackoverflow_data_directory
```
copy the above list and paste it into the prompt that looks like the following and hit enter.
```
(settings) [[]]:
```


After a few mintues you should have get a meesage that says the tap has been Installed.  The message should look something like this:
```
Added extractor 'tap-stackoverflow-sampledata' to your Meltano project

Installing extractor 'tap-stackoverflow-sampledata'...
Installed extractor 'tap-stackoverflow-sampledata'
```

## StackOverflow XML files

You will need to download the Stack Overflow files, uzip them, and place then into a directory.  The files are zipped up using 7zip (.7z) so you will need it to complete the unzip step.  Currently this tap will work with these files. 

|File                                                                                 | Zipped Size | Unzipped Size | Rows     |
|-------------------------------------------------------------------------------------|------------:|--------------:|---------:|
[Badges](https://archive.org/download/stackexchange/stackoverflow.com-Badges.7z)      | 324 MB      | 4.93 GB       | 44,913,194
[Comments](https://archive.org/download/stackexchange/stackoverflow.com-Comments.7z)  | 5 GB        | 24.3 GB       | 85,467,182
[PostLinks](https://archive.org/download/stackexchange/stackoverflow.com-PostLinks.7z)| 110 MB      | 961 MB        | 8,193,698
[Posts](https://archive.org/download/stackexchange/stackoverflow.com-Posts.7z)        | 17.8 GB     | 89.9 GB       | 56,264,788
[Tags](https://archive.org/download/stackexchange/stackoverflow.com-Tags.7z)          | 885.5 KB    | 5.36 MB       | 63,175
[Users](https://archive.org/download/stackexchange/stackoverflow.com-Users.7z)        | 929.9 MB    | 5.76 GB       | 17,922,426
[Votes](https://archive.org/download/stackexchange/stackoverflow.com-Votes.7z)        | 1.4 GB      | 21.1 GB       | 231,441,846

You can use one, two, or all.  

## Configuration

The only configuration you need to provide is the path of the directory you placed the extracted Stackoverflow file(s) in.

## Settings

| Setting                     | Required | Default | Description |
|:----------------------------|:--------:|:-------:|:------------|
| stackoverflow_data_directory| False    | None    | A path to the StackOverflow XML data file(s). |

Singer: config.json
```
{
	"stackoverflow_data_directory" : "C:\\Development\\StackOverflow\\"
}
```

Meltano: meltano.yml
```
    config:
      stackoverflow_data_directory: C:\Development\StackOverflow\
```

## Capabilities

* `catalog`
* `discover`

A full list of supported settings and capabilities is available by running: `tap-stackoverflow-sampledata --about`

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

## Usage

You can easily run `tap-stackoverflow-sampledata` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-stackoverflow-sampledata --version
tap-stackoverflow-sampledata --help
tap-stackoverflow-sampledata --config CONFIG --discover > ./catalog.json
```

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_stackoverflow_sampledata/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-stackoverflow-sampledata` CLI interface directly using `poetry run`:

```bash
poetry run tap-stackoverflow-sampledata --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-stackoverflow-sampledata
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-stackoverflow-sampledata --version
# OR run a test `elt` pipeline:
meltano run tap-stackoverflow-sampledata target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
