# coding=utf-8
"""Plan entity endpoints for the Portfolio for Jira (JPO) REST API.

Reference:
https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/jpo/#!/plan
"""

from .base import JpoResourceMixin


class PlanEndpoints(JpoResourceMixin):
    """Plan entity endpoints for the JPO REST API."""

    def jpo_get_plans(self, page=None, size=None, ids=None):
        """
        Return plan entities.

        Specify pagination with ``page``/``size`` (defaults to page 1, size 1
        server-side) or request specific entities with ``ids``.

        :param page: int, OPTIONAL: Page number.
        :param size: int, OPTIONAL: Page size.
        :param ids: list[int], OPTIONAL: Specific plan ids to return.
        :return: list[dict] - PlanDTO entities.
        """
        params = self._jpo_list_params(page, size, ids)
        return self.get(self._jpo_url("plan"), params=params)

    def jpo_create_plan(self, data):
        """
        Create a new plan entity.

        :param data: dict - PlanDTO payload.
        :return: The new entity Id.
        """
        return self.post(self._jpo_url("plan"), data=data)

    def jpo_get_plans_count(self):
        """
        Return the total plan entities count.

        :return: int
        """
        return self.get(self._jpo_url("plan/count"))

    def jpo_check_plans_exist(self, ids):
        """
        Check the existence of the given plan ids.

        :param ids: list[int] - Plan ids to check.
        :return: API result describing which ids exist.
        """
        return self.post(self._jpo_url("plan/exists"), data=ids)

    def jpo_get_plan(self, plan_id):
        """
        Get a plan entity by id.

        :param plan_id: int - Plan id.
        :return: dict - PlanDTO.
        """
        return self.get(self._jpo_url(f"plan/{plan_id}"))

    def jpo_update_plan(self, plan_id, data):
        """
        Update a plan entity.

        :param plan_id: int - Plan id.
        :param data: dict - PlanDTO payload.
        :return: dict - Updated PlanDTO.
        """
        return self.post(self._jpo_url(f"plan/{plan_id}"), data=data)

    def jpo_delete_plan(self, plan_id):
        """
        Delete a plan entity.

        :param plan_id: int - Plan id.
        :return: response
        """
        return self.delete(self._jpo_url(f"plan/{plan_id}"))
