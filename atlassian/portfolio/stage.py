# coding=utf-8
"""Stage entity endpoints for the Portfolio for Jira (JPO) REST API.

Reference:
https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/jpo/#!/stage

Note: these ``jpo_*`` methods target the official public JPO REST API and are
distinct from the plan-scoped ``get_stages``/``get_stage_name`` helpers that
scrape the legacy ``rest/roadmap/1.0`` UI endpoints.
"""

from .base import JpoResourceMixin


class StageEndpoints(JpoResourceMixin):
    """Stage entity endpoints for the JPO REST API."""

    def jpo_get_stages(self, page=None, size=None, ids=None):
        """
        Return stage entities.

        Specify pagination with ``page``/``size`` (defaults to page 1, size 1
        server-side) or request specific entities with ``ids``.

        :param page: int, OPTIONAL: Page number.
        :param size: int, OPTIONAL: Page size.
        :param ids: list[int], OPTIONAL: Specific stage ids to return.
        :return: list[dict] - StageDTO entities.
        """
        params = self._jpo_list_params(page, size, ids)
        return self.get(self._jpo_url("stage"), params=params)

    def jpo_create_stage(self, data):
        """
        Create a new stage entity.

        :param data: dict - StageDTO payload.
        :return: The new entity Id.
        """
        return self.post(self._jpo_url("stage"), data=data)

    def jpo_get_stages_count(self):
        """
        Return the total stage entities count.

        :return: int
        """
        return self.get(self._jpo_url("stage/count"))

    def jpo_check_stages_exist(self, ids):
        """
        Check the existence of the given stage ids.

        :param ids: list[int] - Stage ids to check.
        :return: API result describing which ids exist.
        """
        return self.post(self._jpo_url("stage/exists"), data=ids)

    def jpo_get_stage(self, stage_id):
        """
        Get a stage entity by id.

        :param stage_id: int - Stage id.
        :return: dict - StageDTO.
        """
        return self.get(self._jpo_url(f"stage/{stage_id}"))

    def jpo_update_stage(self, stage_id, data):
        """
        Update a stage entity.

        :param stage_id: int - Stage id.
        :param data: dict - StageDTO payload.
        :return: dict - Updated StageDTO.
        """
        return self.post(self._jpo_url(f"stage/{stage_id}"), data=data)

    def jpo_delete_stage(self, stage_id):
        """
        Delete a stage entity.

        :param stage_id: int - Stage id.
        :return: response
        """
        return self.delete(self._jpo_url(f"stage/{stage_id}"))
