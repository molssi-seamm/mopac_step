# -*- coding: utf-8 -*-

"""Caculate the forceconstant matrix using MOPAC"""

import logging
from math import sqrt
from pathlib import Path
import textwrap

import mopac_step
import seamm
import seamm_util.printing as printing
from seamm_util import units_class, Q_
from seamm_util.printing import FormattedText as __

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("mopac")


class Forceconstants(mopac_step.Energy):
    def __init__(self, flowchart=None, title="Force Constants", extension=None):
        """Initialize the node"""

        logger.debug("Creating Forceconstants {}".format(self))

        super().__init__(flowchart=flowchart, title=title, extension=extension)

        self._calculation = "vibrations"
        self._model = None
        self._metadata = mopac_step.metadata
        self.parameters = mopac_step.ForceconstantsParameters()

        self.description = "Force Constants (Hessian) calculation"

    def description_text(self, P=None):
        """Prepare information about what this node will do"""

        if not P:
            P = self.parameters.values_to_dict()

        # The energy part of the description
        tmp = super().description_text(P)
        energy_description = textwrap.dedent("\n".join(tmp.splitlines()[1:]))

        # Put in the description of the energy calculation
        text = "The energy and forces will be c" + energy_description[1:]
        text += "\n\n"

        if P["what"] == "full Hessian":
            text += "Creating the full Hessian"
        elif P["what"] == "atom part only":
            text += "Creating the atom part of the Hessian"
        else:
            text += "Creating the cell part of the Hessian"
        text += " (force constant matrix) for {hamiltonian}"

        if P["what"] == "cell part only":
            if P["two-sided_cell"]:
                text += " using two-sided differences of the strain"
            else:
                text += " using one-sided differences of the strain"
        else:
            if P["two-sided_atoms"]:
                if P["two-sided_cell"]:
                    if P["what"] == "full Hessian":
                        text += (
                            " using two-sided differences for both the atoms and strain"
                        )
                    else:
                        text += " using two-sided differences for the atoms"
                else:
                    if P["what"] == "full Hessian":
                        text += (
                            " using two-sided differences for the atoms and one-sided "
                            " for the strain"
                        )
                    else:
                        text += " using two-sided differences for the atoms"
            else:
                if P["two-sided_cell"]:
                    if P["what"] == "full Hessian":
                        text += (
                            " using one-sided differences for the atoms and two-sided "
                            "for the strain"
                        )
                    else:
                        text += " using one-sided differences for the atoms"
                else:
                    if P["what"] == "full Hessian":
                        text += (
                            " using on-sided differences for both the atoms and strain"
                        )
                    else:
                        text += " using one-sided differences for the atoms"
        text += " with a step size of {stepsize}."
        if P["what"] == "cell part only":
            text += (
                " The strain-strain part of the Hessian will be output in {cell_units}."
            )
        elif P["what"] == "full Hessian":
            text += (
                " The atom-atom and atom-strain part of the Hessian will be output in "
                "{atom_units}, while the the strain-strain part will be output in "
                "{cell_units}."
            )
        else:
            text += " The atom-atom part of the Hessian will be output in {atom_units}."

        return self.header + "\n" + __(text, **P, indent=4 * " ").__str__()

    def get_input(self):
        """Get the input for an optimization MOPAC"""

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Have to fix formatting for printing...
        PP = dict(P)
        for key in PP:
            if isinstance(PP[key], units_class):
                PP[key] = "{:~P}".format(PP[key])

        # Save the description for later printing
        self.description = []
        self.description.append(__(self.description_text(PP), **PP, indent=self.indent))

        _, configuration = self.get_system_configuration(None)

        is_periodic = configuration.periodicity != 0

        inputs = []

        # Get the underlying SCF setup
        original = super().get_input()
        # Have to think about MOZYME
        if len(original) > 1:
            raise NotImplementedError("MOZYME not yet handles in forceconstants")

        keywords, _, _ = original[0]
        if "OLDGEO" in keywords:
            keywords.remove("OLDGEO")
        if "1SCF" not in keywords:
            keywords.append("1SCF")

        # Get the cell vectors
        if is_periodic and P["what"] != "atom part only":
            cell_vectors = configuration.cell.vectors(as_array=False)

            if P["two-sided_cell"]:
                # Loop over the strains creating inputs
                for direction, name in zip(
                    range(6), ("xx", "yy", "zz", "yz", "xz", "xy")
                ):
                    vector = 6 * [0.0]
                    vector[direction] = P["stepsize"]
                    configuration.strain(vector)
                    structure = self.parent.mopac_structure()
                    inputs.append(
                        [[*keywords], structure, f"Strained +{P['stepsize']} in {name}"]
                    )
                    # Set the cell back to the original cell.
                    configuration.cell.from_vectors(cell_vectors)

                    # Minus displacement
                    vector = 6 * [0.0]
                    vector[direction] = -P["stepsize"]
                    configuration.strain(vector)
                    structure = self.parent.mopac_structure()
                    inputs.append(
                        [[*keywords], structure, f"Strained -{P['stepsize']} in {name}"]
                    )
                    # Set the cell back to the original cell.
                    configuration.cell.from_vectors(cell_vectors)
            else:
                # Original structure
                inputs.append([[*keywords], None, None])

                # Loop over the strains creating inputs
                for direction, name in zip(
                    range(6), ("xx", "yy", "zz", "yz", "xz", "xy")
                ):
                    vector = 6 * [0.0]
                    vector[direction] = P["stepsize"]
                    configuration.strain(vector)
                    structure = self.parent.mopac_structure()
                    inputs.append(
                        [[*keywords], structure, f"Strained {P['stepsize']} in {name}"]
                    )
                    # Set the cell back to the original cell.
                    configuration.cell.from_vectors(cell_vectors)

        # Add the force calculation
        if P["what"] != "cell part only":
            keywords.remove("1SCF")
            keywords.append("FORCE")
            if "LET" not in keywords:
                keywords.append("LET")
            if "NOREOR" not in keywords:
                keywords.append("NOREOR")
            if P["two-sided_atoms"]:
                if "PRECISE" not in keywords:
                    keywords.append("PRECISE")
            else:
                if "PRECISE" in keywords:
                    keywords.remove("PRECISE")

            structure = self.parent.mopac_structure()
            inputs.append([[*keywords], structure, "Atomic Hessian calculation"])

        return inputs

    def analyze(self, indent="", data_sections=[], out_sections=[], table=None):
        """Parse the output and generating the text output and store the
        data in variables for other stages to access

        There are 8 calculations:
            SPE at the initial geometry
            6 strains
            The forceconstant calculation

        Since the forceconstant matrix is symmetric (we hope!) we will work with the
        lower triangle as a lineary array.
        """
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        _, configuration = self.get_system_configuration(None)
        is_periodic = configuration.periodicity != 0
        n_atoms = configuration.n_atoms
        last = 3 * n_atoms
        result = []

        if P["what"] != "cell part only":
            data = data_sections[-1]
            # It is mass weighted so we need to remove the weighting
            if "ISOTOPIC_MASSES" not in data:
                raise RuntimeError("Found no atomic masses")
            tmp = data["ISOTOPIC_MASSES"]
            n_atoms = len(tmp)

            # Replicate for x, y, z
            mass = []
            for v in tmp:
                for _ in range(3):
                    mass.append(v)

            # Get the atom part of the force constant matrix.
            if "HESSIAN_MATRIX" not in data:
                raise RuntimeError("Found no atomic Hessian matrix!")
            hessian = data["HESSIAN_MATRIX"]

            ij = 0
            factor = Q_(1.0, "mdyne/Å").m_as(P["atom_units"])
            for i in range(last):
                for j in range(i + 1):
                    result.append(factor * hessian[ij] * sqrt(mass[i] * mass[j]))
                    ij += 1

        if is_periodic and P["what"] != "atom part only":
            step = P["stepsize"]
            if P["two-sided_cell"]:
                # Loop through the strained calculations, using finite-differences
                for strain in range(6):
                    data = data_sections[2 * strain]
                    if "GRADIENTS" not in data:
                        raise RuntimeError(
                            f"Found no gradients for strained structure {strain}."
                        )
                    forces = data["GRADIENTS"]
                    if "TRANS_VECTS" not in data:
                        raise RuntimeError(
                            "Found no translation vectors for strained structure "
                            f"{strain}."
                        )

                    f2 = forces[0:last]
                    x0, y0, z0, x1, y1, z1, x2, y2, z2 = data["TRANS_VECTS"]
                    fx0, fy0, fz0, fx1, fy1, fz1, fx2, fy2, fz2 = forces[last:]
                    V = abs(
                        x2 * (y0 * z1 - z0 * y1)
                        + y2 * (z0 * x1 - x0 * z1)
                        + z2 * (x0 * y1 - y0 * x1)
                    )

                    factor = Q_(1.0 / V, "kcal/mol/Å^3").m_as(P["cell_units"])

                    s2 = []
                    s2.append((x0 * fx0 + y0 * fy0 + z0 * fz0) * factor)
                    s2.append((x1 * fx1 + y1 * fy1 + z1 * fz1) * factor)
                    s2.append((x2 * fx2 + y2 * fy2 + z2 * fz2) * factor)
                    syz = x1 * fx2 + y1 * fy2 + z1 * fz2
                    szy = x2 * fx1 + y2 * fy1 + z2 * fz1
                    s2.append(((syz + szy) / 2) * factor)
                    sxz = x0 * fx2 + y0 * fy2 + z0 * fz2
                    szx = x2 * fx0 + y2 * fy0 + z2 * fz0
                    s2.append(((sxz + szx) / 2) * factor)
                    sxy = x0 * fx1 + y0 * fy1 + z0 * fz1
                    syx = x1 * fx0 + y1 * fy0 + z1 * fz0
                    s2.append(((sxy + syx) / 2) * factor)

                    data = data_sections[2 * strain + 1]
                    if "GRADIENTS" not in data:
                        raise RuntimeError(
                            f"Found no gradients for strained structure -{strain}."
                        )
                    forces = data["GRADIENTS"]
                    if "TRANS_VECTS" not in data:
                        raise RuntimeError(
                            "Found no translation vectors for strained structure "
                            f"-{strain}."
                        )

                    f1 = forces[0:last]
                    x0, y0, z0, x1, y1, z1, x2, y2, z2 = data["TRANS_VECTS"]
                    fx0, fy0, fz0, fx1, fy1, fz1, fx2, fy2, fz2 = forces[last:]
                    V = abs(
                        x2 * (y0 * z1 - z0 * y1)
                        + y2 * (z0 * x1 - x0 * z1)
                        + z2 * (x0 * y1 - y0 * x1)
                    )

                    factor = Q_(1.0 / V, "kcal/mol/Å^3").m_as(P["cell_units"])

                    s1 = []
                    s1.append((x0 * fx0 + y0 * fy0 + z0 * fz0) * factor)
                    s1.append((x1 * fx1 + y1 * fy1 + z1 * fz1) * factor)
                    s1.append((x2 * fx2 + y2 * fy2 + z2 * fz2) * factor)
                    syz = x1 * fx2 + y1 * fy2 + z1 * fz2
                    szy = x2 * fx1 + y2 * fy1 + z2 * fz1
                    s1.append(((syz + szy) / 2) * factor)
                    sxz = x0 * fx2 + y0 * fy2 + z0 * fz2
                    szx = x2 * fx0 + y2 * fy0 + z2 * fz0
                    s1.append(((sxz + szx) / 2) * factor)
                    sxy = x0 * fx1 + y0 * fy1 + z0 * fz1
                    syx = x1 * fx0 + y1 * fy0 + z1 * fz0
                    s1.append(((sxy + syx) / 2) * factor)

                    # atoms
                    if P["what"] == "full Hessian":
                        factor = Q_(1.0, "kcal/mol/Å^2").m_as(P["atom_units"])
                        for v1, v2 in zip(f1, f2):
                            result.append((v2 - v1) / (2 * step) * factor)

                    # strains
                    for i in range(strain + 1):
                        result.append((s2[i] - s1[i]) / (2 * step))
            else:
                # Get the forces for the unperturbed system
                data = data_sections[0]

                if "GRADIENTS" not in data:
                    raise RuntimeError("Found no gradients for unstrained structure.")
                forces = data["GRADIENTS"]
                if "TRANS_VECTS" not in data:
                    raise RuntimeError(
                        "Found no translation vectors for unstrained  structure."
                    )

                f0 = forces[0:last]
                x0, y0, z0, x1, y1, z1, x2, y2, z2 = data["TRANS_VECTS"]
                fx0, fy0, fz0, fx1, fy1, fz1, fx2, fy2, fz2 = forces[last:]
                V = abs(
                    x2 * (y0 * z1 - z0 * y1)
                    + y2 * (z0 * x1 - x0 * z1)
                    + z2 * (x0 * y1 - y0 * x1)
                )

                factor = Q_(1.0 / V, "kcal/mol/Å^3").m_as(P["cell_units"])

                s0 = []
                s0.append((x0 * fx0 + y0 * fy0 + z0 * fz0) * factor)
                s0.append((x1 * fx1 + y1 * fy1 + z1 * fz1) * factor)
                s0.append((x2 * fx2 + y2 * fy2 + z2 * fz2) * factor)
                syz = x1 * fx2 + y1 * fy2 + z1 * fz2
                szy = x2 * fx1 + y2 * fy1 + z2 * fz1
                s0.append(((syz + szy) / 2) * factor)
                sxz = x0 * fx2 + y0 * fy2 + z0 * fz2
                szx = x2 * fx0 + y2 * fy0 + z2 * fz0
                s0.append(((sxz + szx) / 2) * factor)
                sxy = x0 * fx1 + y0 * fy1 + z0 * fz1
                syx = x1 * fx0 + y1 * fy0 + z1 * fz0
                s0.append(((sxy + syx) / 2) * factor)

                # Loop through the strained calculations, using finite-differences
                for strain in range(6):
                    data = data_sections[strain + 1]

                    if "GRADIENTS" not in data:
                        raise RuntimeError(
                            f"Found no gradients for strained structure {strain}."
                        )
                    forces = data["GRADIENTS"]
                    if "TRANS_VECTS" not in data:
                        raise RuntimeError(
                            "Found no translation vectors for strained structure "
                            f"{strain}."
                        )

                    f = forces[0:last]
                    x0, y0, z0, x1, y1, z1, x2, y2, z2 = data["TRANS_VECTS"]
                    fx0, fy0, fz0, fx1, fy1, fz1, fx2, fy2, fz2 = forces[last:]
                    V = abs(
                        x2 * (y0 * z1 - z0 * y1)
                        + y2 * (z0 * x1 - x0 * z1)
                        + z2 * (x0 * y1 - y0 * x1)
                    )

                    factor = Q_(1.0 / V, "kcal/mol/Å^3").m_as(P["cell_units"])

                    s = []
                    s.append((x0 * fx0 + y0 * fy0 + z0 * fz0) * factor)
                    s.append((x1 * fx1 + y1 * fy1 + z1 * fz1) * factor)
                    s.append((x2 * fx2 + y2 * fy2 + z2 * fz2) * factor)
                    syz = x1 * fx2 + y1 * fy2 + z1 * fz2
                    szy = x2 * fx1 + y2 * fy1 + z2 * fz1
                    s.append(((syz + szy) / 2) * factor)
                    sxz = x0 * fx2 + y0 * fy2 + z0 * fz2
                    szx = x2 * fx0 + y2 * fy0 + z2 * fz0
                    s.append(((sxz + szx) / 2) * factor)
                    sxy = x0 * fx1 + y0 * fy1 + z0 * fz1
                    syx = x1 * fx0 + y1 * fy0 + z1 * fz0
                    s.append(((sxy + syx) / 2) * factor)

                    # atoms
                    if P["what"] == "full Hessian":
                        factor = Q_(1.0, "kcal/mol/Å^2").m_as(P["atom_units"])
                        for v, v0 in zip(f, f0):
                            result.append(((v - v0) / step) * factor)

                    # strains
                    for i in range(strain + 1):
                        result.append((s[i] - s0[i]) / step)

        directory = Path(self.directory)
        directory.mkdir(parents=True, exist_ok=True)
        if is_periodic and P["what"] == "cell part only":
            n = 6
        elif not is_periodic or P["what"] == "atom part only":
            n = last
        else:
            n = last + 6

        with open(directory / ".." / "hessian.dat", "w") as fd:
            # Write the header
            fd.write("!molssi hessian 1.0\n")
            if is_periodic and P["what"] == "cell part only":
                fd.write("@cell_dof 6\n")
                fd.write(f"@cell_units {P['cell_units']}\n")
            elif not is_periodic or P["what"] == "atom part only":
                fd.write(f"@atom_dof {last}\n")
                fd.write(f"@atom_units {P['atom_units']}\n")
            else:
                fd.write(f"@atom_dof {last}\n")
                fd.write(f"@atom_units {P['atom_units']}\n")
                fd.write("@cell_dof 6\n")
                fd.write(f"@cell_units {P['cell_units']}\n")
            fd.write(f"@total_dof {n}\n")

            ij = 0
            for i in range(n):
                for j in range(i + 1):
                    fd.write(f"{result[ij]:12.6f} ")
                    ij += 1
                fd.write("\n")

        # Let the energy module do its thing
        super().analyze(
            indent=indent,
            data_sections=data_sections,
            out_sections=out_sections,
            table=table,
        )
