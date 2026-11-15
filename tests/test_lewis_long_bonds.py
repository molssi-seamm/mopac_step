# -*- coding: utf-8 -*-

"""Bonds from MOPAC's Lewis structure that are far too long are not used.

MOPAC 23's LEWIS bonds the two oxygens of a nitro group (O...O 2.15 Å) in both
its topography and its Lewis structure, so "use bonds" put an O-O bond into 32
nitro records of a structure set. The data are a real MOPAC 23.2.5 run on
nitromethane (LEWIS LET GEO-OK PM7 AUX).
"""

from pathlib import Path
from unittest.mock import MagicMock

import pytest

pytest.importorskip("mendeleev")

from molsystem import SystemDB  # noqa: E402

import mopac_step  # noqa: E402
import seamm  # noqa: E402
from mopac_step.lewis_structure import LONG_BOND_FACTOR, long_bonds  # noqa: E402

DATA = Path(__file__).resolve().parent / "data" / "lewis_nitro"

SYMBOLS = ["C", "N", "O", "O", "H", "H", "H"]
XYZ = [
    (-1.4947, 0.0, 0.0),
    (0.0, 0.0, 0.0),
    (0.5869, 1.0741, 0.0),
    (0.5869, -1.0741, 0.0),
    (-1.8297, 1.0331, 0.0),
    (-1.8297, -0.5166, 0.8947),
    (-1.8297, -0.5166, -0.8947),
]
# The bonds of nitromethane, 0-based, with bond orders
BONDS = [(0, 1, 1), (1, 2, 2), (1, 3, 1), (0, 4, 1), (0, 5, 1), (0, 6, 1)]


@pytest.fixture
def configuration(tmp_path):
    db = SystemDB(filename=f"file:{tmp_path / 'seamm.db'}")
    system = db.create_system(name="nitromethane")
    configuration = system.create_configuration(name="initial")
    x, y, z = zip(*XYZ)
    ids = configuration.atoms.append(x=x, y=y, z=z, symbol=SYMBOLS)
    i, j, order = zip(*BONDS)
    configuration.bonds.append(
        i=[ids[k] for k in i], j=[ids[k] for k in j], bondorder=list(order)
    )
    return configuration


def test_normal_bonds_are_not_long(configuration):
    assert long_bonds(configuration, [(i, j) for i, j, _ in BONDS]) == []


def test_the_nitro_oxygens_are_too_far_apart(configuration):
    pairs = [(i, j) for i, j, _ in BONDS] + [(2, 3)]
    ((i, j, r, r0),) = long_bonds(configuration, pairs)
    assert (i, j) == (2, 3)
    assert r == pytest.approx(2.1482, abs=1e-3)
    assert r > LONG_BOND_FACTOR * r0


def _analyze(configuration, tmp_path, monkeypatch, use_bonds):
    for name in ("mopac.out", "mopac.aux"):
        (tmp_path / name).write_text((DATA / name).read_text())
    node = mopac_step.LewisStructure()
    node.parameters["use bonds"].value = use_bonds
    node.references = MagicMock()
    monkeypatch.setattr(seamm, "flowchart_variables", seamm.Variables())
    monkeypatch.setattr(
        type(node), "directory", property(lambda self: str(tmp_path)), raising=False
    )
    monkeypatch.setattr(
        node, "get_system_configuration", lambda *a, **k: (None, configuration)
    )
    monkeypatch.setattr(node, "store_results", lambda *a, **k: None)
    printed = []
    monkeypatch.setattr(
        mopac_step.lewis_structure.printer, "normal", lambda text: printed.append(text)
    )
    node.analyze()
    return "\n".join(printed)


def _bonds(configuration):
    ids = configuration.atoms.ids
    index = {atom_id: k for k, atom_id in enumerate(ids)}
    return sorted(
        (index[i], index[j], order)
        for i, j, order in zip(
            configuration.bonds.get_column_data("i"),
            configuration.bonds.get_column_data("j"),
            configuration.bonds.get_column_data("bondorder"),
        )
    )


def test_use_bonds_keeps_the_configuration_bonds(configuration, tmp_path, monkeypatch):
    before = _bonds(configuration)
    text = _analyze(configuration, tmp_path, monkeypatch, "yes")
    assert _bonds(configuration) == before
    assert "bonds in the configuration were not changed" in text
    assert "O3-O4: 2.15 Å" in text


def test_without_use_bonds_nothing_changes(configuration, tmp_path, monkeypatch):
    before = _bonds(configuration)
    text = _analyze(configuration, tmp_path, monkeypatch, "no")
    assert _bonds(configuration) == before
    assert "Warning" not in text
