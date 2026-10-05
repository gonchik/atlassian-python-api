"""
Confluence base module for shared functionality between API versions
"""

import logging
from typing import Dict, List, Optional, Union
from urllib.parse import parse_qsl, urlparse

from atlassian.rest_client import AtlassianRestAPI

log = logging.getLogger(__name__)


class ConfluenceEndpoints:
    """
    Class to define endpoint mappings for different Confluence API versions.
    These endpoints can be accessed through the ConfluenceBase get_endpoint method.
    """

    V1 = {
        "content": "rest/api/content",
        "page": "rest/api/content",
        "page_by_id": "rest/api/content/{id}",
        "child_pages": "rest/api/content/{id}/child/page",
        "content_search": "rest/api/content/search",
        "space": "rest/api/space",
        "space_by_key": "rest/api/space/{key}",
        "spaces": "rest/api/space",
        "page_properties": "rest/api/content/{id}/property",
        "page_property_by_key": "rest/api/content/{id}/property/{key}",
        "page_labels": "rest/api/content/{id}/label",
    }

    V2 = {
        "content": "api/v2/pages",
        "page_by_id": "api/v2/pages/{id}",
        "page": "api/v2/pages",
        "child_pages": "api/v2/pages/{id}/direct-children",
        "page_versions": "api/v2/pages/{id}/versions",
        "page_version": "api/v2/pages/{id}/versions/{version_number}",
        "search": "api/v2/search",
        "spaces": "api/v2/spaces",
        "space_by_id": "api/v2/spaces/{id}",
        "page_properties": "api/v2/pages/{id}/properties",
        "page_property_by_key": "api/v2/pages/{id}/properties/{key}",
        "page_labels": "api/v2/pages/{id}/labels",
        "space_labels": "api/v2/spaces/{id}/labels",
        # Comment endpoints for V2 API
        "page_footer_comments": "api/v2/pages/{id}/footer-comments",
        "page_inline_comments": "api/v2/pages/{id}/inline-comments",
        "blogpost_footer_comments": "api/v2/blogposts/{id}/footer-comments",
        "blogpost_inline_comments": "api/v2/blogposts/{id}/inline-comments",
        "attachment_comments": "api/v2/attachments/{id}/footer-comments",
        "custom_content_comments": "api/v2/custom-content/{id}/footer-comments",
        "footer_comment": "api/v2/footer-comments/{id}",
        "inline_comment": "api/v2/inline-comments/{id}",
        "footer_comments": "api/v2/footer-comments",
        "inline_comments": "api/v2/inline-comments",
        "comment": "api/v2/footer-comments",
        "comment_by_id": "api/v2/footer-comments/{id}",
        "comment_children": "api/v2/footer-comments/{id}/children",
        # Blog post endpoints
        "blogposts": "api/v2/blogposts",
        "blogpost_by_id": "api/v2/blogposts/{id}",
        "blogpost_labels": "api/v2/blogposts/{id}/labels",
        "blogpost_versions": "api/v2/blogposts/{id}/versions",
        "blogpost_version": "api/v2/blogposts/{id}/versions/{version_number}",
        "blogpost_attachments": "api/v2/blogposts/{id}/attachments",
        "blogpost_likes_count": "api/v2/blogposts/{id}/likes/count",
        "blogpost_likes_users": "api/v2/blogposts/{id}/likes/users",
        "blogpost_operations": "api/v2/blogposts/{id}/operations",
        "blogpost_custom_content": "api/v2/blogposts/{id}/custom-content",
        # Attachment endpoints
        "attachments": "api/v2/attachments",
        "attachment_by_id": "api/v2/attachments/{id}",
        "attachment_labels": "api/v2/attachments/{id}/labels",
        "attachment_versions": "api/v2/attachments/{id}/versions",
        "attachment_version": "api/v2/attachments/{id}/versions/{version_number}",
        "attachment_operations": "api/v2/attachments/{id}/operations",
        "attachment_thumbnail": "api/v2/attachments/{id}/thumbnail/download",
        # Smart link (embed) endpoints
        "embeds": "api/v2/embeds",
        "embed_by_id": "api/v2/embeds/{id}",
        "embed_ancestors": "api/v2/embeds/{id}/ancestors",
        "embed_descendants": "api/v2/embeds/{id}/descendants",
        "embed_direct_children": "api/v2/embeds/{id}/direct-children",
        "embed_operations": "api/v2/embeds/{id}/operations",
        # Page hierarchy endpoints
        "page_ancestors": "api/v2/pages/{id}/ancestors",
        "page_descendants": "api/v2/pages/{id}/descendants",
        "page_attachments": "api/v2/pages/{id}/attachments",
        "page_operations": "api/v2/pages/{id}/operations",
        "page_likes_count": "api/v2/pages/{id}/likes/count",
        "page_likes_users": "api/v2/pages/{id}/likes/users",
        "page_custom_content": "api/v2/pages/{id}/custom-content",
        "page_title": "api/v2/pages/{id}/title",
        # Label endpoints
        "labels": "api/v2/labels",
        "label_pages": "api/v2/labels/{id}/pages",
        "label_blogposts": "api/v2/labels/{id}/blogposts",
        "label_attachments": "api/v2/labels/{id}/attachments",
        # Space endpoints
        "space_pages": "api/v2/spaces/{id}/pages",
        "space_blogposts": "api/v2/spaces/{id}/blogposts",
        "space_operations": "api/v2/spaces/{id}/operations",
        "space_permissions_assignments": "api/v2/spaces/{id}/permissions",
        "space_role_assignments": "api/v2/spaces/{id}/role-assignments",
        # Whiteboard endpoints
        "whiteboard": "api/v2/whiteboards",
        "whiteboard_by_id": "api/v2/whiteboards/{id}",
        "whiteboard_children": "api/v2/whiteboards/{id}/direct-children",
        "whiteboard_ancestors": "api/v2/whiteboards/{id}/ancestors",
        # Folder endpoints
        "folder": "api/v2/folders",
        "folder_by_id": "api/v2/folders/{id}",
        # Task endpoints
        "tasks": "api/v2/tasks",
        "task_by_id": "api/v2/tasks/{id}",
        # Database endpoints
        "database": "api/v2/databases",
        "database_by_id": "api/v2/databases/{id}",
        # Custom content endpoints
        "custom_content": "api/v2/custom-content",
        "custom_content_by_id": "api/v2/custom-content/{id}",
        "custom_content_children": "api/v2/custom-content/{id}/children",
        "custom_content_ancestors": "api/v2/custom-content/{id}/ancestors",
        "custom_content_labels": "api/v2/custom-content/{id}/labels",
        "custom_content_operations": "api/v2/custom-content/{id}/operations",
        "custom_content_versions": "api/v2/custom-content/{id}/versions",
        "custom_content_version": "api/v2/custom-content/{id}/versions/{version_number}",
        "custom_content_attachments": "api/v2/custom-content/{id}/attachments",
        "custom_content_properties": "api/v2/custom-content/{id}/properties",
        "custom_content_property_by_key": "api/v2/custom-content/{id}/properties/{key}",
        # Page children (spec path, distinct from direct-children)
        "page_children": "api/v2/pages/{id}/children",
        # App (Forge) property endpoints
        "app_properties": "api/v2/app/properties",
        "app_property_by_key": "api/v2/app/properties/{key}",
    }


class ConfluenceBase(AtlassianRestAPI):
    """Base class for Confluence operations with version support"""

    @staticmethod
    def _is_cloud_url(url: str) -> bool:
        """
        Securely validate if a URL is a Confluence Cloud URL.

        Args:
            url: The URL to validate

        Returns:
            bool: True if the URL is a valid Confluence Cloud URL
        """
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False
        # Ensure we have a valid URL with a hostname
        if not parsed.hostname:
            return False

        # Check Cloud tenant and API-gateway hostnames.
        hostname = parsed.hostname.lower()
        return (
            hostname.endswith(".atlassian.net")
            or hostname.endswith(".jira.com")
            or ConfluenceBase._is_api_gateway_url(url)
        )

    @staticmethod
    def _is_api_gateway_url(url: str) -> bool:
        """Return whether *url* is an Atlassian API gateway Confluence URL."""
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or parsed.hostname != "api.atlassian.com":
            return False
        return parsed.path.startswith("/ex/confluence/")

    def __init__(self, url: str, *args, api_version: Union[str, int] = 1, **kwargs):
        """
        Initialize the Confluence Base instance with version support.

        Args:
            url: The Confluence instance URL
            api_version: API version, 1 or 2, defaults to 1
            args: Arguments to pass to AtlassianRestAPI constructor
            kwargs: Keyword arguments to pass to AtlassianRestAPI constructor
        """
        # Tenant URLs need the Confluence context path. Gateway URLs already
        # contain ``/ex/confluence/{cloudId}`` and must not be rewritten.
        if self._is_cloud_url(url) and not self._is_api_gateway_url(url) and "/wiki" not in url:
            url = AtlassianRestAPI.url_joiner(url, "/wiki")
            if "cloud" not in kwargs:
                kwargs["cloud"] = True

        super(ConfluenceBase, self).__init__(url, *args, **kwargs)
        self.api_version = int(api_version)
        if self.api_version not in [1, 2]:
            raise ValueError("API version must be 1 or 2")

    def get_endpoint(self, endpoint_key: str, **kwargs) -> str:
        """
        Get the appropriate endpoint based on the API version.

        Args:
            endpoint_key: The key for the endpoint in the endpoints dictionary
            kwargs: Format parameters for the endpoint

        Returns:
            The formatted endpoint URL
        """
        endpoints = ConfluenceEndpoints.V1 if self.api_version == 1 else ConfluenceEndpoints.V2

        if endpoint_key not in endpoints:
            raise ValueError(f"Endpoint key '{endpoint_key}' not found for API version {self.api_version}")

        endpoint = endpoints[endpoint_key]

        # Format the endpoint if kwargs are provided
        if kwargs:
            endpoint = endpoint.format(**kwargs)

        return endpoint

    def _get_paged(
        self,
        url: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        flags: Optional[List] = None,
        trailing: Optional[bool] = None,
        absolute: bool = False,
    ):
        """
        Get paged results with version-appropriate pagination.

        Args:
            url: The URL to retrieve
            params: The query parameters
            data: The request data
            flags: Additional flags
            trailing: If True, a trailing slash is added to the URL
            absolute: If True, the URL is used absolute and not relative to the root

        Yields:
            The result elements
        """
        if params is None:
            params = {}

        if self.api_version == 1:
            # V1 API pagination (offset-based)
            while True:
                response = self.get(
                    url,
                    trailing=trailing,
                    params=params,
                    data=data,
                    flags=flags,
                    absolute=absolute,
                )
                if not isinstance(response, dict) or "results" not in response:
                    return

                for value in response.get("results", []):
                    yield value

                # According to Cloud and Server documentation the links are returned the same way:
                # https://developer.atlassian.com/cloud/confluence/rest/api-group-content/#api-wiki-rest-api-content-get
                # https://developer.atlassian.com/server/confluence/pagination-in-the-rest-api/
                url = response.get("_links", {}).get("next")
                if url is None:
                    break
                # From now on we have relative URLs with parameters
                absolute = False
                # Params are now provided by the url
                params = {}
                # Trailing should not be added as it is already part of the url
                trailing = False

        else:
            # V2 API pagination (cursor-based)
            while True:
                response = self.get(
                    url,
                    trailing=trailing,
                    params=params,
                    data=data,
                    flags=flags,
                    absolute=absolute,
                )

                if isinstance(response, list):
                    yield from response
                    return

                if not isinstance(response, dict) or "results" not in response:
                    return

                for value in response.get("results", []):
                    yield value

                # Check for next cursor in _links or in response headers
                next_url = response.get("_links", {}).get("next")

                if not next_url:
                    # Check for Link header
                    if hasattr(self, "response") and self.response and "Link" in self.response.headers:
                        link_header = self.response.headers["Link"]
                        if 'rel="next"' in link_header:
                            import re

                            match = re.search(r"<([^>]*)>;", link_header)
                            if match:
                                next_url = match.group(1)

                if not next_url:
                    break

                if isinstance(next_url, dict):
                    next_url = next_url.get("href")
                if not next_url:
                    break

                # Cursor links are commonly relative and include the endpoint
                # path (for example ``/wiki/api/v2/spaces?cursor=...``).  The
                # endpoint used for the first request is already resolved
                # against the tenant or API-gateway context, so rebuilding it
                # from ``_links.base`` can duplicate ``/wiki`` or drop an
                # ``/ex/confluence/{cloud_id}`` prefix.  Keep the resolved
                # endpoint and advance only its query parameters.
                parsed_next = urlparse(next_url)
                if parsed_next.scheme:
                    url = next_url
                    absolute = True
                    params = {}
                elif parsed_next.query:
                    params = dict(parse_qsl(parsed_next.query, keep_blank_values=True))
                else:
                    # A relative link without a query is unusual for cursor
                    # pagination; retain the previous behavior as a safe
                    # fallback for such responses.
                    url = next_url
                    absolute = False
                    params = {}
                trailing = False

        return

    @staticmethod
    def factory(url: str, api_version: int = 1, *args, **kwargs) -> "ConfluenceBase":
        """
        Factory method to create a Confluence client with the specified API version

        Args:
            url: Confluence Cloud base URL
            api_version: API version to use (1 or 2)
            *args: Variable length argument list
            **kwargs: Keyword arguments

        Returns:
            Configured Confluence client for the specified API version

        Raises:
            ValueError: If api_version is not 1 or 2
        """
        if api_version not in {1, 2}:
            raise ValueError(f"Unsupported API version: {api_version}. Use 1 or 2.")
        if ConfluenceBase._is_cloud_url(url):
            from .confluence.cloud.cloud import ConfluenceCloud

            return ConfluenceCloud(url, *args, api_version=2, **kwargs)
        from .confluence.server.confluence_server import ConfluenceServer

        return ConfluenceServer(url, *args, api_version=api_version, **kwargs)
