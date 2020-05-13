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

"""WTF Forms for arcovid19

"""


# =============================================================================
# IMPORTS
# =============================================================================

import flask_wtf as fwtf

import wtforms as wtf
from wtforms.fields import html5
import wtforms.validators as vldt

import attr

from numpydoc import docscrape

from ..models import InfectionCurve


# =============================================================================
# CUSTOM FIELD
# =============================================================================

class FloatField(wtf.FloatField):
    widget =  wtf.widgets.html5.NumberInput()


# =============================================================================
# CONSTANTS
# =============================================================================

PYTYPE_TO_WTF = {
    bool: wtf.BooleanField,
    int: html5.IntegerField,
    str: wtf.StringField,
    float: FloatField,
}

DEFAULT_VALIDATORS = [vldt.InputRequired()]

# =============================================================================
# INFECTION FORM
# =============================================================================

def make_InfectionCurveForm():

    # form metaclass
    Meta = type("Meta", (object,), {"csrf": False})

    # here gone all the fields
    form_fields = {"Meta": Meta}

    # this gonna store all the model choices
    models = []
    for mname, method in vars(InfectionCurve).items():
        if mname.startswith("do_") and callable(method):
            label = mname.split("_", 1)[-1]
            models.append((mname, label))

    # add the model select to the form
    form_fields["model"] = wtf.SelectField(
        'Model',
        choices=models,
        description="Compartmental model.",
        render_kw={"class": "custom-select custom-select-sm"},
        default=models[0][0])

    # extract all the fields doc from the class documentation
    class_docs = docscrape.ClassDoc(InfectionCurve)
    docs = {
        p.name.split(":")[0]: " ".join(p.desc).strip()
        for p in class_docs.get("Parameters")}

    # create one field for attribute
    for aname, afield in attr.fields_dict(InfectionCurve).items():
        # extract doc
        description = docs.get(aname)

        # extract the label from the field name
        label = " ".join(aname.split("_")).title()

        # add all the validators
        validators = list(DEFAULT_VALIDATORS)

        # add the classes to the field element
        render_kw = {"class": "form-control form-control-sm"}

        # determine the field type
        Field = PYTYPE_TO_WTF.get(afield.type, wtf.StringField)

        # create the field
        ffield = Field(
            label,
            description=description,
            default=afield.default,
            validators=validators,
            render_kw=render_kw)
        form_fields[aname] = ffield

    # create the form itself
    form = type("InfectionCurveForm", (fwtf.FlaskForm,), form_fields)
    return form


InfectionCurveForm = make_InfectionCurveForm()

del make_InfectionCurveForm
