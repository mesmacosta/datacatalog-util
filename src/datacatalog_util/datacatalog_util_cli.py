import argparse
import logging
import sys

from datacatalog_tag_manager import tag_datasource_processor
from datacatalog_util import tag_datasource_exporter
from datacatalog_util import tag_template_datasource_processor
from datacatalog_util import tag_template_datasource_exporter


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

        cls.add_create_tags_cmd(subparsers)

        cls.add_create_tag_templates_cmd(subparsers)

        cls.add_delete_tag_templates_cmd(subparsers)

        cls.add_export_tag_templates_cmd(subparsers)

        cls.add_export_tags_cmd(subparsers)

        return parser.parse_args(argv)

    @classmethod
    def add_export_tag_templates_cmd(cls, subparsers):
        export_tag_templates_parser = subparsers.add_parser('export-tag-templates',
                                                            help='Export Tag Templates')
        export_tag_templates_parser.add_argument('--file-path',
                                                 help='File path where file will be exported')
        export_tag_templates_parser.add_argument('--project-ids',
                                                 help='Project ids to narrow down Templates list,'
                                                 'split by comma',
                                                 required=True)
        export_tag_templates_parser.set_defaults(func=cls.__export_tag_templates)

    @classmethod
    def add_export_tags_cmd(cls, subparsers):
        export_tag_templates_parser = subparsers.add_parser('export-tags',
                                                            help='Export Tags, creates one file'
                                                            'for each teamplate')
        export_tag_templates_parser.add_argument(
            '--dir-path', help='Directory path where files will be exported')
        export_tag_templates_parser.add_argument('--project-ids',
                                                 help='Project ids to narrow down Templates list,'
                                                 'split by comma',
                                                 required=True)
        export_tag_templates_parser.set_defaults(func=cls.__export_tags)

    @classmethod
    def add_delete_tag_templates_cmd(cls, subparsers):
        delete_tag_templates_parser = subparsers.add_parser('delete-tag-templates',
                                                            help='Delete Tag Templates')
        delete_tag_templates_parser.add_argument('--csv-file',
                                                 help='CSV file with Tag Templates information',
                                                 required=True)
        delete_tag_templates_parser.set_defaults(func=cls.__delete_tag_templates)

    @classmethod
    def add_create_tag_templates_cmd(cls, subparsers):
        create_tag_templates_parser = subparsers.add_parser('create-tag-templates',
                                                            help='Create Tag Templates')
        create_tag_templates_parser.add_argument('--csv-file',
                                                 help='CSV file with Tag Templates information',
                                                 required=True)
        create_tag_templates_parser.set_defaults(func=cls.__create_tag_templates)

    @classmethod
    def add_create_tags_cmd(cls, subparsers):
        create_tags_parser = subparsers.add_parser('create-tags', help='Create Tags')
        create_tags_parser.add_argument('--csv-file',
                                        help='CSV file with Tags information',
                                        required=True)
        create_tags_parser.set_defaults(func=cls.__create_tags)

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
