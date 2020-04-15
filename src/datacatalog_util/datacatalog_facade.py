import logging
from functools import lru_cache
import re

from google.api_core import exceptions
from google.cloud import datacatalog
from google.cloud import datacatalog_v1beta1


class DataCatalogFacade:
    """Data Catalog API communication facade."""

    __NESTED_LOG_PREFIX = ' ' * 5

    def __init__(self):
        # Initialize the API client.
        self.__datacatalog = datacatalog.DataCatalogClient()

    def list_tags(self, entry_name):
        return self.__list_tags(entry_name)

    # Currently we don't have a list method, so we are using search which is not exhaustive,
    # and might not return some entries.
    def search_tag_templates(self, project_ids):
        scope = datacatalog_v1beta1.types.SearchCatalogRequest.Scope()

        scope.include_project_ids.extend(project_ids.split(','))

        query = 'type=TAG_TEMPLATE'

        results_iterator = self.__datacatalog.search_catalog(scope=scope,
                                                             query=query,
                                                             order_by='relevance',
                                                             page_size=1000)

        results = []
        for page in results_iterator.pages:
            results.extend(page)

        return results

    # Currently we don't have a list method, so we are using search which is not exhaustive,
    # and might not return some entries.
    def search_tagged_assets(self, project_id, tag_template_id):
        scope = datacatalog_v1beta1.types.SearchCatalogRequest.Scope()

        scope.include_project_ids.extend([project_id])

        query = 'tag:{}.{}'.format(project_id, tag_template_id)

        results_iterator = self.__datacatalog.search_catalog(scope=scope,
                                                             query=query,
                                                             order_by='relevance',
                                                             page_size=1000)

        results = []
        for page in results_iterator.pages:
            results.extend(page)

        return results

    @lru_cache(maxsize=16)
    def get_tag_template(self, name):
        self.__log_operation_start('GET Tag Template: %s', name)
        tag_template = self.__datacatalog.get_tag_template(name=name)
        self.__log_single_object_read_result(tag_template)
        return tag_template

    def get_tag_templates_from_search_results(self, search_results):
        tag_templates = []

        for search_result in search_results:
            template_name = search_result.relative_resource_name
            try:
                tag_template = self.get_tag_template(template_name)
                tag_templates.append(tag_template)
            except exceptions.GoogleAPICallError as e:
                logging.warning('Exception getting Tag Template %s: %s', template_name, str(e))

        return tag_templates

    @classmethod
    def extract_resources_from_template(cls, tag_template_name):
        re_match = re.match(
            r'^projects[/]([_a-zA-Z-\d]+)[/]locations[/]'
            r'([a-zA-Z-\d]+)[/]tagTemplates[/]([@a-zA-Z-_\d]+)$', tag_template_name)

        if re_match:
            project_id, location_id, tag_template_id, = re_match.groups()
            return project_id, location_id, tag_template_id

    @lru_cache(maxsize=16)
    def __list_tags(self, entry_name):
        return [tag for tag in self.__datacatalog.list_tags(parent=entry_name)]

    @classmethod
    def __log_operation_start(cls, message, *args):
        logging.info('')
        logging.info(message, *args)
        logging.info('--------------------------------------------------')

    @classmethod
    def __log_single_object_read_result(cls, the_object):
        logging.info('%sFound!' if the_object else '%sNOT found!', cls.__NESTED_LOG_PREFIX)
