# -*- coding: utf-8 -*-

"""The rules for when the parameters apply, as the flowchart builder uses them (the
dialogs use the same rules; see test_gui.py)."""

import pytest
import seamm
from seamm.builder import FlowchartBuildError, FlowchartBuilder, set_parameters

import mopac_step

CIS = "CIS: CI with singles"


@pytest.fixture(scope="module")
def mopac():
    """A MOPAC step to add sub-steps to."""
    flowchart = seamm.Flowchart(namespace="org.molssi.seamm", directory=".")
    node = flowchart.create_node("MOPAC")
    flowchart.add_node(node)
    return node


def make(mopac, substep):
    subflowchart = mopac.subflowchart
    node = subflowchart.create_node(substep)
    subflowchart.add_node(node)
    return node


def test_energy_applies():
    P = mopac_step.EnergyParameters()
    assert P.applies("uhf")
    assert P.applies("MOZYME")
    assert not P.applies("ci root")
    assert not P.applies("eps")
    assert not P.applies("relative")

    values = {**P.current_values(), "calculation": CIS, "COSMO": "yes"}
    assert not P.applies("uhf", values)
    assert P.applies("ci root", values)
    assert P.applies("eps", values)
    # nMOZYME depends on MOZYME, which does not apply for CI
    assert not P.applies("nMOZYME", values)

    values = {**P.current_values(), "MOZYME": "never", "convergence": "absolute"}
    assert not P.applies("nMOZYME", values)
    assert not P.applies("MOZYME follow-up", values)
    assert P.applies("absolute", values)
    assert not P.applies("relative", values)

    # A variable counts as met, since its value is known only at run time
    values = {**P.current_values(), "calculation": "$calc", "COSMO": "$cosmo"}
    assert P.applies("uhf", values)
    assert P.applies("ci root", values)
    assert P.applies("disex", values)


def test_optimization_applies():
    P = mopac_step.OptimizationParameters()
    assert not P.applies("gnorm")
    assert not P.applies("recalc")
    assert P.applies("pressure")

    values = {
        **P.current_values(),
        "convergence": "relative",
        "method": "TS -- transition state with EF method",
        "LatticeOpt": "No",
    }
    assert P.applies("gnorm", values)
    assert P.applies("recalc", values)
    assert P.applies("dmax", values)
    assert not P.applies("pressure", values)
    assert not P.applies("couple", values)


def test_refused_with_reason(mopac):
    node = make(mopac, "Energy")
    with pytest.raises(FlowchartBuildError) as e:
        set_parameters(node, calculation=CIS, uhf="yes")
    text = str(e.value)
    assert "'uhf' has no effect" in text
    assert "it applies when 'calculation' is 'HF: Hartree-Fock'" in text
    # the step is restored when the setting is refused
    assert node.parameters["calculation"].value == "HF: Hartree-Fock"


def test_refused_chained_reason(mopac):
    node = make(mopac, "Energy")
    with pytest.raises(FlowchartBuildError) as e:
        set_parameters(node, calculation=CIS, nMOZYME=100)
    text = str(e.value)
    assert "'nMOZYME' has no effect" in text
    assert "it needs 'MOZYME', which does not apply" in text


def test_accepted(mopac):
    node = make(mopac, "Energy")
    set_parameters(node, COSMO=True, eps=10.0, convergence="relative", relative=0.01)
    P = node.parameters
    assert P["COSMO"].value == "yes"
    assert float(P["eps"].value) == 10.0
    assert float(P["relative"].value) == 0.01
    # With a variable, the dependent settings are accepted
    set_parameters(node, calculation="$calc", ci_root=2, uhf="yes")


def test_optimization_refused(mopac):
    node = make(mopac, "Optimization")
    with pytest.raises(FlowchartBuildError, match="'gnorm' has no effect"):
        set_parameters(node, gnorm=0.1)
    set_parameters(node, convergence="absolute", gnorm=0.1)

    with pytest.raises(FlowchartBuildError) as e:
        set_parameters(
            node, method="BFGS -- Broyden-Fletcher-Goldfarb-Shanno algorithm", dmax=0.1
        )
    assert "'dmax' has no effect" in str(e.value)
    assert "TS -- transition state with EF method" in str(e.value)
    set_parameters(node, method="EF -- eigenvector following", dmax=0.1, recalc=5)

    with pytest.raises(FlowchartBuildError, match="'pressure' has no effect"):
        set_parameters(node, LatticeOpt=False, pressure=1.0)


def test_builder():
    fb = FlowchartBuilder(title="MOPAC rules")
    mopac = fb.add("MOPAC")
    mopac.add("Energy", COSMO="yes", eps=4.0)
    with pytest.raises(FlowchartBuildError, match="'eps' has no effect"):
        mopac.add("Energy", eps=4.0)


def test_forceconstants_refuses_what_it_does_not_use(mopac):
    """Force constants give the displaced structures themselves and do no MOZYME
    follow-up calculation (MOPAC's FORCE works with MOZYME itself)."""
    node = make(mopac, "Forceconstants")
    for key, value in (
        ("structure", "current"),
        ("MOZYME follow-up", "none"),
    ):
        with pytest.raises(FlowchartBuildError, match="does not use it"):
            set_parameters(node, {key: value})
    set_parameters(node, {"MOZYME": "always"})


@pytest.mark.parametrize(
    "first, structure, expected",
    [
        (True, "default", "initial"),
        (True, "current", "initial"),
        (False, "default", "current"),
        (False, "current", "current"),
        # Was an UnboundLocalError: no structure was chosen
        (False, "initial", "initial"),
    ],
)
def test_starting_structure(first, structure, expected):
    """The previous sub-step's structure (OLDGEO) only after the first sub-step."""
    from mopac_step.energy import starting_structure

    assert starting_structure(structure, first) == expected


def test_no_mozyme_follow_up_for_forceconstants(mopac):
    """Force constants do no follow-up, so neither expect nor describe one."""
    P = {"MOZYME follow-up": "recalculate the energy at the end using exact, "}
    energy = make(mopac, "Energy")
    set_parameters(energy, {"MOZYME": "always"})
    assert energy._mozyme_follow_up(P) == P["MOZYME follow-up"]
    forceconstants = make(mopac, "Forceconstants")
    set_parameters(forceconstants, {"MOZYME": "always"})
    assert forceconstants._mozyme_follow_up(P) == "none"


def test_forceconstants_description(mopac):
    """The description used to splice 'c' onto the Energy description's first word,
    giving 'will be che Hartree-Fock calculation'."""
    node = make(mopac, "Forceconstants")
    node._id = ("2", "1")
    text = node.description_text()
    assert "The energy and forces are calculated as follows. The Hartree-Fock" in text
    assert "che " not in text
