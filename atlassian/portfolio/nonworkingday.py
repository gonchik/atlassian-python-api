# coding=utf-8
"""Non-working day entity endpoints for the Portfolio for Jira (JPO) REST API.

Reference:
https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/jpo/#!/nonworkingday
"""

from .base import JpoResourceMixin


class NonWorkingDayEndpoints(JpoResourceMixin):
    """Non-working day entity endpoints for the JPO REST API."""

    def jpo_get_non_working_days(self, page=None, size=None, ids=None):
        """
        Return non-working day entities.

        Specify pagination with ``page``/``size`` (defaults to page 1, size 1
        server-side) or request specific entities with ``ids``.

        :param page: int, OPTIONAL: Page number.
        :param size: int, OPTIONAL: Page size.
        :param ids: list[int], OPTIONAL: Specific non-working day ids to return.
        :return: list[dict] - NonWorkingDayDTO entities.
        """
        params = self._jpo_list_params(page, size, ids)
        return self.get(self._jpo_url("nonworkingday"), params=params)

    def jpo_create_non_working_day(self, data):
        """
        Create a new non-working day entity.

        :param data: dict - NonWorkingDayDTO payload.
        :return: The new entity Id.
        """
        return self.post(self._jpo_url("nonworkingday"), data=data)

    def jpo_get_non_working_days_count(self):
        """
        Return the total non-working day entities count.

        :return: int
        """
        return self.get(self._jpo_url("nonworkingday/count"))

    def jpo_check_non_working_days_exist(self, ids):
        """
        Check the existence of the given non-working day ids.

        :param ids: list[int] - Non-working day ids to check.
        :return: API result describing which ids exist.
        """
        return self.post(self._jpo_url("nonworkingday/exists"), data=ids)

    def jpo_get_non_working_days_for_plan(self, plan_id):
        """
        Return non-working days configured for a specific plan.

        :param plan_id: int - Plan id.
        :return: list[dict] - NonWorkingDayDTO entities.
        """
        return self.get(self._jpo_url(f"nonworkingday/plan/{plan_id}"))

    def jpo_get_non_working_day(self, non_working_day_id):
        """
        Get a non-working day entity by id.

        :param non_working_day_id: int - Non-working day id.
        :return: dict - NonWorkingDayDTO.
        """
        return self.get(self._jpo_url(f"nonworkingday/{non_working_day_id}"))

    def jpo_update_non_working_day(self, non_working_day_id, data):
        """
        Update a non-working day entity.

        :param non_working_day_id: int - Non-working day id.
        :param data: dict - NonWorkingDayDTO payload.
        :return: dict - Updated NonWorkingDayDTO.
        """
        return self.post(self._jpo_url(f"nonworkingday/{non_working_day_id}"), data=data)

    def jpo_delete_non_working_day(self, non_working_day_id):
        """
        Delete a non-working day entity.

        :param non_working_day_id: int - Non-working day id.
        :return: response
        """
        return self.delete(self._jpo_url(f"nonworkingday/{non_working_day_id}"))
