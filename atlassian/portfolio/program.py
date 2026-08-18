# coding=utf-8
"""Program entity endpoints for the Portfolio for Jira (JPO) REST API.

Reference:
https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/jpo/#!/program
"""

from .base import JpoResourceMixin


class ProgramEndpoints(JpoResourceMixin):
    """Program entity endpoints for the JPO REST API."""

    def jpo_get_programs(self, page=None, size=None, ids=None):
        """
        Return program entities.

        Specify pagination with ``page``/``size`` (defaults to page 1, size 1
        server-side) or request specific entities with ``ids``.

        :param page: int, OPTIONAL: Page number.
        :param size: int, OPTIONAL: Page size.
        :param ids: list[int], OPTIONAL: Specific program ids to return.
        :return: list[dict] - ProgramDTO entities.
        """
        params = self._jpo_list_params(page, size, ids)
        return self.get(self._jpo_url("program"), params=params)

    def jpo_create_program(self, data):
        """
        Create a new program entity.

        :param data: dict - ProgramDTO payload.
        :return: The new entity Id.
        """
        return self.post(self._jpo_url("program"), data=data)

    def jpo_get_programs_count(self):
        """
        Return the total program entities count.

        :return: int
        """
        return self.get(self._jpo_url("program/count"))

    def jpo_check_programs_exist(self, ids):
        """
        Check the existence of the given program ids.

        :param ids: list[int] - Program ids to check.
        :return: API result describing which ids exist.
        """
        return self.post(self._jpo_url("program/exists"), data=ids)

    def jpo_get_program(self, program_id):
        """
        Get a program entity by id.

        :param program_id: int - Program id.
        :return: dict - ProgramDTO.
        """
        return self.get(self._jpo_url(f"program/{program_id}"))

    def jpo_update_program(self, program_id, data):
        """
        Update a program entity.

        :param program_id: int - Program id.
        :param data: dict - ProgramDTO payload.
        :return: dict - Updated ProgramDTO.
        """
        return self.post(self._jpo_url(f"program/{program_id}"), data=data)

    def jpo_delete_program(self, program_id):
        """
        Delete a program entity.

        :param program_id: int - Program id.
        :return: response
        """
        return self.delete(self._jpo_url(f"program/{program_id}"))
