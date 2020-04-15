import unittest
from unittest import mock

import datacatalog_util
from datacatalog_util import datacatalog_util_cli


class TagManagerCLITest(unittest.TestCase):

    def test_parse_args_invalid_subcommand_should_raise_system_exit(self):
        self.assertRaises(SystemExit, datacatalog_util_cli.DatacatalogUtilsCLI._parse_args,
                          ['invalid-subcommand'])

    def test_parse_args_create_tags_missing_mandatory_args_should_raise_system_exit(self):
        self.assertRaises(SystemExit, datacatalog_util_cli.DatacatalogUtilsCLI._parse_args,
                          ['tags', 'create'])

    def test_parse_args_create_tags_should_parse_mandatory_args(self):
        args = datacatalog_util_cli.DatacatalogUtilsCLI._parse_args(
            ['tags', 'create', '--csv-file', 'test.csv'])
        self.assertEqual('test.csv', args.csv_file)

    def test_run_no_args_should_raise_attribute_error(self):
        self.assertRaises(AttributeError, datacatalog_util_cli.DatacatalogUtilsCLI.run, None)

    @mock.patch(
        'datacatalog_util.datacatalog_util_cli.tag_datasource_processor.TagDatasourceProcessor')
    def test_run_create_tags_should_call_tag_creator(self, mock_tag_datasource_processor):
        datacatalog_util_cli.DatacatalogUtilsCLI.run(['tags', 'create', '--csv-file', 'test.csv'])

        tag_datasource_processor = mock_tag_datasource_processor.return_value
        tag_datasource_processor.create_tags_from_csv.assert_called_once()
        tag_datasource_processor.create_tags_from_csv.assert_called_with(file_path='test.csv')

    @mock.patch('datacatalog_util.datacatalog_util_cli.tag_template_datasource_processor.'
                'TagTemplateDatasourceProcessor')
    def test_run_create_tag_templates_should_call_tag_template_creator(
        self, mock_tag_template_datasource_processor):  # noqa: E125

        datacatalog_util_cli.DatacatalogUtilsCLI.run(
            ['tag-templates', 'create', '--csv-file', 'test.csv'])

        tag_template_datasource_processor = mock_tag_template_datasource_processor.return_value
        tag_template_datasource_processor.create_tag_templates_from_csv.assert_called_once()
        tag_template_datasource_processor.create_tag_templates_from_csv.assert_called_with(
            file_path='test.csv')

    @mock.patch('datacatalog_util.datacatalog_util_cli.tag_template_datasource_processor.'
                'TagTemplateDatasourceProcessor')
    def test_run_delete_tag_templates_should_call_correct_method(
        self, mock_tag_template_datasource_processor):  # noqa: E125

        datacatalog_util_cli.DatacatalogUtilsCLI.run(
            ['tag-templates', 'delete', '--csv-file', 'test.csv'])

        tag_template_datasource_processor = mock_tag_template_datasource_processor.return_value
        tag_template_datasource_processor.delete_tag_templates_from_csv.assert_called_once()
        tag_template_datasource_processor.delete_tag_templates_from_csv.assert_called_with(
            file_path='test.csv')

    @mock.patch('datacatalog_util.datacatalog_util_cli.tag_template_datasource_exporter.'
                'TagTemplateDatasourceExporter')
    def test_run_export_tag_templates_should_call_correct_method(
        self, mock_tag_template_datasource_exporter):  # noqa: E125

        datacatalog_util_cli.DatacatalogUtilsCLI.run([
            'tag-templates', 'export', '--file-path', 'test.csv', '--project-ids',
            'my-project1,my-project2'
        ])

        tag_template_datasource_processor = mock_tag_template_datasource_exporter.return_value
        tag_template_datasource_processor.export_tag_templates.assert_called_once()
        tag_template_datasource_processor.export_tag_templates.assert_called_with(
            project_ids='my-project1,my-project2', file_path='test.csv')

    @mock.patch(
        'datacatalog_util.datacatalog_util_cli.tag_datasource_exporter.TagDatasourceExporter')
    def test_run_export_tags_should_call_correct_method(self, mock_tag_datasource_exporter):
        datacatalog_util_cli.DatacatalogUtilsCLI.run([
            'tags', 'export', '--dir-path', 'test.csv', '--project-ids', 'my-project1,my-project2'
        ])

        tag_datasource_processor = mock_tag_datasource_exporter.return_value
        tag_datasource_processor.export_tags.assert_called_once()
        tag_datasource_processor.export_tags.assert_called_with(
            project_ids='my-project1,my-project2', dir_path='test.csv')

    @mock.patch('datacatalog_util.datacatalog_util_cli.DatacatalogUtilsCLI')
    def test_main_should_call_cli_run(self, mock_cli):
        datacatalog_util.main()
        mock_cli.run.assert_called_once()
