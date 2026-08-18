# coding=utf-8
"""Portfolio for Jira (Advanced Roadmaps) REST API client package.

This package combines two sets of endpoints:

* The legacy, plan-scoped ``rest/roadmap/1.0`` endpoints used by the
  Portfolio/Advanced Roadmaps web UI (see :mod:`atlassian.portfolio.legacy`).
  These require a ``plan_id`` to be supplied when constructing the client.
* The official public Portfolio for Jira (JPO) REST API, exposed below
  ``rest/jpo-api/1.0`` and documented at
  https://docs.atlassian.com/portfolio-for-jira-server/REST/2.13.0/jpo/.
  These are the ``jpo_*`` methods, split by entity into ``plan.py``,
  ``hierarchy.py``, ``program.py``, ``stage.py`` and ``nonworkingday.py``.
"""

import logging

from ..rest_client import AtlassianRestAPI
from .base import JPO_API_ROOT
from .hierarchy import HierarchyEndpoints
from .legacy import LegacyRoadmapEndpoints
from .nonworkingday import NonWorkingDayEndpoints
from .plan import PlanEndpoints
from .program import ProgramEndpoints
from .stage import StageEndpoints

log = logging.getLogger(__name__)

__all__ = ["Portfolio"]


class Portfolio(
    LegacyRoadmapEndpoints,
    PlanEndpoints,
    HierarchyEndpoints,
    ProgramEndpoints,
    StageEndpoints,
    NonWorkingDayEndpoints,
    AtlassianRestAPI,
):
    """Client for Portfolio for Jira (Advanced Roadmaps).

    Examples
    --------
    Legacy, plan-scoped endpoints (requires ``plan_id``):

    >>> portfolio = Portfolio(plan_id=1, url="https://jira.example.com", token="TOKEN")
    >>> portfolio.get_plan()

    Official public JPO REST API endpoints (``plan_id`` not required):

    >>> portfolio = Portfolio(url="https://jira.example.com", token="TOKEN")
    >>> portfolio.jpo_get_plans()
    >>> portfolio.jpo_create_program({"title": "New Program"})
    """

    JPO_API_ROOT = JPO_API_ROOT

    def __init__(self, plan_id=None, *args, **kwargs):
        self.plan_id = plan_id
        super(Portfolio, self).__init__(*args, **kwargs)
