# datacatalog-util

[![CircleCI][1]][2] [![PyPi][7]][8] [![License][9]][9] [![Issues][10]][11]

A Python package to manage Google Cloud Data Catalog helper commands and scripts.

**Disclaimer: This is not an officially supported Google product.**

## Commands List

| Command                  | Description                     | Documentation Link | Code Repo |
| ---                      | ---                             | ---                | ---       |
| **create-tags**          | Load Tags from CSV file.        | [GO][12]           | [GO][18]  |
| **export-tags**          | Export Tags to CSV file.        | [GO][13]           | [GO][17]  |
| **create-tag-templates** | Load Templates from CSV file.   | [GO][14]           | [GO][17]  |
| **delete-tag-templates** | Delete Templates from CSV file. | [GO][15]           | [GO][17]  |
| **export-tag-templates** | Export Templates to CSV file.   | [GO][16]           | [GO][17]  |


## 1. Environment setup

### 1.1. Python + virtualenv

Using [virtualenv][3] is optional, but strongly recommended unless you use [Docker](#12-docker).

#### 1.1.1. Install Python 3.6+

#### 1.1.2. Create a folder

This is recommended so all related stuff will reside at same place, making it easier to follow
below instructions.

````bash
mkdir ./datacatalog-util
cd ./datacatalog-util
````

_All paths starting with `./` in the next steps are relative to the `utilsr`
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

#### 1.2.1. Get the source code
```bash
git clone https://github.com/mesmacosta/datacatalog-util
cd ./datacatalog-util
```

### 1.3. Auth credentials

#### 1.3.1. Create a service account and grant it below roles

- BigQuery Metadata Viewer
- Data Catalog Admin
- A custom role with `bigquery.datasets.updateTag` and `bigquery.tables.updateTag` permissions 

#### 1.3.2. Download a JSON key and save it as
- `./credentials/datacatalog-util.json`

#### 1.3.3. Set the environment variables

_This step may be skipped if you're using [Docker](#12-docker)._

```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/credentials/datacatalog-util.json
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
datacatalog-util create-tags --csv-file CSV_FILE_PATH
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
datacatalog-util export-tags --project-ids my-project --dir-path DIR_PATH
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
datacatalog-util create-tag-templates --csv-file CSV_FILE_PATH
```

### 4.3. Run the datacatalog-util script - Delete the Tag Templates

- Python + virtualenv

```bash
datacatalog-util delete-tag-templates --csv-file CSV_FILE_PATH
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
datacatalog-util export-tag-templates --project-ids my-project --file-path CSV_FILE_PATH
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