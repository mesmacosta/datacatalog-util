<!---
Note: This tutorial is meant for Google Cloud Shell, and can be opened by going to
http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/filesets/TUTORIAL.EXPORT.md)--->
# Data Catalog Util Export Filesets Tutorial

<!-- TODO: analytics id? -->
<walkthrough-author name="mesmacosta@gmail.com" tutorialName="Data Catalog Util Export Filesets Tutorial" repositoryUrl="https://github.com/mesmacosta/datacatalog-util"></walkthrough-author>

## Intro

This tutorial will walk you through the execution of the Data Catalog Util Export Filesets CLI. 
If you don't have Filesets in your Project, you may run the Load Filesets tutorial first.

## Python CLI

This tutorial uses a Python CLI, if you want to look at the code open:
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/src/datacatalog_util/datacatalog_util_cli.py"
                              text="datacatalog_util_cli.py">
</walkthrough-editor-open-file>.

Otherwise go to the next step.

## CSV fields

Go to the
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/README.md" text="README.md">
</walkthrough-editor-open-file> file, and find the 7. Export Filesets to CSV file.
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
gcloud iam service-accounts create datacatalog-util-filst-exp-sa \
--display-name  "Service Account for Data Catalog Util Filesets Export CLI" \
--project $PROJECT_ID
```

Next create a credentials folder where the Service Account will be saved.
```bash
mkdir -p ~/credentials
```

Next create and download the Service Account Key.
```bash
gcloud iam service-accounts keys create "datacatalog-util-filst-exp-sa.json" \
--iam-account "datacatalog-util-filst-exp-sa@$PROJECT_ID.iam.gserviceaccount.com" \
&& mv datacatalog-util-filst-exp-sa.json ~/credentials/datacatalog-util-filst-exp-sa.json
```

Next add Data Catalog admin role to the Service Account.
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:datacatalog-util-filst-exp-sa@$PROJECT_ID.iam.gserviceaccount.com" \
--quiet \
--project $PROJECT_ID \
--role "roles/datacatalog.admin"
```

Next set up the credentials environment variable.
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/credentials/datacatalog-util-filst-exp-sa.json
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

## Execute the Python CLI

Run the Python CLI:

Create an output folder:
```bash
mkdir -p ~/output
```

Run the CLI:
```bash
datacatalog-util filesets export --project-ids $PROJECT_ID --file-path ~/output/filesets.csv
```

Let's see the output:
```bash
ls -l ~/output
```

Use the Cloud Editor to see the <walkthrough-editor-open-file filePath="output/filesets.csv" text="filesets.csv">
</walkthrough-editor-open-file> file, or upload it to Google Sheets to better visualize it.

## Congratulations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You've successfully finished the Data Catalog Util Export Filesets Tutorial.
