#!/usr/bin/env python3.7 
"""Parser of data tables"""

import os
from datetime import datetime
import numpy as np 
import pandas as pd 

from provincias import provincias as pcias
from provincias import status

TABLA_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTfinng5SDBH9RSJMHJk28dUlW3VVSuvqaBSGzU-fYRTVLCzOkw1MnY17L2tWsSOppHB96fr21Ykbyv/pub?output=xls"


def parse_urltable(taburl=TABLA_URL, tabshape='wide'):
    """
    Utility function to parse Excel table from specific URL.

    Parameters
    ----------

    taburl: string
        The url for the excel table to parse. Default is ivco19 team table

    tabshape: string, 'wide' or 'long'
        The format of the table. If wide, dates are going to be columns.
        If in turn, long, dates are going to be rows, regions are going to be columns.
        Under the hood is callin df.transpose() method from Pandas.

    
    Returns
    -------

    df_infar: Pandas.DataFrame object

        A table parsing the Excel file spreadsheet 0 (called BD).
        It features a pandas multi index, with the following hierarchy:
            level 0: cod_provincia  -  Argentina states
            level 1: cod_status  -  Four states of disease patients (R, C, A, D)
    """
    #load table and replace Nan by zeros
    df_infar = pd.read_excel(taburl, sheet_name=0, nrows=96).fillna(0)
    
    # Parsear provincias en codigos standard
    df_infar.rename(columns={'Provicia \\ día': 'Pcia_status'}, inplace=True)
    for irow, arow in df_infar.iterrows():
        pst = arow['Pcia_status'].split()
        stat = status.get(pst[-1])
        if stat is None:
            print(stat, pst[-1], 'stopped 0')
            break
        pcia = pst[:-2]
        if len(pcia)>1:
            provincia = ''
            for ap in pcia:
                provincia += ap + ' '
            provincia = provincia.strip()
        else:
            provincia = pcia[0].strip()
        provincia_code = pcias.get(provincia)

        df_infar.loc[irow, 'cod_provincia'] = provincia_code
        df_infar.loc[irow, 'cod_status'] = stat
        df_infar.loc[irow, 'provincia_status'] = provincia_code+'_'+stat

    # reindex table with multi-index
    index = pd.MultiIndex.from_frame(df_infar[['cod_provincia', 'cod_status']])
    df_infar.index = index

    # drop duplicate columns
    df_infar.drop(columns=['cod_status', 'cod_provincia'], inplace=True)
    cols = list(df_infar.columns)
    df_infar = df_infar[[cols[-1]]+cols[:-1]]

    # calculate the total number per categorie per state, and the global 
    for astatus in np.unique(df_infar.index.get_level_values(1)):
        filter_confirmados = df_infar.index.get_level_values('cod_status').isin([astatus])
        sums = df_infar[filter_confirmados].sum(axis=0)
        dates = [adate for adate in sums.index if isinstance(adate, datetime)]
        df_infar.loc[('ARG', astatus), dates] = sums[dates].astype(int)

        df_infar.loc[('ARG', astatus), 'provincia_status'] = 'ARG_'+astatus

    n_c = df_infar.loc[('ARG', 'C'), dates].values
    growth_rate_C = (n_c[1:]/n_c[:-1])-1
    df_infar.loc[('ARG', 'growth_rate_C'), dates[1:]] = growth_rate_C

    # transpose if wide format
    if tabshape=='wide':
        return(df_infar)
    elif tabshape=='long':
        return(df_infar.transpose())
    else:
        print('returning wide and long table')
        return(df_infar, df_infar.transpose())

if __name__=='__main__':

    print(parse_urltable())