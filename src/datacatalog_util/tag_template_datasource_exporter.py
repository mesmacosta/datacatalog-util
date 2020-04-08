import logging
import os

import pandas as pd

from . import constant, datacatalog_entity_factory, datacatalog_facade


class TagTemplateDatasourceExporter:

    def __init__(self):
        self.__datacatalog_facade = datacatalog_facade.DataCatalogFacade()

    def export_tag_templates(self, project_ids, file_path=None):
        """
        Export Tag Templates found by searching Data Catalog.

        :param file_path: File path to be exported to.
        :param project_ids: Project ids to narrow down search results.
        """
        logging.info('')
        logging.info('===> Export Tag Templates [STARTED]')

        logging.info('')
        logging.info('Exporting the Tag Templates...')
        self.__export_tag_templates(project_ids, file_path)

        logging.info('')
        logging.info('==== Export Tag Templates [FINISHED] =============')

    def __export_tag_templates(self, project_ids, file_path=None):
        search_results = self.__datacatalog_facade.search_tag_templates(project_ids)
        tag_templates = self.__datacatalog_facade.get_tag_templates_from_search_results(
            search_results)
        dataframe = self.__tag_templates_to_dataframe(tag_templates)

        if file_path is None:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates.csv')

        dataframe.to_csv(file_path)
        logging.info('Check the generated file at: %s', file_path)

    @classmethod
    def __tag_templates_to_dataframe(cls, tag_templates):
        dataframe = pd.DataFrame(columns=constant.TAG_TEMPLATES_DS_COLUMNS_ORDER)

        for tag_template in tag_templates:
            tag_template_name = tag_template.name
            tag_template_display_name = tag_template.display_name

            fields = tag_template.fields

            for field_id, field_values in fields.items():
                field_display_name = field_values.display_name
                field_type = field_values.type
                allowed_values = field_type.enum_type.allowed_values
                enum_values = ''
                if len(field_type.enum_type.allowed_values) > 0:
                    enum_values = constant.ENUM_VALUES_SEPARATOR.join(
                        [allowed_value.display_name for allowed_value in allowed_values])
                    field_type_str = 'ENUM'
                else:
                    field_type_str = datacatalog_entity_factory.DataCatalogEntityFactory.\
                        get_primitive_field_type_for(field_type.primitive_type)

                field_index = list(fields.keys()).index(field_id)

                if field_index == 0:
                    dataframe = dataframe.append(
                        {
                            constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[0]: tag_template_name,
                            constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[1]: tag_template_display_name,
                            constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[2]: field_id,
                            constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[3]: field_display_name,
                            constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[4]: field_type_str,
                            constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[5]: enum_values
                        },
                        ignore_index=True)
                else:
                    dataframe = dataframe.append(
                        {
                            constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[0]: '',
                            constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[1]: '',
                            constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[2]: field_id,
                            constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[3]: field_display_name,
                            constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[4]: field_type_str,
                            constant.TAG_TEMPLATES_DS_COLUMNS_ORDER[5]: enum_values
                        },
                        ignore_index=True)

        dataframe.set_index(constant.TAG_TEMPLATES_DS_TEMPLATE_NAME_COLUMN_LABEL, inplace=True)

        return dataframe
