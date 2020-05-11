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

import flask
from flask.views import View

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
    template_name = "InfectionCurve.html"


# =============================================================================
# Blueprint
# =============================================================================

wavid19 = flask.Blueprint("arcovid19", "arcovid19.web.bp")

wavid19.add_url_rule(
    '/', view_func=InfectionCurveView.as_view("index"))
wavid19.add_url_rule(
    '/icurve', view_func=InfectionCurveView.as_view("ivcurve"))




