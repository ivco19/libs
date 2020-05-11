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

import pytest

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import arcovid19


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

TEST_DATA_PATH = PATH / "data"

TEST_PLOTS_PATH = PATH / "plots"


# =============================================================================
# SETUP
# =============================================================================

def setup_function(func):
    arcovid19.CACHE.clear()


# =============================================================================
# TESTING
# =============================================================================

def test_SIR_migration():
    expected = pd.read_excel(TEST_DATA_PATH / "test_SIR_migration.xlsx")
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

    np.testing.assert_array_almost_equal(result.df, expected, decimal=8)
    assert result.model_name == "SIR"


def test_SEIR_migration():
    expected = pd.read_excel(TEST_DATA_PATH / "test_SEIR_migration.xlsx")
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

    np.testing.assert_array_almost_equal(result.df, expected, decimal=8)
    assert result.model_name == "SEIR"


def test_SEIRF_migration():
    expected = pd.read_excel(TEST_DATA_PATH / "test_SEIRF_migration.xlsx")
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

    np.testing.assert_array_almost_equal(result.df, expected, decimal=8)
    assert result.model_name == "SEIRF"


# =============================================================================
# PLOT TEST
# =============================================================================

# separados por que son mucho mas lentos y es bueno dehabilitarlos

@pytest.mark.mpl_image_compare(baseline_dir=str(TEST_PLOTS_PATH))
def test_SIR_plot_migration():
    expected = pd.read_excel(TEST_DATA_PATH / "test_SIR_migration.xlsx")
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

    fig, ax = plt.subplots()
    result.plot(ax=ax, only=["I", "C", "R"], fill=True, log=True)

    return fig


@pytest.mark.mpl_image_compare(baseline_dir=str(TEST_PLOTS_PATH))
def test_SEIR_plot_migration():
    expected = pd.read_excel(TEST_DATA_PATH / "test_SEIR_migration.xlsx")
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
    result = curve.do_SEIR(**sir_conf)

    fig, ax = plt.subplots()
    result.plot(ax=ax, only=["S", "E", "I", "R"], fill=True, log=True)

    return fig


@pytest.mark.mpl_image_compare(baseline_dir=str(TEST_PLOTS_PATH))
def test_SEIRF_plot_migration():
    expected = pd.read_excel(TEST_DATA_PATH / "test_SEIRF_migration.xlsx")
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
    result = curve.do_SEIRF(**sir_conf)

    fig, ax = plt.subplots()
    result.plot(ax=ax, only=["S", "E", "I", "R", "F"], fill=True, log=True)

    return fig
