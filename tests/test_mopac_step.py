#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mopac_step` package."""

import pytest
import mopac_step  # noqa: F401


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_estimated_seconds():
    from mopac_step.mopac import estimated_seconds

    single = estimated_seconds(["PM7 1SCF"], 3)
    assert single < 1
    assert estimated_seconds(["PM7"], 3) > single  # an optimization
    assert estimated_seconds(["PM7 FORCE"], 3) > single
    assert estimated_seconds(["PM7 1SCF"], 500) > 60
    assert estimated_seconds(["PM7 1SCF", "PM7 1SCF"], 3) == 2 * single
