<!---
Note: This tutorial is meant for Google Cloud Shell, and can be opened by going to
http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/TUTORIAL.md)--->
# Data Catalog Util Tutorial

<!-- TODO: analytics id? -->
<walkthrough-author name="mesmacosta@gmail.com" tutorialName="Data Catalog Util Tutorial" repositoryUrl="https://github.com/mesmacosta/datacatalog-util"></walkthrough-author>

## Intro

This tutorial will walk you through the execution of the Data Catalog Util CLI.

## Python CLI

This tutorial uses a Python CLI, if you want to look at the code open:
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/src/datacatalog_util/datacatalog_util_cli.py"
                              text="datacatalog_util_cli.py">
</walkthrough-editor-open-file>.

Otherwise go to the next step.

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
gcloud iam service-accounts create datacatalog-util-sa \
--display-name  "Service Account for Data Catalog Util Tags Export CLI" \
--project $PROJECT_ID
```

Next create a credentials folder where the Service Account will be saved.
```bash
mkdir -p ~/credentials
```

Next create and download the Service Account Key.
```bash
gcloud iam service-accounts keys create "datacatalog-util-sa.json" \
--iam-account "datacatalog-util-sa@$PROJECT_ID.iam.gserviceaccount.com" \
&& mv datacatalog-util-sa.json ~/credentials/datacatalog-util-sa.json
```

Next add Data Catalog admin role to the Service Account.
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:datacatalog-util-sa@$PROJECT_ID.iam.gserviceaccount.com" \
--quiet \
--project $PROJECT_ID \
--role "roles/datacatalog.admin"
```

Next add Storage admin role to the Service Account.
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:datacatalog-util-sa@$PROJECT_ID.iam.gserviceaccount.com" \
--quiet \
--project $PROJECT_ID \
--role "roles/storage.admin"
```

Next set up the credentials environment variable.
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/credentials/datacatalog-util-sa.json
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

## Verify the command groups

Run the Python CLI:

```bash
datacatalog-util --help
```

You should receive the following output:
```
tag-templates       Tag Templates commands
tags                Tags commands
filesets            Filesets commands
object-storage      Object Storage commands
```

## Verify the Tag Templates group

```bash
datacatalog-util tag-templates --help
```

You should receive the following output:
```
create              Create Tag Templates from CSV
delete              Delete Tag Templates from CSV
export              Export Tag Templates to CSV
```

## Verify the Tags group

```bash
datacatalog-util tags --help
```

You should receive the following output:
```
create              Create Tags from CSV
delete              Delete Tags from CSV
export              Export Tags to CSV, creates one file for each
                    teamplate
```

## Verify the Filesets group

```bash
datacatalog-util filesets --help
```

You should receive the following output:
```
create              Create Tag Templates from CSV
enrich              Enrich GCS filesets with Tags
clean-up-templates-and-tags
                    Clean up the Fileset Enhancer Template and Tags From
                    the Fileset Entries
delete              Delete Filesets Entry Groups and Entries from CSV
export              Export Filesets to CSV
```

## Verify the Object Storage group

```bash
datacatalog-util object-storage --help
```

You should receive the following output:
```
sync-entries        Synchronize Entries
delete-entries      Delete Entries
```

## Congratulations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You've successfully finished the Data Catalog Util Tutorial. For more details on each command, please look at each command tutorial on the README.md file.
