#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Bruno Sanchez, Vanessa Daza,
#                     Juan B Cabral, Marcelo Lares,
#                     Nadia Luczywo, Dante Paz, Rodrigo Quiroga,
#                     Martín de los Ríos, Federico Stasyszyn
#                     Cristian Giuppone.
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/libs/master/LICENSE

# =============================================================================
# DOCS
# =============================================================================

"""Translate utilities for arcovi19.web.

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import pathlib
import atexit

from unittest import mock

import attr

import sh


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

MAPPING_FILE = PATH / "babel" / "babel.cfg"

TEMPLATE_POT = PATH / "babel" / "messages.pot"

INPUT_DIR = PATH / "arcovid19" / "web"

TRANSLATIONS_DIR = PATH / "arcovid19" / "web" / "translations"

DYNAMIC_I18N = TRANSLATIONS_DIR / "_dyn.py"

LANGS = ["es", "en"]


@atexit.register
def _remove_dynamic():
    try:
        os.remove(DYNAMIC_I18N)
    except Exception:
        pass


# =============================================================================
# EXTENSION CLASS
# =============================================================================


@attr.s(frozen=True)
class DynGetText:

    lines = attr.ib(init=False, factory=list)

    def lgtext(self, value):
        self.lines.append(f"flask_babel.lazy_gettext('{value}')")

    def getvalue(self):
        return "\n".join(["import flask_babel"] + self.lines)


# =============================================================================
# FUNCTIONS
# =============================================================================


def translate():

    print(f"Create dynamic file '{DYNAMIC_I18N}'")
    dgt = DynGetText()
    with mock.patch("flask_babel.lazy_gettext", dgt.lgtext):
        import arcovid19  # noqa

    with open(DYNAMIC_I18N, "w") as fp:
        fp.write(dgt.getvalue())

    print(f"Update the messages template '{TEMPLATE_POT}'")
    sh.pybabel.extract(
        mapping_file=MAPPING_FILE,
        keywords="lazy_gettext",
        project="arcovid19",
        copyright_holder="arcovid19",
        output_file=TEMPLATE_POT,
        input_dirs=".",
    )

    # create (if is needed) all the language files
    print(f"Create all the language files in '{TRANSLATIONS_DIR}'")
    for lang in LANGS:
        lang_path = TRANSLATIONS_DIR / lang / "LC_MESSAGES" / "messages.po"
        if not lang_path.exists():
            print(f"    -> NEW-LANG Creating '{lang}' files")
            sh.pybabel.init(
                input_file=TEMPLATE_POT,
                output_dir=TRANSLATIONS_DIR,
                locale=lang,
            )

    print("Update all the language files")
    sh.pybabel.update(input_file=TEMPLATE_POT, output_dir=TRANSLATIONS_DIR)

    print("Compiling")
    sh.pybabel.compile(directory=TRANSLATIONS_DIR)

    print("Done!")


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    translate()
