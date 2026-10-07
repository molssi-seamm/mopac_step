# -*- coding: utf-8 -*-
"""The step's timing benchmark declaration (seamm_exec.timing_benchmark)."""

import pytest

import mopac_step


def test_declaration_shape():
    d = mopac_step.TIMING_BENCHMARK
    assert d["program"] == "mopac" and d["step"] == "MOPAC" and not d["parallel"]
    assert d["parameter"] == "hamiltonian"
    sizes = [s["size"] for s in d["systems"]]
    assert sizes == sorted(sizes) and sizes[0] == 3 and sizes[-1] == 3002
    assert set(d["chemistries"]) == {"PM7", "PM6-ORG"}
    for limits in (*d["chemistries"].values(), *d["tasks"].values()):
        assert limits["quick"] <= limits["full"]
    variant = d["variants"]["Energy"][1]
    assert variant["MOZYME"] == "never" and variant["_min_size"] == 300


def test_spec_builds():
    tb = pytest.importorskip("seamm_exec.timing_benchmark")
    if not hasattr(tb, "declarations"):
        pytest.skip("seamm_exec without benchmark discovery")
    assert tb.declarations(refresh=True).get("mopac") is mopac_step.TIMING_BENCHMARK
    text = tb.build_spec(("mopac",), "quick")
    assert 'hamiltonian: "PM7"' in text and 'hamiltonian: "PM6-ORG"' in text
    assert 'MOZYME: "never"' in text and "C" * 1000 not in text
