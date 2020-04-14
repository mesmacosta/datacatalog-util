import os
import unittest
from unittest import mock

import pandas as pd
from google.cloud import datacatalog_v1beta1
from pandas._testing import assert_frame_equal

from datacatalog_util import tag_template_datasource_exporter, constant


class TagDatasourceExporterTest(unittest.TestCase):

    @mock.patch('datacatalog_util.datacatalog_facade.DataCatalogFacade')
    def setUp(self, mock_datacatalog_facade):
        self.__tag_template_datasource_exporter = tag_template_datasource_exporter. \
            TagTemplateDatasourceExporter()
        # Shortcut for the object assigned to self.__datacatalog_facade.__datacatalog
        self.__datacatalog_facade = mock_datacatalog_facade.return_value
        self.__csv_file_path = os.path.dirname(os.path.abspath(__file__))
        self.__template_file_path = os.path.join(self.__csv_file_path, 'templates.csv')

    def test_constructor_should_set_instance_attributes(self):
        self.assertIsNotNone(self.__tag_template_datasource_exporter.
                             __dict__['_TagTemplateDatasourceExporter__datacatalog_facade'])

    def test_export_tag_templates_when_no_templates_should_create_empty_file(self):
        self.__tag_template_datasource_exporter.export_tag_templates('my-project',
                                                                     self.__template_file_path)

        created_template_file = pd.read_csv(self.__template_file_path)

        # Cleans up templates file.
        os.remove(self.__template_file_path)

        self.assertTrue(created_template_file.empty)

        self.assertEqual(1, self.__datacatalog_facade.search_tag_templates.call_count)
        self.assertEqual(
            1, self.__datacatalog_facade.get_tag_templates_from_search_results.call_count)

    def test_export_tag_templates_when_templates_should_create_file(self):
        tag_template_id = 'my_template'
        tag_template_id_2 = 'my_template_2'

        search_template_result = MockedObject()
        search_template_result.relative_resource_name = tag_template_id
        search_template_result_2 = MockedObject()
        search_template_result_2.relative_resource_name = tag_template_id_2
        self.__datacatalog_facade.search_tag_templates.return_value = [
            search_template_result, search_template_result_2
        ]

        self.__datacatalog_facade.get_tag_templates_from_search_results.return_value = [
            create_default_template(tag_template_id),
            create_default_template(tag_template_id_2)
        ]

        self.__tag_template_datasource_exporter.export_tag_templates('my-project',
                                                                     self.__template_file_path)

        created_templates_file = pd.read_csv(self.__template_file_path)
        expected_templates_file = pd.read_csv(
            os.path.join(self.__csv_file_path, 'data', 'templates.csv'))

        # Cleans up templates file.
        os.remove(self.__template_file_path)

        # Fill null fields so the sorting will produce deterministic results.
        created_templates_file[constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[0]].fillna(method='pad',
                                                                                  inplace=True)
        created_templates_file[constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[1]].fillna(method='pad',
                                                                                  inplace=True)
        expected_templates_file[constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[0]].fillna(method='pad',
                                                                                   inplace=True)
        expected_templates_file[constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[1]].fillna(method='pad',
                                                                                   inplace=True)

        created_templates_file.set_index(constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[0], inplace=True)
        expected_templates_file.set_index(constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[0], inplace=True)

        self.assertEqual(1, self.__datacatalog_facade.search_tag_templates.call_count)
        self.assertEqual(
            1, self.__datacatalog_facade.get_tag_templates_from_search_results.call_count)

        assert_frame_equal(
            created_templates_file.sort_values([
                constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[0],
                constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[2]
            ]),
            expected_templates_file.sort_values([
                constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[0],
                constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[2]
            ]))


def create_default_template(template_name):
    tag_template = datacatalog_v1beta1.types.TagTemplate()

    tag_template.name = template_name

    tag_template.display_name = template_name

    tag_template.fields['source'].display_name = 'Source of data asset'
    tag_template.fields['source'].type.primitive_type = \
        datacatalog_v1beta1.enums.FieldType.PrimitiveType.STRING.value

    tag_template.fields['num_rows'].display_name = 'Number of rows in data asset'
    tag_template.fields['num_rows'].type.primitive_type = \
        datacatalog_v1beta1.enums.FieldType.PrimitiveType.DOUBLE.value

    tag_template.fields['has_pii'].display_name = 'Has PII'
    tag_template.fields['has_pii'].type.primitive_type = \
        datacatalog_v1beta1.enums.FieldType.PrimitiveType.BOOL.value

    tag_template.fields['pii_type'].display_name = 'PII type'
    tag_template.fields['pii_type'].type.enum_type \
        .allowed_values.add().display_name = 'EMAIL'
    tag_template.fields['pii_type'].type.enum_type \
        .allowed_values.add().display_name = 'SOCIAL SECURITY NUMBER'
    tag_template.fields['pii_type'].type.enum_type \
        .allowed_values.add().display_name = 'NONE'

    tag_template.fields['execution_time'].type.primitive_type = \
        datacatalog_v1beta1.enums.FieldType.PrimitiveType.TIMESTAMP.value

    return tag_template


class MockedObject(object):

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]
