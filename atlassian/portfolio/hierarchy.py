# coding=utf-8
"""Hierarchy level entity endpoints for the Portfolio for Jira (JPO) REST API.

Reference:
https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/jpo/#!/hierarchy
"""

from .base import JpoResourceMixin


class HierarchyEndpoints(JpoResourceMixin):
    """Hierarchy level entity endpoints for the JPO REST API."""

    def jpo_get_hierarchies(self, page=None, size=None, ids=None):
        """
        Return hierarchy level entities.

        Specify pagination with ``page``/``size`` (defaults to page 1, size 1
        server-side) or request specific entities with ``ids``.

        :param page: int, OPTIONAL: Page number.
        :param size: int, OPTIONAL: Page size.
        :param ids: list[int], OPTIONAL: Specific hierarchy level ids to return.
        :return: list[dict] - HierarchyLevelDTO entities.
        """
        params = self._jpo_list_params(page, size, ids)
        return self.get(self._jpo_url("hierarchy"), params=params)

    def jpo_create_hierarchy(self, data):
        """
        Create a new hierarchy level entity.

        :param data: dict - HierarchyLevelDTO payload.
        :return: The new entity Id.
        """
        return self.post(self._jpo_url("hierarchy"), data=data)

    def jpo_get_hierarchies_count(self):
        """
        Return the total hierarchy level entities count.

        :return: int
        """
        return self.get(self._jpo_url("hierarchy/count"))

    def jpo_check_hierarchies_exist(self, ids):
        """
        Check the existence of the given hierarchy level ids.

        :param ids: list[int] - Hierarchy level ids to check.
        :return: API result describing which ids exist.
        """
        return self.post(self._jpo_url("hierarchy/exists"), data=ids)

    def jpo_get_hierarchy(self, hierarchy_id):
        """
        Get a hierarchy level entity by id.

        :param hierarchy_id: int - Hierarchy level id.
        :return: dict - HierarchyLevelDTO.
        """
        return self.get(self._jpo_url(f"hierarchy/{hierarchy_id}"))

    def jpo_update_hierarchy(self, hierarchy_id, data):
        """
        Update a hierarchy level entity.

        :param hierarchy_id: int - Hierarchy level id.
        :param data: dict - HierarchyLevelDTO payload.
        :return: dict - Updated HierarchyLevelDTO.
        """
        return self.post(self._jpo_url(f"hierarchy/{hierarchy_id}"), data=data)

    def jpo_delete_hierarchy(self, hierarchy_id):
        """
        Delete a hierarchy level entity.

        :param hierarchy_id: int - Hierarchy level id.
        :return: response
        """
        return self.delete(self._jpo_url(f"hierarchy/{hierarchy_id}"))
