# Constants used for Tagging the informed Datasource, Tags Table.
TAGS_DS_FIELD_ID_COLUMN_LABEL = 'field_id'
TAGS_DS_FIELD_TYPE_COLUMN_LABEL = 'field_type'
TAGS_DS_FIELD_VALUE_COLUMN_LABEL = 'field_value'
TAGS_DS_LINKED_RESOURCE_COLUMN_LABEL = 'linked_resource'
TAGS_DS_RELATIVE_RESOURCE_NAME_COLUMN_LABEL = 'relative_resource_name'
TAGS_DS_SCHEMA_COLUMN_COLUMN_LABEL = 'column'
TAGS_DS_TEMPLATE_NAME_COLUMN_LABEL = 'template_name'
TAGS_DS_TAG_NAME_COLUMN_LABEL = 'tag_name'

TAGS_DS_EXPORT_COLUMNS_ORDER = (TAGS_DS_RELATIVE_RESOURCE_NAME_COLUMN_LABEL,
                                TAGS_DS_LINKED_RESOURCE_COLUMN_LABEL,
                                TAGS_DS_TEMPLATE_NAME_COLUMN_LABEL, TAGS_DS_TAG_NAME_COLUMN_LABEL,
                                TAGS_DS_SCHEMA_COLUMN_COLUMN_LABEL, TAGS_DS_FIELD_ID_COLUMN_LABEL,
                                TAGS_DS_FIELD_TYPE_COLUMN_LABEL, TAGS_DS_FIELD_VALUE_COLUMN_LABEL)

# Constants used for exporting tags summary.
TAGS_DS_SUMMARY_TAG_TEMPLATE_NAME = 'template_name'
TAGS_DS_SUMMARY_TAGS_COUNT = 'tags_count'
TAGS_DS_SUMMARY_TAGGED_ENTRIES_COUNT = 'tagged_entries_count'
TAGS_DS_SUMMARY_TAGGED_COLUMNS_COUNT = 'tagged_columns_count'
TAGS_DS_SUMMARY_TAG_STRING_FIELDS_COUNT = 'tag_string_fields_count'
TAGS_DS_SUMMARY_TAG_BOOL_FIELDS_COUNT = 'tag_bool_fields_count'
TAGS_DS_SUMMARY_TAG_DOUBLE_FIELDS_COUNT = 'tag_double_fields_count'
TAGS_DS_SUMMARY_TAG_TIMESTAMP_FIELDS_COUNT = 'tag_timestamp_fields_count'
TAGS_DS_SUMMARY_TAG_ENUM_FIELDS_COUNT = 'tag_enum_fields_count'

# Expected order for the CSV header columns, Tag Summary Table.
TAGS_DS_SUMMARY_COLUMNS_ORDER = (TAGS_DS_SUMMARY_TAG_TEMPLATE_NAME, TAGS_DS_SUMMARY_TAGS_COUNT,
                                 TAGS_DS_SUMMARY_TAGGED_ENTRIES_COUNT,
                                 TAGS_DS_SUMMARY_TAGGED_COLUMNS_COUNT,
                                 TAGS_DS_SUMMARY_TAG_STRING_FIELDS_COUNT,
                                 TAGS_DS_SUMMARY_TAG_BOOL_FIELDS_COUNT,
                                 TAGS_DS_SUMMARY_TAG_DOUBLE_FIELDS_COUNT,
                                 TAGS_DS_SUMMARY_TAG_TIMESTAMP_FIELDS_COUNT,
                                 TAGS_DS_SUMMARY_TAG_ENUM_FIELDS_COUNT)
