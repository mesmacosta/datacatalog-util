import logging

from google.api_core import exceptions
import pandas as pd

from . import constant, datacatalog_entity_factory, datacatalog_facade


class TagTemplateDatasourceProcessor:

    def __init__(self):
        self.__datacatalog_facade = datacatalog_facade.DataCatalogFacade()

    def create_tag_templates_from_csv(self, file_path):
        """
        Create Tag Templates by reading information from a CSV file.

        :param file_path: The CSV file path.
        :return: A list with all Tag Templates created.
        """
        logging.info('')
        logging.info('===> Create Tag Templates from CSV [STARTED]')

        logging.info('')
        logging.info('Reading CSV file: %s...', file_path)
        dataframe = pd.read_csv(file_path)

        logging.info('')
        logging.info(f'Creating the Tag Templates...')
        created_tag_templates = self.__create_tag_templates_from_dataframe(dataframe)

        logging.info('')
        logging.info('==== Create Tag Templates from CSV [FINISHED] =============')

        return created_tag_templates

    def delete_tag_templates_from_csv(self, file_path):
        """
        Delete Tag Templates by reading information from a CSV file.

        :param file_path: The CSV file path.
        """
        logging.info('')
        logging.info('===> Delete Tag Templates from CSV [STARTED]')

        logging.info('')
        logging.info('Reading CSV file: %s...', file_path)
        dataframe = pd.read_csv(file_path)

        logging.info('')
        logging.info('Deleting the Tag Templates...')
        self.__delete_tag_templates_from_dataframe(dataframe)

        logging.info('')
        logging.info('==== Delete Tag Templates from CSV [FINISHED] =============')

    def __create_tag_templates_from_dataframe(self, dataframe):
        normalized_df = self.__normalize_dataframe(dataframe)
        normalized_df.set_index(constant.TAG_TEMPLATES_DS_TEMPLATE_NAME_COLUMN_LABEL, inplace=True)

        created_tag_templates = []
        for tag_template_name in normalized_df.index.unique().tolist():

            template_subset = normalized_df.loc[[tag_template_name]]

            # Save memory by deleting data already copied to a subset.
            normalized_df.drop(tag_template_name, inplace=True)

            tag_template = self.__create_tag_template_from_dataframe(template_subset)

            project_id, location_id, tag_template_id = \
                self.__datacatalog_facade.extract_resources_from_template(tag_template_name)

            try:
                created_tag_template = self.__datacatalog_facade.create_tag_template(
                    project_id, location_id, tag_template_id, tag_template)
                created_tag_templates.extend([created_tag_template])
                logging.info('Template %s created.', tag_template_name)
            except exceptions.AlreadyExists:
                logging.warning('Template %s already exists.', tag_template_name)

        return created_tag_templates

    def __delete_tag_templates_from_dataframe(self, dataframe):
        normalized_df = self.__normalize_dataframe(dataframe)
        normalized_df.set_index(constant.TAG_TEMPLATES_DS_TEMPLATE_NAME_COLUMN_LABEL, inplace=True)

        for tag_template_name in normalized_df.index.unique().tolist():

            try:
                self.__datacatalog_facade.delete_tag_template(tag_template_name)
                logging.info('Template %s deleted.', tag_template_name)
            except exceptions.GoogleAPICallError as e:
                logging.warning('Exception deleting template %s.: %s', tag_template_name, str(e))

    @classmethod
    def __normalize_dataframe(cls, dataframe):
        # Reorder dataframe columns.
        ordered_df = dataframe.reindex(columns=constant.TAG_TEMPLATES_DS_COLUMNS_ORDER, copy=False)

        # Fill NA/NaN values by propagating the last valid observation forward to next valid.
        filled_subset = ordered_df[constant.TAG_TEMPLATES_DS_FILLABLE_COLUMNS].fillna(method='pad')

        # Rebuild the dataframe by concatenating the fillable and non-fillable columns.
        rebuilt_df = pd.concat(
            [filled_subset, ordered_df[constant.TAG_TEMPLATES_DS_NON_FILLABLE_COLUMNS]], axis=1)

        return rebuilt_df

    def __create_tag_template_from_dataframe(self, dataframe):
        template_name = dataframe.index.unique().tolist()[0]

        fields_subset = \
            dataframe.loc[[template_name], constant.TAG_TEMPLATES_DS_FIELD_ID_COLUMN_LABEL:]

        fields_dict = self.__convert_fields_dataframe_to_dict(fields_subset)

        tag_template_dict = {
            'name': template_name,
            'display_name':
            dataframe[constant.TAG_TEMPLATES_DS_TEMPLATE_DISPLAY_NAME_COLUMN_LABEL][0],
            'fields': fields_dict
        }

        return self.__create_tag_template_from_dict(tag_template_dict)

    @classmethod
    def __create_tag_template_from_dict(cls, tag_template_dict):
        return datacatalog_entity_factory.DataCatalogEntityFactory.make_tag_template(
            tag_template_dict)

    @classmethod
    def __convert_fields_dataframe_to_dict(cls, dataframe):
        base_dict = dataframe.to_dict(orient='records')

        id_to_field_map = {}
        for base_object in base_dict:
            enum_values = base_object[constant.TAG_TEMPLATES_DS_FIELD_ENUM_VALUES_COLUMN_LABEL]

            if not isinstance(enum_values, str):
                enum_values = ''

            id_to_field_map[base_object[constant.TAG_TEMPLATES_DS_FIELD_ID_COLUMN_LABEL]] = \
                {
                    constant.TAG_TEMPLATES_DS_FIELD_DISPLAY_NAME_COLUMN_LABEL:
                        base_object[constant.TAG_TEMPLATES_DS_FIELD_DISPLAY_NAME_COLUMN_LABEL],
                    constant.TAG_TEMPLATES_DS_FIELD_TYPE_COLUMN_LABEL:
                        base_object[constant.TAG_TEMPLATES_DS_FIELD_TYPE_COLUMN_LABEL],
                    constant.TAG_TEMPLATES_DS_FIELD_ENUM_VALUES_COLUMN_LABEL:
                        enum_values.split(
                            constant.ENUM_VALUES_SEPARATOR)
                }

        return id_to_field_map
