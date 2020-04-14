#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Bruno Sanchez, Vanessa Daza,
#                     Juan B Cabral, Marcelo Lares,
#                     Nadia Luczywo, Dante Paz, Rodrigo Quiroga,
#                     Martín de los Ríos, Federico Stasyszyn
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/libs/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Command line interfaces to access different Argentina-Related databases of
COVID-19 data from the Arcovid19 group.

"""

__all__ = ["main"]


# =============================================================================
# IMPORTS
# =============================================================================

import sys

from .cases import load_cases, CASES_URL


# =============================================================================
# CONSTANTS
# =============================================================================

DESCRIPTION = __doc__


# =============================================================================
# MAIN_
# =============================================================================

def cases(*, url=CASES_URL, force=False, out=None):
    """Retrieve and store the cases database in CSV format.

    url: str
        The url for the excel table to parse. Default is ivco19 team table.

    out: PATH (default=stdout)
        The output path to the CSV file. If it's not provided the
        data is printed in the stdout.

    force:
        If you want to ignore the local cache or retrieve a new value.

    """
    cases = load_cases(url=url, force=force)
    if out is not None:
        cases.to_csv(out)
    else:
        cases.to_csv(sys.stdout)


def main():
    """Run the arcovid19 command line interface."""
    from clize import run

    run(cases)
