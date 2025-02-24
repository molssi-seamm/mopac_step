# -*- coding: utf-8 -*-

"""Setup and run MOPAC"""

import logging
from pathlib import Path
import textwrap
import traceback

import numpy as np

import mopac_step
from molsystem import RMSD
import seamm
import seamm_util.printing as printing
from seamm_util import units_class
from seamm_util.printing import FormattedText as __

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("mopac")


class Optimization(mopac_step.Energy):
    def __init__(self, flowchart=None, title="Optimization", extension=None):
        """Initialize the node"""

        logger.debug("Creating Optimization {}".format(self))

        super().__init__(flowchart=flowchart, title=title, extension=extension)

        self._calculation = "optimization"
        self._model = None
        self._metadata = mopac_step.metadata
        self.parameters = mopac_step.OptimizationParameters()
        self.description = "A structural optimization"

    def description_text(self, P=None):
        """Prepare information about what this node will do"""

        if not P:
            P = self.parameters.values_to_dict()

        # The energy part of the description
        tmp = super().description_text(P)
        energy_description = textwrap.dedent("\n".join(tmp.splitlines()[1:]))

        # Hamiltonian followed by convergence
        text = "Geometry optimization with the "
        if P["method"] == "default":
            text += "default optimizer (EF for small systems," " L-BFGS for larger)."
        elif P["method"][0:1] == "EF":
            text += "eigenvector following (EF) method."
        elif P["method"][0:3] == "BFGS":
            text += "BFGS method."
        elif P["method"][0:5] == "L-BFGS":
            text += "L-BFGS small memory version of the BFGS method."
        elif P["method"].startswith("TS"):
            text += "EF method for a transition state."
        elif P["method"].startswith("SIGMA"):
            text += "McIver-Komornicki method for transition states."
        elif P["method"].startswith("NLLSQ"):
            text += "Bartel's method of nonlinear least squares of the gradient."
        else:
            text += "optimization method determined at runtime by '{method}'."

        if P["LatticeOpt"]:
            pressure = P["pressure"]
            if isinstance(pressure, units_class):
                pressure = f"{pressure:~P}"
            text += (
                " The cell for periodic systems will also be optimized, with an "
                f"applied pressure of {pressure}."
            )
        else:
            text += " The cell for periodic systems will not be optimized."

        if P["gnorm"] == "default":
            text += " The geometrical convergence is the default of 1.0 kcal/mol/Å."
        elif P["gnorm"][0] == "$":
            text += (
                " The geometrical convergence will be determined "
                "at runtime by '{gnorm}'."
            )
        else:
            text += " The geometrical convergence is {gnorm}."

        # Put in the description of the energy calculation
        text += "\n\n" + energy_description
        text += "\n\n"

        if self.is_expr(P["hamiltonian"]):
            kwargs = {"Hamiltonian": "{{" + P["hamiltonian"] + "}}"}
        else:
            kwargs = {"Hamiltonian": P["hamiltonian"]}
        text += seamm.standard_parameters.structure_handling_description(P, **kwargs)

        return self.header + "\n" + __(text, **P, indent=4 * " ").__str__()

    def get_input(self):
        """Get the input for an optimization MOPAC"""

        references = self.parent.references
        bibliography = self.parent._bibliography

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # Have to fix formatting for printing...
        PP = dict(P)
        for key in PP:
            if isinstance(PP[key], units_class):
                PP[key] = "{:~P}".format(PP[key])

        system, configuration = self.get_system_configuration(None)

        # Let parent know about cell optimization
        self.parent._lattice_opt = P["LatticeOpt"]

        # Get the inputs from the energy class. This also sets the description properly.
        inputs = super().get_input()

        # Remove the 1SCF keyword from the energy setup
        # 'keywords' is a reference, so will change in situ.
        keywords, _, _ = inputs[0]
        if "1SCF" in keywords:
            keywords.remove("1SCF")

        # Pressure
        if configuration.periodicity == 3 and P["LatticeOpt"]:
            pressure = P["pressure"]
            pressure = pressure.to("GPa").magnitude
            keywords.append(f"P={pressure}GPa")

        # and the optimization-specific parts
        method = P["method"]
        if method == "default":
            pass
        elif method[0:2] == "EF":
            keywords.append("EF")
            if P["recalc"] != "never":
                keywords.append(f'RECALC={P["recalc"]}')
            if str(P["dmax"]) != self.parameters["dmax"].default:
                keywords.append("DMAX={}".format(P["dmax"]))
            references.cite(
                raw=bibliography["Baker_1986"],
                alias="Baker_1986",
                module="mopac_step",
                level=1,
                note="Eigenvector-following minimizer.",
            )
        elif method[0:4] == "BFGS":
            keywords.append("BFGS")
            references.cite(
                raw=bibliography["Broyden_1970"],
                alias="Broyden_1970",
                module="mopac_step",
                level=1,
                note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
            )
            references.cite(
                raw=bibliography["Fletcher_1970"],
                alias="Fletcher_1970",
                module="mopac_step",
                level=1,
                note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
            )
            references.cite(
                raw=bibliography["Goldfarb_1970"],
                alias="Goldfarb_1970",
                module="mopac_step",
                level=1,
                note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
            )
            references.cite(
                raw=bibliography["Shanno_1970"],
                alias="Shanno_1970",
                module="mopac_step",
                level=1,
                note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
            )
            references.cite(
                raw=bibliography["Thiel_1988"],
                alias="Thiel_1988",
                module="mopac_step",
                level=1,
                note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
            )
        elif method[0:6] == "L-BFGS":
            keywords.append("LBFGS")
            references.cite(
                raw=bibliography["Nocedal_1980"],
                alias="Nocedal_1980",
                module="mopac_step",
                level=1,
                note="Limited-memory BFGS (L-BFGS) minimizer.",
            )
        elif method[0:2] == "TS":
            keywords.append("TS")
            if P["recalc"] != "never":
                keywords.append(f'RECALC={P["recalc"]}')
            if str(P["dmax"]) != self.parameters["dmax"].default:
                keywords.append("DMAX={}".format(P["dmax"]))
            references.cite(
                raw=bibliography["Baker_1986"],
                alias="Baker_1986",
                module="mopac_step",
                level=1,
                note="Eigenvector-following minimizer for transition states.",
            )
        elif method[0:5] == "SIGMA":
            keywords.append("SIGMA")
            references.cite(
                raw=bibliography["McIver_1971"],
                alias="McIver_1971",
                module="mopac_step",
                level=1,
                note="Gradient-norm minimizer for transition states.",
            )
            references.cite(
                raw=bibliography["McIver_1972"],
                alias="McIver_1972",
                module="mopac_step",
                level=1,
                note="Gradient-norm minimizer for transition states.",
            )
        elif method[0:5] == "NLLSQ":
            keywords.append("NLLSQ")
            references.cite(
                raw=bibliography["Bartels_1972"],
                alias="Bartels_1972",
                module="mopac_step",
                level=1,
                note="NLLSQ gradient-norm minimizer for transition states.",
            )
        else:
            text = "Don't recognize optimization method '{}'".format(P["method"])
            logger.critical(text)
            raise RuntimeError(text)

        if P["cycles"] != "unlimited":
            keywords.append("CYCLES={}".format(P["cycles"]))
        if P["convergence"] not in ("normal", "precise"):
            if P["gnorm"] != self.parameters["gnorm"].default:
                keywords.append("GNORM={}".format(P["gnorm"]))

        return inputs

    def analyze(self, indent="", data_sections=[], out_sections=[], table=None):
        """Parse the output and generating the text output and store the
        data in variables for other stages to access
        """

        # Get the parameters used
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        starting_system, starting_configuration = self.get_system_configuration(None)

        # Get the data.
        data = data_sections[0]

        # If the optimizer used was the default, put in the correct citations

        references = self.parent.references
        bibliography = self.parent._bibliography

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        if P["method"] == "default":
            tmp = "\n".join(out_sections[0])
            if (
                "GEOMETRY OPTIMISED USING EIGENVECTOR FOLLOWING (EF)" in tmp
                or "Geometry optimization using EF" in tmp
            ):
                opt_method = "EF -- eigenvector following"
                references.cite(
                    raw=bibliography["Baker_1986"],
                    alias="Baker_1986",
                    module="mopac_step",
                    level=1,
                    note="Eigenvector-following minimizer.",
                )
            elif (
                "Geometry optimization using BFGS" in tmp or "SATISFIED IN BFGS" in tmp
            ):
                opt_method = "BFGS -- Broyden-Fletcher-Goldfarb-Shanno algorithm"
                references.cite(
                    raw=bibliography["Broyden_1970"],
                    alias="Broyden_1970",
                    module="mopac_step",
                    level=1,
                    note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
                )
                references.cite(
                    raw=bibliography["Fletcher_1970"],
                    alias="Fletcher_1970",
                    module="mopac_step",
                    level=1,
                    note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
                )
                references.cite(
                    raw=bibliography["Goldfarb_1970"],
                    alias="Goldfarb_1970",
                    module="mopac_step",
                    level=1,
                    note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
                )
                references.cite(
                    raw=bibliography["Shanno_1970"],
                    alias="Shanno_1970",
                    module="mopac_step",
                    level=1,
                    note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
                )
                references.cite(
                    raw=bibliography["Thiel_1988"],
                    alias="Thiel_1988",
                    module="mopac_step",
                    level=1,
                    note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
                )
            elif (
                "Geometry optimization using L-BFGS" in tmp
                or "SATISFIED IN L-BFGS" in tmp
            ):
                opt_method = (
                    "L-BFGS -- Limited memory Broyden-Fletcher-Goldfarb-Shanno "
                    "algorithm"
                )
                references.cite(
                    raw=bibliography["Broyden_1970"],
                    alias="Broyden_1970",
                    module="mopac_step",
                    level=1,
                    note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
                )
                references.cite(
                    raw=bibliography["Fletcher_1970"],
                    alias="Fletcher_1970",
                    module="mopac_step",
                    level=1,
                    note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
                )
                references.cite(
                    raw=bibliography["Goldfarb_1970"],
                    alias="Goldfarb_1970",
                    module="mopac_step",
                    level=1,
                    note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
                )
                references.cite(
                    raw=bibliography["Shanno_1970"],
                    alias="Shanno_1970",
                    module="mopac_step",
                    level=1,
                    note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
                )
                references.cite(
                    raw=bibliography["Thiel_1988"],
                    alias="Thiel_1988",
                    module="mopac_step",
                    level=1,
                    note="Broyden-Fletcher-Goldfarb-Shanno (BFGS) minimizer.",
                )
            else:
                logger.warning("Could not find which minimizer was used!")
                opt_method = "default -- but could not find which was used"
        else:
            opt_method = P["method"]

        # The results
        if "NUMBER_SCF_CYCLES" in data_sections[0]:
            text = (
                f"The geometry optimization using {opt_method} -- converged in "
                "{NUMBER_SCF_CYCLES} iterations."
            )
        else:
            data["NUMBER_SCF_CYCLES"] = len(data["HEAT_OF_FORM_UPDATED"])
            data["HEAT_OF_FORMATION"] = data["HEAT_OF_FORM_UPDATED"][-1]
            data["GRADIENT_NORM"] = data["GRADIENT_NORM_UPDATED"][-1]
            text = (
                f"The geometry optimization using {opt_method} -- did not converge in "
                "{NUMBER_SCF_CYCLES} steps. The following results are for the final "
                "structure.\n"
            )

        # Update the structure
        periodicity = starting_configuration.periodicity
        if "ATOM_X_OPT" in data or "ATOM_X_UPDATED" in data:
            initial_RDKMol = starting_configuration.to_RDKMol()

            if P["structure handling"] == "Ignore":
                system = starting_configuration
                configuration = starting_configuration
            else:
                system, configuration = self.get_system_configuration(
                    P, same_as=starting_configuration
                )
                if periodicity != 0 and P["LatticeOpt"]:
                    if "TRANS_VECTS" in data:
                        vectors = data["TRANS_VECTS"]
                        lattice = [
                            [vectors[0], vectors[1], vectors[2]],
                            [vectors[3], vectors[4], vectors[5]],
                            [vectors[6], vectors[7], vectors[8]],
                        ]
                        configuration.cell.from_vectors(lattice)
                    elif "TRANS_VECTS_UPDATED" in data:
                        vectors = data["TRANS_VECTS_UPDATED"][-1]
                        lattice = [
                            [vectors[0], vectors[1], vectors[2]],
                            [vectors[3], vectors[4], vectors[5]],
                            [vectors[6], vectors[7], vectors[8]],
                        ]
                        configuration.cell.from_vectors(lattice)
                    else:
                        logger.warning(
                            "Expected updated lattice vectors, but did not find!"
                        )
            xyz = []
            if "ATOM_X_OPT" in data:
                it = iter(data["ATOM_X_OPT"])
            else:
                it = iter(data["ATOM_X_UPDATED"][-1])
            for x in it:
                xyz.append([float(x), float(next(it)), float(next(it))])

            if configuration.symmetry.n_symops > 1:
                # Convert to coordinates of just the asymmetric atoms.
                xyz, delta = configuration.symmetry.symmetrize_coordinates(
                    xyz, fractionals=False
                )
                delta = np.array(delta)
                displacement = np.linalg.norm(delta, axis=1)
                max_disp = displacement.max()
                text += (
                    f"\nThe largest displacement from symmetry was {max_disp:.6f} Å.\n"
                )

            if P["structure handling"] == "Ignore":
                RDKMol = starting_configuration.to_RDKMol()
                RDKMol.GetConformer(0).SetPositions(np.array(xyz))
            else:
                configuration.atoms.set_coordinates(xyz, fractionals=False)
                RDKMol = configuration.to_RDKMol()

            result = RMSD(RDKMol, initial_RDKMol, symmetry=True, flavor="rdkit")
            data["RMSD"] = result["RMSD"]
            data["displaced atom"] = result["displaced atom"]
            data["maximum displacement"] = result["maximum displacement"]

            result = configuration.RMSD(
                initial_RDKMol, symmetry=True, include_h=True, flavor="rdkit"
            )
            data["RMSD with H"] = result["RMSD"]
            data["displaced atom with H"] = result["displaced atom"]
            data["maximum displacement with H"] = result["maximum displacement"]

            text += seamm.standard_parameters.set_names(
                system, configuration, P, _first=True, Hamiltonian=P["hamiltonian"]
            )

        # Write the structure out for viewing.
        directory = Path(self.directory)
        directory.mkdir(parents=True, exist_ok=True)

        if periodicity == 0:
            configuration.to_sdf(directory / "optimized.sdf")
        else:
            #  MMCIF file has bonds
            try:
                path = directory / "optimized.mmcif"
                path.write_text(configuration.to_mmcif_text())
            except Exception:
                message = "Error creating the mmcif file\n\n" + traceback.format_exc()
                logger.warning(message)
            # CIF file has cell
            if configuration.periodicity == 3:
                try:
                    path = directory / "optimized.cif"
                    path.write_text(configuration.to_cif_text())
                except Exception:
                    message = "Error creating the cif file\n\n" + traceback.format_exc()
                    logger.warning(message)

        printer.normal(__(text, **data, indent=8 * " "))

        super().analyze(
            indent=indent,
            data_sections=data_sections,
            out_sections=out_sections,
            table=table,
        )
