<!---
Note: This tutorial is meant for Google Cloud Shell, and can be opened by going to
http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/filesets/TUTORIAL.LOAD.md)--->
# Data Catalog Util Filesets Tutorial

<!-- TODO: analytics id? -->
<walkthrough-author name="mesmacosta@gmail.com" tutorialName="Data Catalog Util Load Filesets Tutorial" repositoryUrl="https://github.com/mesmacosta/datacatalog-util"></walkthrough-author>

## Intro

This tutorial will walk you through the execution of the Data Catalog Util Load Filesets CLI.

## Python CLI

This tutorial uses a Python CLI, if you want to look at the code open:
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/src/datacatalog_util/datacatalog_util_cli.py"
                              text="datacatalog_util_cli.py">
</walkthrough-editor-open-file>.

Otherwise go to the next step.

## CSV fields

Go to the
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/README.md" text="README.md">
</walkthrough-editor-open-file> file, and find the ## 6. Filesets Commands.
This section explains the CSV columns used to create Data Catalog Filesets.

## Set Up the Service Account

First, let's set up the Service Account. (You may skip this, if you already have your Service Account)

Start by setting your project ID. Replace the placeholder to your project.
```bash
gcloud config set project MY_PROJECT_PLACEHOLDER
```

Next load it in a environment variable.
```bash
export PROJECT_ID=$(gcloud config get-value project)
```

Then create a Service Account.
```bash
gcloud iam service-accounts create datacatalog-util-filst-load-sa \
--display-name  "Service Account for Data Catalog Util Filesets Load CLI" \
--project $PROJECT_ID
```

Next create a credentials folder where the Service Account will be saved.
```bash
mkdir -p ~/credentials
```

Next create and download the Service Account Key.
```bash
gcloud iam service-accounts keys create "datacatalog-util-filst-load-sa.json" \
--iam-account "datacatalog-util-filst-load-sa@$PROJECT_ID.iam.gserviceaccount.com" \
&& mv datacatalog-util-filst-load-sa.json ~/credentials/datacatalog-util-filst-load-sa.json
```

Next add Data Catalog admin role to the Service Account.
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:datacatalog-util-filst-load-sa@$PROJECT_ID.iam.gserviceaccount.com" \
--quiet \
--project $PROJECT_ID \
--role "roles/datacatalog.admin"
```

Next set up the credentials environment variable.
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/credentials/datacatalog-util-filst-load-sa.json
```

## Install the Python CLI

Install and config the datacatalog-util CLI.
```bash
pip3 install --upgrade datacatalog-util --user
```
Next load it to your PATH.
```bash
export PATH=~/.local/bin:$PATH
```

Next test it out.
```bash
datacatalog-util --help
```

## Create a Cloud Storage bucket with CSV files

You may skip this, if you already have a Cloud Storage bucket with files in your project.

Enable Big Query API
```bash
gcloud services enable storage.googleapis.com --project $PROJECT_ID
```

Create a CSV file to load the Cloud Storage bucket. Copy this manually.
```
cat > us_state_salesregions_1.csv << EOF
id,state_code,state_name,sales_region
1,MO,Missouri,Region_1
2,SC,South Carolina,Region_1
3,IN,Indiana,Region_1
6,DE,Delaware,Region_2
15,VT,Vermont,Region_2
16,DC,District of Columbia,Region_2
19,CT,Connecticut,Region_2
20,ME,Maine,Region_2
EOF
```

Create a second CSV file. Copy this manually.
```
cat > us_state_salesregions_2.csv << EOF
id,state_code,state_name,sales_region
21,AL,Alabama,Region_1
22,AK,Alaska,Region_1
23,AZ,Arizona,Region_1
26,AR,Arkansas,Region_2
25,CA,California,Region_2
26,CO,Colorado,Region_2
29,DE,Delaware,Region_2
30,FL,Florida,Region_2
EOF
```

Create a Cloud Storage bucket
```bash
gsutil mb gs://filesets_load_tutorial_$PROJECT_ID/
```

Upload CSV files to Cloud Storage bucket
```bash
gsutil cp us_state_salesregions_1.csv gs://filesets_load_tutorial_$PROJECT_ID/
```

```bash
gsutil cp us_state_salesregions_2.csv gs://filesets_load_tutorial_$PROJECT_ID/
```

## Update the sample CSV file with Project and Filesets data

Open the CSV file at:
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/sample-input/create-filesets/fileset-entry-opt-1-all-metadata.csv"
                              text="fileset-entry-opt-1-all-metadata.csv">
</walkthrough-editor-open-file>.

Replace the placeholders with your Project information
```
Replace PROJECT_ID with your Project
Replace ENTRY_GROUP_ID with filesets_load_group
Replace ENTRY_ID with filesets_load_tutorial
Replace TEMPLATE_ID with my_tutorial_template
Replace MY_BUCKET_NAME with gs://filesets_load_tutorial_$PROJECT_ID/ <- Change $PROJECT_ID placeholder to your project

The CSV column schema is already set up for this tutorial, we won't use the schema in this tutorial, but it's important to know about it.
```
If you want to know more about use cases for Filesets Schemas, go to:
[Join Streaming Data with Dataflow SQL](https://cloud.google.com/dataflow/docs/samples/join-streaming-data-with-sql)

## Execute the Python CLI

Run the Python CLI:
```bash
datacatalog-util filesets create \
--project-id $PROJECT_ID \
--csv-file ~/cloudshell_open/datacatalog-util/sample-input/create-filesets/fileset-entry-opt-1-all-metadata.csv
```

## Search for the Created Filesets

Go to Data Catalog search UI:
[Search UI](https://console.cloud.google.com/datacatalog?qTypes=FILESET)

Check the search results, and verify the created filesets.

## Delete Filesets

Run the Python CLI:
```bash
datacatalog-util filesets delete \
--project-id $PROJECT_ID \
--csv-file ~/cloudshell_open/datacatalog-util/sample-input/create-filesets/fileset-entry-opt-1-all-metadata.csv
```

## Search for the Created Filesets

Go to Data Catalog search UI:
[Search UI](https://console.cloud.google.com/datacatalog?qTypes=FILESET)

Check the search results, and verify that there are no results. Filesets for the `filesets_load_tutorial` 
have been deleted.

## Congratulations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You've successfully finished the Data Catalog Util Load Filesets.
