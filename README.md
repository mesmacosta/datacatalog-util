# Datacatalog Util [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Data%20Catalog%20util%20scripts%20&url=https://github.com/mesmacosta/datacatalog-util&via=github&hashtags=datacatalog,python,bulk,bigdata)


[![CircleCI][1]][2] [![PyPi][7]][8] [![License][9]][9] [![Issues][10]][11]

A Python package to manage Google Cloud Data Catalog helper commands and scripts.

**Disclaimer: This is not an officially supported Google product.**

## Commands List

| Group          | Command                        | Description                                         | Documentation Link | Code Repo |
| ---            | ---                            | ---                                                 | ---                | ---       |
| `tags`         |**create**                      | Load Tags from CSV file.                            | [GO][12]           | [GO][18]  |
| `tags`         |**export**                      | Export Tags to CSV file.                            | [GO][13]           | [GO][26]  |
| `tag-templates`|**create**                      | Load Templates from CSV file.                       | [GO][14]           | [GO][24]  |
| `tag-templates`|**delete**                      | Delete Templates from CSV file.                     | [GO][15]           | [GO][24]  |
| `tag-templates`|**export**                      | Export Templates to CSV file.                       | [GO][16]           | [GO][25]  |
| `filesets`     |**enrich**                      | Enrich GCS filesets with Tags.                      | [GO][20]           | [GO][19]  |
| `filesets`     |**create-template**             | Create Filesets Template in chosen Project.         | [GO][27]           | [GO][19]  |
| `filesets`     |**clean-up-templates-and-tags** | Cleans up Fileset Templates and Tags.               | [GO][21]           | [GO][19]  |
| `filesets`     |**clean-up-all**                | Clean up Fileset Entries, Their Tags and Templates. | [GO][22]           | [GO][19]  |


## Executing in Cloud Shell
````bash
# Set your SERVICE ACCOUNT, for instructions go to 1.3. Auth credentials
# This name is just a suggestion, feel free to name it following your naming conventions
export GOOGLE_APPLICATION_CREDENTIALS=~/datacatalog-util-sa.json

# Install datacatalog-util 
pip3 install datacatalog-util --user

# Add to your PATH
export PATH=~/.local/bin:$PATH

# Look for available commands
datacatalog-util --help
````

## 1. Environment setup

### 1.1. Python + virtualenv

Using [virtualenv][3] is optional, but strongly recommended unless you use [Docker](#12-docker).

#### 1.1.1. Install Python 3.6+

#### 1.1.2. Get the source code
```bash
git clone https://github.com/mesmacosta/datacatalog-util
cd ./datacatalog-util
```

_All paths starting with `./` in the next steps are relative to the `datacatalog-util`
folder._

#### 1.1.3. Create and activate an isolated Python environment

```bash
pip install --upgrade virtualenv
python3 -m virtualenv --python python3 env
source ./env/bin/activate
```

#### 1.1.4. Install the package

```bash
pip install --upgrade .
```

### 1.2. Docker

Docker may be used as an alternative to run the script. In this case, please disregard the
[Virtualenv](#11-python--virtualenv) setup instructions.

### 1.3. Auth credentials

#### 1.3.1. Create a service account and grant it below roles

- Data Catalog Admin
- Storage Admin

#### 1.3.2. Download a JSON key and save it as
This name is just a suggestion, feel free to name it following your naming conventions
- `./credentials/datacatalog-util-sa.json`

#### 1.3.3. Set the environment variables

_This step may be skipped if you're using [Docker](#12-docker)._

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/credentials/datacatalog-util-sa.json
```

## 2. Load Tags from CSV file

### 2.1. Create a CSV file representing the Tags to be created

Tags are composed of as many lines as required to represent all of their fields. The columns are
described as follows:

| Column              | Description                                            | Mandatory |
| ---                 | ---                                                    | ---       |
| **linked_resource** | Full name of the asset the Entry refers to.            | Y         |
| **template_name**   | Resource name of the Tag Template for the Tag.         | Y         |
| **column**          | Attach Tags to a column belonging to the Entry schema. | N         |
| **field_id**        | Id of the Tag field.                                   | Y         |
| **field_value**     | Value of the Tag field.                                | Y         |

*TIPS* 
- [sample-input/create-tags][4] for reference;
- [Data Catalog Sample Tags][5] (Google Sheets) may help to create/export the CSV.

### 2.2. Run the datacatalog-util script

- Python + virtualenv

```bash
datacatalog-util tags create --csv-file CSV_FILE_PATH
```

- Docker

```bash
docker build --rm --tag datacatalog-util .
docker run --rm --tty \
  --volume CREDENTIALS_FILE_FOLDER:/credentials --volume CSV_FILE_FOLDER:/data \
  datacatalog-util create-tags --csv-file /data/CSV_FILE_NAME
```

## 3. Export Tags to CSV file

### 3.1. A list of CSV files, each representing one Template will be created.
One file with summary with stats about each template, will also be created on the same directory.

The columns for the summary file are described as follows:

| Column                         | Description                                              | 
| ---                            | ---                                                      | 
| **template_name**              | Resource name of the Tag Template for the Tag.           | 
| **tags_count**                 | Number of tags found from the template.                  | 
| **tagged_entries_count**       | Number of tagged entries with the template.              | 
| **tagged_columns_count**       | Number of tagged columns with the template.              | 
| **tag_string_fields_count**    | Number of used String fields on tags of the template.    | 
| **tag_bool_fields_count**      | Number of used Bool fields on tags of the template.      | 
| **tag_double_fields_count**    | Number of used Double fields on tags of the template.    | 
| **tag_timestamp_fields_count** | Number of used Timestamp fields on tags of the template. | 
| **tag_enum_fields_count**      | Number of used Enum fields on tags of the template.      | 

The columns for each template file are described as follows:

| Column                     | Description                                            | 
| ---                        | ---                                                    |
| **relative_resource_name** | Full resource name of the asset the Entry refers to.   |
| **linked_resource**        | Full name of the asset the Entry refers to.            |
| **template_name**          | Resource name of the Tag Template for the Tag.         | 
| **tag_name**               | Resource name of the Tag.                              |
| **column**                 | Attach Tags to a column belonging to the Entry schema. |
| **field_id**               | Id of the Tag field.                                   |
| **field_type**             | Type of the Tag field.                                 | 
| **field_value**            | Value of the Tag field.                                | 

### 3.2. Run the datacatalog-util script

- Python + virtualenv

```bash
datacatalog-util tags export --project-ids my-project --dir-path DIR_PATH
```

## 4. Load Templates from CSV file

### 4.1. Create a CSV file representing the Templates to be created

Templates are composed of as many lines as required to represent all of their fields. The columns are
described as follows:

| Column                 | Description                                    | Mandatory |
| ---                    | ---                                            | ---       |
| **template_name**      | Resource name of the Tag Template for the Tag. | Y         |
| **display_name**       | Resource name of the Tag Template for the Tag. | Y         |
| **field_id**           | Id of the Tag Template field.                  | Y         |
| **field_display_name** | Display name of the Tag Template field.        | Y         |
| **field_type**         | Type of the Tag Template field.                | Y         |
| **enum_values**        | Values for the Enum field.                     | N         |


### 4.2. Run the datacatalog-util script - Create the Tag Templates

- Python + virtualenv

```bash
datacatalog-util tag-templates create --csv-file CSV_FILE_PATH
```

### 4.3. Run the datacatalog-util script - Delete the Tag Templates

- Python + virtualenv

```bash
datacatalog-util tag-templates delete --csv-file CSV_FILE_PATH
```

*TIPS* 
- [sample-input/create-tag-templates][6] for reference;

## 5. Export Templates to CSV file

### 5.1. A CSV file representing the Templates will be created

Templates are composed of as many lines as required to represent all of their fields. The columns are
described as follows:

| Column                 | Description                                    | 
| ---                    | ---                                            | 
| **template_name**      | Resource name of the Tag Template for the Tag. | 
| **display_name**       | Resource name of the Tag Template for the Tag. | 
| **field_id**           | Id of the Tag Template field.                  | 
| **field_display_name** | Display name of the Tag Template field.        | 
| **field_type**         | Type of the Tag Template field.                | 
| **enum_values**        | Values for the Enum field.                     | 

### 5.2. Run the datacatalog-util script

- Python + virtualenv

```bash
datacatalog-util tag-templates export --project-ids my-project --file-path CSV_FILE_PATH
```

## 6. Filesets Commands

### 6.1. Enrich GCS Filesets with Tags
Users are able to choose the Tag fields from the list provided at [Tags][23]

```bash
datacatalog-util filesets --project-ids my-project enrich
```

### 6.1.1 Enrich all fileset entries using Tag Template from a different Project (Good way to reuse the same Template)
Check step below to see how to create the template in a different project.

```bash
datacatalog-util filesets --project-id my_project \
  enrich --tag-template-name projects/my_different_project/locations/us-central1/tagTemplates/fileset_enricher_findings
```

### 6.2. Create Fileset Enricher Tag Template in a different Project 
Creates the fileset enricher template in chosen project.

```bash
datacatalog-util filesets --project-id my_different_project \
    create-template
```

### 6.3. clean up template and tags
Cleans up the Template and Tags from the Fileset Entries, running the main command will recreate those.

```bash
datacatalog-util filesets --project-ids my-project clean-up-templates-and-tags 
```

### 6.4.  clean up all (Non Reversible, be careful)
Cleans up the Fileset Entries, Template and Tags. You have to re create the Fileset entries if you need to restore the state,
which is outside the scope of this script.

```bash
datacatalog-util filesets --project-ids my-project clean-up-all

```


[1]: https://circleci.com/gh/mesmacosta/datacatalog-util.svg?style=svg
[2]: https://circleci.com/gh/mesmacosta/datacatalog-util
[3]: https://virtualenv.pypa.io/en/latest/
[4]: https://github.com/mesmacosta/datacatalog-util/tree/master/sample-input/create-tags
[5]: https://docs.google.com/spreadsheets/d/1bqeAXjLHUq0bydRZj9YBhdlDtuu863nwirx8t4EP_CQ
[6]: https://github.com/mesmacosta/datacatalog-util/tree/master/sample-input/create-tag-templates
[7]: https://img.shields.io/pypi/v/datacatalog-util.svg
[8]: https://pypi.org/project/datacatalog-util/
[9]: https://img.shields.io/github/license/mesmacosta/datacatalog-util.svg
[10]: https://img.shields.io/github/issues/mesmacosta/datacatalog-util.svg
[11]: https://github.com/mesmacosta/datacatalog-util/issues
[12]: https://github.com/mesmacosta/datacatalog-util#2-load-tags-from-csv-file
[13]: https://github.com/mesmacosta/datacatalog-util#3-export-tags-to-csv-file
[14]: https://github.com/mesmacosta/datacatalog-util#4-load-templates-from-csv-file
[15]: https://github.com/mesmacosta/datacatalog-util#43-run-the-datacatalog-util-script---delete-the-tag-templates
[16]: https://github.com/mesmacosta/datacatalog-util#5-export-templates-to-csv-file
[17]: https://github.com/mesmacosta/datacatalog-util
[18]: https://github.com/ricardolsmendes/datacatalog-tag-manager
[19]: https://github.com/mesmacosta/datacatalog-fileset-enricher
[20]: https://github.com/mesmacosta/datacatalog-util#61-enrich-gcs-filesets-with-tags
[21]: https://github.com/mesmacosta/datacatalog-util#62-clean-up-template-and-tags
[22]: https://github.com/mesmacosta/datacatalog-util#63--clean-up-all-non-reversible-be-careful
[23]: https://github.com/mesmacosta/datacatalog-fileset-enricher#1-created-tags
[24]: https://github.com/mesmacosta/datacatalog-tag-template-processor
[25]: https://github.com/mesmacosta/datacatalog-tag-template-exporter
[26]: https://github.com/mesmacosta/datacatalog-tag-exporter
[27]: https://github.com/mesmacosta/datacatalog-util#62-create-fileset-enricher-tag-template-in-a-different-project
