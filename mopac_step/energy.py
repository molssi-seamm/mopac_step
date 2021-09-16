# -*- coding: utf-8 -*-

"""Setup and run MOPAC"""

import logging
import seamm
import seamm.data
from seamm_util import units_class
import seamm_util.printing as printing
from seamm_util.printing import FormattedText as __
import mopac_step
import copy

logger = logging.getLogger(__name__)
job = printing.getPrinter()
printer = printing.getPrinter("mopac")


class Energy(seamm.Node):
    def __init__(self, flowchart=None, title="Energy", extension=None):
        """Initialize the node"""

        logger.debug("Creating Energy {}".format(self))

        super().__init__(flowchart=flowchart, title=title, extension=extension)

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

        text = "Single-point energy using {hamiltonian}, converged to "
        # Convergence
        if P["convergence"] == "normal":
            text += "the 'normal' level of 1.0e-04 kcal/mol."
        elif P["convergence"] == "precise":
            text += "the 'precise' level of 1.0e-06 kcal/mol."
        elif P["convergence"] == "relative":
            text += "a factor of {relative} times the " "normal criterion."
        elif P["convergence"] == "absolute":
            text += "converged to {absolute}"

        return self.header + "\n" + __(text, **P, indent=4 * " ").__str__()

    def get_input(self):
        """Get the input for an energy calculation for MOPAC"""
        system_db = self.get_variable("_system_db")
        configuration = system_db.system.configuration
        references = self.parent.references

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

        if P["calculate gradients"]:
            keywords.append("GRADIENTS")

        # Add any extra keywords so that they appear at the end
        metadata = mopac_step.keyword_metadata
        for keyword in P["extra keywords"]:
            if "=" in keyword:
                keyword, value = keyword.split("=")
                if keyword not in metadata or "format" not in metadata[keyword]:
                    keywords.append(keyword + "=" + value)
                else:
                    keywords.append(metadata[keyword]["format"].format(keyword, value))

        return keywords

    def analyze(self, indent="", data={}, out=[]):
        """Parse the output and generating the text output and store the
        data in variables for other stages to access
        """
        P = self.parameters.current_values_to_dict(
            context=seamm.flowchart_variables._data
        )

        text = "The heat of formation is {HEAT_OF_FORMATION} kcal/mol"

        if P["calculate gradients"]:
            text += " with a gradient norm of {GRADIENT_NORM} kcal/mol/Å."
        else:
            text += ". The gradients weren't calculated."

        text += " The system has {POINT_GROUP} symmetry."

        printer.normal(__(text, **data, indent=self.indent + 4 * " "))

        # Put any requested results into variables or tables
        self.store_results(
            data=data,
            properties=mopac_step.properties,
            results=self.parameters["results"].value,
            create_tables=self.parameters["create tables"].get(),
        )
