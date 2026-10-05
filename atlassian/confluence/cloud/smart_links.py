"""Confluence Cloud V2 smart link (embed) operations."""

from typing import Any, Dict, List, Optional

from ...confluence_base import ConfluenceBase


class SmartLinkOperations(ConfluenceBase):
    """Base component implementing Confluence Cloud smart link endpoints."""

    def create_smart_link(
        self,
        space_id: str,
        embed_url: str,
        title: Optional[str] = None,
        parent_id: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Create a smart link in a Confluence Cloud space.

        Scoped tokens require ``write:embed:confluence``.
        """
        data: Dict[str, str] = {"spaceId": space_id, "embedUrl": embed_url}
        if title is not None:
            data["title"] = title
        if parent_id is not None:
            data["parentId"] = parent_id
        return self.post(self.get_endpoint("embeds"), data=data)

    def get_smart_link(
        self,
        embed_id: str,
        include_collaborators: Optional[bool] = None,
        include_direct_children: Optional[bool] = None,
        include_operations: Optional[bool] = None,
        include_properties: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Return a smart link by ID.

        Scoped tokens require ``read:embed:confluence``.
        """
        optional_params = {
            "include-collaborators": include_collaborators,
            "include-direct-children": include_direct_children,
            "include-operations": include_operations,
            "include-properties": include_properties,
        }
        params = {key: value for key, value in optional_params.items() if value is not None}
        endpoint = self.get_endpoint("embed_by_id", id=embed_id)
        if not params:
            return self.get(endpoint)
        return self.get(endpoint, params=params)

    def get_smart_link_by_id(self, embed_id: str, **kwargs: Any) -> Optional[Dict[str, Any]]:
        """Backward-compatible alias for :meth:`get_smart_link`."""
        return self.get_smart_link(embed_id, **kwargs)

    def delete_smart_link(self, embed_id: str) -> bool:
        """Move a smart link to the Confluence Cloud trash.

        Scoped tokens require ``delete:embed:confluence``.
        """
        self.delete(self.get_endpoint("embed_by_id", id=embed_id))
        return True

    def get_smart_link_ancestors(self, embed_id: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Return the ancestors of a smart link."""
        params = {} if limit is None else {"limit": limit}
        response = self.get(self.get_endpoint("embed_ancestors", id=embed_id), params=params or None)
        if response is None:
            return []
        return response.get("results", [])

    def get_smart_link_descendants(
        self, embed_id: str, depth: Optional[int] = None, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Return every descendant of a smart link, following pagination."""
        params: Dict[str, Any] = {"limit": limit}
        if depth is not None:
            params["depth"] = depth
        return list(self._get_paged(self.get_endpoint("embed_descendants", id=embed_id), params=params))

    def get_smart_link_direct_children(
        self, embed_id: str, sort: Optional[str] = None, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Return the direct children of a smart link, following pagination."""
        params: Dict[str, Any] = {"limit": limit}
        if sort is not None:
            params["sort"] = sort
        return list(self._get_paged(self.get_endpoint("embed_direct_children", id=embed_id), params=params))

    def get_smart_link_operations(self, embed_id: str) -> List[Dict[str, Any]]:
        """Return the operations the current user can perform on a smart link."""
        response = self.get(self.get_endpoint("embed_operations", id=embed_id))
        return (response or {}).get("operations", [])
