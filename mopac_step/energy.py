# -*- coding: utf-8 -*-

"""Setup and run MOPAC"""

import copy
import csv
import logging
from pathlib import Path
import textwrap

from tabulate import tabulate

import mopac_step
import seamm
import seamm.data
from seamm_util import Q_, units_class
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("mopac")


class Energy(seamm.Node):
    def __init__(self, flowchart=None, title="Energy", extension=None):
        """Initialize the node"""

        logger.debug("Creating Energy {}".format(self))

        super().__init__(flowchart=flowchart, title=title, extension=extension)

        self._calculation = "energy"
        self._model = None
        self._metadata = mopac_step.metadata
        self.parameters = mopac_step.EnergyParameters()
        self.description = "A single point energy calculation"

    @property
    def header(self):
        """A printable header for this section of output"""
        return "Step {}: {}".format(".".join(str(e) for e in self._id), self.title)

    @property
    def version(self):
        """The semantic version of this module."""
        return mopac_step.__version__

    @property
    def git_revision(self):
        """The git version of this module."""
        return mopac_step.__git_revision__

    def description_text(self, P=None):
        """Prepare information about what this node will do"""

        if not P:
            P = self.parameters.values_to_dict()

        text = "Calculated with {hamiltonian}, converged to "
        # Convergence
        if P["convergence"] == "normal":
            text += "the 'normal' level of 1.0e-04 kcal/mol."
        elif P["convergence"] == "precise":
            text += "the 'precise' level of 1.0e-06 kcal/mol."
        elif P["convergence"] == "relative":
            text += "a factor of {relative} times the normal criterion."
        elif P["convergence"] == "absolute":
            text += "converged to {absolute}."

        if self.parameters["uhf"].is_expr:
            text += (
                " Whether to use spin-unrestricted SCF (UHF) for closed-shell molecules"
                "will be determined by '{uhf}'."
            )
        elif self.parameters["uhf"].get():
            text += " The SCF will be spin-unrestricted (UHF) for all molecules."
        else:
            text += (
                " The SCF will be restricted for closed-shell molecules (RHF) and "
                "spin-unrestricted (UHF) for all others."
            )

        # MOZYME localized molecular orbitals.
        if P["MOZYME"] == "always":
            text += (
                "\n\nThe SCF will be solved using localized molecular orbitals "
                "(MOZYME), which is faster than the traditional method for larger "
                "systems."
            )
            used_mozyme = True
        elif P["MOZYME"] == "for larger systems":
            text += (
                "\n\nThe SCF will be solved using localized molecular orbitals "
                "(MOZYME) for systems with {nMOZYME} atoms or more. This method is "
                "faster than the traditional method for larger systems."
            )
            used_mozyme = True
        else:
            used_mozyme = False

        if used_mozyme:
            follow_up = P["MOZYME follow-up"]
            if "exact" in follow_up:
                text += (
                    " The energy given by MOZYME slowly accumulates error due to the "
                    "increasing non-orthogonality of the localized orbitals after "
                    "many iterations. A single point energy using the traditional "
                    "method will be run to get the correct energy."
                )
            elif "new" in follow_up:
                text += (
                    " The energy given by MOZYME slowly accumulates error due to the "
                    "increasing non-orthogonality of the localized orbitals after "
                    "many iterations. A single point energy using fresh localized "
                    "orbitals will be run to get the correct energy."
                )
            elif follow_up == "none":
                text += (
                    " The energy given by MOZYME slowly accumulates error due to the "
                    "increasing non-orthogonality of the localized orbitals after "
                    "many iterations. No follow-up calculation will be done, so be "
                    "careful with the final energies produced."
                )
                used_mozyme = False
            else:
                logger.error(f"Don't recognize the MOZYME follow-up: '{follow_up}'")

        # Handle COSMO
        if self.parameters["COSMO"].is_expr:
            text += (
                "\n\n'{COSMO}' will determine whether to use the COSMO solvation "
                "model. If it is used the parameters will be "
            )
        elif self.parameters["COSMO"].get():
            text += "\n\nThe COSMO solvation model will be used with "

        if self.parameters["COSMO"].is_expr or self.parameters["COSMO"].get():
            text += (
                "dielectric constant = {eps}, solvent radius = {rsolve}, "
                "{nspa} grid points per atom, and a cutoff of {disex}."
            )

        # And bond orders
        if P["bond orders"] == "yes":
            text += "\n\nThe bond orders will be calculated."
        elif P["bond orders"] == "yes, and apply to structure":
            text += (
                "\n\nThe bond orders will be calculated and used to set the bonding "
                "for the structure."
            )

        return self.header + "\n" + __(text, **P, indent=4 * " ").__str__()

    def get_input(self):
        """Get the input for an energy calculation for MOPAC"""
        system, configuration = self.get_system_configuration(None)
        references = self.parent.references

        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        # The model chemistry, for labeling properties.
        self.model = P["hamiltonian"]

        # Have to fix formatting for printing...
        PP = dict(P)
        for key in PP:
            if isinstance(PP[key], units_class):
                PP[key] = "{:~P}".format(PP[key])

        # Save the description for later printing
        self.description = []
        self.description.append(__(self.description_text(PP), **PP, indent=self.indent))

        # Start gathering the keywords
        keywords = copy.deepcopy(P["extra keywords"])
        keywords.append("1SCF")
        keywords.append(P["hamiltonian"])

        if P["hamiltonian"] == "AM1":
            elements = configuration.atoms.symbols
            references.cite(
                raw=self.parent._bibliography["Dewar_1985c"],
                alias="Dewar_1985c",
                module="mopac_step",
                level=1,
                note="Main reference for AM1 + C, H, N, O.",
            )
            for element in ("F", "Cl", "Br", "I"):
                if element in elements:
                    references.cite(
                        raw=self.parent._bibliography["Dewar_1988"],
                        alias="Dewar_1988",
                        module="mopac_step",
                        level=1,
                        note="AM1 parameters for F, Cl, Br, I.",
                    )
                    break
            if "Al" in elements:
                references.cite(
                    raw=self.parent._bibliography["Dewar_1990"],
                    alias="Dewar_1990",
                    module="mopac_step",
                    level=1,
                    note="AM1 parameters for Al.",
                )
            if "Si" in elements:
                references.cite(
                    raw=self.parent._bibliography["Dewar_1987b"],
                    alias="Dewar_1987b",
                    module="mopac_step",
                    level=1,
                    note="AM1 parameters for Si.",
                )
            if "P" in elements:
                references.cite(
                    raw=self.parent._bibliography["Dewar_1989"],
                    alias="Dewar_1989",
                    module="mopac_step",
                    level=1,
                    note="AM1 parameters for P.",
                )
            if "S" in elements:
                references.cite(
                    raw=self.parent._bibliography["Dewar_1990b"],
                    alias="Dewar_1990b",
                    module="mopac_step",
                    level=1,
                    note="AM1 parameters for S.",
                )
            if "Zn" in elements:
                references.cite(
                    raw=self.parent._bibliography["Dewar_1988b"],
                    alias="Dewar_1988b",
                    module="mopac_step",
                    level=1,
                    note="AM1 parameters for Zn.",
                )
            if "Ge" in elements:
                references.cite(
                    raw=self.parent._bibliography["Dewar_1989b"],
                    alias="Dewar_1989b",
                    module="mopac_step",
                    level=1,
                    note="AM1 parameters for Ge.",
                )
            if "Mo" in elements:
                references.cite(
                    raw=self.parent._bibliography["Voityuk_2000"],
                    alias="Voityuk_2000",
                    module="mopac_step",
                    level=1,
                    note="AM1 parameters for Mo.",
                )
            if "Hg" in elements:
                references.cite(
                    raw=self.parent._bibliography["Dewar_1989c"],
                    alias="Dewar_1989c",
                    module="mopac_step",
                    level=1,
                    note="AM1 parameters for Hg.",
                )
            for element in (
                "Li",
                "Be",
                "Na",
                "Mg",
                "K",
                "Ca",
                "Ga",
                "As",
                "Se",
                "Rb",
                "Sr",
                "In",
                "Sn",
                "Sb",
                "Te",
                "Cs",
                "Ba",
                "Pb",
                "Bi",
            ):
                if element in elements:
                    references.cite(
                        raw=self.parent._bibliography["Stewart_2004"],
                        alias="Stewart_2004",
                        module="mopac_step",
                        level=1,
                        note="AM1 parameterization for main-group elements.",
                    )
                    break
        elif P["hamiltonian"] == "MNDO" or P["hamiltonian"] == "MNDOD":
            elements = configuration.atoms.symbols
            references.cite(
                raw=self.parent._bibliography["Dewar_1977"],
                alias="Dewar_1977",
                module="mopac_step",
                level=1,
                note="Main reference for MNDO + C, H, N, O.",
            )
            if "Be" in elements:
                references.cite(
                    raw=self.parent._bibliography["Dewar_1978"],
                    alias="Dewar_1978",
                    module="mopac_step",
                    level=1,
                    note="MNDO parameters for Be.",
                )
            if "B" in elements or "Al" in elements:
                if "B" in elements or P["hamiltonian"] == "MNDO":
                    references.cite(
                        raw=self.parent._bibliography["Davis_1981"],
                        alias="Davis_1981",
                        module="mopac_step",
                        level=1,
                        note="MNDO parameters for B and Al.",
                    )
            if "F" in elements:
                references.cite(
                    raw=self.parent._bibliography["Dewar_1978b"],
                    alias="Dewar_1978b",
                    module="mopac_step",
                    level=1,
                    note="MNDO parameters for F.",
                )
            if "Si" in elements and P["hamiltonian"] == "MNDO":
                references.cite(
                    raw=self.parent._bibliography["Dewar_1986"],
                    alias="Dewar_1986",
                    module="mopac_step",
                    level=1,
                    note="Revised MNDO parameters for Si.",
                )
            if "P" in elements and P["hamiltonian"] == "MNDO":
                references.cite(
                    raw=self.parent._bibliography["Dewar_1978b"],
                    alias="Dewar_1978b",
                    module="mopac_step",
                    level=1,
                    note="MNDO parameters for P.",
                )
            if "S" in elements and P["hamiltonian"] == "MNDO":
                references.cite(
                    raw=self.parent._bibliography["Dewar_1986b"],
                    alias="Dewar_1986b",
                    module="mopac_step",
                    level=1,
                    note="MNDO parameters for S.",
                )
            if "Cl" in elements and P["hamiltonian"] == "MNDO":
                references.cite(
                    raw=self.parent._bibliography["Dewar_1983"],
                    alias="Dewar_1983",
                    module="mopac_step",
                    level=1,
                    note="MNDO parameters for Cl.",
                )
            if "Zn" in elements and P["hamiltonian"] == "MNDO":
                references.cite(
                    raw=self.parent._bibliography["Dewar_1986c"],
                    alias="Dewar_1986c",
                    module="mopac_step",
                    level=1,
                    note="MNDO parameters for Zn.",
                )
            if "Ge" in elements:
                references.cite(
                    raw=self.parent._bibliography["Dewar_1987"],
                    alias="Dewar_1987",
                    module="mopac_step",
                    level=1,
                    note="MNDO parameters for Ge.",
                )
            if "Br" in elements and P["hamiltonian"] == "MNDO":
                references.cite(
                    raw=self.parent._bibliography["Dewar_1983b"],
                    alias="Dewar_1983b",
                    module="mopac_step",
                    level=1,
                    note="MNDO parameters for Br.",
                )
            if "Sn" in elements:
                references.cite(
                    raw=self.parent._bibliography["Dewar_1984"],
                    alias="Dewar_1984",
                    module="mopac_step",
                    level=1,
                    note="MNDO parameters for Sn.",
                )
            if "I" in elements and P["hamiltonian"] == "MNDO":
                references.cite(
                    raw=self.parent._bibliography["Dewar_1984b"],
                    alias="Dewar_1984b",
                    module="mopac_step",
                    level=1,
                    note="MNDO parameters for I.",
                )
            if "Hg" in elements and P["hamiltonian"] == "MNDO":
                references.cite(
                    raw=self.parent._bibliography["Dewar_1985"],
                    alias="Dewar_1985",
                    module="mopac_step",
                    level=1,
                    note="MNDO parameters for Hg.",
                )
            if "Pb" in elements:
                references.cite(
                    raw=self.parent._bibliography["Dewar_1985b"],
                    alias="Dewar_1985b",
                    module="mopac_step",
                    level=1,
                    note="MNDO parameters for Pb.",
                )
            for element in (
                "Na",
                "Mg",
                "K",
                "Ca",
                "Ga",
                "As",
                "Se",
                "Rb",
                "Sr",
                "In",
                "Sb",
                "Te",
                "Cs",
                "Ba",
                "Tl",
                "Bi",
            ):
                if element in elements:
                    references.cite(
                        raw=self.parent._bibliography["Stewart_2004"],
                        alias="Stewart_2004",
                        module="mopac_step",
                        level=1,
                        note="MNDO parameterization for main-group elements.",
                    )
                    break
            if P["hamiltonian"] == "MNDOD":
                for element in (
                    "Al",
                    "Si",
                    "P",
                    "S",
                    "Cl",
                    "Br",
                    "I",
                    "Zn",
                    "Cd",
                    "Hg",
                ):
                    if element in elements:
                        references.cite(
                            raw=self.parent._bibliography["Thiel_1992"],
                            alias="Thiel_1992",
                            module="mopac_step",
                            level=1,
                            note=("MNDO-D formalism for d-orbitals."),
                        )
                        references.cite(
                            raw=self.parent._bibliography["Thiel_1996"],
                            alias="Thiel_1996",
                            module="mopac_step",
                            level=1,
                            note=(
                                "MNDO-D, parameters for Al, Si, P, S, Cl, Br, "
                                "I, Zn, Cd, and Hg."
                            ),
                        )
                        break
        elif P["hamiltonian"] == "PM3":
            elements = configuration.atoms.symbols
            references.cite(
                raw=self.parent._bibliography["Stewart_1989"],
                alias="Stewart_1989",
                module="mopac_step",
                level=1,
                note="The citation for the MOPAC parameterization.",
            )
            for element in (
                "Be",
                "Mg",
                "Zn",
                "Ga",
                "Ge",
                "As",
                "Se",
                "Cd",
                "In",
                "Sn",
                "Sb",
                "Te",
                "Hg",
                "Tl",
                "Pb",
                "Bi",
            ):
                if element in elements:
                    references.cite(
                        raw=self.parent._bibliography["Stewart_1991"],
                        alias="Stewart_1991",
                        module="mopac_step",
                        level=1,
                        note="The citation for the MOPAC parameterization.",
                    )
                    break
            if "Li" in elements:
                references.cite(
                    raw=self.parent._bibliography["Anders_1993"],
                    alias="Anders_1993",
                    module="mopac_step",
                    level=1,
                    note="The citation for the MOPAC parameterization.",
                )
            for element in ("B", "Na", "K", "Ca", "Rb", "Sr", "Cs", "Ba"):
                if element in elements:
                    references.cite(
                        raw=self.parent._bibliography["Stewart_2004"],
                        alias="Stewart_2004",
                        module="mopac_step",
                        level=1,
                        note="The citation for the MOPAC parameterization.",
                    )
                    break
        elif "PM6" in P["hamiltonian"]:
            references.cite(
                raw=self.parent._bibliography["Stewart_2007"],
                alias="Stewart_2007",
                module="mopac_step",
                level=1,
                note="The PM6 parameterization in MOPAC.",
            )
            if P["hamiltonian"] == "PM6-D3":
                references.cite(
                    raw=self.parent._bibliography["Grimme_2010"],
                    alias="Grimme_2010",
                    module="mopac_step",
                    level=1,
                    note="Dispersion correction by Grimme, et al.",
                )
            if P["hamiltonian"] == "PM6-DH+":
                references.cite(
                    raw=self.parent._bibliography["Korth_2010"],
                    alias="Korth_2010",
                    module="mopac_step",
                    level=1,
                    note="Hydrogen-bonding correction by Korth.",
                )
            if "PM6-DH2" in P["hamiltonian"]:
                references.cite(
                    raw=self.parent._bibliography["Korth_2009"],
                    alias="Korth_2009",
                    module="mopac_step",
                    level=1,
                    note="Hydrogen-bonding and dispersion correction.",
                )
                references.cite(
                    raw=self.parent._bibliography["Rezac_2009"],
                    alias="Rezac_2009",
                    module="mopac_step",
                    level=1,
                    note="Hydrogen-bonding and dispersion correction.",
                )
            if P["hamiltonian"] == "PM6-DH2x":
                references.cite(
                    raw=self.parent._bibliography["Rezac_2011"],
                    alias="Rezac_2011",
                    module="mopac_step",
                    level=1,
                    note="Halogen-bonding correction.",
                )
            if "PM6-D3H4" in P["hamiltonian"]:
                references.cite(
                    raw=self.parent._bibliography["Rezac_2011"],
                    alias="Rezac_2011",
                    module="mopac_step",
                    level=1,
                    note="Hydrogen-bonding and dispersion correction.",
                )
                references.cite(
                    raw=self.parent._bibliography["Vorlova_2015"],
                    alias="Vorlova_2015",
                    module="mopac_step",
                    level=1,
                    note="Hydrogen-hydrogen repulsion correction.",
                )
            if P["hamiltonian"] == "PM6-D3H4x":
                references.cite(
                    raw=self.parent._bibliography["Brahmkshatriya_2013"],
                    alias="Brahmkshatriya_2013",
                    module="mopac_step",
                    level=1,
                    note="Halogen-oxygen and halogen-nitrogen correction.",
                )
        elif "PM7" in P["hamiltonian"]:
            references.cite(
                raw=self.parent._bibliography["Stewart_2012"],
                alias="Stewart_2012",
                module="mopac_step",
                level=1,
                note="The PM7 parameterization in MOPAC.",
            )
        elif P["hamiltonian"] == "RM1":
            references.cite(
                raw=self.parent._bibliography["Rocha_2006"],
                alias="Rocha_2006",
                module="mopac_step",
                level=1,
                note="RM1 parameterization.",
            )

        # which structure? may need to set default first...
        if P["structure"] == "default":
            if self._id[-1] == "1":
                structure = "initial"
            else:
                structure = "current"
        elif self._id[-1] == "1":
            structure = "initial"
        elif P["structure"] == "current":
            structure = "current"

        if structure == "current":
            keywords.append("OLDGEO")

        if P["convergence"] == "normal":
            pass
        elif P["convergence"] == "precise":
            keywords.append("PRECISE")
        elif P["convergence"] == "relative":
            keywords.append("RELSCF=" + P["relative"])
        elif P["convergence"] == "absolute":
            keywords.append("SCFSCRT=" + P["absolute"])
        else:
            raise RuntimeError(
                "Don't recognize convergence '{}'".format(P["convergence"])
            )

        if P["uhf"]:
            keywords.append("UHF")

        if P["MOZYME"] == "always":
            keywords.append("MOZYME")
        elif (
            P["MOZYME"] == "for larger systems"
            and configuration.n_atoms >= P["nMOZYME"]
        ):
            keywords.append("MOZYME")

        if P["COSMO"]:
            keywords.append(f"EPS={P['eps']}")
            rsolve = P["rsolve"].to("Å").magnitude
            keywords.append(f"RSOLVE={rsolve}")
            keywords.append(f"NSPA={P['nspa']}")
            keywords.append(f"DISEX={P['disex']}")

        if P["calculate gradients"]:
            keywords.append("GRADIENTS")

        if "yes" in P["bond orders"]:
            keywords.append("BONDS")

        # Add any extra keywords so that they appear at the end
        metadata = self.metadata["keywords"]
        for keyword in P["extra keywords"]:
            if "=" in keyword:
                keyword, value = keyword.split("=")
                if keyword not in metadata or "format" not in metadata[keyword]:
                    keywords.append(keyword + "=" + value)
                else:
                    keywords.append(metadata[keyword]["format"].format(keyword, value))

        result = []
        result.append([[*keywords], None, None])

        # Handle MOZYME follow-up calculations
        if "MOZYME" in keywords:
            follow_up = P["MOZYME follow-up"]
            if "exact" in follow_up:
                keywords.remove("MOZYME")
                if "1SCF" not in keywords:
                    keywords.append("1SCF")
                keywords.append("OLDGEO")
                result.append([[*keywords], None, "MOZYME follow-up using MOPAC"])
            elif "new" in follow_up:
                if "1SCF" not in keywords:
                    keywords.append("1SCF")
                keywords.append("OLDGEO")
                result.append([[*keywords], None, "MOZYME follow-up, reinitializing"])
            elif follow_up == "none":
                pass
            else:
                logger.error(f"Don't recognize the MOZYME follow-up: '{follow_up}'")

        return result

    def analyze(self, indent="", data_sections=[], out_sections=[], table=None):
        """Parse the output and generating the text output and store the
        data in variables for other stages to access
        """
        options = self.parent.options

        # Get the parameters used
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        system, starting_configuration = self.get_system_configuration(None)

        if P["MOZYME"] == "always":
            used_mozyme = True
        elif (
            P["MOZYME"] == "for larger systems"
            and starting_configuration.n_atoms >= P["nMOZYME"]
        ):
            used_mozyme = True
        else:
            used_mozyme = False

        if used_mozyme:
            follow_up = P["MOZYME follow-up"]
            if "exact" in follow_up:
                pass
            elif "new" in follow_up:
                pass
            elif follow_up == "none":
                used_mozyme = False
            else:
                logger.error(f"Don't recognize the MOZYME follow-up: '{follow_up}'")

        if table is None:
            table = {
                "Property": [],
                "Value": [],
                "Units": [],
            }
        text = ""

        if used_mozyme:
            data = {**data_sections[0]}
            data.update(data_sections[1])
        else:
            data = data_sections[0]

        if "GRADIENT_NORM" in data:
            tmp = data["GRADIENT_NORM"]
            table["Property"].append("Gradient Norm")
            table["Value"].append(f"{tmp:.2f}")
            table["Units"].append("kcal/mol/Å")

        if "POINT_GROUP" in data and data["POINT_GROUP"] != "":
            text += "The molecule has {POINT_GROUP} symmetry."
        else:
            text += "The symmetry of the molecule was not determined."

        if "HEAT_OF_FORMATION" in data:
            tmp = data["HEAT_OF_FORMATION"]
            table["Property"].append("Enthalpy of Formation")
            table["Value"].append(f"{tmp:.2f}")
            table["Units"].append("kcal/mol")

            tmp = Q_(tmp, "kcal/mol").to("kJ/mol").magnitude
            data["Enthalpy of Formation"] = tmp
            table["Property"].append("")
            table["Value"].append(f"{tmp:.2f}")
            table["Units"].append("kJ/mol")

            if used_mozyme and "HEAT_OF_FORMATION" in data_sections[0]:
                tmp2 = data_sections[0]["HEAT_OF_FORMATION"]
                tmp2 = Q_(tmp2, "kcal/mol").to("kJ/mol").magnitude
                table["Property"].append("MOZYME Enthalpy of Formation")
                table["Value"].append(f"{tmp2:.2f}")
                table["Units"].append("kJ/mol")

                tmp2 -= tmp
                table["Property"].append("Othonormality error in EoF")
                table["Value"].append(f"{tmp2:.2f}")
                table["Units"].append("kJ/mol")

                if abs(tmp2) > 10.0:
                    text += (
                        "\n\nWarning: The non-orthogonality of the localized orbitals "
                        f"led to an error in the enthalpy of formation of {tmp2:.2f} "
                        "kJ/mol. This is expected if there were many iterations of "
                        "geometry optimization. Otherwise check the results carefully."
                    )
                    if "exact" in follow_up:
                        text += (
                            " You followed up with an exact calculation. A large "
                            "difference in the energy could indicate a problem "
                            "with the localcized molecular orbitals. Check the MOPAC "
                            "output carefully!"
                        )

        if "SPIN_COMPONENT" in data:
            tmp = data["SPIN_COMPONENT"]
            table["Property"].append("Sz")
            table["Value"].append(f"{tmp:.2f}")
            table["Units"].append("")

        if "TOTAL_SPIN" in data:
            tmp = data["TOTAL_SPIN"]
            table["Property"].append("S^2")
            table["Value"].append(f"{tmp:.2f}")
            table["Units"].append("")

        if "IONIZATION_POTENTIAL" in data:
            tmp = data["IONIZATION_POTENTIAL"]
            table["Property"].append("Ionization Energy")
            table["Value"].append(f"{tmp:.2f}")
            table["Units"].append("eV")

        if "DIPOLE" in data:
            tmp = data["DIPOLE"]
            table["Property"].append("Dipole Moment")
            table["Value"].append(f"{tmp:.2f}")
            table["Units"].append("Debye")

        if "EIGENVALUES" in data or "ALPHA_EIGENVALUES" in data:
            Elumo = None
            Ehomo = None
            if "EIGENVALUES" in data and "MOLECULAR_ORBITAL_OCCUPANCIES" in data:
                for occ, E in zip(
                    data["MOLECULAR_ORBITAL_OCCUPANCIES"], data["EIGENVALUES"]
                ):
                    if occ > 0.1:
                        Ehomo = E
                    else:
                        Elumo = E
                        break
            elif (
                "ALPHA_EIGENVALUES" in data
                and "ALPHA_MOLECULAR_ORBITAL_OCCUPANCIES" in data
                and "BETA_EIGENVALUES" in data
                and "BETA_MOLECULAR_ORBITAL_OCCUPANCIES" in data
            ):
                for occ, E in zip(
                    data["ALPHA_MOLECULAR_ORBITAL_OCCUPANCIES"],
                    data["ALPHA_EIGENVALUES"],
                ):
                    if occ > 0.1:
                        Ehomo = E
                    else:
                        Elumo = E
                        break
                for occ, E in zip(
                    data["BETA_MOLECULAR_ORBITAL_OCCUPANCIES"],
                    data["BETA_EIGENVALUES"],
                ):
                    if occ > 0.1:
                        if E > Ehomo:
                            Ehomo = E
                    else:
                        if Elumo is None or E < Elumo:
                            Elumo = E
                        break

            data["HOMO Energy"] = Ehomo
            table["Property"].append("HOMO Energy")
            table["Value"].append(f"{Ehomo:.2f}")
            table["Units"].append("eV")
            if Elumo is not None:
                data["LUMO Energy"] = Elumo
                table["Property"].append("LUMO Energy")
                table["Value"].append(f"{Elumo:.2f}")
                table["Units"].append("eV")
                data["HOMO-LUMO Gap"] = Elumo - Ehomo
                table["Property"].append("Gap")
                table["Value"].append(f"{Elumo - Ehomo:.2f}")
                table["Units"].append("eV")

        if "AREA" in data:
            tmp = data["AREA"]
            table["Property"].append("COSMO Area")
            table["Value"].append(f"{tmp:.2f}")
            table["Units"].append("Å^2")

        if "VOLUME" in data:
            tmp = data["VOLUME"]
            table["Property"].append("COSMO Volume")
            table["Value"].append(f"{tmp:.2f}")
            table["Units"].append("Å^3")

        text_lines = []
        text_lines.append("                     Results")
        text_lines.append(
            tabulate(
                table,
                headers="keys",
                tablefmt="psql",
                colalign=("center", "decimal", "left"),
            )
        )
        text_lines.append("\n\n")

        # Get charges and spins, etc.
        directory = Path(self.directory)
        directory.mkdir(parents=True, exist_ok=True)

        system, configuration = self.get_system_configuration(None)
        symbols = configuration.atoms.symbols
        atoms = configuration.atoms
        if "ATOM_CHARGES" in data:
            # Add to atoms (in coordinate table)
            if "charge" not in atoms:
                atoms.add_attribute(
                    "charge", coltype="float", configuration_dependent=True
                )
            atoms["charge"][0:] = data["ATOM_CHARGES"]

            # Print the charges and dump to a csv file
            chg_tbl = {
                "Atom": [*range(1, len(symbols) + 1)],
                "Element": symbols,
                "Charge": [],
            }
            with open(directory / "atom_properties.csv", "w", newline="") as fd:
                writer = csv.writer(fd)
                if "AO_SPINS" in data:
                    # Sum to atom spins...
                    spins = len(symbols) * [0.0]
                    for spin, indx in zip(data["AO_SPINS"], data["AO_ATOMINDEX"]):
                        spins[indx - 1] += spin

                    # Add to atoms (in coordinate table)
                    if "spin" not in atoms:
                        atoms.add_attribute(
                            "spin", coltype="float", configuration_dependent=True
                        )
                        atoms["spin"][0:] = spins

                    header = "        Atomic charges and spins"
                    chg_tbl["Spin"] = []
                    writer.writerow(["Atom", "Element", "Charge", "Spin"])
                    for atom, symbol, q, s in zip(
                        range(1, len(symbols) + 1),
                        symbols,
                        data["ATOM_CHARGES"],
                        spins,
                    ):
                        q = f"{q:.3f}"
                        s = f"{s:.3f}"

                        writer.writerow([atom, symbol, q, s])

                        chg_tbl["Charge"].append(q)
                        chg_tbl["Spin"].append(s)
                else:
                    header = "        Atomic charges"
                    writer.writerow(["Atom", "Element", "Charge"])
                    for atom, symbol, q in zip(
                        range(1, len(symbols) + 1),
                        symbols,
                        data["ATOM_CHARGES"],
                    ):
                        q = f"{q:.2f}"
                        writer.writerow([atom, symbol, q])

                        chg_tbl["Charge"].append(q)
            if len(symbols) <= int(options["max_atoms_to_print"]):
                text_lines.append(header)
                text_lines.append(
                    tabulate(
                        chg_tbl,
                        headers="keys",
                        tablefmt="psql",
                        colalign=("center", "center"),
                    )
                )

        text = str(__(text, **data, indent=self.indent + 4 * " "))
        text += "\n\n"
        text += textwrap.indent("\n".join(text_lines), self.indent + 7 * " ")

        if "BOND_ORDERS" in data:
            text += self._bond_orders(
                P["bond orders"], data["BOND_ORDERS"], starting_configuration
            )

        printer.normal(text)

        if used_mozyme and "CPU_TIME" in data_sections[0]:
            t0 = data_sections[0]["CPU_TIME"]
            if "CPU_TIME" in data:
                t1 = data["CPU_TIME"]
                text = (
                    f"This MOZYME calculation took {t0:.2f} s and the follow-up "
                    f"took {t1:.2f} s."
                )
            else:
                text = f"The MOZYME calculation took {t0:.2f} s."
        elif "CPU_TIME" in data:
            t0 = data_sections[0]["CPU_TIME"]
            text = f"This calculation took {t0:.2f} s."
        printer.normal(str(__(text, **data, indent=self.indent + 4 * " ")))

        # Put any requested results into variables or tables
        self.store_results(
            configuration=configuration,
            data=data,
            create_tables=self.parameters["create tables"].get(),
        )

    def _bond_orders(self, control, bond_order_matrix, configuration):
        """Analyze and print the bond orders, and optionally use for the bonding
        in the structure.

        Parameters
        ----------
        control : str
            The control option for the bond order analysis
        bond_order_matrix : [float]
            Lower triangular part of the bond order matrix.
        configuration : molsystem.Configuration
            The configuration to put the bonds on, if requested.
        """
        text = ""
        n_atoms = configuration.n_atoms
        bond_i = []
        bond_j = []
        bond_order = []
        bond_order_str = []
        orders = []
        ij = 0
        for j in range(n_atoms):
            for i in range(j + 1):
                if i != j:
                    order = bond_order_matrix[ij]
                    if order > 0.5:
                        bond_i.append(i)
                        bond_j.append(j)
                        if order > 1.3 and order < 1.7:
                            bond_order.append(5)
                            bond_order_str.append("aromatic")
                        else:
                            bond_order.append(round(order))
                            bond_order_str.append(str(round(order)))
                        orders.append(order)
                ij += 1

        symbols = configuration.atoms.symbols
        options = self.parent.options
        text_lines = []
        if len(symbols) <= int(options["max_atoms_to_print"]):
            if "name" in configuration.atoms:
                name = configuration.atoms.get_column_data("name")
            else:
                name = []
                count = {}
                for symbol in symbols:
                    if symbol not in count:
                        count[symbol] = 1
                    else:
                        count[symbol] += 1
                    name.append(f"{symbol}{count[symbol]}")
            table = {
                "i": [name[i] for i in bond_i],
                "j": [name[j] for j in bond_j],
                "bond order": orders,
                "bond multiplicity": bond_order_str,
            }
            tmp = tabulate(
                table,
                headers="keys",
                tablefmt="pretty",
                disable_numparse=True,
                colalign=("center", "center", "right", "center"),
            )
            length = len(tmp.splitlines()[0])
            text_lines.append("\n")
            text_lines.append("Bond Orders".center(length))
            text_lines.append(
                tabulate(
                    table,
                    headers="keys",
                    tablefmt="psql",
                    colalign=("center", "center", "decimal", "center"),
                )
            )
            text += "\n\n"
            text += textwrap.indent("\n".join(text_lines), self.indent + 7 * " ")

        if control == "yes, and apply to structure":
            ids = configuration.atoms.ids
            iatoms = [ids[i] for i in bond_i]
            jatoms = [ids[j] for j in bond_j]
            configuration.bonds.delete()
            configuration.bonds.append(i=iatoms, j=jatoms, bondorder=bond_order)
            text2 = (
                "\nReplaced the bonds in the configuration with those from the "
                "calculated bond orders.\n"
            )

            text += str(__(text2, indent=self.indent + 4 * " "))

        return text
