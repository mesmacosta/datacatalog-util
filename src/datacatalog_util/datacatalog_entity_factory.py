from google.cloud import datacatalog_v1beta1


class DataCatalogEntityFactory:
    __TRUTHS = {1, '1', 't', 'T', 'true', 'True', 'TRUE'}

    @classmethod
    def make_tag_template(cls, tag_template_dict):
        tag_template = datacatalog_v1beta1.types.TagTemplate()

        tag_template.display_name = tag_template_dict['display_name']

        fields = tag_template_dict['fields']

        for field_id, items in fields.items():
            field_display_name = items['field_display_name']
            field_type = items['field_type']

            tag_template.fields[field_id].display_name = field_display_name

            if field_type == 'BOOL':
                tag_template.fields[field_id].type.primitive_type = \
                    datacatalog_v1beta1.enums.FieldType.PrimitiveType.BOOL.value
            elif field_type == 'DOUBLE':
                tag_template.fields[field_id].type.primitive_type = \
                    datacatalog_v1beta1.enums.FieldType.PrimitiveType.DOUBLE.value
            elif field_type == 'STRING':
                tag_template.fields[field_id].type.primitive_type = \
                    datacatalog_v1beta1.enums.FieldType.PrimitiveType.STRING.value
            elif field_type == 'TIMESTAMP':
                tag_template.fields[field_id].type.primitive_type = \
                    datacatalog_v1beta1.enums.FieldType.PrimitiveType.TIMESTAMP.value
            elif field_type == 'ENUM':
                enum_values = items['enum_values']
                for enum_value in enum_values:
                    tag_template.fields[field_id].type.enum_type \
                        .allowed_values.add().display_name = enum_value

        return tag_template

    @classmethod
    def get_primitive_field_type_for(cls, primitive_type):
        return datacatalog_v1beta1.enums.FieldType.PrimitiveType(primitive_type).name
