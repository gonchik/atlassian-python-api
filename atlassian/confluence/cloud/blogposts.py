"""Confluence Cloud V2 blog post operations."""

from typing import Any, Dict, List, Optional

from ...confluence_base import ConfluenceBase


class BlogPostOperations(ConfluenceBase):
    """Base component implementing Confluence Cloud blog post endpoints."""

    def create_blog_post(
        self,
        space_id: str,
        title: Optional[str] = None,
        body: Optional[str] = None,
        status: str = "current",
        body_format: str = "storage",
        private: Optional[bool] = None,
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        """Create a blog post in a Confluence Cloud space.

        Scoped tokens require ``write:page:confluence`` (blog posts share the
        page scope). ``status`` must be ``current`` (requires ``title`` and
        ``body``) or ``draft``. ``private`` is sent as the API query parameter;
        the remaining optional values are fields in the request body.
        """
        if status not in ("current", "draft"):
            raise ValueError("status must be 'current' or 'draft'")
        if body_format not in ("storage", "atlas_doc_format", "wiki"):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'wiki'")
        if status == "current" and (title is None or body is None):
            raise ValueError("title and body are required when creating a non-draft blog post")
        data: Dict[str, Any] = {"spaceId": space_id, "status": status}
        if title is not None:
            data["title"] = title
        if body is not None:
            data["body"] = {body_format: {"representation": body_format, "value": body}}
        data.update(kwargs)
        if private is None:
            return self.post(self.get_endpoint("blogposts"), data=data)
        return self.post(self.get_endpoint("blogposts"), data=data, params={"private": private})

    def get_blog_posts(
        self,
        ids: Optional[List[str]] = None,
        space_id: Optional[str] = None,
        sort: Optional[str] = None,
        status: Optional[str] = None,
        title: Optional[str] = None,
        body_format: Optional[str] = None,
        cursor: Optional[str] = None,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """Return every blog post matching the filters, following pagination.

        Scoped tokens require ``read:page:confluence``. One of ``ids`` or
        ``space_id`` narrows the query; without either, all blog posts the
        caller can see are returned.
        """
        params: Dict[str, Any] = {"limit": limit}
        if ids:
            params["id"] = ids
        if space_id is not None:
            params["space-id"] = space_id
        if sort is not None:
            params["sort"] = sort
        if status is not None:
            params["status"] = status
        if title is not None:
            params["title"] = title
        if body_format is not None:
            params["body-format"] = body_format
        if cursor is not None:
            params["cursor"] = cursor
        return list(self._get_paged(self.get_endpoint("blogposts"), params=params))

    def get_blog_post_by_id(
        self,
        blogpost_id: str,
        body_format: Optional[str] = None,
        get_draft: Optional[bool] = None,
        status: Optional[str] = None,
        version: Optional[int] = None,
        include_labels: Optional[bool] = None,
        include_properties: Optional[bool] = None,
        include_operations: Optional[bool] = None,
        include_likes: Optional[bool] = None,
        include_versions: Optional[bool] = None,
        include_version: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Return a blog post by ID.

        Scoped tokens require ``read:page:confluence``.
        """
        optional_params = {
            "body-format": body_format,
            "get-draft": get_draft,
            "status": status,
            "version": version,
            "include-labels": include_labels,
            "include-properties": include_properties,
            "include-operations": include_operations,
            "include-likes": include_likes,
            "include-versions": include_versions,
            "include-version": include_version,
        }
        params = {key: value for key, value in optional_params.items() if value is not None}
        endpoint = self.get_endpoint("blogpost_by_id", id=blogpost_id)
        if not params:
            return self.get(endpoint)
        return self.get(endpoint, params=params)

    def update_blog_post(
        self,
        blogpost_id: str,
        title: Optional[str] = None,
        body: Optional[str] = None,
        status: str = "current",
        version: Optional[int] = None,
        body_format: str = "storage",
        **kwargs: Any,
    ) -> Optional[Dict[str, Any]]:
        """Update a blog post.

        The API requires ``id``, ``status``, ``title``, ``body`` and ``version``
        in the request body; missing values are filled from the current blog
        post when not supplied. Extra fields (for example ``createdAt``) can be
        passed through ``kwargs``.
        """
        if status not in ("current", "draft"):
            raise ValueError("status must be 'current' or 'draft'")
        if body_format not in ("storage", "atlas_doc_format", "wiki"):
            raise ValueError("body_format must be one of 'storage', 'atlas_doc_format', or 'wiki'")
        if version is None:
            current = self.get_blog_post_by_id(blogpost_id)
            version = (current or {}).get("version", {}).get("number", 0)
        data: Dict[str, Any] = {"id": blogpost_id, "status": status, "version": {"number": version + 1}}
        if title is None:
            current = self.get_blog_post_by_id(blogpost_id)
            title = (current or {}).get("title")
        if body is not None:
            data["body"] = {body_format: {"representation": body_format, "value": body}}
        elif title is not None:
            current = self.get_blog_post_by_id(blogpost_id, body_format=body_format)
            existing = (current or {}).get("body", {}).get(body_format, {}).get("value")
            data["body"] = {body_format: {"representation": body_format, "value": existing or ""}}
        if title is not None:
            data["title"] = title
        data.update(kwargs)
        return self.put(self.get_endpoint("blogpost_by_id", id=blogpost_id), data=data)

    def delete_blog_post(self, blogpost_id: str, purge: Optional[bool] = None, draft: Optional[bool] = None) -> bool:
        """Delete a blog post, or purge it from the trash.

        Scoped tokens require ``delete:page:confluence``.
        """
        params = {key: value for key, value in {"purge": purge, "draft": draft}.items() if value is not None}
        endpoint = self.get_endpoint("blogpost_by_id", id=blogpost_id)
        if params:
            self.delete(endpoint, params=params)
        else:
            self.delete(endpoint)
        return True

    def get_blog_post_labels(
        self, blogpost_id: str, prefix: Optional[str] = None, sort: Optional[str] = None, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Return every label on a blog post, following pagination."""
        params: Dict[str, Any] = {"limit": limit}
        if prefix is not None:
            params["prefix"] = prefix
        if sort is not None:
            params["sort"] = sort
        return list(self._get_paged(self.get_endpoint("blogpost_labels", id=blogpost_id), params=params))

    def get_blog_post_versions(
        self, blogpost_id: str, body_format: Optional[str] = None, sort: Optional[str] = None, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Return every version of a blog post, following pagination."""
        params: Dict[str, Any] = {"limit": limit}
        if body_format is not None:
            params["body-format"] = body_format
        if sort is not None:
            params["sort"] = sort
        return list(self._get_paged(self.get_endpoint("blogpost_versions", id=blogpost_id), params=params))

    def get_blog_post_version(self, blogpost_id: str, version_number: int) -> Optional[Dict[str, Any]]:
        """Return details for one blog post version."""
        return self.get(self.get_endpoint("blogpost_version", id=blogpost_id, version_number=version_number))

    def get_blog_post_likes_count(self, blogpost_id: str) -> int:
        """Return the number of likes on a blog post."""
        response = self.get(self.get_endpoint("blogpost_likes_count", id=blogpost_id))
        return int((response or {}).get("count", 0))

    def get_blog_post_likes_users(self, blogpost_id: str, limit: int = 25) -> List[Dict[str, Any]]:
        """Return every user who liked a blog post, following pagination."""
        return list(self._get_paged(self.get_endpoint("blogpost_likes_users", id=blogpost_id), params={"limit": limit}))

    def get_blog_post_operations(self, blogpost_id: str) -> List[Dict[str, Any]]:
        """Return the operations the current user can perform on a blog post."""
        response = self.get(self.get_endpoint("blogpost_operations", id=blogpost_id))
        return (response or {}).get("operations", [])

    def get_blog_post_attachments(
        self,
        blogpost_id: str,
        sort: Optional[str] = None,
        status: Optional[str] = None,
        media_type: Optional[str] = None,
        filename: Optional[str] = None,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """Return every attachment on a blog post, following pagination."""
        optional_params = {
            "sort": sort,
            "status": status,
            "mediaType": media_type,
            "filename": filename,
            "limit": limit,
        }
        params = {key: value for key, value in optional_params.items() if value is not None}
        return list(self._get_paged(self.get_endpoint("blogpost_attachments", id=blogpost_id), params=params))

    def get_blog_post_custom_content(
        self,
        blogpost_id: str,
        type: Optional[str] = None,
        sort: Optional[str] = None,
        body_format: Optional[str] = None,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """Return the custom content of the given type in a blog post, following pagination."""
        optional_params = {"type": type, "sort": sort, "body-format": body_format, "limit": limit}
        params = {key: value for key, value in optional_params.items() if value is not None}
        return list(self._get_paged(self.get_endpoint("blogpost_custom_content", id=blogpost_id), params=params))
