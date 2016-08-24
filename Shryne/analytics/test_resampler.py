#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def test_sentiment_cleaning():
    """Where neutral = 1 or if +ve, -ve
        and neutral = 0 then replace with nan"""

    sent = pd.DataFrame({'neutral' : [1,0,1.000001,0.999999,1.0]})