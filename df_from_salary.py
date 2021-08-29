# -*- coding: utf-8 -*-
"""
Created on Sun Aug 15 12:57:25 2021

@author: HP
"""

import glassdor_scrapper as gs
import pandas as pd

num_jobs = 800
keyword = 'data scientist'
driver_path = 'chromedriver'
sleep_time = 10
df = gs.get_jobs(keyword, num_jobs, False, driver_path, sleep_time)

df.to_csv('job_data.csv')