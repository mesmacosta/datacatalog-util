import argparse
import logging
import sys

from datacatalog_fileset_enricher import datacatalog_fileset_enricher
from datacatalog_tag_manager import tag_datasource_processor
from datacatalog_tag_template_exporter import tag_template_datasource_exporter
from datacatalog_tag_template_processor import tag_template_datasource_processor

from datacatalog_util import tag_datasource_exporter


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

        return parser.parse_args(argv)

    @classmethod
    def add_tags_cmd(cls, subparsers):
        tags_parser = subparsers.add_parser("tags", help="Tags commands")

        tags_subparsers = tags_parser.add_subparsers()

        cls.add_create_tags_cmd(tags_subparsers)

        cls.add_export_tags_cmd(tags_subparsers)

    @classmethod
    def add_tag_templates_cmd(cls, subparsers):
        tag_templates_parser = subparsers.add_parser("tag-templates",
                                                     help="Tag Templates commands")

        tag_templates_subparsers = tag_templates_parser.add_subparsers()

        cls.add_create_tag_templates_cmd(tag_templates_subparsers)

        cls.add_delete_tag_templates_cmd(tag_templates_subparsers)

        cls.add_export_tag_templates_cmd(tag_templates_subparsers)

    @classmethod
    def add_export_tags_cmd(cls, subparsers):
        export_tags_parser = subparsers.add_parser('export',
                                                   help='Export Tags to CSV,'
                                                        ' creates one file'
                                                        ' for each teamplate')
        export_tags_parser.add_argument('--dir-path',
                                        help='Directory path where files will be exported')
        export_tags_parser.add_argument('--project-ids',
                                        help='Project ids to narrow down Templates list,'
                                             'split by comma',
                                        required=True)
        export_tags_parser.set_defaults(func=cls.__export_tags)

    @classmethod
    def add_export_tag_templates_cmd(cls, subparsers):
        export_tag_templates_parser = subparsers.add_parser('export',
                                                            help='Export Tag Templates to CSV')
        export_tag_templates_parser.add_argument('--file-path',
                                                 help='File path where file will be exported')
        export_tag_templates_parser.add_argument('--project-ids',
                                                 help='Project ids to narrow down Templates list,'
                                                      'split by comma',
                                                 required=True)
        export_tag_templates_parser.set_defaults(func=cls.__export_tag_templates)

    @classmethod
    def add_fileset_enricher_cmd(cls, subparsers):
        filesets_parser = subparsers.add_parser("filesets", help="Filesets commands")

        filesets_parser.add_argument('--project-id', help='Project id', required=True)

        filesets_subparsers = filesets_parser.add_subparsers()

        enrich_filesets = filesets_subparsers.add_parser('enrich',
                                                         help='Enrich GCS filesets with Tags')

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
        clean_up_tags.set_defaults(func=cls.__clean_up_fileset_template_and_tags)

        clean_up_all = filesets_subparsers.add_parser(
            'clean-up-all',
            help='Clean up Fileset Entries, Their Tags and the Fileset Enhancer Template')
        clean_up_all.set_defaults(func=cls.__clean_up_all_filesets)

    @classmethod
    def add_delete_tag_templates_cmd(cls, subparsers):
        delete_tag_templates_parser = subparsers.add_parser('delete',
                                                            help='Delete Tag Templates from CSV')
        delete_tag_templates_parser.add_argument('--csv-file',
                                                 help='CSV file with Tag Templates information',
                                                 required=True)
        delete_tag_templates_parser.set_defaults(func=cls.__delete_tag_templates)

    @classmethod
    def add_create_tag_templates_cmd(cls, subparsers):
        create_tag_templates_parser = subparsers.add_parser('create',
                                                            help='Create Tag Templates from CSV')
        create_tag_templates_parser.add_argument('--csv-file',
                                                 help='CSV file with Tag Templates information',
                                                 required=True)
        create_tag_templates_parser.set_defaults(func=cls.__create_tag_templates)

    @classmethod
    def add_create_tags_cmd(cls, subparsers):
        create_tags_parser = subparsers.add_parser('create', help='Create Tags from CSV')
        create_tags_parser.add_argument('--csv-file',
                                        help='CSV file with Tags information',
                                        required=True)
        create_tags_parser.set_defaults(func=cls.__create_tags)

    @classmethod
    def __enrich_fileset(cls, args):
        tag_fields = None
        if args.tag_fields:
            tag_fields = args.tag_fields.split(',')

        datacatalog_fileset_enricher.DatacatalogFilesetEnricher(args.project_id).run(
            args.entry_group_id, args.entry_id, tag_fields, args.bucket_prefix)

    @classmethod
    def __clean_up_fileset_template_and_tags(cls, args):
        datacatalog_fileset_enricher.DatacatalogFilesetEnricher(
            args.project_id).clean_up_fileset_template_and_tags()

    @classmethod
    def __clean_up_all_filesets(cls, args):
        datacatalog_fileset_enricher.DatacatalogFilesetEnricher(args.project_id).clean_up_all()

    @classmethod
    def __create_tags(cls, args):
        tag_datasource_processor.TagDatasourceProcessor().create_tags_from_csv(
            file_path=args.csv_file)

    @classmethod
    def __create_tag_templates(cls, args):
        tag_template_datasource_processor.TagTemplateDatasourceProcessor(
        ).create_tag_templates_from_csv(file_path=args.csv_file)

    @classmethod
    def __delete_tag_templates(cls, args):
        tag_template_datasource_processor.TagTemplateDatasourceProcessor(
        ).delete_tag_templates_from_csv(file_path=args.csv_file)

    @classmethod
    def __export_tag_templates(cls, args):
        tag_template_datasource_exporter.TagTemplateDatasourceExporter().export_tag_templates(
            project_ids=args.project_ids, file_path=args.file_path)

    @classmethod
    def __export_tags(cls, args):
        tag_datasource_exporter.TagDatasourceExporter().export_tags(project_ids=args.project_ids,
                                                                    dir_path=args.dir_path)


def main():
    argv = sys.argv
    DatacatalogUtilsCLI.run(argv[1:] if len(argv) > 0 else argv)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
