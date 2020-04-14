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

"""Utilities to access different Argentina-Related databases of
COVID-19 data from the Arcovid19 group.

"""

__version__ = "0.4.1"


# =============================================================================
# PUBLIC API
# =============================================================================

from .cache import CACHE, from_cache  # noqa
from .cases import load_cases  # noqa
