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

import pytest

import numpy as np

import pandas as pd

from matplotlib.testing.decorators import check_figures_equal

import arcovid19
from arcovid19.cases import LABEL_DATE_FORMAT


# =============================================================================
# CONSTANTS
# =============================================================================

PATH = pathlib.Path(os.path.abspath(os.path.dirname(__file__)))

LOCAL_CASES = PATH.parent / "databases" / "cases.xlsx"

LOCAL_AREA_POP = PATH.parent / "databases" / "extra" / "arg_provs.dat"


# =============================================================================
# SETUP
# =============================================================================

def setup_function(func):
    arcovid19.CACHE.clear()


# =============================================================================
# INTEGRATION
# =============================================================================

# @pytest.mark.integtest
# def test_load_cases_remote():
#     local = arcovid19.load_cases(url=LOCAL_CASES)
#     local = local[local.dates]
#     local[local.isnull()] = 143

#     remote = arcovid19.load_cases()
#     remote = remote[remote.dates]
#     remote[remote.isnull()] = 143

#     assert np.all(local == remote)


# =============================================================================
# UNITEST
# =============================================================================

def test_load_cases_local():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)
    assert isinstance(df, arcovid19.cases.CasesFrame)


def test_delegation():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)

    assert repr(df) == repr(df.df)
    assert df.transpose == df.df.transpose


def test_areapop():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)
    assert np.all(df.areapop == df.extra["areapop"])


def test_dates():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)
    assert isinstance(df.dates, list)


def test_totcases():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)
    assert isinstance(df.tot_cases, float)


def test_last_grate():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)
    assert isinstance(df.last_growth_rate(), float)


def test_full_grate():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)
    assert isinstance(df.grate_full_period(), pd.Series)


def test_full_grate_provincias():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)
    for name, code in arcovid19.cases.PROVINCIAS.items():
        wname = df.grate_full_period(provincia=name)
        wcode = df.grate_full_period(provincia=code)
        assert isinstance(wname, pd.Series)
        assert isinstance(wcode, pd.Series)


def test_grate_provincias():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)
    for name, code in arcovid19.cases.PROVINCIAS.items():
        wname = df.last_growth_rate(provincia=name)
        wcode = df.last_growth_rate(provincia=code)

        if np.isnan(wname):
            assert np.isnan(wcode)
        else:
            assert wname == wcode


def test_grate_provincia_invalida():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)
    with pytest.raises(ValueError):
        df.last_growth_rate(provincia="colorado")


def test_get_item():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)
    value = df[df.provincia_status == "CBA_C"]
    expected = df.df[df.provincia_status == "CBA_C"]
    assert np.all(value == expected)


def test_restore_time_serie():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)
    tsdf = df.restore_time_serie()
    for prov in arcovid19.cases.PROVINCIAS.values():
        for code in arcovid19.cases.STATUS.values():
            orig_row = df.loc[(prov, code)][df.dates].values
            ts = tsdf.loc[(prov, code)][df.dates].values
            assert np.all(ts.cumsum() == orig_row)


# =============================================================================
# PLOTS
# =============================================================================

def test_invalid_plot_name():
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)
    with pytest.raises(ValueError):
        df.plot("_plot_df")


@check_figures_equal()
def test_plot_call(fig_test, fig_ref):
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot(ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.curva_epi_pais(ax=exp_ax)


@check_figures_equal()
def test_plot_curva_epi_pais(fig_test, fig_ref):
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot("curva_epi_pais", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.curva_epi_pais(ax=exp_ax)


@check_figures_equal()
def test_plot_grate_full_period(fig_test, fig_ref):
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot("grate_full_period", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.grate_full_period(ax=exp_ax)


@check_figures_equal()
def test_plot_time_serie_all(fig_test, fig_ref):
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot("time_serie_all", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.time_serie_all(ax=exp_ax)


@check_figures_equal()
def test_plot_time_serie(fig_test, fig_ref):
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot("time_serie", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.time_serie(ax=exp_ax)


@check_figures_equal()
def test_plot_time_serie_all_equivalent_calls(fig_test, fig_ref):
    cases = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)

    # fig test
    fig_test.set_size_inches(12, 12)
    test_ax = fig_test.subplots()
    cases.plot.time_serie_all(ax=test_ax)
    test_ax.set_title("")

    # expected
    fig_ref.set_size_inches(12, 12)
    exp_ax = fig_ref.subplots()

    cases.plot.time_serie(
        deceased=False, active=False, recovered=False, ax=exp_ax)
    for prov in sorted(arcovid19.cases.CODE_TO_POVINCIA):
        cases.plot.time_serie(
            prov, deceased=False, active=False, recovered=False, ax=exp_ax)

    exp_ax.set_title("")


@check_figures_equal()
def test_plot_barplot(fig_test, fig_ref):
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot("barplot", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.barplot(ax=exp_ax)


@check_figures_equal()
def test_plot_boxplot(fig_test, fig_ref):
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)

    # fig test
    test_ax = fig_test.subplots()
    test_ax = df.plot("boxplot", ax=test_ax)

    # expected
    exp_ax = fig_ref.subplots()
    df.plot.boxplot(ax=exp_ax)


# =============================================================================
# BUGS
# =============================================================================

@pytest.mark.parametrize(
    "plot_name", ["time_serie", "time_serie_all"])
def test_plot_all_dates_ticks(plot_name):
    df = arcovid19.load_cases(
        cases_url=LOCAL_CASES, areas_pop_url=LOCAL_AREA_POP)

    expected = [d.strftime(LABEL_DATE_FORMAT) for d in df.dates]
    ax = df.plot(plot_name)
    labels = [tlabel.get_text() for tlabel in ax.get_xticklabels()]
    ticks = ax.get_xticks()

    assert len(labels) == len(ticks)
    assert labels == expected
