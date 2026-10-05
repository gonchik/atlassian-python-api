"""Tests for the Confluence Cloud V2 blog post, attachment, smart link, page
hierarchy, label, and comment operations added from the official OpenAPI spec."""

from unittest.mock import patch

from atlassian.confluence.cloud.cloud import ConfluenceCloud


def _client():
    return ConfluenceCloud("https://example.atlassian.net", token="t")


# ---------------------------------------------------------------------------
# Blog posts
# ---------------------------------------------------------------------------


def test_blog_post_crud_uses_v2_routes():
    client = _client()
    with patch.object(client, "post", return_value={}) as post:
        client.create_blog_post(space_id="S1", title="T", body="B", body_format="storage")
    assert post.call_args_list[0].args == ("api/v2/blogposts",)
    assert post.call_args_list[0].kwargs["data"] == {
        "spaceId": "S1",
        "status": "current",
        "title": "T",
        "body": {"storage": {"representation": "storage", "value": "B"}},
    }

    with patch.object(client, "get", return_value={}) as get:
        client.get_blog_posts(space_id="S1", status="current", limit=10)
    assert get.call_args_list[0].args == ("api/v2/blogposts",)
    assert get.call_args_list[0].kwargs["params"] == {
        "limit": 10,
        "space-id": "S1",
        "status": "current",
    }

    with patch.object(client, "get", return_value={}) as get:
        client.get_blog_post_by_id("123", include_labels=True)
    assert get.call_args_list[0].args == ("api/v2/blogposts/123",)
    assert get.call_args_list[0].kwargs["params"] == {"include-labels": True}

    with patch.object(client, "delete", return_value=None) as delete:
        assert client.delete_blog_post("123", purge=True) is True
    assert delete.call_args_list[0].args == ("api/v2/blogposts/123",)
    assert delete.call_args_list[0].kwargs["params"] == {"purge": True}


def test_update_blog_post_autofetches_version_and_title():
    client = _client()
    current = {"title": "Old", "version": {"number": 2}, "body": {"storage": {"value": "old"}}}
    with patch.object(client, "get", return_value=current) as get, patch.object(client, "put", return_value={}) as put:
        client.update_blog_post("123", body="New body")
    assert get.call_args_list[0].args == ("api/v2/blogposts/123",)
    assert put.call_args_list[0].args == ("api/v2/blogposts/123",)
    data = put.call_args_list[0].kwargs["data"]
    assert data["version"] == {"number": 3}
    assert data["title"] == "Old"
    assert data["body"] == {"storage": {"representation": "storage", "value": "New body"}}


def test_blog_post_subresources_use_v2_routes():
    client = _client()
    with (
        patch.object(client, "_get_paged", return_value=iter([])) as paged,
        patch.object(client, "get", return_value={"results": []}) as get,
    ):
        client.get_blog_post_labels("123", prefix="team")
        client.get_blog_post_versions("123", body_format="storage")
        client.get_blog_post_likes_users("123")
        client.get_blog_post_attachments("123", media_type="image/png")
        client.get_blog_post_custom_content("123", type="example")
        client.get_blog_post_likes_count("123")
        client.get_blog_post_operations("123")
        client.get_blog_post_version("123", 1)
    assert paged.call_args_list[0].args == ("api/v2/blogposts/123/labels",)
    assert paged.call_args_list[0].kwargs["params"] == {"limit": 25, "prefix": "team"}
    assert paged.call_args_list[1].args == ("api/v2/blogposts/123/versions",)
    assert paged.call_args_list[1].kwargs["params"] == {"limit": 25, "body-format": "storage"}
    assert paged.call_args_list[2].args == ("api/v2/blogposts/123/likes/users",)
    assert paged.call_args_list[3].args == ("api/v2/blogposts/123/attachments",)
    assert paged.call_args_list[3].kwargs["params"] == {"limit": 25, "mediaType": "image/png"}
    assert paged.call_args_list[4].args == ("api/v2/blogposts/123/custom-content",)
    assert get.call_args_list[0].args == ("api/v2/blogposts/123/likes/count",)
    assert get.call_args_list[1].args == ("api/v2/blogposts/123/operations",)
    assert get.call_args_list[2].args == ("api/v2/blogposts/123/versions/1",)


def test_blog_post_validation():
    client = _client()
    for bad in (
        lambda: client.create_blog_post(space_id="S1", status="bogus"),
        lambda: client.create_blog_post(space_id="S1", status="current"),
        lambda: client.update_blog_post("123", status="bogus"),
    ):
        try:
            bad()
            raise AssertionError("expected ValueError")
        except ValueError:
            pass


def test_attachment_operations_use_v2_routes():
    client = _client()
    with (
        patch.object(client, "_get_paged", return_value=iter([])) as paged,
        patch.object(client, "get", return_value={"results": []}) as get,
        patch.object(client, "delete", return_value=None) as delete,
    ):
        client.get_attachments(ids=["A1", "A2"], media_type="image/png")
        client.get_attachment_by_id("123", include_labels=True)
        assert client.delete_attachment("123") is True
        client.get_attachment_labels("123")
        client.get_attachment_versions("123")
        client.get_attachment_version("123", 2)
        client.get_attachment_operations("123")
    assert paged.call_args_list[0].args == ("api/v2/attachments",)
    assert paged.call_args_list[0].kwargs["params"] == {"limit": 25, "id": ["A1", "A2"], "mediaType": "image/png"}
    assert get.call_args_list[0].args == ("api/v2/attachments/123",)
    assert get.call_args_list[0].kwargs["params"] == {"include-labels": True}
    assert delete.call_args_list[0].args == ("api/v2/attachments/123",)
    assert paged.call_args_list[1].args == ("api/v2/attachments/123/labels",)
    assert paged.call_args_list[2].args == ("api/v2/attachments/123/versions",)
    assert get.call_args_list[1].args == ("api/v2/attachments/123/versions/2",)
    assert get.call_args_list[2].args == ("api/v2/attachments/123/operations",)


def test_attachment_thumbnail_returns_bytes():
    client = _client()
    response = type("R", (), {"content": b"png-bytes", "status_code": 200})()
    with patch.object(client, "get", return_value=response) as get:
        assert client.get_attachment_thumbnail("123", height=200, width=300) == b"png-bytes"
    assert get.call_args_list[0].args == ("api/v2/attachments/123/thumbnail/download",)
    assert get.call_args_list[0].kwargs["params"] == {"height": 200, "width": 300}
    assert get.call_args_list[0].kwargs["advanced_mode"] is True


# ---------------------------------------------------------------------------
# Smart links (embeds)
# ---------------------------------------------------------------------------


def test_smart_link_crud_uses_v2_routes():
    client = _client()
    with patch.object(client, "post", return_value={}) as post:
        client.create_smart_link(space_id="S1", embed_url="https://example.com", title="Example")
    assert post.call_args_list[0].args == ("api/v2/embeds",)
    assert post.call_args_list[0].kwargs["data"] == {
        "spaceId": "S1",
        "embedUrl": "https://example.com",
        "title": "Example",
    }

    with patch.object(client, "get", return_value={}) as get:
        client.get_smart_link("E1", include_operations=True)
    assert get.call_args_list[0].args == ("api/v2/embeds/E1",)
    assert get.call_args_list[0].kwargs["params"] == {"include-operations": True}

    with patch.object(client, "delete", return_value=None) as delete:
        assert client.delete_smart_link("E1") is True
    assert delete.call_args_list[0].args == ("api/v2/embeds/E1",)


def test_smart_link_hierarchy_uses_v2_routes():
    client = _client()
    with (
        patch.object(client, "_get_paged", return_value=iter([])) as paged,
        patch.object(client, "get", return_value={"results": []}) as get,
    ):
        client.get_smart_link_ancestors("E1")
        client.get_smart_link_descendants("E1", depth=2)
        client.get_smart_link_direct_children("E1", sort="title")
        client.get_smart_link_operations("E1")
    assert get.call_args_list[0].args == ("api/v2/embeds/E1/ancestors",)
    assert paged.call_args_list[0].args == ("api/v2/embeds/E1/descendants",)
    assert paged.call_args_list[0].kwargs["params"] == {"limit": 25, "depth": 2}
    assert paged.call_args_list[1].args == ("api/v2/embeds/E1/direct-children",)
    assert get.call_args_list[1].args == ("api/v2/embeds/E1/operations",)


# ---------------------------------------------------------------------------
# Page extras: hierarchy, likes, operations, title
# ---------------------------------------------------------------------------


def test_page_extras_use_v2_routes():
    client = _client()
    with (
        patch.object(client, "_get_paged", return_value=iter([])) as paged,
        patch.object(client, "get", return_value={"results": []}) as get,
        patch.object(client, "put", return_value={}) as put,
    ):
        client.get_page_ancestors("123")
        client.get_page_descendants("123", depth=3)
        client.get_page_attachments("123")
        client.get_page_custom_content("123", type="example")
        client.get_page_likes_count("123")
        client.get_page_likes_users("123")
        client.get_page_operations("123")
        client.update_page_title("123", "New Title")
    assert get.call_args_list[0].args == ("api/v2/pages/123/ancestors",)
    assert paged.call_args_list[0].args == ("api/v2/pages/123/descendants",)
    assert paged.call_args_list[0].kwargs["params"] == {"limit": 25, "depth": 3}
    assert paged.call_args_list[1].args == ("api/v2/pages/123/attachments",)
    assert paged.call_args_list[2].args == ("api/v2/pages/123/custom-content",)
    assert get.call_args_list[1].args == ("api/v2/pages/123/likes/count",)
    assert paged.call_args_list[3].args == ("api/v2/pages/123/likes/users",)
    assert get.call_args_list[2].args == ("api/v2/pages/123/operations",)
    assert put.call_args_list[0].args == ("api/v2/pages/123/title",)
    assert put.call_args_list[0].kwargs["data"] == {"status": "current", "title": "New Title"}


# ---------------------------------------------------------------------------
# Labels
# ---------------------------------------------------------------------------


def test_label_operations_use_v2_routes():
    client = _client()
    with patch.object(client, "_get_paged", return_value=iter([])) as paged:
        client.get_labels(prefix="team")
        client.get_label_pages("L1", space_id="S1")
        client.get_label_blogposts("L1")
        client.get_label_attachments("L1")
    assert paged.call_args_list[0].args == ("api/v2/labels",)
    assert paged.call_args_list[0].kwargs["params"] == {"limit": 25, "prefix": "team"}
    assert paged.call_args_list[1].args == ("api/v2/labels/L1/pages",)
    assert paged.call_args_list[1].kwargs["params"] == {"limit": 25, "space-id": "S1"}
    assert paged.call_args_list[2].args == ("api/v2/labels/L1/blogposts",)
    assert paged.call_args_list[3].args == ("api/v2/labels/L1/attachments",)


# ---------------------------------------------------------------------------
# Comment endpoint fixes (spec: /footer-comments/{id} and /inline-comments/{id})
# ---------------------------------------------------------------------------


def test_comment_crud_uses_spec_routes():
    client = _client()
    with (
        patch.object(client, "get", return_value={}) as get,
        patch.object(client, "put", return_value={}) as put,
        patch.object(client, "delete", return_value=None) as delete,
    ):
        client.get_comment_by_id("C1")
        client.get_comment_by_id("C1", comment_type="inline-comments")
        client.update_comment("C1", "body", version=2)
        client.update_comment("C1", "body", version=2, comment_type="inline-comments", resolved=True)
        assert client.delete_comment("C1") is True
        client.delete_comment("C1", comment_type="inline-comments")
    assert get.call_args_list[0].args == ("api/v2/footer-comments/C1",)
    assert get.call_args_list[1].args == ("api/v2/inline-comments/C1",)
    assert put.call_args_list[0].args == ("api/v2/footer-comments/C1",)
    assert put.call_args_list[1].args == ("api/v2/inline-comments/C1",)
    assert put.call_args_list[1].kwargs["data"]["resolved"] is True
    assert delete.call_args_list[0].args == ("api/v2/footer-comments/C1",)
    assert delete.call_args_list[1].args == ("api/v2/inline-comments/C1",)


def test_comment_creates_use_spec_routes():
    client = _client()
    with patch.object(client, "post", return_value={}) as post:
        client.create_page_footer_comment("P1", "hello")
        client.create_page_inline_comment(
            "P1", "note", {"textSelection": "x", "textSelectionMatchCount": 1, "textSelectionMatchIndex": 0}
        )
        client.create_comment_reply("C1", "reply")
    assert post.call_args_list[0].args == ("api/v2/footer-comments",)
    assert post.call_args_list[1].args == ("api/v2/inline-comments",)
    assert post.call_args_list[2].args == ("api/v2/footer-comments",)


def test_comment_type_validation():
    client = _client()
    for bad in (
        lambda: client.get_comment_by_id("C1", comment_type="bogus"),
        lambda: client.update_comment("C1", "b", 1, comment_type="bogus"),
        lambda: client.delete_comment("C1", comment_type="bogus"),
    ):
        try:
            bad()
            raise AssertionError("expected ValueError")
        except ValueError:
            pass


def test_whiteboard_children_uses_spec_route():
    client = _client()
    with patch.object(client, "_get_paged", return_value=iter([])) as paged:
        client.get_whiteboard_children("W1")
    assert paged.call_args_list[0].args == ("api/v2/whiteboards/W1/direct-children",)
