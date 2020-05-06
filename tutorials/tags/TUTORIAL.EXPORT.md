<!---
Note: This tutorial is meant for Google Cloud Shell, and can be opened by going to
http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/tags/TUTORIAL.EXPORT.md--->
# Data Catalog Util Export Tags Tutorial

<!-- TODO: analytics id? -->
<walkthrough-author name="mesmacosta@gmail.com" tutorialName="Data Catalog Util Export Tags Tutorial" repositoryUrl="https://github.com/mesmacosta/datacatalog-util"></walkthrough-author>

## Intro

This tutorial will walk you through the execution of the Data Catalog Fileset Exporter.

## Python CLI

This script is a Python CLI, if you want to look at the code open:
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-fileset-exporter/src/datacatalog_fileset_exporter/datacatalog_fileset_exporter_cli.py"
                              text="datacatalog_fileset_exporter_cli.py">
</walkthrough-editor-open-file>.

Otherwise go to the next step.

## CSV fields

Go to the
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-fileset-exporter/README.md" text="README.md">
</walkthrough-editor-open-file> file, and find the 5. Export Filesets to CSV file section.
This section explains the CSV columns created when the Python CLI is executed.

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
gcloud iam service-accounts create datacatalog-fs-exporter-sa \
--display-name  "Service Account for Fileset Exporter" \
--project $PROJECT_ID
```

Next create a credentials folder where the Service Account will be saved.
```bash
mkdir -p ~/credentials
```

Next create and download the Service Account Key.
```bash
gcloud iam service-accounts keys create "datacatalog-fs-exporter-sa.json" \
--iam-account "datacatalog-fs-exporter-sa@$PROJECT_ID.iam.gserviceaccount.com" \
&& mv datacatalog-fs-exporter-sa.json ~/credentials/datacatalog-fs-exporter-sa.json
```

Next add Data Catalog admin role to the Service Account.
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:datacatalog-fs-exporter-sa@$PROJECT_ID.iam.gserviceaccount.com" \
--quiet \
--project $PROJECT_ID \
--role "roles/datacatalog.admin"
```

Next set up the credentials environment variable.
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/credentials/datacatalog-fs-exporter-sa.json
```

## Install the Python CLI

Install and config the datacatalog-fileset-exporter CLI.
```bash
pip3 install datacatalog-fileset-exporter --user
```
Next load it to your PATH.
```bash
export PATH=~/.local/bin:$PATH
```

Next test it out.
```bash
datacatalog-fileset-exporter --help
```

## Execute the Python CLI

Run the Python CLI:

Create an output folder:
```bash
mkdir -p ~/output
```

Run the CLI:
```bash
datacatalog-fileset-exporter filesets export --project-ids $PROJECT_ID --file-path ~/output/filesets.csv
```

Let's see the output:
```bash
cat ~/output/filesets.csv
```

Use the Cloud Editor to see the <walkthrough-editor-open-file filePath="output/filesets.csv" text="filesets.csv">
</walkthrough-editor-open-file> file, or upload it to Google Sheets to better visualize it.

## Congratulations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You've successfully finished the Data Catalog Fileset Exporter Tutorial.
