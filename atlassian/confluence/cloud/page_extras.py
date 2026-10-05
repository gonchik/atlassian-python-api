"""Confluence Cloud V2 page hierarchy, likes, and label operations."""

from typing import Any, Dict, List, Optional

from ...confluence_base import ConfluenceBase


class PageExtrasOperations(ConfluenceBase):
    """Base component implementing Confluence Cloud page hierarchy endpoints."""

    def get_page_ancestors(self, page_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Return the ancestors of a page, from the root down to the direct parent.

        Scoped tokens require ``read:page:confluence``.
        """
        params = {} if limit is None else {"limit": limit}
        response = self.get(self.get_endpoint("page_ancestors", id=page_id), params=params or None)
        if response is None:
            return []
        return response.get("results", [])

    def get_page_descendants(self, page_id: str, depth: Optional[int] = None, limit: int = 25) -> List[Dict[str, Any]]:
        """Return every descendant of a page, following pagination.

        Scoped tokens require ``read:page:confluence``.
        """
        params: Dict[str, Any] = {"limit": limit}
        if depth is not None:
            params["depth"] = depth
        return list(self._get_paged(self.get_endpoint("page_descendants", id=page_id), params=params))

    def get_page_attachments(
        self,
        page_id: str,
        sort: Optional[str] = None,
        status: Optional[str] = None,
        media_type: Optional[str] = None,
        filename: Optional[str] = None,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """Return every attachment on a page, following pagination.

        Scoped tokens require ``read:attachment:confluence``.
        """
        optional_params = {
            "sort": sort,
            "status": status,
            "mediaType": media_type,
            "filename": filename,
            "limit": limit,
        }
        params = {key: value for key, value in optional_params.items() if value is not None}
        return list(self._get_paged(self.get_endpoint("page_attachments", id=page_id), params=params))

    def get_page_custom_content(
        self,
        page_id: str,
        type: Optional[str] = None,
        sort: Optional[str] = None,
        body_format: Optional[str] = None,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """Return the custom content of the given type in a page, following pagination."""
        optional_params = {"type": type, "sort": sort, "body-format": body_format, "limit": limit}
        params = {key: value for key, value in optional_params.items() if value is not None}
        return list(self._get_paged(self.get_endpoint("page_custom_content", id=page_id), params=params))

    def get_page_likes_count(self, page_id: str) -> int:
        """Return the number of likes on a page."""
        response = self.get(self.get_endpoint("page_likes_count", id=page_id))
        return int((response or {}).get("count", 0))

    def get_page_likes_users(self, page_id: str, limit: int = 25) -> List[Dict[str, Any]]:
        """Return every user who liked a page, following pagination."""
        return list(self._get_paged(self.get_endpoint("page_likes_users", id=page_id), params={"limit": limit}))

    def get_page_operations(self, page_id: str) -> List[Dict[str, Any]]:
        """Return the operations the current user can perform on a page."""
        response = self.get(self.get_endpoint("page_operations", id=page_id))
        return (response or {}).get("operations", [])

    def update_page_title(self, page_id: str, title: str, status: str = "current") -> Optional[Dict[str, Any]]:
        """Update the title of a page without bumping its version.

        Scoped tokens require ``write:page:confluence``.
        """
        if status not in ("current", "draft"):
            raise ValueError("status must be 'current' or 'draft'")
        return self.put(self.get_endpoint("page_title", id=page_id), data={"status": status, "title": title})

    # ------------------------------------------------------------------
    # Labels
    # ------------------------------------------------------------------

    def get_labels(
        self,
        label_ids: Optional[List[str]] = None,
        prefix: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """Return every label matching the filters, following pagination.

        Scoped tokens require ``read:page:confluence``.
        """
        params: Dict[str, Any] = {"limit": limit}
        if label_ids:
            params["label-id"] = label_ids
        if prefix is not None:
            params["prefix"] = prefix
        if sort is not None:
            params["sort"] = sort
        return list(self._get_paged(self.get_endpoint("labels"), params=params))

    def get_label_pages(
        self,
        label_id: str,
        space_id: Optional[str] = None,
        body_format: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """Return every page with the given label, following pagination."""
        optional_params = {"space-id": space_id, "body-format": body_format, "sort": sort, "limit": limit}
        params = {key: value for key, value in optional_params.items() if value is not None}
        return list(self._get_paged(self.get_endpoint("label_pages", id=label_id), params=params))

    def get_label_blogposts(
        self,
        label_id: str,
        space_id: Optional[str] = None,
        body_format: Optional[str] = None,
        sort: Optional[str] = None,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """Return every blog post with the given label, following pagination."""
        optional_params = {"space-id": space_id, "body-format": body_format, "sort": sort, "limit": limit}
        params = {key: value for key, value in optional_params.items() if value is not None}
        return list(self._get_paged(self.get_endpoint("label_blogposts", id=label_id), params=params))

    def get_label_attachments(self, label_id: str, sort: Optional[str] = None, limit: int = 25) -> List[Dict[str, Any]]:
        """Return every attachment with the given label, following pagination."""
        optional_params = {"sort": sort, "limit": limit}
        params = {key: value for key, value in optional_params.items() if value is not None}
        return list(self._get_paged(self.get_endpoint("label_attachments", id=label_id), params=params))
