import unittest
from unittest import mock

import pandas as pd
from google.cloud.datacatalog import enums, types

from datacatalog_util import tag_template_datasource_processor


@mock.patch('datacatalog_util.tag_template_datasource_processor.pd.read_csv')
class TagTemplateDatasourceProcessorTest(unittest.TestCase):

    @mock.patch('datacatalog_util.datacatalog_facade.DataCatalogFacade')
    def setUp(self, mock_datacatalog_facade):
        self.__tag_datasource_processor = tag_template_datasource_processor. \
            TagTemplateDatasourceProcessor()
        # Shortcut for the object assigned to self.__tag_datasource_processor.__datacatalog_facade
        self.__datacatalog_facade = mock_datacatalog_facade.return_value

    def test_constructor_should_set_instance_attributes(self, mock_read_csv):
        self.assertIsNotNone(self.__tag_datasource_processor.
                             __dict__['_TagTemplateDatasourceProcessor__datacatalog_facade'])

    def test_create_tag_templates_from_csv_should_succeed(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            data={
                'template_name':
                ['my-template', 'my-template', 'my-template', 'my-template', 'my-template'],
                'display_name': [
                    'My Template for test', 'My Template for test', 'My Template for test',
                    'My Template for test', 'My Template for test'
                ],
                'field_id':
                ['string_field', 'boolean_field', 'double_field', 'timestamp_field', 'enum_field'],
                'field_display_name': [
                    'My String Field', 'My Boolean Field', 'My Double Field', 'My Timestamp Field',
                    'My Enum Field'
                ],
                'field_type': [
                    'STRING',
                    'BOOL',
                    'DOUBLE',
                    'TIMESTAMP',
                    'ENUM',
                ],
                'enum_values': [None, None, None, None, 'PII_1|PII_2|PII_3|PII_4|PII_5|PII_6']
            })

        self.execute_create_tag_template_and_assert()

    def test_create_tag_templates_from_csv_missing_values_should_succeed(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            data={
                'template_name': ['my-template', None, None, None, None],
                'display_name': ['My Template for test', None, None, None, None],
                'field_id':
                ['string_field', 'boolean_field', 'double_field', 'timestamp_field', 'enum_field'],
                'field_display_name': [
                    'My String Field', 'My Boolean Field', 'My Double Field', 'My Timestamp Field',
                    'My Enum Field'
                ],
                'field_type': [
                    'STRING',
                    'BOOL',
                    'DOUBLE',
                    'TIMESTAMP',
                    'ENUM',
                ],
                'enum_values': [None, None, None, None, 'PII_1|PII_2|PII_3|PII_4|PII_5|PII_6']
            })

        self.execute_create_tag_template_and_assert()

    def test_create_tag_templates_from_csv_unordered_columns_should_succeed(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            data={
                'field_id':
                ['string_field', 'boolean_field', 'double_field', 'timestamp_field', 'enum_field'],
                'field_display_name': [
                    'My String Field', 'My Boolean Field', 'My Double Field', 'My Timestamp Field',
                    'My Enum Field'
                ],
                'display_name': ['My Template for test', None, None, None, None],
                'enum_values': [None, None, None, None, 'PII_1|PII_2|PII_3|PII_4|PII_5|PII_6'],
                'field_type': [
                    'STRING',
                    'BOOL',
                    'DOUBLE',
                    'TIMESTAMP',
                    'ENUM',
                ],
                'template_name': ['my-template', None, None, None, None]
            })

        self.execute_create_tag_template_and_assert()

    def test_delete_tag_templates_from_csv_should_succeed(self, mock_read_csv):
        mock_read_csv.return_value = pd.DataFrame(
            data={
                'template_name':
                ['my-template', 'my-template', 'my-template', 'my-template', 'my-template'],
                'display_name': [
                    'My Template for test', 'My Template for test', 'My Template for test',
                    'My Template for test', 'My Template for test'
                ],
                'field_id':
                ['string_field', 'boolean_field', 'double_field', 'timestamp_field', 'enum_field'],
                'field_display_name': [
                    'My String Field', 'My Boolean Field', 'My Double Field', 'My Timestamp Field',
                    'My Enum Field'
                ],
                'field_type': [
                    'STRING',
                    'BOOL',
                    'DOUBLE',
                    'TIMESTAMP',
                    'ENUM',
                ],
                'enum_values': [None, None, None, None, 'PII_1|PII_2|PII_3|PII_4|PII_5|PII_6']
            })

        self.__tag_datasource_processor.delete_tag_templates_from_csv('file-path')
        self.assertEqual(1, self.__datacatalog_facade.delete_tag_template.call_count)
        self.assertEqual(0, self.__datacatalog_facade.get_tag_template.call_count)
        self.assertEqual(0, self.__datacatalog_facade.extract_resources_from_template.call_count)

    def execute_create_tag_template_and_assert(self):
        datacatalog_facade = self.__datacatalog_facade
        datacatalog_facade.get_tag_template.return_value = make_fake_tag_template()
        datacatalog_facade.create_or_update_tag.side_effect = lambda *args: args[1]
        project_id, location_id, tag_template_id = 'my_project', 'my_location', 'my-template'
        datacatalog_facade.extract_resources_from_template.return_value = (project_id, location_id,
                                                                           tag_template_id)
        datacatalog_facade.create_tag_template.side_effect = mock_created_tag_template
        created_tag_templates = self.__tag_datasource_processor.create_tag_templates_from_csv(
            'file-path')
        self.assertEqual(1, len(created_tag_templates))
        created_tag_template = created_tag_templates[0]
        self.assertEqual('my-template', created_tag_template.name)
        string_field = created_tag_template.fields['string_field']
        boolean_field = created_tag_template.fields['boolean_field']
        double_field = created_tag_template.fields['double_field']
        timestamp_field = created_tag_template.fields['timestamp_field']
        enum_field = created_tag_template.fields['enum_field']
        self.assertEqual('My String Field', string_field.display_name)
        self.assertEqual(2, string_field.type.primitive_type)
        self.assertEqual('My Boolean Field', boolean_field.display_name)
        self.assertEqual(3, boolean_field.type.primitive_type)
        self.assertEqual('My Double Field', double_field.display_name)
        self.assertEqual(1, double_field.type.primitive_type)
        self.assertEqual('My Timestamp Field', timestamp_field.display_name)
        self.assertEqual(4, timestamp_field.type.primitive_type)
        enum_allowed_values = enum_field.type.enum_type.allowed_values
        self.assertEqual('My Enum Field', enum_field.display_name)
        self.assertEqual('PII_1', enum_allowed_values[0].display_name)
        self.assertEqual('PII_2', enum_allowed_values[1].display_name)
        self.assertEqual('PII_3', enum_allowed_values[2].display_name)
        self.assertEqual('PII_4', enum_allowed_values[3].display_name)
        self.assertEqual('PII_5', enum_allowed_values[4].display_name)
        self.assertEqual('PII_6', enum_allowed_values[5].display_name)


def mock_created_tag_template(*args):
    tag_template_id = args[2]
    create_tag_template = args[3]
    create_tag_template.name = tag_template_id
    return create_tag_template


def make_fake_tag_template():
    tag_template = types.TagTemplate()
    tag_template.name = 'test_template'
    tag_template.fields['bool_field'].type.primitive_type = enums.FieldType.PrimitiveType.BOOL
    tag_template.fields['string_field'].type.primitive_type = enums.FieldType.PrimitiveType.STRING

    return tag_template
