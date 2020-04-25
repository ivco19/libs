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

"""Core functionalities for arcovid19

"""

__all__ = ["Frame", "Plotter"]


# =============================================================================
# IMPORTS
# =============================================================================

import logging

import attr


# =============================================================================
# CONSTANTS
# =============================================================================

logger = logging.getLogger("arcovid19.core")


# =============================================================================
# CASES
# =============================================================================

@attr.s(repr=False)
class Plotter:

    cstats = attr.ib()

    def __repr__(self):
        return f"CasesPlot({hex(id(self.cstats))})"

    def __call__(self, plot_name=None, ax=None, **kwargs):
        """x.__call__() == x()"""
        plot_name = plot_name or ""

        if plot_name.startswith("_"):
            raise ValueError(f"Invalid plot_name '{plot_name}'")

        plot = getattr(self, plot_name, self.grate_full_period_all)
        ax = plot(ax=ax, **kwargs)
        return ax


@attr.s(repr=False)
class Frame:

    df = attr.ib()
    plot = attr.ib(init=False)

    @plot.default
    def _plot_default(self):
        plot_cls = self.plot_cls
        return plot_cls(cstats=self)

    def __dir__(self):
        """x.__dir__() <==> dir(x)"""
        return super().__dir__() + dir(self.df)

    def __repr__(self):
        """x.__repr__() <==> repr(x)"""
        return repr(self.df)

    def __getattr__(self, a):
        """x.__getattr__(y) <==> x.y

        Redirect all te missing calls to the internal datadrame.

        """
        return getattr(self.df, a)

    def __getitem__(self, k):
        """x.__getitem__(y) <==> x[y]"""
        return self.df.__getitem__(k)
