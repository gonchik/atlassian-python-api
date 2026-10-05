"""Confluence Cloud V2 attachment operations."""

from typing import Any, Dict, List, Optional

from ...confluence_base import ConfluenceBase


class AttachmentOperations(ConfluenceBase):
    """Base component implementing Confluence Cloud attachment endpoints."""

    def get_attachments(
        self,
        ids: Optional[List[str]] = None,
        sort: Optional[str] = None,
        status: Optional[str] = None,
        media_type: Optional[str] = None,
        filename: Optional[str] = None,
        limit: int = 25,
    ) -> List[Dict[str, Any]]:
        """Return every attachment matching the filters, following pagination.

        Scoped tokens require ``read:attachment:confluence``.
        """
        params: Dict[str, Any] = {"limit": limit}
        if ids:
            params["id"] = ids
        if sort is not None:
            params["sort"] = sort
        if status is not None:
            params["status"] = status
        if media_type is not None:
            params["mediaType"] = media_type
        if filename is not None:
            params["filename"] = filename
        return list(self._get_paged(self.get_endpoint("attachments"), params=params))

    def get_attachment_by_id(
        self,
        attachment_id: str,
        version: Optional[int] = None,
        include_labels: Optional[bool] = None,
        include_properties: Optional[bool] = None,
        include_operations: Optional[bool] = None,
        include_versions: Optional[bool] = None,
        include_version: Optional[bool] = None,
    ) -> Optional[Dict[str, Any]]:
        """Return an attachment by ID.

        Scoped tokens require ``read:attachment:confluence``.
        """
        optional_params = {
            "version": version,
            "include-labels": include_labels,
            "include-properties": include_properties,
            "include-operations": include_operations,
            "include-versions": include_versions,
            "include-version": include_version,
        }
        params = {key: value for key, value in optional_params.items() if value is not None}
        endpoint = self.get_endpoint("attachment_by_id", id=attachment_id)
        if not params:
            return self.get(endpoint)
        return self.get(endpoint, params=params)

    def delete_attachment(self, attachment_id: str, purge: Optional[bool] = None) -> bool:
        """Delete an attachment, or purge it from the trash.

        Scoped tokens require ``delete:attachment:confluence``.
        """
        if purge is None:
            self.delete(self.get_endpoint("attachment_by_id", id=attachment_id))
        else:
            self.delete(self.get_endpoint("attachment_by_id", id=attachment_id), params={"purge": purge})
        return True

    def get_attachment_labels(
        self, attachment_id: str, prefix: Optional[str] = None, sort: Optional[str] = None, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Return every label on an attachment, following pagination."""
        params: Dict[str, Any] = {"limit": limit}
        if prefix is not None:
            params["prefix"] = prefix
        if sort is not None:
            params["sort"] = sort
        return list(self._get_paged(self.get_endpoint("attachment_labels", id=attachment_id), params=params))

    def get_attachment_versions(
        self, attachment_id: str, sort: Optional[str] = None, limit: int = 25
    ) -> List[Dict[str, Any]]:
        """Return every version of an attachment, following pagination."""
        params: Dict[str, Any] = {"limit": limit}
        if sort is not None:
            params["sort"] = sort
        return list(self._get_paged(self.get_endpoint("attachment_versions", id=attachment_id), params=params))

    def get_attachment_version(self, attachment_id: str, version_number: int) -> Optional[Dict[str, Any]]:
        """Return details for one attachment version."""
        return self.get(self.get_endpoint("attachment_version", id=attachment_id, version_number=version_number))

    def get_attachment_operations(self, attachment_id: str) -> List[Dict[str, Any]]:
        """Return the operations the current user can perform on an attachment."""
        response = self.get(self.get_endpoint("attachment_operations", id=attachment_id))
        return (response or {}).get("operations", [])

    def get_attachment_thumbnail(
        self,
        attachment_id: str,
        version: Optional[int] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
    ) -> Optional[bytes]:
        """Return the thumbnail image bytes of an attachment."""
        optional_params = {"version": version, "height": height, "width": width}
        params = {key: value for key, value in optional_params.items() if value is not None}
        endpoint = self.get_endpoint("attachment_thumbnail", id=attachment_id)
        if params:
            return self.get(endpoint, params=params, advanced_mode=True).content
        return self.get(endpoint, advanced_mode=True).content
