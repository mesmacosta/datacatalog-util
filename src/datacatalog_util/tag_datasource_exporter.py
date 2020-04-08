import logging
import os

from google.api_core import exceptions
from google.protobuf.json_format import MessageToDict
import pandas as pd
from tabulate import tabulate

from . import constant, datacatalog_facade


class TagDatasourceExporter:

    def __init__(self):
        self.__datacatalog_facade = datacatalog_facade.DataCatalogFacade()

    def export_tags(self, project_ids, dir_path=None):
        """
        Export Tags found by searching Data Catalog.

        :param dir_path: Directory path to be exported to.
        :param project_ids: Project ids to narrow down search results.
        """
        logging.info('')
        logging.info('===> Export Tags [STARTED]')

        logging.info('')
        logging.info('Exporting the Tags...')
        self.__export_tags(project_ids, dir_path)

        logging.info('')
        logging.info('==== Export Tags [FINISHED] =============')

    def __export_tags(self, project_ids, dir_path=None):
        search_results = self.__datacatalog_facade.search_tag_templates(project_ids)

        if dir_path is None:
            dir_path = os.path.dirname(os.path.abspath(__file__))

        summary_dataframe = None

        for search_result in search_results:
            template_dataframe = None
            tag_template_name = search_result.relative_resource_name

            project_id, location_id, tag_template_id = \
                self.__datacatalog_facade.extract_resources_from_template(tag_template_name)

            logging.info('')
            logging.info('Looking for Tags from Template: {}...'.format(tag_template_id))

            tagged_assets = self.__datacatalog_facade.search_tagged_assets(
                project_id, tag_template_id)

            entry_name = ''
            for tagged_asset in tagged_assets:
                try:
                    entry_name = tagged_asset.relative_resource_name

                    logging.info('Loading Tags from Entry: {}...'.format(entry_name))

                    linked_resource = tagged_asset.linked_resource
                    relative_resource_name = tagged_asset.relative_resource_name

                    tags = self.__datacatalog_facade.list_tags(entry_name)
                    asset_dataframe = self.__tags_to_dataframe(linked_resource,
                                                               relative_resource_name,
                                                               tag_template_name, tags)

                    if template_dataframe is not None:
                        template_dataframe = template_dataframe.append(asset_dataframe)
                    else:
                        template_dataframe = asset_dataframe
                except exceptions.PermissionDenied:
                    logging.warning(
                        'Permission denied when processing up Entry %s.'
                        ' The resource will be skipped.', entry_name)

            if template_dataframe is not None:
                file_path = os.path.join(dir_path, '{}.csv'.format(tag_template_id))
                template_dataframe.to_csv(file_path)
                logging.info('==> Tags from Template: {} exported.'.format(tag_template_id))

                if summary_dataframe is not None:
                    summary_dataframe = summary_dataframe.append(template_dataframe)
                else:
                    summary_dataframe = template_dataframe
            else:
                template_dataframe = self.__create_empty_dataframe(tag_template_name)
                logging.info('No Tags found for Template: {}.'.format(tag_template_id))
                if summary_dataframe is not None:
                    summary_dataframe = summary_dataframe.append(template_dataframe)
                else:
                    summary_dataframe = template_dataframe

        if summary_dataframe is not None:
            summary_dataframe.set_index(constant.TAGS_DS_TEMPLATE_NAME_COLUMN_LABEL, inplace=True)
            summary_dataframe_with_stats = self.__create_summary_file(summary_dataframe)

            file_path = os.path.join(dir_path, 'summary.csv')
            summary_dataframe_with_stats.to_csv(file_path)

            logging.info('')
            logging.info('SUMMARY TABLE')
            pd.set_option('display.max_rows', 1000)
            logging.info('\n {}'.format(
                tabulate(summary_dataframe_with_stats, headers='keys', tablefmt='psql')))
            logging.info('')
            logging.info('Check the generated summary file at: %s', file_path)
            logging.info('Check additional files for templates with tags at: %s', dir_path)

    @classmethod
    def __create_summary_file(cls, summary_dataframe):
        dataframe = pd.DataFrame(columns=constant.TAGS_DS_SUMMARY_COLUMNS_ORDER)

        key_values = summary_dataframe.index.unique().tolist()
        for key_value in key_values:
            # We use an array with: [key_value] to make sure the dataframe loc
            # always returns a dataframe, and not a Series
            template_subset = summary_dataframe.loc[[key_value]]
            summary_dataframe.drop(key_value, inplace=True)

            tag_template_name = key_value
            tags_count = template_subset['tag_name'][template_subset['tag_name'] != ''].nunique()
            tagged_columns_count = template_subset['column'][
                template_subset['column'] != ''].nunique()
            tagged_entries_count = tags_count - tagged_columns_count
            field_type_count = template_subset['field_type'].value_counts()

            string_fields_count = 0
            bool_fields_count = 0
            double_fields_count = 0
            timestamp_fields_count = 0
            enum_fields_count = 0

            for key, value in field_type_count.iteritems():
                if key == 'STRING':
                    string_fields_count = value
                elif key == 'BOOL':
                    bool_fields_count = value
                elif key == 'DOUBLE':
                    double_fields_count = value
                elif key == 'TIMESTAMP':
                    timestamp_fields_count = value
                elif key == 'ENUM':
                    enum_fields_count = value

            dataframe = dataframe.append(
                {
                    constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[0]: tag_template_name,
                    constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[1]: tags_count,
                    constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[2]: tagged_entries_count,
                    constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[3]: tagged_columns_count,
                    constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[4]: string_fields_count,
                    constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[5]: bool_fields_count,
                    constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[6]: double_fields_count,
                    constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[7]: timestamp_fields_count,
                    constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[8]: enum_fields_count
                },
                ignore_index=True)

        dataframe.set_index(constant.TAGS_DS_SUMMARY_COLUMNS_ORDER[0], inplace=True)
        return dataframe

    @classmethod
    def __tags_to_dataframe(cls, linked_resource, relative_resource_name, tag_template_name, tags):
        dataframe = pd.DataFrame(columns=constant.TAGS_DS_EXPORT_COLUMNS_ORDER)

        for tag in tags:
            current_tag_template_name = tag.template
            if tag_template_name == current_tag_template_name:
                tag_name = tag.name
                column = tag.column
                fields = tag.fields

                for field_id, field_values in fields.items():
                    # We must convert the message to a dict,
                    # otherwise the protobuf message initialize the types
                    # and we are not able to verify what type the field is.
                    field_values_dict = MessageToDict(field_values)

                    string_value = field_values_dict.get('stringValue')
                    bool_value = field_values_dict.get('boolValue')
                    double_value = field_values_dict.get('doubleValue')
                    timestamp_value = field_values_dict.get('timestampValue')
                    enum_value = field_values_dict.get('enumValue', {}).get('displayName')

                    field_type = None
                    field_value = None

                    if string_value is not None:
                        field_value = string_value
                        field_type = 'STRING'
                    elif bool_value is not None:
                        field_value = bool_value
                        field_type = 'BOOL'
                    elif double_value is not None:
                        field_value = double_value
                        field_type = 'DOUBLE'
                    elif timestamp_value is not None:
                        field_value = timestamp_value
                        field_type = 'TIMESTAMP'
                    elif enum_value is not None:
                        field_value = enum_value
                        field_type = 'ENUM'

                    field_index = list(fields.keys()).index(field_id)

                    if field_index == 0:
                        dataframe = dataframe.append(
                            {
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[0]: relative_resource_name,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[1]: linked_resource,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[2]: tag_template_name,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[3]: tag_name,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[4]: column,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[5]: field_id,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[6]: field_type,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[7]: field_value
                            },
                            ignore_index=True)
                    else:
                        dataframe = dataframe.append(
                            {
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[0]: '',
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[1]: linked_resource,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[2]: tag_template_name,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[3]: tag_name,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[4]: column,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[5]: field_id,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[6]: field_type,
                                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[7]: field_value
                            },
                            ignore_index=True)

        dataframe.set_index(constant.TAGS_DS_RELATIVE_RESOURCE_NAME_COLUMN_LABEL, inplace=True)

        return dataframe

    @classmethod
    def __create_empty_dataframe(cls, tag_template_name):
        dataframe = pd.DataFrame(columns=constant.TAGS_DS_EXPORT_COLUMNS_ORDER)

        dataframe = dataframe.append(
            {
                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[0]: 'EMPTY_RESOURCE',
                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[1]: '',
                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[2]: tag_template_name,
                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[3]: '',
                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[4]: '',
                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[5]: '',
                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[6]: '',
                constant.TAGS_DS_EXPORT_COLUMNS_ORDER[7]: ''
            },
            ignore_index=True)

        dataframe.set_index(constant.TAGS_DS_RELATIVE_RESOURCE_NAME_COLUMN_LABEL, inplace=True)

        return dataframe
