#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020, Bruno Sanchez, Mauricio Koraj, Vanessa Daza,
#                     Juan B Cabral, Mariano Dominguez, Marcelo Lares,
#                     Nadia Luczywo, Dante Paz, Rodrigo Quiroga,
#                     Martín de los Ríos, Federico Stasyszyn,
#                     Cristian Giuppone.
# License: BSD-3-Clause
#   Full Text: https://raw.githubusercontent.com/ivco19/libs/master/LICENSE


# =============================================================================
# DOCS
# =============================================================================

"""Core functionalities for arcovid19

"""

__all__ = ["wavid19"]


# =============================================================================
# IMPORTS
# =============================================================================

import io
import datetime as dt

import jinja2

import matplotlib.pyplot as plt

import flask
from flask.views import View

from ..models import load_infection_curve
from . import forms


# =============================================================================
# BASE CLASS
# =============================================================================

class TemplateView(View):

    def get_template_name(self):
        return self.template_name

    def get_context_data(self):
        return {}

    def render_template(self, context):
        return flask.render_template(self.get_template_name(), **context)

    def dispatch_request(self):
        context = self.get_context_data()
        return self.render_template(context)


# =============================================================================
# VIEWS
# =============================================================================

class InfectionCurveView(TemplateView):

    methods = ['GET', 'POST']
    template_name = "InfectionCurve.html"

    def subplots(self):
        return plt.subplots(frameon=False, figsize=(12, 8))

    def get_img(self, fig):
        buf = io.StringIO()

        fig.tight_layout()
        fig.savefig(buf, format='svg')
        svg = buf.getvalue()
        buf.close()

        return jinja2.Markup(svg)

    def make_plots(self, result):
        fig_linear, ax_linear = self.subplots()
        result.plot(ax=ax_linear, fill=.05)

        fig_log, ax_log = self.subplots()
        result.plot(ax=ax_log, log=True)

        return {
            "Linear": self.get_img(fig_linear),
            "Log": self.get_img(fig_log)
        }

    def get_context_data(self):
        context_data = {}

        form = forms.InfectionCurveForm()
        if form.validate_on_submit():
            # get all the data as string
            data = form.data.copy()

            # extract the model method name
            method_name = data.pop("model")

            # instantiate the curve
            curve = load_infection_curve(**data)

            # extract the method
            method = getattr(curve, method_name)

            # get the result
            result = method()

            # create the plots
            context_data["plots"] = self.make_plots(result)

            # add the results to the context
            context_data["result"] = result

        context_data["form"] = form
        return context_data


class DownloadView(InfectionCurveView):

    methods = ['POST']
    content_type = (
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def dispatch_request(self):
        context_data = self.get_context_data()
        result = context_data["result"]

        now = dt.datetime.now().isoformat()
        fname = f"arcovid19_{result.model_name}_{now}.xlsx"

        fileobj = io.BytesIO()
        result.to_excel(fileobj)

        response = flask.make_response(fileobj.getvalue())
        response.headers.set('Content-Type', self.content_type)
        response.headers.set(
            'Content-Disposition', 'attachment', filename=fname)

        return response


# =============================================================================
# Blueprint
# =============================================================================

wavid19 = flask.Blueprint("arcovid19", "arcovid19.web.bp")

wavid19.add_url_rule(
    '/', view_func=InfectionCurveView.as_view("index"))
wavid19.add_url_rule(
    '/icurve', view_func=InfectionCurveView.as_view("icurve"))
wavid19.add_url_rule(
    '/download_model', view_func=DownloadView.as_view("download_model"))