#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Guard tests keeping the MDI method sets in lock-step across two files.

The set of MOPAC semiempirical methods reachable through the MDI engine is
declared in two places that must agree:

* ``mopac_step/mopac_step.py``      -- ``MOPACStep._MDI_CAPABLE_METHODS``
* ``mopac_step/data/mopac_mdi.py``  -- the argparse ``--method`` ``choices``

If they drift, ``get_model_chemistry_options(mdi_only=True)`` will advertise a
method the engine refuses (or hide one it accepts). These tests fail loudly
when that happens.

``mopac_mdi.py`` is read as text and parsed with :mod:`ast` rather than
imported, because (a) it lives in ``data/`` and is not an importable module,
and (b) it is written to run under the ``seamm-mopac`` environment, so
importing it here -- in the ``seamm`` test environment -- could fail on
``mopactools`` / ``mdi`` that are not installed on this side.
"""

import ast
import importlib.resources

from mopac_step.mopac_step import MOPACStep


def _engine_method_choices():
    """Return the ``--method`` ``choices`` list from ``data/mopac_mdi.py``.

    Walks the AST for an ``add_argument('--method', ..., choices=[...])``
    call and returns the literal string choices, without importing or
    executing the engine script.
    """
    source = (
        importlib.resources.files("mopac_step") / "data" / "mopac_mdi.py"
    ).read_text()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if not (isinstance(func, ast.Attribute) and func.attr == "add_argument"):
            continue
        if not node.args:
            continue
        first = node.args[0]
        if not (isinstance(first, ast.Constant) and first.value == "--method"):
            continue
        for kw in node.keywords:
            if kw.arg == "choices":
                return [
                    elt.value for elt in kw.value.elts if isinstance(elt, ast.Constant)
                ]
        raise AssertionError(
            "Found the --method argument in data/mopac_mdi.py but it has no "
            "choices=[...] keyword."
        )

    raise AssertionError(
        "Could not find an add_argument('--method', ..., choices=[...]) call "
        "in data/mopac_mdi.py."
    )


def test_mdi_capable_methods_match_engine_choices():
    """``_MDI_CAPABLE_METHODS`` must equal the engine's ``--method`` choices."""
    engine_choices = set(_engine_method_choices())
    advertised = set(MOPACStep._MDI_CAPABLE_METHODS)

    missing_in_engine = advertised - engine_choices
    missing_in_step = engine_choices - advertised

    assert not missing_in_engine, (
        "MOPACStep._MDI_CAPABLE_METHODS advertises methods the engine does "
        f"not accept via --method: {sorted(missing_in_engine)}. Either add "
        "them to mopac_mdi.py's --method choices or remove them from "
        "_MDI_CAPABLE_METHODS."
    )
    assert not missing_in_step, (
        "data/mopac_mdi.py --method accepts choices not advertised in "
        f"MOPACStep._MDI_CAPABLE_METHODS: {sorted(missing_in_step)}. Either "
        "add them to _MDI_CAPABLE_METHODS or remove them from the engine's "
        "--method choices."
    )


def test_periodic_validated_is_subset_of_capable():
    """Every periodic-validated method must also be MDI-capable.

    A method cannot be validated periodic via MDI unless it is reachable via
    MDI in the first place, so ``_MDI_PERIODIC_VALIDATED`` must be a subset of
    ``_MDI_CAPABLE_METHODS``.
    """
    capable = set(MOPACStep._MDI_CAPABLE_METHODS)
    periodic = set(MOPACStep._MDI_PERIODIC_VALIDATED)

    extra = periodic - capable
    assert not extra, (
        "_MDI_PERIODIC_VALIDATED contains methods absent from "
        f"_MDI_CAPABLE_METHODS: {sorted(extra)}"
    )
