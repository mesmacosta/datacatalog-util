from google.cloud import datacatalog_v1beta1


class DataCatalogEntityFactory:
    __TRUTHS = {1, '1', 't', 'T', 'true', 'True', 'TRUE'}

    @classmethod
    def get_primitive_field_type_for(cls, primitive_type):
        return datacatalog_v1beta1.enums.FieldType.PrimitiveType(primitive_type).name
