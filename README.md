# Datacatalog Util [![Tweet](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Data%20Catalog%20util%20scripts%20&url=https://github.com/mesmacosta/datacatalog-util&via=github&hashtags=datacatalog,python,bulk,bigdata)


[![CircleCI][1]][2] [![PyPi][7]][8] [![License][9]][9] [![Issues][10]][11]

A Python package to manage Google Cloud Data Catalog helper commands and scripts.

**Disclaimer: This is not an officially supported Google product.**

## Commands List

| Group            | Command                        | Description                                             | Documentation Link | Code Repo |
| ---              | ---                            | ---                                                     | ---                | ---       |
| `tags`           |**create**                      | Load Tags from CSV file.                                | [GO][12]           | [GO][18]  |
| `tags`           |**delete**                      | Delete Tags from CSV file.                              | [GO][31]           | [GO][26]  |
| `tags`           |**export**                      | Export Tags to CSV file.                                | [GO][13]           | [GO][26]  |
| `tag-templates`  |**create**                      | Load Templates from CSV file.                           | [GO][14]           | [GO][24]  |
| `tag-templates`  |**delete**                      | Delete Templates from CSV file.                         | [GO][15]           | [GO][24]  |
| `tag-templates`  |**export**                      | Export Templates to CSV file.                           | [GO][16]           | [GO][25]  |
| `filesets`       |**create**                      | Create GCS filesets from CSV file.                      | [GO][29]           | [GO][28]  |
| `filesets`       |**enrich**                      | Enrich GCS filesets with Tags.                          | [GO][20]           | [GO][19]  |
| `filesets`       |**clean-up-templates-and-tags** | Cleans up the Fileset Template and their Tags.          | [GO][21]           | [GO][19]  |
| `filesets`       |**delete**                      | Delete GCS filesets from CSV file.                      | [GO][30]           | [GO][28]  |
| `filesets`       |**export**                      | Export Filesets to CSV file.                            | [GO][34]           | [GO][33]  |
| `object-storage` |**create-entries**              | Create Entries for each Object Storage File.            | [GO][36]           | [GO][35]  |
| `object-storage` |**delete-entries**              | Delete Entries that belong to the Object Storage Files. | [GO][37]           | [GO][35]  |


-----

## Execute Tutorial in Cloud Shell
[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/TUTORIAL.md)


<!--
  ⚠️ DO NOT UPDATE THE TABLE OF CONTENTS MANUALLY ️️⚠️
  run `npx markdown-toc -i README.md`.

  Please stick to 80-character line wraps as much as you can.
-->

## Table of Contents

<!-- toc -->

- [1. Environment setup](#1-environment-setup)
  * [1.1. Python + virtualenv](#11-python--virtualenv)
    + [1.1.1. Install Python 3.6+](#111-install-python-36)
    + [1.1.2. Get the source code](#112-get-the-source-code)
    + [1.1.3. Create and activate an isolated Python environment](#113-create-and-activate-an-isolated-python-environment)
    + [1.1.4. Install the package](#114-install-the-package)
  * [1.2. Docker](#12-docker)
  * [1.3. Auth credentials](#13-auth-credentials)
    + [1.3.1. Create a service account and grant it below roles](#131-create-a-service-account-and-grant-it-below-roles)
    + [1.3.2. Download a JSON key and save it as](#132-download-a-json-key-and-save-it-as)
    + [1.3.3. Set the environment variables](#133-set-the-environment-variables)
- [2. Load Tags from CSV file](#2-load-tags-from-csv-file)
  * [2.1. Create a CSV file representing the Tags to be created](#21-create-a-csv-file-representing-the-tags-to-be-created)
    + [2.1.1 Execute Tutorial in Cloud Shell](#211-execute-tutorial-in-cloud-shell)
  * [2.2. Run the datacatalog-util script - Create the Tags](#22-run-the-datacatalog-util-script---create-the-tags)
  * [2.3. Run the datacatalog-util script - Delete the Tags](#23-run-the-datacatalog-util-script---delete-the-tags)
- [3. Export Tags to CSV file](#3-export-tags-to-csv-file)
  * [3.1. A list of CSV files, each representing one Template will be created.](#31-a-list-of-csv-files-each-representing-one-template-will-be-created)
    + [3.1.1 Execute Tutorial in Cloud Shell](#311-execute-tutorial-in-cloud-shell)
  * [3.2. Run tags export](#32-run-tags-export)
  * [3.3 Run tags export filtering Tag Templates](#33-run-tags-export-filtering-tag-templates)
- [4. Load Templates from CSV file](#4-load-templates-from-csv-file)
  * [4.1. Create a CSV file representing the Templates to be created](#41-create-a-csv-file-representing-the-templates-to-be-created)
    + [4.1.1 Execute Tutorial in Cloud Shell](#411-execute-tutorial-in-cloud-shell)
  * [4.2. Run the datacatalog-util script - Create the Tag Templates](#42-run-the-datacatalog-util-script---create-the-tag-templates)
  * [4.3. Run the datacatalog-util script - Delete the Tag Templates](#43-run-the-datacatalog-util-script---delete-the-tag-templates)
- [5. Export Templates to CSV file](#5-export-templates-to-csv-file)
  * [5.1. A CSV file representing the Templates will be created](#51-a-csv-file-representing-the-templates-will-be-created)
    + [5.1.1 Execute Tutorial in Cloud Shell](#511-execute-tutorial-in-cloud-shell)
  * [5.2. Run the datacatalog-util script](#52-run-the-datacatalog-util-script)
- [6. Filesets Commands](#6-filesets-commands)
  * [6.1. Create a CSV file representing the Entry Groups and Entries to be created](#61-create-a-csv-file-representing-the-entry-groups-and-entries-to-be-created)
    + [6.1.1 Execute Tutorial in Cloud Shell](#611-execute-tutorial-in-cloud-shell)
  * [6.2. Create the Filesets Entry Groups and Entries](#62-create-the-filesets-entry-groups-and-entries)
  * [6.3. Enrich GCS Filesets with Tags](#63-enrich-gcs-filesets-with-tags)
    + [6.3.1 Enrich all fileset entries using Tag Template from a different Project (Good way to reuse the same Template)](#631-enrich-all-fileset-entries-using-tag-template-from-a-different-project-good-way-to-reuse-the-same-template)
    + [6.3.2 Execute Fileset Enricher Tutorial in Cloud Shell](#632-execute-fileset-enricher-tutorial-in-cloud-shell)
  * [6.4. clean up template and tags](#64-clean-up-template-and-tags)
  * [6.5. Delete the Filesets Entry Groups and Entries](#65-delete-the-filesets-entry-groups-and-entries)
- [7. Export Filesets to CSV file](#7-export-filesets-to-csv-file)
  * [7.1. A CSV file representing the Filesets will be created](#71-a-csv-file-representing-the-filesets-will-be-created)
    + [7.1.1 Execute Tutorial in Cloud Shell](#711-execute-tutorial-in-cloud-shell)
  * [7.2. Run the datacatalog-util script](#72-run-the-datacatalog-util-script)
- [8. DataCatalog Object Storage commands](#8-datacatalog-object-storage-commands)
  * [8.1 Execute Tutorial in Cloud Shell](#81-execute-tutorial-in-cloud-shell)
  * [8.2. Create DataCatalog entries based on object storage files](#82-create-datacatalog-entries-based-on-object-storage-files)
  * [8.3. Delete object storage entries on entry group](#83-delete-object-storage-entries-on-entry-group)
- [9. Data Catalog Templates Examples](#9-data-catalog-templates-examples)

<!-- tocstop -->

-----

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

#### 2.1.1 Execute Tutorial in Cloud Shell

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/tags/TUTORIAL.LOAD.md)

### 2.2. Run the datacatalog-util script - Create the Tags

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

### 2.3. Run the datacatalog-util script - Delete the Tags

- Python + virtualenv

```bash
datacatalog-util tags delete --csv-file CSV_FILE_PATH
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

#### 3.1.1 Execute Tutorial in Cloud Shell

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/tags/TUTORIAL.EXPORT.md)

### 3.2. Run tags export

- Python + virtualenv

```bash
datacatalog-util tags export --project-ids my-project --dir-path DIR_PATH
```

### 3.3 Run tags export filtering Tag Templates

- Python + virtualenv

```bash
datacatalog-util tags export --project-ids my-project \
--dir-path DIR_PATH \
--tag-templates-names projects/my-project/locations/us-central1/tagTemplates/my-template,\
projects/my-project/locations/us-central1/tagTemplates/my-template-2 

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

#### 4.1.1 Execute Tutorial in Cloud Shell

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/tag-templates/TUTORIAL.LOAD.md)


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

#### 5.1.1 Execute Tutorial in Cloud Shell

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/tag-templates/TUTORIAL.EXPORT.md)


### 5.2. Run the datacatalog-util script

- Python + virtualenv

```bash
datacatalog-util tag-templates export --project-ids my-project --file-path CSV_FILE_PATH
```

## 6. Filesets Commands

### 6.1. Create a CSV file representing the Entry Groups and Entries to be created

Filesets are composed of as many lines as required to represent all of their fields. The columns are
described as follows:

| Column                        | Description               | Mandatory |
| ---                           | ---                       | ---       |
| **entry_group_name**          | Entry Group Name.         | Y         |
| **entry_group_display_name**  | Entry Group Display Name. | Y         |
| **entry_group_description**   | Entry Group Description.  | Y         |
| **entry_id**                  | Entry ID.                 | Y         |
| **entry_display_name**        | Entry Display Name.       | Y         |
| **entry_description**         | Entry Description.        | Y         |
| **entry_file_patterns**       | Entry File Patterns.      | Y         |
| **schema_column_name**        | Schema column name.       | N         |
| **schema_column_type**        | Schema column type.       | N         |
| **schema_column_description** | Schema column description.| N         |
| **schema_column_mode**        | Schema column mode.       | N         |

#### 6.1.1 Execute Tutorial in Cloud Shell

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/filesets/TUTORIAL.LOAD.md)


### 6.2. Create the Filesets Entry Groups and Entries

- Python + virtualenv

```bash
datacatalog-util filesets create --csv-file CSV_FILE_PATH
```

*TIPS* 
- [sample-input/create-filesets][32] for reference;

### 6.3. Enrich GCS Filesets with Tags
Users are able to choose the Tag fields from the list provided at [Tags][23]

```bash
datacatalog-util filesets enrich --project-id my-project 
```

#### 6.3.1 Enrich all fileset entries using Tag Template from a different Project (Good way to reuse the same Template)

If you are using a different Project, make sure the Service Account has the following permissions on that Project or that Template:
* Data Catalog TagTemplate Creator
* Data Catalog TagTemplate User

```bash
datacatalog-util filesets \
  --project-id my_project \
  enrich --tag-template-name projects/my_different_project/locations/us-central1/tagTemplates/fileset_enricher_findings
```

#### 6.3.2 Execute Fileset Enricher Tutorial in Cloud Shell

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/filesets/TUTORIAL.ENRICH.md)


### 6.4. clean up template and tags
Cleans up the Template and Tags from the Fileset Entries, running the main command will recreate those.

```bash
datacatalog-util filesets clean-up-templates-and-tags --project-id my-project 
```

### 6.5. Delete the Filesets Entry Groups and Entries

- Python + virtualenv

```bash
datacatalog-util filesets delete --csv-file CSV_FILE_PATH
```

## 7. Export Filesets to CSV file

### 7.1. A CSV file representing the Filesets will be created

Filesets are composed of as many lines as required to represent all of their fields. The columns are
described as follows:

| Column                        | Description               | Mandatory |
| ---                           | ---                       | ---       |
| **entry_group_name**          | Entry Group Name.         | Y         |
| **entry_group_display_name**  | Entry Group Display Name. | Y         |
| **entry_group_description**   | Entry Group Description.  | Y         |
| **entry_id**                  | Entry ID.                 | Y         |
| **entry_display_name**        | Entry Display Name.       | Y         |
| **entry_description**         | Entry Description.        | Y         |
| **entry_file_patterns**       | Entry File Patterns.      | Y         |
| **schema_column_name**        | Schema column name.       | N         |
| **schema_column_type**        | Schema column type.       | N         |
| **schema_column_description** | Schema column description.| N         |
| **schema_column_mode**        | Schema column mode.       | N         |

#### 7.1.1 Execute Tutorial in Cloud Shell

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/filesets/TUTORIAL.EXPORT.md)


### 7.2. Run the datacatalog-util script

- Python + virtualenv

```bash
datacatalog-util filesets export --project-ids my-project --file-path CSV_FILE_PATH
```

## 8. DataCatalog Object Storage commands

### 8.1 Execute Tutorial in Cloud Shell

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/object-storage/TUTORIAL.LOAD.md)


### 8.2. Create DataCatalog entries based on object storage files

```bash
datacatalog-util \
  object-storage sync-entries --type cloud_storage \
  --project-id my_project \
  --entry-group-name projects/my_project/locations/us-central1/entryGroups/my_entry_group \
  --bucket-prefix my_bucket
```

### 8.3. Delete object storage entries on entry group

```bash
datacatalog-util \
  object-storage delete-entries --type cloud_storage \
  --project-id my_project \
  --entry-group-name projects/my_project/locations/us-central1/entryGroups/my_entry_group
```

## 9. Data Catalog Templates Examples

[templates_examples.md](docs/templates_examples.md)

[1]: https://circleci.com/gh/mesmacosta/datacatalog-util.svg?style=svg
[2]: https://circleci.com/gh/mesmacosta/datacatalog-util
[3]: https://virtualenv.pypa.io/en/latest/
[4]: https://github.com/mesmacosta/datacatalog-util/tree/master/sample-input/create-tags
[5]: https://docs.google.com/spreadsheets/d/1bqeAXjLHUq0bydRZj9YBhdlDtuu863nwirx8t4EP_CQ
[6]: https://github.com/mesmacosta/datacatalog-util/tree/master/sample-input/create-tag-templates
[7]: https://img.shields.io/pypi/v/datacatalog-util.svg?force_cache=true
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
[20]: https://github.com/mesmacosta/datacatalog-util#63-enrich-gcs-filesets-with-tags
[21]: https://github.com/mesmacosta/datacatalog-util#64-clean-up-template-and-tags
[23]: https://github.com/mesmacosta/datacatalog-fileset-enricher#1-created-tags
[24]: https://github.com/mesmacosta/datacatalog-tag-template-processor
[25]: https://github.com/mesmacosta/datacatalog-tag-template-exporter
[26]: https://github.com/mesmacosta/datacatalog-tag-exporter
[27]: https://github.com/mesmacosta/datacatalog-util#62-create-fileset-enricher-tag-template-in-a-different-project
[28]: https://github.com/mesmacosta/datacatalog-fileset-processor
[29]: https://github.com/mesmacosta/datacatalog-util#61-create-a-csv-file-representing-the-entry-groups-and-entries-to-be-created
[30]: https://github.com/mesmacosta/datacatalog-util#65-delete-the-filesets-entry-groups-and-entries
[31]: https://github.com/mesmacosta/datacatalog-util#23-run-the-datacatalog-util-script---delete-the-tags
[32]: https://github.com/mesmacosta/datacatalog-util/tree/master/sample-input/create-filesets
[33]: https://github.com/mesmacosta/datacatalog-fileset-exporter
[34]: https://github.com/mesmacosta/datacatalog-util#7-export-filesets-to-csv-file
[35]: https://github.com/mesmacosta/datacatalog-object-storage-processor
[36]: https://github.com/mesmacosta/datacatalog-util#82-create-datacatalog-entries-based-on-object-storage-files
[37]: https://github.com/mesmacosta/datacatalog-util#83-delete-up-object-storage-entries-on-entry-group
