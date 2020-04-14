import os
import unittest
from unittest import mock

import pandas as pd
from google.cloud import datacatalog_v1beta1
from pandas._testing import assert_frame_equal

from datacatalog_util import tag_datasource_exporter, constant


class TagDatasourceExporterTest(unittest.TestCase):

    @mock.patch('datacatalog_util.datacatalog_facade.DataCatalogFacade')
    def setUp(self, mock_datacatalog_facade):
        self.__tag_datasource_exporter = tag_datasource_exporter.TagDatasourceExporter()
        # Shortcut for the object assigned to self.__datacatalog_facade.__datacatalog
        self.__datacatalog_facade = mock_datacatalog_facade.return_value
        self.__csv_file_path = os.path.dirname(os.path.abspath(__file__))
        self.__summary_file_path = os.path.join(self.__csv_file_path, 'summary.csv')

    def tearDown(self):
        if os.path.exists(self.__summary_file_path):
            os.remove(self.__summary_file_path)

    def test_constructor_should_set_instance_attributes(self):
        self.assertIsNotNone(
            self.__tag_datasource_exporter.__dict__['_TagDatasourceExporter__datacatalog_facade'])

    def test_export_tags_when_no_templates_should_not_create_csv_files(self):
        self.__tag_datasource_exporter.export_tags('my-project')
        self.assertEqual(1, self.__datacatalog_facade.search_tag_templates.call_count)
        self.assertEqual(0, self.__datacatalog_facade.extract_resources_from_template.call_count)
        self.assertEqual(0, self.__datacatalog_facade.search_tagged_assets.call_count)
        self.assertEqual(0, self.__datacatalog_facade.list_tags.call_count)

    def test_export_tags_when_no_tags_should_create_summary_file(self):
        search_result = MockedObject()
        search_result.relative_resource_name = 'my_template'
        self.__datacatalog_facade.search_tag_templates.return_value = [search_result]

        project_id, location_id, tag_template_id = 'my_project', 'my_location', 'my_template'

        self.__datacatalog_facade.extract_resources_from_template.return_value = (project_id,
                                                                                  location_id,
                                                                                  tag_template_id)

        self.__tag_datasource_exporter.export_tags('my-project', self.__csv_file_path)

        created_summary_file = pd.read_csv(self.__summary_file_path)

        self.assertEqual(1, self.__datacatalog_facade.search_tag_templates.call_count)
        self.assertEqual(1, self.__datacatalog_facade.extract_resources_from_template.call_count)
        self.assertEqual(1, self.__datacatalog_facade.search_tagged_assets.call_count)
        self.assertEqual(0, self.__datacatalog_facade.list_tags.call_count)
        # Must have only one template with 0 tags
        self.assertEqual(1, len(created_summary_file))
        first_row = created_summary_file.iloc[0]

        self.assertEqual('my_template', first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[0]])
        self.assertEqual(0, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[1]])
        self.assertEqual(0, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[2]])
        self.assertEqual(0, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[3]])
        self.assertEqual(0, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[4]])
        self.assertEqual(0, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[5]])
        self.assertEqual(0, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[6]])
        self.assertEqual(0, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[7]])
        self.assertEqual(0, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[8]])

    def test_export_tags_when_tags_should_create_summary_file_and_template_file(self):
        tag_template_id = 'my_template'
        tag_template_id_2 = 'my_template_2'

        search_template_result = MockedObject()
        search_template_result.relative_resource_name = tag_template_id
        search_template_result_2 = MockedObject()
        search_template_result_2.relative_resource_name = tag_template_id_2
        self.__datacatalog_facade.search_tag_templates.return_value = [
            search_template_result, search_template_result_2
        ]

        project_id, location_id = 'my_project', 'my_location'

        self.__datacatalog_facade.extract_resources_from_template.side_effect = [
            (project_id, location_id, tag_template_id),
            (project_id, location_id, tag_template_id_2)
        ]

        search_tag_result = MockedObject()
        search_tag_result.relative_resource_name = 'my_tagged_entry'
        search_tag_result.linked_resource = 'my_tagged_entry_linked_resource'

        self.__datacatalog_facade.search_tagged_assets.return_value = [search_tag_result]

        self.__datacatalog_facade.list_tags.side_effect = [[
            create_default_tag(tag_template_id, 'my_tag_1')
        ], [create_default_tag(tag_template_id_2, 'my_tag_2')]]

        self.__tag_datasource_exporter.export_tags('my-project', self.__csv_file_path)

        created_summary_file = pd.read_csv(self.__summary_file_path)

        template_1_path = os.path.join(self.__csv_file_path, '{}.csv'.format(tag_template_id))
        template_2_path = os.path.join(self.__csv_file_path, '{}.csv'.format(tag_template_id_2))

        # Cleans up template files.
        os.remove(template_1_path)
        os.remove(template_2_path)

        self.assertEqual(1, self.__datacatalog_facade.search_tag_templates.call_count)
        self.assertEqual(2, self.__datacatalog_facade.extract_resources_from_template.call_count)
        self.assertEqual(2, self.__datacatalog_facade.search_tagged_assets.call_count)
        self.assertEqual(2, self.__datacatalog_facade.list_tags.call_count)
        self.assertEqual(2, len(created_summary_file))
        first_row = created_summary_file.iloc[0]

        self.assertEqual('my_template', first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[0]])
        self.assertEqual(1, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[1]])
        self.assertEqual(1, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[2]])
        self.assertEqual(0, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[3]])
        self.assertEqual(1, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[4]])
        self.assertEqual(1, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[5]])
        self.assertEqual(1, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[6]])
        self.assertEqual(1, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[7]])
        self.assertEqual(1, first_row[constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[8]])

    def test_export_tags_when_tags_on_columns_should_create_summary_file_and_template_file(self):
        tag_template_id = 'my_template'
        tag_template_id_2 = 'my_template_2'

        search_template_result = MockedObject()
        search_template_result.relative_resource_name = tag_template_id
        search_template_result_2 = MockedObject()
        search_template_result_2.relative_resource_name = tag_template_id_2
        self.__datacatalog_facade.search_tag_templates.return_value = [
            search_template_result, search_template_result_2
        ]

        project_id, location_id = 'my_project', 'my_location'

        self.__datacatalog_facade.extract_resources_from_template.side_effect = [
            (project_id, location_id, tag_template_id),
            (project_id, location_id, tag_template_id_2)
        ]

        search_tag_result = MockedObject()
        search_tag_result.relative_resource_name = 'my_tagged_entry'
        search_tag_result.linked_resource = 'my_tagged_entry_linked_resource'

        self.__datacatalog_facade.search_tagged_assets.return_value = [search_tag_result]

        self.__datacatalog_facade.list_tags.side_effect = [[
            create_default_tag(tag_template_id, 'my_tag_1', 'my_col')
        ], [create_default_tag(tag_template_id_2, 'my_tag_2', 'my_col')]]

        self.__tag_datasource_exporter.export_tags('my-project', self.__csv_file_path)

        created_summary_file = pd.read_csv(self.__summary_file_path)

        expected_summary_file = pd.read_csv(
            os.path.join(self.__csv_file_path, 'data', 'summary.csv'))

        template_1_path = os.path.join(self.__csv_file_path, '{}.csv'.format(tag_template_id))
        template_2_path = os.path.join(self.__csv_file_path, '{}.csv'.format(tag_template_id_2))

        created_template_1_file = pd.read_csv(template_1_path)
        created_template_2_file = pd.read_csv(template_2_path)

        expected_template_1_file = pd.read_csv(
            os.path.join(self.__csv_file_path, 'data', '{}.csv'.format(tag_template_id)))
        expected_template_2_file = pd.read_csv(
            os.path.join(self.__csv_file_path, 'data', '{}.csv'.format(tag_template_id_2)))

        # Fill null fields so the sorting will produce deterministic results.
        created_template_1_file[constant.TAGS_DS_EXPORT_COLUMNS_ORDER[0]].fillna(method='pad',
                                                                                 inplace=True)
        created_template_2_file[constant.TAGS_DS_EXPORT_COLUMNS_ORDER[0]].fillna(method='pad',
                                                                                 inplace=True)
        expected_template_1_file[constant.TAGS_DS_EXPORT_COLUMNS_ORDER[0]].fillna(method='pad',
                                                                                  inplace=True)
        expected_template_2_file[constant.TAGS_DS_EXPORT_COLUMNS_ORDER[0]].fillna(method='pad',
                                                                                  inplace=True)

        # Remove numeric index so the sorting will produce deterministic results.
        created_template_1_file.set_index(constant.TAGS_DS_EXPORT_COLUMNS_ORDER[0], inplace=True)
        created_template_2_file.set_index(constant.TAGS_DS_EXPORT_COLUMNS_ORDER[0], inplace=True)
        expected_template_1_file.set_index(constant.TAGS_DS_EXPORT_COLUMNS_ORDER[0], inplace=True)
        expected_template_2_file.set_index(constant.TAGS_DS_EXPORT_COLUMNS_ORDER[0], inplace=True)

        # Filter out timestamp fields, since its filled with execution time.
        created_template_1_file = created_template_1_file[
            created_template_1_file.field_type != 'TIMESTAMP']
        created_template_2_file = created_template_2_file[
            created_template_2_file.field_type != 'TIMESTAMP']
        expected_template_1_file = expected_template_1_file[
            expected_template_1_file.field_type != 'TIMESTAMP']
        expected_template_2_file = expected_template_2_file[
            expected_template_2_file.field_type != 'TIMESTAMP']

        # Cleans up template files.
        os.remove(template_1_path)
        os.remove(template_2_path)

        self.assertEqual(1, self.__datacatalog_facade.search_tag_templates.call_count)
        self.assertEqual(2, self.__datacatalog_facade.extract_resources_from_template.call_count)
        self.assertEqual(2, self.__datacatalog_facade.search_tagged_assets.call_count)
        self.assertEqual(2, self.__datacatalog_facade.list_tags.call_count)
        self.assertEqual(2, len(created_summary_file))

        assert_frame_equal(
            created_summary_file.sort_values([constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[0]]),
            expected_summary_file.sort_values([constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[0]]))

        assert_frame_equal(
            created_template_1_file.sort_values([constant.TAGS_DS_EXPORT_COLUMNS_ORDER[5]]),
            expected_template_1_file.sort_values([constant.TAGS_DS_EXPORT_COLUMNS_ORDER[5]]))

        assert_frame_equal(
            created_template_2_file.sort_values([constant.TAGS_DS_EXPORT_COLUMNS_ORDER[5]]),
            expected_template_2_file.sort_values([constant.TAGS_DS_EXPORT_COLUMNS_ORDER[5]]))


def create_default_tag(template_name, tag_name, column_name=None):
    tag = datacatalog_v1beta1.types.Tag()

    tag.name = tag_name
    tag.template = template_name

    tag.fields['source'].string_value = 'Copied from tlc_yellow_trips_2017'
    tag.fields['num_rows'].double_value = 113496874
    tag.fields['has_pii'].bool_value = False
    tag.fields['pii_type'].enum_value.display_name = 'NONE'
    tag.fields['timestamp_field'].timestamp_value.FromJsonString(pd.Timestamp.utcnow().isoformat())

    if column_name:
        tag.column = column_name

    return tag


class MockedObject(object):

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        return self.__dict__[key]
