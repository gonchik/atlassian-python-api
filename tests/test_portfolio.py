from unittest.mock import patch

from atlassian import Portfolio


def make_portfolio(plan_id=None):
    return Portfolio(plan_id, url="https://jira.example.com")


################################################################################################
# Legacy rest/roadmap/1.0 endpoints
################################################################################################


def test_get_plan():
    portfolio = make_portfolio(1959)
    with patch.object(portfolio, "get", return_value={"id": 1959}) as get:
        assert portfolio.get_plan() == {"id": 1959}
    get.assert_called_once_with("rest/roadmap/1.0/plans/1959.json")


def test_get_stages():
    portfolio = make_portfolio(1959)
    with patch.object(portfolio, "get", return_value={"collection": []}) as get:
        assert portfolio.get_stages() == {"collection": []}
    get.assert_called_once_with("rest/roadmap/1.0/plans/1959/stages.json")


def test_get_teams_and_team_name():
    portfolio = make_portfolio(1959)
    teams = {"collection": [{"id": "12", "title": "Team A"}]}
    with patch.object(portfolio, "get", return_value=teams) as get:
        assert portfolio.get_team_name(12) == "Team A"
    get.assert_called_once_with("rest/roadmap/1.0/plans/1959/teams.json")


def test_get_releases_delegates_to_streams():
    portfolio = make_portfolio(1959)
    with patch.object(portfolio, "get", return_value={"collection": []}) as get:
        assert portfolio.get_releases() == {"collection": []}
    get.assert_called_once_with("rest/roadmap/1.0/plans/1959/streams.json")


def test_get_filter():
    portfolio = make_portfolio(1959)
    with patch.object(portfolio, "post", return_value={}) as post:
        assert portfolio.get_filter(limit=100) == {}
    post.assert_called_once_with("rest/roadmap/1.0/plans/1959/workitems/filter.json", data={"limit": 100})


def test_get_jql_issues():
    portfolio = make_portfolio(1959)
    with patch.object(portfolio, "post", return_value={"data": {"items": ["ITEM-1"]}}) as post:
        assert portfolio.get_jql_issues("project = TEST") == ["ITEM-1"]
    post.assert_called_once_with(
        "rest/roadmap/1.0/system/import.json",
        data={
            "planId": "1959",
            "query": "project = TEST",
            "excludeLinked": True,
            "epicFetchEnabled": True,
            "maxResults": 500,
            "estimationMethod": "estimates",
            "loadStoryPoints": True,
        },
    )


def test_get_epic():
    portfolio = make_portfolio(1959)
    stages = {"collection": [{"id": "3", "title": "Build"}]}
    teams = {"collection": [{"id": "12", "title": "Team A"}]}
    epic = {
        "title": "Epic 1",
        "description": "Description",
        "teamId": 12,
        "links": [{"link": "PROJ-1"}],
        "estimates": {"stages": [{"targetId": "3", "value": 5}]},
    }
    with patch.object(portfolio, "get", side_effect=[stages, teams]):
        result = portfolio.get_epic(epic)
    assert result == {
        "title": "Epic 1",
        "team": "Team A",
        "description": "Description",
        "issuekey": "PROJ-1",
        "estimates": {"Build": 5, "Total": 5},
    }


################################################################################################
# Official public JPO REST API (rest/jpo-api/1.0)
################################################################################################


def test_jpo_get_plans_without_filters():
    portfolio = make_portfolio()
    with patch.object(portfolio, "get", return_value=[]) as get:
        assert portfolio.jpo_get_plans() == []
    get.assert_called_once_with("rest/jpo-api/1.0/plan", params=None)


def test_jpo_get_plans_with_pagination_and_ids():
    portfolio = make_portfolio()
    with patch.object(portfolio, "get", return_value=[]) as get:
        assert portfolio.jpo_get_plans(page=2, size=10, ids=[1, 2]) == []
    get.assert_called_once_with("rest/jpo-api/1.0/plan", params={"page": 2, "size": 10, "ids": [1, 2]})


def test_jpo_create_plan():
    portfolio = make_portfolio()
    payload = {"title": "New Plan"}
    with patch.object(portfolio, "post", return_value=1) as post:
        assert portfolio.jpo_create_plan(payload) == 1
    post.assert_called_once_with("rest/jpo-api/1.0/plan", data=payload)


def test_jpo_get_plans_count():
    portfolio = make_portfolio()
    with patch.object(portfolio, "get", return_value=3) as get:
        assert portfolio.jpo_get_plans_count() == 3
    get.assert_called_once_with("rest/jpo-api/1.0/plan/count")


def test_jpo_check_plans_exist():
    portfolio = make_portfolio()
    with patch.object(portfolio, "post", return_value=[1]) as post:
        assert portfolio.jpo_check_plans_exist([1, 2]) == [1]
    post.assert_called_once_with("rest/jpo-api/1.0/plan/exists", data=[1, 2])


def test_jpo_get_plan():
    portfolio = make_portfolio()
    with patch.object(portfolio, "get", return_value={"id": 1}) as get:
        assert portfolio.jpo_get_plan(1) == {"id": 1}
    get.assert_called_once_with("rest/jpo-api/1.0/plan/1")


def test_jpo_update_plan():
    portfolio = make_portfolio()
    payload = {"title": "Updated Plan"}
    with patch.object(portfolio, "post", return_value=payload) as post:
        assert portfolio.jpo_update_plan(1, payload) == payload
    post.assert_called_once_with("rest/jpo-api/1.0/plan/1", data=payload)


def test_jpo_delete_plan():
    portfolio = make_portfolio()
    with patch.object(portfolio, "delete", return_value={}) as delete:
        assert portfolio.jpo_delete_plan(1) == {}
    delete.assert_called_once_with("rest/jpo-api/1.0/plan/1")


def test_jpo_hierarchy_crud():
    portfolio = make_portfolio()
    payload = {"title": "Initiative", "issueTypeIds": ["10000"]}

    with patch.object(portfolio, "get", return_value=[]) as get:
        assert portfolio.jpo_get_hierarchies() == []
    get.assert_called_once_with("rest/jpo-api/1.0/hierarchy", params=None)

    with patch.object(portfolio, "post", return_value=1) as post:
        assert portfolio.jpo_create_hierarchy(payload) == 1
    post.assert_called_once_with("rest/jpo-api/1.0/hierarchy", data=payload)

    with patch.object(portfolio, "get", return_value=2) as get:
        assert portfolio.jpo_get_hierarchies_count() == 2
    get.assert_called_once_with("rest/jpo-api/1.0/hierarchy/count")

    with patch.object(portfolio, "post", return_value=[1]) as post:
        assert portfolio.jpo_check_hierarchies_exist([1]) == [1]
    post.assert_called_once_with("rest/jpo-api/1.0/hierarchy/exists", data=[1])

    with patch.object(portfolio, "get", return_value=payload) as get:
        assert portfolio.jpo_get_hierarchy(1) == payload
    get.assert_called_once_with("rest/jpo-api/1.0/hierarchy/1")

    with patch.object(portfolio, "post", return_value=payload) as post:
        assert portfolio.jpo_update_hierarchy(1, payload) == payload
    post.assert_called_once_with("rest/jpo-api/1.0/hierarchy/1", data=payload)

    with patch.object(portfolio, "delete", return_value={}) as delete:
        assert portfolio.jpo_delete_hierarchy(1) == {}
    delete.assert_called_once_with("rest/jpo-api/1.0/hierarchy/1")


def test_jpo_program_crud():
    portfolio = make_portfolio()
    payload = {"title": "Program", "owner": "user"}

    with patch.object(portfolio, "get", return_value=[]) as get:
        assert portfolio.jpo_get_programs() == []
    get.assert_called_once_with("rest/jpo-api/1.0/program", params=None)

    with patch.object(portfolio, "post", return_value=1) as post:
        assert portfolio.jpo_create_program(payload) == 1
    post.assert_called_once_with("rest/jpo-api/1.0/program", data=payload)

    with patch.object(portfolio, "get", return_value=2) as get:
        assert portfolio.jpo_get_programs_count() == 2
    get.assert_called_once_with("rest/jpo-api/1.0/program/count")

    with patch.object(portfolio, "post", return_value=[1]) as post:
        assert portfolio.jpo_check_programs_exist([1]) == [1]
    post.assert_called_once_with("rest/jpo-api/1.0/program/exists", data=[1])

    with patch.object(portfolio, "get", return_value=payload) as get:
        assert portfolio.jpo_get_program(1) == payload
    get.assert_called_once_with("rest/jpo-api/1.0/program/1")

    with patch.object(portfolio, "post", return_value=payload) as post:
        assert portfolio.jpo_update_program(1, payload) == payload
    post.assert_called_once_with("rest/jpo-api/1.0/program/1", data=payload)

    with patch.object(portfolio, "delete", return_value={}) as delete:
        assert portfolio.jpo_delete_program(1) == {}
    delete.assert_called_once_with("rest/jpo-api/1.0/program/1")


def test_jpo_stage_crud():
    portfolio = make_portfolio()
    payload = {"planId": 1959, "title": "Build", "weight": 1.0}

    with patch.object(portfolio, "get", return_value=[]) as get:
        assert portfolio.jpo_get_stages() == []
    get.assert_called_once_with("rest/jpo-api/1.0/stage", params=None)

    with patch.object(portfolio, "post", return_value=1) as post:
        assert portfolio.jpo_create_stage(payload) == 1
    post.assert_called_once_with("rest/jpo-api/1.0/stage", data=payload)

    with patch.object(portfolio, "get", return_value=2) as get:
        assert portfolio.jpo_get_stages_count() == 2
    get.assert_called_once_with("rest/jpo-api/1.0/stage/count")

    with patch.object(portfolio, "post", return_value=[1]) as post:
        assert portfolio.jpo_check_stages_exist([1]) == [1]
    post.assert_called_once_with("rest/jpo-api/1.0/stage/exists", data=[1])

    with patch.object(portfolio, "get", return_value=payload) as get:
        assert portfolio.jpo_get_stage(1) == payload
    get.assert_called_once_with("rest/jpo-api/1.0/stage/1")

    with patch.object(portfolio, "post", return_value=payload) as post:
        assert portfolio.jpo_update_stage(1, payload) == payload
    post.assert_called_once_with("rest/jpo-api/1.0/stage/1", data=payload)

    with patch.object(portfolio, "delete", return_value={}) as delete:
        assert portfolio.jpo_delete_stage(1) == {}
    delete.assert_called_once_with("rest/jpo-api/1.0/stage/1")


def test_jpo_non_working_day_crud_and_plan_lookup():
    portfolio = make_portfolio()
    payload = {"planId": 1959, "title": "Company Holiday", "start": 1, "end": 2}

    with patch.object(portfolio, "get", return_value=[]) as get:
        assert portfolio.jpo_get_non_working_days() == []
    get.assert_called_once_with("rest/jpo-api/1.0/nonworkingday", params=None)

    with patch.object(portfolio, "post", return_value=1) as post:
        assert portfolio.jpo_create_non_working_day(payload) == 1
    post.assert_called_once_with("rest/jpo-api/1.0/nonworkingday", data=payload)

    with patch.object(portfolio, "get", return_value=2) as get:
        assert portfolio.jpo_get_non_working_days_count() == 2
    get.assert_called_once_with("rest/jpo-api/1.0/nonworkingday/count")

    with patch.object(portfolio, "post", return_value=[1]) as post:
        assert portfolio.jpo_check_non_working_days_exist([1]) == [1]
    post.assert_called_once_with("rest/jpo-api/1.0/nonworkingday/exists", data=[1])

    with patch.object(portfolio, "get", return_value=[payload]) as get:
        assert portfolio.jpo_get_non_working_days_for_plan(1959) == [payload]
    get.assert_called_once_with("rest/jpo-api/1.0/nonworkingday/plan/1959")

    with patch.object(portfolio, "get", return_value=payload) as get:
        assert portfolio.jpo_get_non_working_day(1) == payload
    get.assert_called_once_with("rest/jpo-api/1.0/nonworkingday/1")

    with patch.object(portfolio, "post", return_value=payload) as post:
        assert portfolio.jpo_update_non_working_day(1, payload) == payload
    post.assert_called_once_with("rest/jpo-api/1.0/nonworkingday/1", data=payload)

    with patch.object(portfolio, "delete", return_value={}) as delete:
        assert portfolio.jpo_delete_non_working_day(1) == {}
    delete.assert_called_once_with("rest/jpo-api/1.0/nonworkingday/1")
