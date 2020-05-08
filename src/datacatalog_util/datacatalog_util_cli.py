import argparse
import logging
import sys

from datacatalog_fileset_enricher import datacatalog_fileset_enricher
from datacatalog_fileset_exporter import datacatalog_fileset_exporter_cli
from datacatalog_fileset_processor import datacatalog_fileset_processor_cli
from datacatalog_tag_exporter import datacatalog_tag_exporter_cli
from datacatalog_tag_manager import tag_datasource_processor
from datacatalog_tag_template_exporter import datacatalog_tag_template_exporter_cli
from datacatalog_tag_template_processor import datacatalog_tag_template_processor_cli
from datacatalog_object_storage_processor import datacatalog_object_storage_processor_cli


class DatacatalogUtilsCLI:

    @classmethod
    def run(cls, argv):
        cls.__setup_logging()

        args = cls._parse_args(argv)
        args.func(args)

    @classmethod
    def __setup_logging(cls):
        logging.basicConfig(level=logging.INFO)

    @classmethod
    def _parse_args(cls, argv):
        parser = argparse.ArgumentParser(description=__doc__,
                                         formatter_class=argparse.RawDescriptionHelpFormatter)

        subparsers = parser.add_subparsers()

        cls.add_tag_templates_cmd(subparsers)

        cls.add_tags_cmd(subparsers)

        cls.add_fileset_enricher_cmd(subparsers)

        datacatalog_object_storage_processor_cli.DatacatalogObjectStorageProcessorCLI.\
            add_object_storage_parser(subparsers)

        return parser.parse_args(argv)

    @classmethod
    def add_tags_cmd(cls, subparsers):
        tags_parser = subparsers.add_parser("tags", help="Tags commands")

        tags_subparsers = tags_parser.add_subparsers()

        cls.add_create_tags_cmd(tags_subparsers)

        cls.add_delete_tags_cmd(tags_subparsers)

        datacatalog_tag_exporter_cli.DatacatalogTagExporterCLI.add_export_tags_cmd(tags_subparsers)

    @classmethod
    def add_tag_templates_cmd(cls, subparsers):
        tag_templates_parser = subparsers.add_parser("tag-templates",
                                                     help="Tag Templates commands")

        tag_templates_subparsers = tag_templates_parser.add_subparsers()

        datacatalog_tag_template_processor_cli.DatacatalogTagTemplateProcessorCLI.\
            add_create_tag_templates_cmd(tag_templates_subparsers)

        datacatalog_tag_template_processor_cli.DatacatalogTagTemplateProcessorCLI.\
            add_delete_tag_templates_cmd(tag_templates_subparsers)

        datacatalog_tag_template_exporter_cli.DatacatalogTagTemplateExporterCLI.\
            add_export_tag_templates_cmd(tag_templates_subparsers)

    @classmethod
    def add_fileset_enricher_cmd(cls, subparsers):
        filesets_parser = subparsers.add_parser("filesets", help="Filesets commands")

        filesets_subparsers = filesets_parser.add_subparsers()

        datacatalog_fileset_processor_cli.DatacatalogFilesetProcessorCLI.\
            add_create_filesets_cmd(filesets_subparsers)

        enrich_filesets = filesets_subparsers.add_parser('enrich',
                                                         help='Enrich GCS filesets with Tags')

        enrich_filesets.add_argument('--project-id', help='Project id', required=True)
        enrich_filesets.add_argument('--tag-template-name',
                                     help='Name of the Fileset Enrich template,'
                                     'i.e: '
                                     'projects/my-project/locations/us-central1/tagTemplates/'
                                     'my_template_test')

        enrich_filesets.add_argument('--entry-group-id', help='Entry Group ID')
        enrich_filesets.add_argument('--entry-id', help='Entry ID')
        enrich_filesets.add_argument('--tag-fields',
                                     help='Specify the fields you want on the generated Tags,'
                                     ' split by comma, use the list available in the docs')
        enrich_filesets.add_argument('--bucket-prefix',
                                     help='Specify a bucket prefix if you want to avoid scanning'
                                     ' too many GCS buckets')
        enrich_filesets.set_defaults(func=cls.__enrich_fileset)

        clean_up_tags = filesets_subparsers.add_parser(
            'clean-up-templates-and-tags',
            help='Clean up the Fileset Enhancer Template and Tags From the Fileset Entries')
        clean_up_tags.add_argument('--project-id', help='Project id', required=True)

        clean_up_tags.set_defaults(func=cls.__clean_up_fileset_template_and_tags)

        datacatalog_fileset_processor_cli.DatacatalogFilesetProcessorCLI.\
            add_delete_filesets_cmd(filesets_subparsers)

        # ADD filesets export command.
        datacatalog_fileset_exporter_cli.DatacatalogFilesetExporterCLI.add_export_filesets_cmd(
            filesets_subparsers)

    @classmethod
    def add_create_tags_cmd(cls, subparsers):
        create_tags_parser = subparsers.add_parser('create', help='Create Tags from CSV')
        create_tags_parser.add_argument('--csv-file',
                                        help='CSV file with Tags information',
                                        required=True)
        create_tags_parser.set_defaults(func=cls.__create_tags)

    @classmethod
    def add_delete_tags_cmd(cls, subparsers):
        create_tags_parser = subparsers.add_parser('delete', help='Delete Tags from CSV')
        create_tags_parser.add_argument('--csv-file',
                                        help='CSV file with Tags information',
                                        required=True)
        create_tags_parser.set_defaults(func=cls.__delete_tags)

    @classmethod
    def __enrich_fileset(cls, args):
        tag_fields = None
        if args.tag_fields:
            tag_fields = args.tag_fields.split(',')

        datacatalog_fileset_enricher.DatacatalogFilesetEnricher(args.project_id).run(
            args.entry_group_id, args.entry_id, tag_fields, args.bucket_prefix,
            args.tag_template_name)

    @classmethod
    def __clean_up_fileset_template_and_tags(cls, args):
        datacatalog_fileset_enricher.DatacatalogFilesetEnricher(
            args.project_id).clean_up_fileset_template_and_tags()

    @classmethod
    def __create_tags(cls, args):
        tag_datasource_processor.TagDatasourceProcessor().create_tags_from_csv(
            file_path=args.csv_file)

    @classmethod
    def __delete_tags(cls, args):
        tag_datasource_processor.TagDatasourceProcessor().delete_tags_from_csv(
            file_path=args.csv_file)


def main():
    argv = sys.argv
    DatacatalogUtilsCLI.run(argv[1:] if len(argv) > 0 else argv)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
