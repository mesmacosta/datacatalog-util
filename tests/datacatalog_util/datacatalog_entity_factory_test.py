import unittest

from google.cloud.datacatalog import enums

from datacatalog_util import datacatalog_entity_factory


class DataCatalogEntityFactoryTest(unittest.TestCase):
    __BOOL_TYPE = enums.FieldType.PrimitiveType.BOOL
    __DOUBLE_TYPE = enums.FieldType.PrimitiveType.DOUBLE
    __STRING_TYPE = enums.FieldType.PrimitiveType.STRING
    __TIMESTAMP_TYPE = enums.FieldType.PrimitiveType.TIMESTAMP

    def test_make_tag_template_valid_boolean_values_should_set_fields(self):

        tag_template_dict = {
            'display_name': 'My Tag Template',
            'fields': {
                'my_bool_field': {
                    'field_display_name': 'My BOOL field',
                    'field_type': 'BOOL'
                }
            }
        }

        tag_template = datacatalog_entity_factory.DataCatalogEntityFactory.make_tag_template(
            tag_template_dict)

        my_bool_field = tag_template.fields['my_bool_field']

        self.assertEqual(tag_template_dict['display_name'], tag_template.display_name)
        self.assertEqual(tag_template_dict['fields']['my_bool_field']['field_display_name'],
                         my_bool_field.display_name)
        self.assertEqual(self.__BOOL_TYPE, my_bool_field.type.primitive_type)

    def test_make_tag_template_valid_double_values_should_set_fields(self):

        tag_template_dict = {
            'display_name': 'My Tag Template',
            'fields': {
                'my_double_field': {
                    'field_display_name': 'My DOUBLE field',
                    'field_type': 'DOUBLE'
                }
            }
        }

        tag_template = datacatalog_entity_factory.DataCatalogEntityFactory.make_tag_template(
            tag_template_dict)

        my_double_field = tag_template.fields['my_double_field']

        self.assertEqual(tag_template_dict['display_name'], tag_template.display_name)
        self.assertEqual(tag_template_dict['fields']['my_double_field']['field_display_name'],
                         my_double_field.display_name)
        self.assertEqual(self.__DOUBLE_TYPE, my_double_field.type.primitive_type)

    def test_make_tag_template_valid_string_values_should_set_fields(self):

        tag_template_dict = {
            'display_name': 'My Tag Template',
            'fields': {
                'my_string_field': {
                    'field_display_name': 'My STRING field',
                    'field_type': 'STRING'
                }
            }
        }

        tag_template = datacatalog_entity_factory.DataCatalogEntityFactory.make_tag_template(
            tag_template_dict)

        my_string_field = tag_template.fields['my_string_field']

        self.assertEqual(tag_template_dict['display_name'], tag_template.display_name)
        self.assertEqual(tag_template_dict['fields']['my_string_field']['field_display_name'],
                         my_string_field.display_name)
        self.assertEqual(self.__STRING_TYPE, my_string_field.type.primitive_type)

    def test_make_tag_template_valid_timestamp_values_should_set_fields(self):

        tag_template_dict = {
            'display_name': 'My Tag Template',
            'fields': {
                'my_timestamp_field': {
                    'field_display_name': 'My TIMESTAMP field',
                    'field_type': 'TIMESTAMP'
                }
            }
        }

        tag_template = datacatalog_entity_factory.DataCatalogEntityFactory.make_tag_template(
            tag_template_dict)

        my_timestamp_field = tag_template.fields['my_timestamp_field']

        self.assertEqual(tag_template_dict['display_name'], tag_template.display_name)
        self.assertEqual(tag_template_dict['fields']['my_timestamp_field']['field_display_name'],
                         my_timestamp_field.display_name)
        self.assertEqual(self.__TIMESTAMP_TYPE, my_timestamp_field.type.primitive_type)

    def test_make_tag_template_valid_enum_values_should_set_fields(self):

        tag_template_dict = {
            'display_name': 'My Tag Template',
            'fields': {
                'my_enum_field': {
                    'field_display_name': 'My ENUM field',
                    'field_type': 'ENUM',
                    'enum_values': ['1', '2']
                }
            }
        }

        tag_template = datacatalog_entity_factory.DataCatalogEntityFactory.make_tag_template(
            tag_template_dict)

        my_enum_field = tag_template.fields['my_enum_field']

        self.assertEqual(tag_template_dict['display_name'], tag_template.display_name)
        self.assertEqual(tag_template_dict['fields']['my_enum_field']['field_display_name'],
                         my_enum_field.display_name)
        self.assertEqual(tag_template_dict['fields']['my_enum_field']['enum_values'][0],
                         my_enum_field.type.enum_type.allowed_values[0].display_name)
        self.assertEqual(tag_template_dict['fields']['my_enum_field']['enum_values'][1],
                         my_enum_field.type.enum_type.allowed_values[1].display_name)
