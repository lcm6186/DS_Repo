# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 14:55:49 2022

@author: Luke Morris
"""

import pandas as pd
import numpy as np

def upcCoder(upc_list):
    """
    upcCoder takes in a list of UPCs within a dataframe and adds the leading 
    0's, to a 12-digit UPC
    
    Parameters
    ----------
    df : TYPE, optional
        DESCRIPTION. The default is df.

    Returns
    -------
    df : TYPE
        DESCRIPTION.

    """
    upc_list = upc_list.astype(str)
    UPC12 = []

    for upc in upc_list:
        UPC12.append(upc.zfill(12))
    
    return UPC12