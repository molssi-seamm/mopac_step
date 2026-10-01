# -*- coding: utf-8 -*-

"""Smoke test of the Tk dialogs: create them and re-lay them out for every choice
that drives the layout, checking that the controls shown are those that the
parameters' rules say apply. Skipped when no display is available."""

import itertools

import pytest

SUBSTEPS = ("Energy", "Optimization", "IR Spectrum", "Thermodynamics", "Forceconstants")

# Parameters that have a control in the dialog which is never laid out: the
# structure to use, and the handling of subsequent structures (MOPAC makes only one).
NOT_LAID_OUT = {"structure", "subsequent structure handling"}


@pytest.fixture()
def root():
    import tkinter as tk

    try:
        root = tk.Tk()
    except tk.TclError:
        pytest.skip("no display available for Tk")
    root.withdraw()
    import Pmw

    Pmw.initialise(root)
    yield root
    root.destroy()


def make(root, substep):
    import seamm

    flowchart = seamm.Flowchart(namespace="org.molssi.seamm", directory=".")
    mopac = flowchart.create_node("MOPAC")
    flowchart.add_node(mopac)
    subflowchart = mopac.subflowchart
    tk_subflowchart = seamm.TkFlowchart(
        master=root, flowchart=subflowchart, namespace="org.molssi.seamm.mopac.tk"
    )
    node = subflowchart.create_node(substep)
    subflowchart.add_node(node)
    plugin = tk_subflowchart.plugin_manager.get(substep)
    tk_node = plugin.create_tk_node(
        tk_flowchart=tk_subflowchart,
        node=node,
        canvas=tk_subflowchart.canvas,
        x=100,
        y=100,
    )
    tk_node.create_dialog()
    return tk_node


def check(tk_node):
    """The shown controls are exactly those that apply."""
    tk_node.reset_dialog()
    P = tk_node.node.parameters
    values = tk_node._widget_values()
    for key in P:
        if key == "results" or key not in tk_node or key in NOT_LAID_OUT:
            continue
        shown = tk_node[key].grid_info() != {}
        if shown:
            assert P.applies(key, values), f"{key} is shown but does not apply"
        else:
            assert not P.applies(key, values), f"{key} applies but is not shown"
    return values


def restore(tk_node, keys):
    P = tk_node.node.parameters
    for key in keys:
        tk_node[key].set(P[key].default)


@pytest.mark.parametrize("substep", SUBSTEPS)
def test_energy_layouts_follow_the_rules(root, substep):
    tk_node = make(root, substep)
    P = tk_node.node.parameters
    drivers = {
        "calculation": (*P["calculation"].enumeration, "$calculation"),
        "MOZYME": (*P["MOZYME"].enumeration, "$mozyme"),
        "convergence": (*P["convergence"].enumeration, "$convergence"),
        "COSMO": ("yes", "no", "$cosmo"),
    }
    for combination in itertools.product(*drivers.values()):
        for key, value in zip(drivers, combination):
            tk_node[key].set(value)
        check(tk_node)
    restore(tk_node, drivers)

    # A few cases spelled out
    tk_node["calculation"].set("CIS: CI with singles")
    check(tk_node)
    assert tk_node["uhf"].grid_info() == {}
    assert tk_node["MOZYME"].grid_info() == {}
    assert tk_node["nMOZYME"].grid_info() == {}
    assert tk_node["ci root"].grid_info() != {}

    tk_node["calculation"].set("HF: Hartree-Fock")
    tk_node["MOZYME"].set("never")
    check(tk_node)
    assert tk_node["MOZYME"].grid_info() != {}
    assert tk_node["MOZYME follow-up"].grid_info() == {}

    tk_node["convergence"].set("$convergence")
    check(tk_node)
    assert tk_node["relative"].grid_info() != {}
    assert tk_node["absolute"].grid_info() != {}


def test_optimization_layouts_follow_the_rules(root):
    tk_node = make(root, "Optimization")
    P = tk_node.node.parameters
    drivers = {
        "LatticeOpt": ("Yes", "No", "$lattice"),
        "method": (*P["method"].enumeration, "$method"),
        "convergence": (*P["convergence"].enumeration, "$convergence"),
    }
    for combination in itertools.product(*drivers.values()):
        for key, value in zip(drivers, combination):
            tk_node[key].set(value)
        check(tk_node)
    restore(tk_node, drivers)

    tk_node["method"].set("BFGS -- Broyden-Fletcher-Goldfarb-Shanno algorithm")
    tk_node["LatticeOpt"].set("No")
    check(tk_node)
    for key in ("recalc", "dmax", "gnorm", "pressure", "allow shear", "couple"):
        assert tk_node[key].grid_info() == {}, key

    tk_node["method"].set("TS -- transition state with EF method")
    tk_node["convergence"].set("absolute")
    check(tk_node)
    for key in ("recalc", "dmax", "gnorm"):
        assert tk_node[key].grid_info() != {}, key
