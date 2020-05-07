<!---
Note: This tutorial is meant for Google Cloud Shell, and can be opened by going to
http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/open?git_repo=https://github.com/mesmacosta/datacatalog-util&tutorial=tutorials/tag-templates/TUTORIAL.LOAD.md)--->
# Data Catalog Util Load Tag Templates Tutorial

<!-- TODO: analytics id? -->
<walkthrough-author name="mesmacosta@gmail.com" tutorialName="Data Catalog Util Load Tag Templates Tutorial" repositoryUrl="https://github.com/mesmacosta/datacatalog-util"></walkthrough-author>

## Intro

This tutorial will walk you through the execution of the Data Catalog Util Load Tag Templates CLI.

## Python CLI

This tutorial uses a Python CLI, if you want to look at the code open:
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/src/datacatalog_util/datacatalog_util_cli.py"
                              text="datacatalog_util_cli.py">
</walkthrough-editor-open-file>.

Otherwise go to the next step.

## CSV fields

Go to the
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/README.md" text="README.md">
</walkthrough-editor-open-file> file, and find the 4. Load Templates from CSV file.
This section explains the CSV columns used to create Data Catalog Tag Templates.

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
gcloud iam service-accounts create datacatalog-util-tmplate-ld-sa \
--display-name  "Service Account for Data Catalog Util Tag Templates Load CLI" \
--project $PROJECT_ID
```

Next create a credentials folder where the Service Account will be saved.
```bash
mkdir -p ~/credentials
```

Next create and download the Service Account Key.
```bash
gcloud iam service-accounts keys create "datacatalog-util-tmplate-ld-sa.json" \
--iam-account "datacatalog-util-tmplate-ld-sa@$PROJECT_ID.iam.gserviceaccount.com" \
&& mv datacatalog-util-tmplate-ld-sa.json ~/credentials/datacatalog-util-tmplate-ld-sa.json
```

Next add Data Catalog admin role to the Service Account.
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
--member "serviceAccount:datacatalog-util-tmplate-ld-sa@$PROJECT_ID.iam.gserviceaccount.com" \
--quiet \
--project $PROJECT_ID \
--role "roles/datacatalog.admin"
```

Next set up the credentials environment variable.
```bash
export GOOGLE_APPLICATION_CREDENTIALS=~/credentials/datacatalog-util-tmplate-ld-sa.json
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

## Update the sample CSV file with Project and Template info

Open the CSV file at:
<walkthrough-editor-open-file filePath="cloudshell_open/datacatalog-util/sample-input/create-tag-templates/tag-templates-opt-1-all-metadata.csv"
                              text="tag-templates-opt-1-all-metadata.csv">
</walkthrough-editor-open-file>.

Replace the placeholders with your Project information
```
Replace PROJECT_ID with your Project
Replace TEMPLATE_ID with my_tutorial_template
```

## Execute the Python CLI

Run the Python CLI:
```bash
datacatalog-util tag-templates create \
--csv-file ~/cloudshell_open/datacatalog-util/sample-input/create-tag-templates/tag-templates-opt-1-all-metadata.csv
```

Now it should succeed.

## Search for the Created Tag Templates

Go to Data Catalog search UI:
[Search UI](https://console.cloud.google.com/datacatalog?q=my_tutorial_template&qTypes=TAG_TEMPLATE)

Check the search results, and verify the created Tag Template.

## Delete Tag Templates

Run the Python CLI:
```bash
datacatalog-util tag-templates delete \
--csv-file ~/cloudshell_open/datacatalog-util/sample-input/create-tag-templates/tag-templates-opt-1-all-metadata.csv
```

## Search for the Created Tag Templates

Go to Data Catalog search UI:
[Search UI](https://console.cloud.google.com/datacatalog?q=my_tutorial_template&qTypes=TAG_TEMPLATE)

Check the search results, and verify that there are no results. The Tag Template `my_tutorial_template` 
have been deleted.

## Congratulations!

<walkthrough-conclusion-trophy></walkthrough-conclusion-trophy>

You've successfully finished the Data Catalog Util Load Tag Templates Tutorial.
