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

"""Test suite

"""


# =============================================================================
# IMPORTS
# =============================================================================

import os
import pathlib
import tempfile
import io

import pytest

import numpy as np

import pandas as pd

import arcovid19


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))


# =============================================================================
# SETUP
# =============================================================================

def setup_function(func):
    arcovid19.CACHE.clear()


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def webclient():
    app = arcovid19.web.create_app()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['WTF_CSRF_METHODS'] = []  # This is the magic

    with app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


# =============================================================================
# TEST INDEX
# =============================================================================

def test_web_index(webclient):
    index_response = webclient.get("/")
    icurve_response = webclient.get("/icurve")

    assert index_response.status_code == 200
    assert icurve_response.status_code == 200
    assert index_response.data == icurve_response.data


def test_web_post_icurve(webclient):
    data = {
        'population': 600000, 'N_init': 10, 'R': 1.2,
        'intervention_start': 15, 'intervention_end': 25,
        'intervention_decrease': 70.0, 't_incubation': 5, 't_infectious': 9,
        't_death': 32.0, 'mild_recovery': 11.0, 'bed_stay': 28.0,
        'bed_rate': 0.2, 'bed_wait': 5, 'beta': 1.236, 'sigma': 1.1,
        'gamma': 1.1, 't_max': 200, 'dt': 1.0}

    response = webclient.post('/icurve', data=data)
    assert response.status_code == 200
    assert "field-error" not in str(response.data)


def test_web_missing_data_post_icurve(webclient):
    conf = {
        'population': 600000, 'N_init': 10, 'R': 1.2,
        'intervention_start': 15, 'intervention_end': 25,
        'intervention_decrease': 70.0, 't_incubation': 5, 't_infectious': 9,
        't_death': 32.0, 'mild_recovery': 11.0, 'bed_stay': 28.0,
        'bed_rate': 0.2, 'bed_wait': 5, 'beta': 1.236, 'sigma': 1.1,
        'gamma': 1.1, 't_max': 200, 'dt': 1.0}

    for rk in conf.keys():
        data = {k: v for k, v in conf.items() if k != rk}
        post_response = webclient.post('/icurve', data=data)
        assert post_response.status_code == 200
        assert "field-error" in str(post_response.data)

        get_response = webclient.get('/icurve', data=data)
        assert get_response.status_code == 200
        assert "field-error" not in str(get_response.data)


def test_web_download_data(webclient):
    curve_conf = {
        'population': 600000, 'N_init': 10, 'R': 1.2,
        'intervention_start': 15, 'intervention_end': 25,
        'intervention_decrease': 70.0, 't_incubation': 5, 't_infectious': 9,
        't_death': 32.0, 'mild_recovery': 11.0, 'bed_stay': 28.0,
        'bed_rate': 0.2, 'bed_wait': 5, 'beta': 1.236, 'sigma': 1.1,
        'gamma': 1.1}
    sir_conf = {'t_max': 200, 'dt': 1.0}

    curve = arcovid19.load_infection_curve(**curve_conf)
    expected = curve.do_SIR(**sir_conf)

    data = {"model": "do_SIR"}
    data.update(curve_conf)
    data.update(sir_conf)
    response = webclient.post('/download_model', data=data)

    ectype = (
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    assert response.status_code == 200
    assert response.headers["Content-Type"] == ectype

    # validate result
    result = pd.read_excel(io.BytesIO(response.data), sheet_name="Data")
    result = result.set_index("ts")

    # validate in the 8 decimal place
    np.testing.assert_array_almost_equal(result, expected.df, decimal=8)

    config = pd.read_excel(io.BytesIO(response.data), sheet_name="Config")
    config = config.set_index("Attribute")

    assert config.to_dict()["Value"] == data
