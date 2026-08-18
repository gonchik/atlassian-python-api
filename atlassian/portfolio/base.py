# coding=utf-8
"""Shared helpers for the Portfolio for Jira REST API client."""

#: Root of the official public Portfolio for Jira (JPO) REST API.
#: Reference: https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/jpo/
JPO_API_ROOT = "rest/jpo-api/1.0"


class JpoResourceMixin:
    """Mixin providing a helper to build JPO REST API resource URLs.

    Intended to be combined with :class:`atlassian.rest_client.AtlassianRestAPI`
    (or another class exposing ``get``/``post``/``delete`` and ``url_joiner``).
    """

    #: Overridable in subclasses/combined classes if a different root is needed.
    JPO_API_ROOT = JPO_API_ROOT

    def _jpo_url(self, resource):
        """
        Build a URL below the JPO REST API root.

        :param resource: str - Resource path appended to ``rest/jpo-api/1.0``.
        :return: str - Full relative URL.
        """
        return self.url_joiner(self.JPO_API_ROOT, resource)

    @staticmethod
    def _jpo_list_params(page=None, size=None, ids=None):
        """
        Build query parameters for the JPO "list entities" endpoints.

        :param page: int, OPTIONAL: Page number. Defaults to 1 server-side.
        :param size: int, OPTIONAL: Page size. Defaults to 1 server-side.
        :param ids: list[int], OPTIONAL: Specific entity ids to return.
        :return: dict or None
        """
        params = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if ids is not None:
            params["ids"] = ids
        return params or None
