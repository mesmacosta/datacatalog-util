<!---
Note: This tutorial is meant for Google Cloud Shell, and can be opened by going to
http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/tags/TUTORIAL.LOAD.md)--->
# Data Catalog Util Load Tags Tutorial

<!-- TODO: analytics id? -->
<walkthrough-author name="mesmacosta@gmail.com" tutorialName="Data Catalog Util Load Tags Tutorial" repositoryUrl="https://github.com/mesmacosta/datacatalog-util"></walkthrough-author>

## Intro

This tutorial will walk you through the execution of the Data Catalog Util Load Tags CLI.

## Python CLI

This tutorial uses a Python CLI, if you want to look at the code open:
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/src/datacatalog_util/datacatalog_util_cli.py"
                              text="datacatalog_util_cli.py">
</walkthrough-editor-open-file>.

Otherwise go to the next step.

## CSV fields

Go to the
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/README.md" text="README.md">
</walkthrough-editor-open-file> file, and find the 2. Load Tags from CSV file.
This section explains the CSV columns used to create Data Catalog Tags.

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
gcloud iam service-accounts create datacatalog-util-tags-load-sa \
--display-name  "Service Account for Data Catalog Util Tags Load CLI" \
--project $PROJECT_ID
```

Next create a credentials folder where the Service Account will be saved.
```bash
mkdir -p ~/credentials
```

Next create and download the Service Account Key.
```bash
gcloud iam service-accounts keys create "datacatalog-util-tags-load-sa.json" \
--iam-account "datacatalog-util-tags-load-sa@$PROJECT_ID.iam.gserviceaccount.com" \
&& mv datacatalog-util-tags-load-sa.json ~/credentials/datacatalog-util-tags-load-sa.json
```

Next add Data Catalog admin role to the Service Account.
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:datacatalog-util-tags-load-sa@$PROJECT_ID.iam.gserviceaccount.com" \
--quiet \
--project $PROJECT_ID \
--role "roles/datacatalog.admin"
```

Next add Big Query admin role to the Service Account.
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:datacatalog-util-tags-load-sa@$PROJECT_ID.iam.gserviceaccount.com" \
--quiet \
--project $PROJECT_ID \
--role "roles/bigquery.admin"
```

Next set up the credentials environment variable.
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/credentials/datacatalog-util-tags-load-sa.json
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

## Create a Big Query Table

You may skip this, if you already have a Big Query Table in your project.

Enable Big Query API
```bash
gcloud services enable bigquery.googleapis.com --project $PROJECT_ID
```

Create a CSV file to load the Big Query table. Copy this manually.
```
cat > us_state_salesregions.csv << EOF
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

Create Big Query Dataset
```bash
bq --location=US mk -d \
--default_table_expiration 3600 \
--description "This is my dataset." \
us_state_sales
```

Create Big Query table
```bash
bq mk \
-t \
--expiration 3600 \
--description "This is my Sales Regions Table" \
us_state_sales.us_state_salesregions \
id:NUMERIC,state_code:STRING,state_name:STRING,sales_region:STRING
```

Load Big Query Table with CSV
```bash
bq load --quote "" \
--skip_leading_rows 1 \
--format=csv us_state_sales.us_state_salesregions us_state_salesregions.csv
```

## Update the sample CSV file with Project and Big Query Table

Open the CSV file at:
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/sample-input/create-tags/tags-opt-1-all-metadata.csv"
                              text="tags-opt-1-all-metadata.csv">
</walkthrough-editor-open-file>.

Replace the placeholders with your Project information
```
Replace PROJECT_ID with your Project
Replace DATASET_ID with us_state_sales
Replace TABLE_ID with us_state_salesregions
Replace TEMPLATE_ID with my_tutorial_template
```

## Execute the Python CLI

Run the Python CLI:
```bash
datacatalog-util tags create \
--csv-file ~/cloudshell_open/datacatalog-util/sample-input/create-tags/tags-opt-1-all-metadata.csv
```

You will receive the error:
```
WARNING:root:Permission denied when getting Tag Template 
projects/uat-tools/locations/us-central1/tagTemplates/my_tutorial_template.
Unable to create Tags using it.
```
Because the Tag Template does not exist, so lets create it.

## Create the Tag Template

Open the CSV file at:
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/sample-input/create-tag-templates/tag-templates-opt-1-all-metadata.csv"
                              text="tag-templates-opt-1-all-metadata.csv">
</walkthrough-editor-open-file>.

Replace the placeholders with your Project information
```
Replace PROJECT_ID with your Project
Replace TEMPLATE_ID with my_tutorial_template
```

Run the Python CLI:
```bash
datacatalog-util tag-templates create \
--csv-file ~/cloudshell_open/datacatalog-util/sample-input/create-tag-templates/tag-templates-opt-1-all-metadata.csv
```

## Create Tags

Run the Python CLI:
```bash
datacatalog-util tags create \
--csv-file ~/cloudshell_open/datacatalog-util/sample-input/create-tags/tags-opt-1-all-metadata.csv
```

Now it should succeed.

## Search for the Created Tags

Go to Data Catalog search UI:
[Search UI](https://console.cloud.google.com/datacatalog?q=tag:my_tutorial_template)

Check the search results, and verify the created tags. There will be tags at the Dataset, 
Table and Column levels.

## Delete Tags

Run the Python CLI:
```bash
datacatalog-util tags delete \
--csv-file ~/cloudshell_open/datacatalog-util/sample-input/create-tags/tags-opt-1-all-metadata.csv
```

## Search for the Created Tags

Go to Data Catalog Search UI:
[Search UI](https://console.cloud.google.com/datacatalog?q=tag:my_tutorial_template)

Check the search results, and verify that there are no results. Tags for the `my_tutorial_template` 
have been deleted.

## Congratulations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You've successfully finished the Data Catalog Util Load Tags Tutorial.
