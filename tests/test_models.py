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

"""Test suite

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import pathlib

# import pytest

import numpy as np

import pandas as pd

# from matplotlib.testing.decorators import check_figures_equal

import arcovid19


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

TEST_DATA_PATH = PATH / "data"


# =============================================================================
# SETUP
# =============================================================================

def setup_function(func):
    arcovid19.CACHE.clear()


# =============================================================================
# TESTING
# =============================================================================

def test_SIR_migration():
    expected = pd.read_excel(TEST_DATA_PATH / "df_test_SIR_migration.xlsx")
    expected = expected.set_index("ts")
    expected.index = expected.index.astype(float)

    curve_conf = {
        'population': 600000,
        'N_init': 10,
        'R': 1.2,
        'intervention_start': 15.0,
        'intervention_end': 25.0,
        'intervention_decrease': 70.0,
        't_incubation': 5.0,
        't_infectious': 9.0}
    sir_conf = {'t_max': 200.0, 'dt': 1.0}

    curve = arcovid19.load_infection_curve(**curve_conf)
    result = curve.do_SIR(**sir_conf)

    np.testing.assert_array_almost_equal(result, expected, decimal=8)


def test_SEIR_migration():
    expected = pd.read_excel(TEST_DATA_PATH / "df_test_SEIR_migration.xlsx")
    expected = expected.set_index("ts")
    expected.index = expected.index.astype(float)

    curve_conf = {
        'population': 600000,
        'N_init': 10,
        'R': 1.2,
        'intervention_start': 15.0,
        'intervention_end': 25.0,
        'intervention_decrease': 70.0,
        't_incubation': 5.0,
        't_infectious': 9.0}
    seir_conf = {'t_max': 200.0, 'dt': 1.0}

    curve = arcovid19.load_infection_curve(**curve_conf)
    result = curve.do_SEIR(**seir_conf)

    np.testing.assert_array_almost_equal(result, expected, decimal=8)


def test_SEIRF_migration():
    expected = pd.read_excel(TEST_DATA_PATH / "df_test_SEIRF_migration.xlsx")
    expected = expected.set_index("ts")
    expected.index = expected.index.astype(float)

    curve_conf = {
        'population': 600000,
        'N_init': 10,
        'R': 1.2,
        'intervention_start': 15.0,
        'intervention_end': 25.0,
        'intervention_decrease': 70.0,
        't_incubation': 5.0,
        't_infectious': 9.0}
    seirf_conf = {'t_max': 200.0, 'dt': 1.0}

    curve = arcovid19.load_infection_curve(**curve_conf)
    result = curve.do_SEIRF(**seirf_conf)

    np.testing.assert_array_almost_equal(result, expected, decimal=8)
