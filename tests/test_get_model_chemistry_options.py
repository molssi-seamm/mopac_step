# -*- coding: utf-8 -*-
"""Tests for MOPACStep.get_model_chemistry_options().

These exercise the metadata-driven model-chemistry protocol described in
docs/developer_guide/campaigns/2026-06-22/PLAN_model_chemistry_step.rst,
specifically the MOPAC implementation. See also
NOTES_mopac_model_chemistry_metadata.rst for the metadata corrections
these tests are written against (real element coverage extracted from
MOPAC's own parameter source, the Sparkle/lanthanide distinction, and
the open question about whether SPARKLES is reachable via the MDI path
at all).
"""

import pytest  # noqa: F401

import mopac_step

# Mirrors MOPACStep._MDI_CAPABLE_METHODS -- mopactools.api.MopacSystem's
# model_dict scope, independently restated here so a future accidental
# edit to one doesn't silently agree with itself.
EXPECTED_MDI_CAPABLE = {"PM7", "PM6-D3H4", "PM6-ORG", "PM6", "AM1", "RM1"}

# Mirrors MOPACStep._MDI_PERIODIC_VALIDATED -- methods actually run
# periodic via MDI and confirmed working this week, per
# NOTES_qm_mdi_engines_validation.rst.
EXPECTED_PERIODIC_VALIDATED = {"PM7", "PM6-ORG", "PM6"}

# Methods with a documented sparkle_elements entry as of 2026-06-22+.
# All ten PM7/PM6-family parameterizations share the same core NDDO
# Hamiltonian, so all share the same elements/sparkle_elements coverage
# -- per Paul, the dispersion/H-bond/halogen-bond correction terms on
# the six PM6 variants are either general (D3 dispersion) or simply
# inactive (contribute zero) for elements outside their specific
# domain, so they don't narrow what the underlying calculation can
# actually run on. This applies regardless of each variant's own
# periodic_mdi status (e.g. PM6-D3H4/D3H4X are still excluded from
# periodic+MDI use, but that's a periodicity question, independent of
# which elements/lanthanide-Sparkle treatment applies).
#
# RM1 deliberately excluded despite also covering lanthanides: its
# parameters are real NDDO data for the full La-Lu range, not
# Sparkle-only like PM6/PM7's Ce-Yb gap -- a materially different
# situation despite both involving the same block of elements.
EXPECTED_HAS_SPARKLE_ELEMENTS = {
    "PM7",
    "PM7-TS",
    "PM6",
    "PM6-ORG",
    "PM6-D3",
    "PM6-DH+",
    "PM6-DH2",
    "PM6-DH2X",
    "PM6-D3H4",
    "PM6-D3H4X",
}


def _all_metadata_names():
    """Every parameterization name present in the raw metadata, computed
    independently of the classmethod under test."""
    names = set()
    for class_data in mopac_step.metadata["computational models"].values():
        for family_data in class_data["models"].values():
            names |= set(family_data["parameterizations"].keys())
    return names


def test_no_filters_returns_everything_in_metadata():
    """With no filters, every parameterization in metadata["computational
    models"] should appear, and nothing else."""
    options = mopac_step.MOPACStep.get_model_chemistry_options()
    assert set(options.keys()) == _all_metadata_names()
    # Sanity check this is non-trivial, not two empty sets agreeing.
    assert len(options) >= 15


def test_mdi_only_returns_exactly_the_mopactools_scope():
    """mdi_only=True should return exactly the methods mopactools'
    model_dict supports -- no more, no less -- each with launch info
    filled in."""
    options = mopac_step.MOPACStep.get_model_chemistry_options(mdi_only=True)
    assert set(options.keys()) == EXPECTED_MDI_CAPABLE
    for name, info in options.items():
        assert info["mdi_capable"] is True
        assert info["mdi_method_arg"] == name


def test_periodic_only_returns_exactly_the_validated_three():
    """periodic_only=True is deliberately conservative: only methods
    actually run periodic via MDI and confirmed working, never just
    because some metadata flag suggests a method should work."""
    options = mopac_step.MOPACStep.get_model_chemistry_options(periodic_only=True)
    assert set(options.keys()) == EXPECTED_PERIODIC_VALIDATED
    for info in options.values():
        assert info["periodic_mdi"] is True


def test_periodic_and_mdi_together_is_consistent():
    """Combining both filters should not add anything beyond the
    periodic-validated set, since all three validated methods are also
    MDI-capable by construction."""
    options = mopac_step.MOPACStep.get_model_chemistry_options(
        periodic_only=True, mdi_only=True
    )
    assert set(options.keys()) == EXPECTED_PERIODIC_VALIDATED


def test_pm6_d3h4_is_mdi_capable_but_not_periodic_validated():
    """PM6-D3H4 is the known trap this protocol exists to catch: it IS
    in mopactools' model_dict (mdi_capable=True), but MOPAC's own
    documentation says D3H4 does not work under periodic boundary
    conditions, so it must never appear when periodic_only is True."""
    all_options = mopac_step.MOPACStep.get_model_chemistry_options()
    assert all_options["PM6-D3H4"]["mdi_capable"] is True
    assert all_options["PM6-D3H4"]["periodic_mdi"] is False

    periodic_options = mopac_step.MOPACStep.get_model_chemistry_options(
        periodic_only=True
    )
    assert "PM6-D3H4" not in periodic_options


def test_non_mdi_method_has_no_launch_info():
    """A method outside mopactools' scope (e.g. PM6-D3, a correction
    variant not in the six-method MDI list) should report
    mdi_capable=False and no script/arg to launch with."""
    options = mopac_step.MOPACStep.get_model_chemistry_options()
    info = options["PM6-D3"]
    assert info["mdi_capable"] is False
    assert info["mdi_method_arg"] is None


def test_am1_and_rm1_present_as_mdi_capable():
    """AM1 and RM1 were added to metadata.py after the original MDI
    scope was first established from mopactools alone -- confirm they
    now appear correctly now that real metadata entries exist for them."""
    options = mopac_step.MOPACStep.get_model_chemistry_options(mdi_only=True)
    assert "AM1" in options
    assert "RM1" in options
    assert options["AM1"]["type"] == "SQM"
    assert options["RM1"]["type"] == "SQM"


def test_model_chemistry_string_format():
    """The citable model-chemistry string should always be
    "MOPAC:SQM@<method name>", per the established nomenclature."""
    options = mopac_step.MOPACStep.get_model_chemistry_options()
    for name, info in options.items():
        assert info["model_chemistry"] == f"MOPAC:SQM@{name}"


def test_sparkle_elements_present_only_where_documented():
    """All ten PM7/PM6-family parameterizations document a
    sparkle_elements field (same core NDDO Hamiltonian, same lanthanide
    treatment across all variants, including the six dispersion/H-bond/
    halogen-bond correction methods -- those correction terms are either
    general or simply inactive for elements outside their own domain,
    so they don't narrow elemental coverage). RM1 also covers
    lanthanides but via genuine NDDO parameters for the full La-Lu
    range rather than the Sparkle-only Ce-Yb gap PM6/PM7 have, so it
    correctly has no sparkle_elements entry. AM1/PM3/MNDO/MNDOD don't
    reach the lanthanide block at all, so no Sparkle question arises
    for them either.

    This is checked against the classmethod's own output, not by
    re-walking raw metadata -- the point is to catch exactly the kind
    of "added to metadata but never wired into the classmethod" gap
    that this field hit on its first draft.
    """
    options = mopac_step.MOPACStep.get_model_chemistry_options()
    for name, info in options.items():
        if name in EXPECTED_HAS_SPARKLE_ELEMENTS:
            assert (
                info["sparkle_elements"] is not None
            ), f"{name} should have a sparkle_elements value"
        else:
            assert info["sparkle_elements"] is None, (
                f"{name} unexpectedly has a sparkle_elements value -- "
                "update EXPECTED_HAS_SPARKLE_ELEMENTS if this is "
                "intentional, e.g. after checking RM1's lanthanide "
                "treatment more carefully"
            )


def test_elements_field_present_for_every_option():
    """Every option should at least have a (possibly empty) elements
    string -- catches a future entry added to metadata.py without an
    "elements" key at all, which param.get("elements", "") would
    otherwise silently paper over."""
    options = mopac_step.MOPACStep.get_model_chemistry_options()
    for name, info in options.items():
        assert isinstance(info["elements"], str)
        assert info["elements"] != "", (
            f"{name} has an empty elements string -- likely a missing "
            "metadata entry rather than a genuine empty range"
        )
