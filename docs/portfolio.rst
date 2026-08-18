Portfolio for Jira (Advanced Roadmaps)
=======================================

The ``Portfolio`` client wraps two sets of endpoints:

* Legacy, plan-scoped ``rest/roadmap/1.0`` endpoints used internally by the
  Portfolio/Advanced Roadmaps web UI. These require a ``plan_id``.
* The official public Portfolio for Jira (JPO) REST API, exposed below
  ``rest/jpo-api/1.0``. See the API reference:
  https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/jpo/

Legacy plan-scoped usage
-------------------------

.. code-block:: python

    from atlassian import Portfolio

    portfolio = Portfolio(
        1959,  # plan_id
        url="https://jira.example.com",
        username="admin",
        password="admin",
    )

    plan = portfolio.get_plan()
    stages = portfolio.get_stages()
    teams = portfolio.get_teams()
    issues = portfolio.get_jql_issues("project = TEST")

Official public JPO REST API usage
------------------------------------

``plan_id`` is optional for the ``jpo_*`` methods, which operate on entity
ids passed explicitly:

.. code-block:: python

    from atlassian import Portfolio

    portfolio = Portfolio(
        url="https://jira.example.com",
        username="admin",
        password="admin",
    )

    # Plans
    plans = portfolio.jpo_get_plans(page=1, size=50)
    plan_id = portfolio.jpo_create_plan({"title": "New Plan"})
    plan = portfolio.jpo_get_plan(plan_id)
    portfolio.jpo_update_plan(plan_id, {"title": "Renamed Plan"})
    portfolio.jpo_delete_plan(plan_id)

    # Hierarchy levels
    portfolio.jpo_get_hierarchies()
    portfolio.jpo_create_hierarchy({"title": "Initiative", "issueTypeIds": ["10000"]})

    # Programs
    portfolio.jpo_get_programs()
    portfolio.jpo_create_program({"title": "New Program", "owner": "admin"})

    # Stages
    portfolio.jpo_get_stages()
    portfolio.jpo_create_stage({"planId": plan_id, "title": "Build", "weight": 1.0})

    # Non-working days
    portfolio.jpo_get_non_working_days_for_plan(plan_id)
    portfolio.jpo_create_non_working_day(
        {"planId": plan_id, "title": "Company Holiday", "start": 1, "end": 2}
    )

Every entity (``plan``, ``hierarchy``, ``program``, ``stage``,
``nonworkingday``) exposes the same CRUD shape: ``jpo_get_<entities>``,
``jpo_create_<entity>``, ``jpo_get_<entities>_count``,
``jpo_check_<entities>_exist``, ``jpo_get_<entity>``,
``jpo_update_<entity>``, and ``jpo_delete_<entity>``.

API reference
-------------

.. autoclass:: atlassian.portfolio.Portfolio
   :members:
   :undoc-members:
   :show-inheritance:
