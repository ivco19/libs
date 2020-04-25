#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Bruno Sanchez, Mauricio Koraj, Vanessa Daza,
#                     Juan B Cabral, Mariano Dominguez, Marcelo Lares,
#                     Nadia Luczywo, Dante Paz, Rodrigo Quiroga,
#                     Martín de los Ríos, Federico Stasyszyn
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/libs/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Utilities to Utility function to parse all the actual cases of the
COVID-19 in Argentina.

"""

__all__ = [
    "CODE_TO_POVINCIA",
    "D0", "Q1",
    "CasesPlot",
    "CasesFrame",
    "load_cases"]


# =============================================================================
# IMPORTS
# =============================================================================

import datetime as dt
import itertools as it

import logging

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

import unicodedata

from . import cache, core


# =============================================================================
# CONSTANTS
# =============================================================================

CASES_URL = "https://github.com/ivco19/libs/raw/master/databases/cases.xlsx"


AREAS_POP_URL = 'https://github.com/ivco19/libs/raw/master/databases/extra/arg_provs.dat'  # noqa


DATE_FORMAT = '%m/%d/%y'


PROVINCIAS = {
    'CABA': 'CABA',
    'Bs As': 'BA',
    'Córdoba': 'CBA',
    'San Luis': 'SL',
    'Chaco': 'CHA',
    'Río Negro': 'RN',
    'Santa Fe': 'SF',
    'Tierra del F': 'TF',
    'Jujuy': 'JY',
    'Salta': 'SAL',
    'Entre Ríos': 'ER',
    'Corrientes': 'COR',
    'Santiago Est': 'SDE',
    'Neuquen': 'NQ',
    'Mendoza': 'MDZ',
    'Tucumán': 'TUC',
    'Santa Cruz': 'SC',
    'Chubut': 'CHU',
    'Misiones': 'MIS',
    'Formosa': 'FOR',
    'Catamarca': 'CAT',
    'La Rioja': 'LAR',
    'San Juan': 'SJU',
    'La Pampa': 'LPA'}


# this alias fixes the original typos
PROVINCIAS_ALIAS = {
    'Tierra del Fuego': "TF",
    'Neuquén': "NQ",
    "Santiago del Estero": "SDE"
}

#: List of Argentina provinces
CODE_TO_POVINCIA = {
    v: k for k, v in it.chain(PROVINCIAS.items(), PROVINCIAS_ALIAS.items())}

STATUS = {
    'Recuperado': 'R',
    'Recuperados': 'R',
    'Confirmados': 'C',
    'Confirmado': 'C',
    'Activos': 'A',
    'Muertos': 'D'}


#: Pandemia Start 2020-03-11
D0 = dt.datetime(year=2020, month=3, day=11)


#:  Argentine quarantine starts 2020-03-20
Q1 = dt.datetime(year=2020, month=3, day=20)


logger = logging.getLogger("arcovid19.cases")


# =============================================================================
# FUNCTIONS_
# =============================================================================

def safe_log(array):
    """Convert all -inf to 0"""
    with np.errstate(divide='ignore'):
        res = np.log(array.astype(float))
    res[np.isneginf(res)] = 0
    return res


# =============================================================================
# CASES
# =============================================================================

class CasesPlot(core.Plotter):

    def _plot_df(
        self, *, odf, prov_name, prov_code,
        confirmed, active, recovered, deceased, norm=1.
    ):

        columns = {}
        if confirmed:
            cseries = odf.loc[(prov_code, 'C')][self.cstats.dates].values
            columns[f"{prov_name} Confirmed"] = cseries / norm
        if active:
            cseries = odf.loc[(prov_code, 'A')][self.cstats.dates].values
            columns[f"{prov_name} Active"] = cseries / norm
        if recovered:
            cseries = odf.loc[(prov_code, 'R')][self.cstats.dates].values
            columns[f"{prov_name} Recovered"] = cseries / norm
        if deceased:
            cseries = odf.loc[(prov_code, 'D')][self.cstats.dates].values
            columns[f"{prov_name} Deceased"] = cseries / norm
        pdf = pd.DataFrame(columns)
        return pdf

    def grate_full_period_all(
        self, ax=None, argentina=True,
        exclude=None, **kwargs
    ):

        kwargs.setdefault("confirmed", True)
        kwargs.setdefault("active", False)
        kwargs.setdefault("recovered", False)
        kwargs.setdefault("deceased", False)

        exclude = [] if exclude is None else exclude

        if ax is None:
            ax = plt.gca()
            fig = plt.gcf()

            height = len(PROVINCIAS) - len(exclude) - int(argentina)
            height = 4 if height <= 0 else (height)

            fig.set_size_inches(12, height)

        if argentina:
            self.grate_full_period(provincia=None, ax=ax, **kwargs)

        exclude = [] if exclude is None else exclude
        exclude = [self.cstats.get_provincia_name_code(e)[1] for e in exclude]

        for code in sorted(CODE_TO_POVINCIA):
            if code in exclude:
                continue
            self.grate_full_period(provincia=code, ax=ax, **kwargs)

        labels = [d.date() for d in self.cstats.dates]
        ticks = np.arange(len(labels))

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=labels, rotation=45)

        ax.set_title(
            "COVID-19 Grow in Argentina by Province\n"
            f"{labels[0]} - {labels[-1]}")
        ax.set_xlabel("Date")
        ax.set_ylabel("N")

        return ax

    def grate_full_period_all_commented(
        self, ax=None, argentina=True,
        exclude=None, log=False, **kwargs
    ):
        """
        method: grate_full_period_all_commented()

        This function plots the time series, similar to grate_full_period_all,
        but including a second axis and comments about the start of quarantine

        """

        kwargs.setdefault("confirmed", True)
        kwargs.setdefault("active", False)
        kwargs.setdefault("recovered", False)
        kwargs.setdefault("deceased", False)

        exclude = [] if exclude is None else exclude

        if ax is None:
            ax = plt.gca()
            fig = plt.gcf()

            height = len(PROVINCIAS) - len(exclude) - int(argentina)
            height = 4 if height <= 0 else (height)

            fig.set_size_inches(12, height)

        if argentina:
            self.grate_full_period(provincia=None, ax=ax, **kwargs)

        exclude = [] if exclude is None else exclude
        exclude = [self.cstats.get_provincia_name_code(e)[1] for e in exclude]

        for code in sorted(CODE_TO_POVINCIA):
            if code in exclude:
                continue
            self.grate_full_period(provincia=code, ax=ax, **kwargs)

        labels = [d.date() for d in self.cstats.dates]

        ispace = int(len(labels) / 10)
        ticks = np.arange(len(labels))[::ispace]
        slabels = [l.strftime("%d.%b") for l in labels][::ispace]
        lmin, lmax = labels[0].strftime("%d.%b"), labels[-1].strftime("%d.%b")

        t = np.array([(dd - D0).days for dd in self.cstats.dates])

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=slabels, rotation=0, fontsize=16)
        ax.set_title(
            "COVID-19 Grow in Argentina by Province, between "
            f"{lmin} and {lmax}", fontsize=16)
        ax.set_xlabel("Date", fontsize=16)
        ax.set_ylabel("Cumulative number of cases", fontsize=16)
        ax.tick_params(axis='x', direction='in', length=8)

        if log:
            ax.set(yscale='log')

        # add a second axis
        ax2 = ax.twiny()
        ax2.set_xlim(min(t), max(t))
        ax2.set_xlabel(
            "days from pandemic declaration", fontsize=16, color='blue')

        d_ini = (Q1 - D0).days
        d_fin = ax2.get_xlim()[1]

        ax2.axvspan(d_ini, d_fin, alpha=0.1, color='yellow')

        ax2.tick_params(
            axis='x', direction='in', length=10, pad=-28,
            color='blue', labelcolor='blue', labelsize=16)

        return ax

    def full_period_normalized(
        self, ax=None, argentina=True,
        exclude=None, log=False, **kwargs
    ):
        """
        method: full_period_normalized()

        This function plots the time series, similar to grate_full_period_all,
        but including a second axis and comments about the start of quarantine

        """

        kwargs.setdefault("confirmed", True)
        kwargs.setdefault("active", False)
        kwargs.setdefault("recovered", False)
        kwargs.setdefault("deceased", False)
        exclude = [] if exclude is None else exclude
        if ax is None:
            ax = plt.gca()
            fig = plt.gcf()
            height = len(PROVINCIAS) - len(exclude) - int(argentina)
            height = 4 if height <= 0 else (height)
            fig.set_size_inches(12, height)
        if argentina:
            self.grate_full_period(provincia=None, ax=ax, **kwargs)
        exclude = [] if exclude is None else exclude
        exclude = [self.cstats.get_provincia_name_code(e)[1] for e in exclude]
        for code in sorted(CODE_TO_POVINCIA):
            if code in exclude:
                continue
            self.grate_full_period(provincia=code, ax=ax, **kwargs)

        labels = [d.date() for d in self.cstats.dates]
        ispace = int(len(labels) / 10)
        ticks = np.arange(len(labels))[::ispace]
        slabels = [l.strftime("%d.%b") for l in labels][::ispace]
        lmin, lmax = labels[0].strftime("%d.%b"), labels[-1].strftime("%d.%b")

        t = np.array([(dd - D0).days for dd in self.cstats.dates])

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=slabels, rotation=0, fontsize=16)
        ax.set_title(
            "COVID-19 Grow in Argentina by Province, between "
            f"{lmin} and {lmax}", fontsize=16)
        ax.set_xlabel("Date", fontsize=16)
        ax.set_ylabel("Cumulative number of cases", fontsize=16)
        ax.tick_params(axis='x', direction='in', length=8)
        if log:
            ax.set(yscale='log')

        # add a second axis
        ax2 = ax.twiny()
        ax2.set_xlim(min(t), max(t))
        ax2.set_xlabel(
            "days from pandemic declaration", fontsize=16, color='blue')

        d_ini = (Q1 - D0).days
        d_fin = ax2.get_xlim()[1]

        ax2.axvspan(d_ini, d_fin, alpha=0.1, color='yellow')
        ax2.tick_params(
            axis='x', direction='in', length=10, pad=-28,
            color='blue', labelcolor='blue', labelsize=16)

        return ax

    def grate_full_period(
        self, provincia=None, confirmed=True,
        active=True, recovered=True, deceased=True,
        ax=None, log=False, norm=False, **kwargs
    ):
        if provincia is None:
            prov_name, prov_c = "Argentina", "ARG"
        else:
            prov_name, prov_c = self.cstats.get_provincia_name_code(provincia)

        # READ PROVINCES DATA
        areapop = self.ctats.areapop
        population = areapop['pop'][areapop['key'] == prov_c].values[0]

        norm_factor = (population / 1.e6) if norm else 1.
        ax = plt.gca() if ax is None else ax

        pdf = self._plot_df(
            odf=self.cstats.df, prov_name=prov_name, prov_code=prov_c,
            confirmed=confirmed, active=active,
            recovered=recovered, deceased=deceased, norm=norm_factor)
        pdf.plot.line(ax=ax, **kwargs)
        labels = [d.date() for d in self.cstats.dates]
        ticks = np.arange(len(labels))
        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=labels, rotation=45)
        ax.set_title(
            f"COVID-19 Grow in {prov_name}\n"
            f"{labels[0]} - {labels[-1]}")
        ax.set_xlabel("Date")
        ax.set_ylabel("N")
        ax.legend()
        if log:
            ax.set(yscale='log')
        return ax

    def time_serie_all(
        self, ax=None, argentina=True,
        exclude=None, **kwargs
    ):
        kwargs.setdefault("confirmed", True)
        kwargs.setdefault("active", False)
        kwargs.setdefault("recovered", False)
        kwargs.setdefault("deceased", False)

        exclude = [] if exclude is None else exclude

        if ax is None:
            ax = plt.gca()
            fig = plt.gcf()

            height = len(PROVINCIAS) - len(exclude) - int(argentina)
            height = 4 if height <= 0 else (height)

            fig.set_size_inches(12, height)

        if argentina:
            self.time_serie(provincia=None, ax=ax, **kwargs)

        exclude = [] if exclude is None else exclude
        exclude = [self.cstats.get_provincia_name_code(e)[1] for e in exclude]

        for code in sorted(CODE_TO_POVINCIA):
            if code in exclude:
                continue
            self.time_serie(provincia=code, ax=ax, **kwargs)

        labels = [d.date() for d in self.cstats.dates]
        ticks = np.arange(len(labels))

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=labels, rotation=45)

        ax.set_title(
            "COVID-19 cases by date in Argentina by Province\n"
            f"{labels[0]} - {labels[-1]}")
        ax.set_xlabel("Date")
        ax.set_ylabel("N")

        return ax

    def time_serie(
        self, provincia=None, confirmed=True,
        active=True, recovered=True, deceased=True,
        ax=None, **kwargs
    ):
        if provincia is None:
            prov_name, prov_c = "Argentina", "ARG"
        else:
            prov_name, prov_c = self.cstats.get_provincia_name_code(provincia)

        ax = plt.gca() if ax is None else ax

        ts = self.cstats.restore_time_serie()
        pdf = self._plot_df(
            odf=ts, prov_name=prov_name, prov_code=prov_c,
            confirmed=confirmed, active=active,
            recovered=recovered, deceased=deceased)
        pdf.plot.line(ax=ax, **kwargs)

        labels = [d.date() for d in self.cstats.dates]
        ticks = np.arange(len(labels))

        ax.set_xticks(ticks=ticks)
        ax.set_xticklabels(labels=labels, rotation=45)

        ax.set_title(
            f"COVID-19 cases by date in {prov_name}\n"
            f"{labels[0]} - {labels[-1]}")
        ax.set_xlabel("Date")
        ax.set_ylabel("N")

        ax.legend()

        return ax

    def barplot(
        self, provincia=None, confirmed=True,
        active=True, recovered=True, deceased=True,
        ax=None, **kwargs
    ):
        ax = plt.gca() if ax is None else ax

        if provincia is None:
            prov_name, prov_c = "Argentina", "ARG"
        else:
            prov_name, prov_c = self.cstats.get_provincia_name_code(provincia)

        ts = self.cstats.restore_time_serie()
        pdf = self._plot_df(
            odf=ts, prov_name=prov_name, prov_code=prov_c,
            confirmed=confirmed, active=active,
            recovered=recovered, deceased=deceased)

        pdf.plot.bar(ax=ax, **kwargs)

        ax.set_xlabel("Date")
        ax.set_ylabel("N")

        labels = [d.date() for d in self.cstats.dates]
        ax.set_xticklabels(labels, rotation=45)
        ax.legend()

        return ax

    def boxplot(
        self, provincia=None, confirmed=True,
        active=True, recovered=True, deceased=True,
        ax=None, **kwargs
    ):
        ax = plt.gca() if ax is None else ax

        if provincia is None:
            prov_name, prov_c = "Argentina", "ARG"
        else:
            prov_name, prov_c = self.cstats.get_provincia_name_code(provincia)

        ts = self.cstats.restore_time_serie()
        pdf = self._plot_df(
            odf=ts, prov_name=prov_name, prov_code=prov_c,
            confirmed=confirmed, active=active,
            recovered=recovered, deceased=deceased)
        pdf.plot.box(ax=ax, **kwargs)

        ax.set_ylabel("N")

        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

        return ax


class CasesFrame(core.Frame):
    """Wrapper around the `load_cases()` table.

    This class adds functionalities around the dataframe.

    """

    plot_cls = CasesPlot

    @property
    def dates(self):
        """Returns the dates for which we have data.

        Useful to use as time column (row) list for wide (long) format.

        """
        return [
            adate for adate in self.df.columns
            if isinstance(adate, dt.datetime)]

    @property
    def tot_cases(self):
        """Returns latest value of total confirmed cases"""
        return self.df.loc[('ARG', 'C'), self.dates[-1]]

    def get_provincia_name_code(self, provincia):
        """Resolve and validate the name and code of a given provincia
        name or code.

        """
        def norm(text):
            text = text.lower()
            text = unicodedata.normalize('NFD', text)\
                .encode('ascii', 'ignore')\
                .decode("utf-8")
            return str(text)
        prov_norm = norm(provincia)
        for name, code in PROVINCIAS.items():
            if norm(name) == prov_norm or norm(code) == prov_norm:
                return CODE_TO_POVINCIA[code], code

        for alias, code in PROVINCIAS_ALIAS.items():
            if prov_norm == norm(alias):
                return CODE_TO_POVINCIA[code], code

        raise ValueError(f"Unknown provincia'{provincia}'")

    def restore_time_serie(self):
        """Retrieve a new pandas.DataFrame but with observations
        by Date.
        """
        def _cumdiff(row):
            shifted = np.roll(row, 1)
            shifted[0] = 0
            diff = row - shifted
            return diff

        idxs = ~self.df.index.isin([('ARG', 'growth_rate_C')])
        cols = self.dates

        uncum = self.df.copy()
        uncum.loc[idxs, cols] = uncum.loc[idxs][cols].apply(_cumdiff, axis=1)
        return uncum

    def last_growth_rate(self, provincia=None):
        """Returns the last available growth rate for the whole country
        if provincia is None, or for only the named region.

        """
        return self.grate_full_period(provincia=provincia)[self.dates[-1]]

    def grate_full_period(self, provincia=None):
        """Estimates growth rate for the period where we have data

        """
        # R0 de Arg sí es None
        if provincia is None:
            idx_region = ('ARG', 'growth_rate_C')
            return(self.df.loc[idx_region, self.dates[1:]])

        pcia_code = self.get_provincia_name_code(provincia)[1]

        idx_region = (pcia_code, 'C')

        I_n = self.df.loc[idx_region, self.dates[1:]].values.astype(float)
        I_n_1 = self.df.loc[idx_region, self.dates[:-1]].values.astype(float)

        growth_rate = np.array((I_n / I_n_1) - 1)
        growth_rate[np.where(np.isinf(growth_rate))] = np.nan

        return pd.Series(index=self.dates[1:], data=growth_rate)


def load_cases(url=CASES_URL, force=False):
    """Utility function to parse all the actual cases of the COVID-19 in
    Argentina.


    Parameters
    ----------

    url: str
        The url for the excel table to parse. Default is ivco19 team table.

    force : bool (default=False)
        If you want to ignore the local cache and retrieve a new value.

    Returns
    -------

    CasesFrame: Pandas-DataFrame like object with all the arcovid19 datatabase.

        It features a pandas multi index, with the following hierarchy:

        - level 0: cod_provincia - Argentina states
        - level 1: cod_status - Four states of disease patients (R, C, A, D)

    """
    df_infar = cache.from_cache(
        tag="cases.load_cases", force=force,
        function=pd.read_excel, io=url, sheet_name=0, nrows=96)

    areapop = cache.from_cache(
        tag="cases.load_caces[areapop]", force=force,
        function=pd.read_csv, filepath_or_buffer=AREAS_POP_URL)

    # load table and replace Nan by zeros
    df_infar = df_infar.fillna(0)

    # Parsear provincias en codigos standard
    df_infar.rename(columns={'Provicia \\ día': 'Pcia_status'}, inplace=True)
    for irow, arow in df_infar.iterrows():
        pst = arow['Pcia_status'].split()
        stat = STATUS.get(pst[-1])

        pcia = pst[:-2]
        if len(pcia) > 1:
            provincia = ''
            for ap in pcia:
                provincia += ap + ' '
            provincia = provincia.strip()

        else:
            provincia = pcia[0].strip()

        provincia_code = PROVINCIAS.get(provincia)

        df_infar.loc[irow, 'cod_provincia'] = provincia_code
        df_infar.loc[irow, 'cod_status'] = stat
        df_infar.loc[irow, 'provincia_status'] = f"{provincia_code}_{stat}"

    # reindex table with multi-index
    index = pd.MultiIndex.from_frame(df_infar[['cod_provincia', 'cod_status']])
    df_infar.index = index

    # drop duplicate columns
    df_infar.drop(columns=['cod_status', 'cod_provincia'], inplace=True)
    cols = list(df_infar.columns)
    df_infar = df_infar[[cols[-1]] + cols[:-1]]

    # calculate the total number per categorie per state, and the global
    for astatus in np.unique(df_infar.index.get_level_values(1)):
        filter_confirmados = df_infar.index.get_level_values(
            'cod_status').isin([astatus])
        sums = df_infar[filter_confirmados].sum(axis=0)
        dates = [date for date in sums.index if isinstance(date, dt.datetime)]
        df_infar.loc[('ARG', astatus), dates] = sums[dates].astype(int)

        df_infar.loc[('ARG', astatus), 'provincia_status'] = f"ARG_{astatus}"

    n_c = df_infar.loc[('ARG', 'C'), dates].values
    growth_rate_C = (n_c[1:] / n_c[:-1]) - 1
    df_infar.loc[('ARG', 'growth_rate_C'), dates[1:]] = growth_rate_C

    return CasesFrame(df=df_infar, extra={"areapop": areapop})
