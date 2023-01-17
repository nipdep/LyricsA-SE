# Song IR Application
#     __Version__ : 0.1
#     __Last_updated__ : 14/01/2022
# 

import os 
import sys 
from datetime import datetime, date, timedelta
from h2o_wave import Q, app, ui, data, main, on, handle_on, core

from .pages.layout import * 
from .pages.home_page import home_page #, add_handle, setup_handle
from .pages.setting_page import setting_page
from .pages.about_page import about_page
from .pages.page1 import *
from .pages.page2 import *
from .pages.page3 import *
from .utils import * 

import warnings
warnings.filterwarnings("ignore")

@app('/')
async def serve(q: Q):
    print(q.args)

    query_dict = core.expando_to_dict(core.clone_expando(q.args))
    # cmd_list = ['preview_card-0']
    # for c in q.args:
    #     if c in cmd_list:
    #         print(c)

    details = {'status': 'default'}
    if q.args.reset:
        q.user.init = False

    # if q.client.theme_dark == None:
    #     q.client.theme_dark = True

    if q.user.init != True:
        details = {'status': 'default'}
        last_q = ''
        await initialize_app(q)
    else:
        last_q = list(query_dict.keys())[-1]

    if q.args.home_tab:
        q.args.tabs = 'home_tab'

    if q.args.go_page1:
        q.args.tabs = 'page1'
    elif q.args.go_page2:
        q.args.tabs = 'page2'
    elif q.args.go_page3:
        q.args.tabs = 'page3'

    if q.args.page1_search:
        q.args.tabs = 'page1'
        query_data = page1_reader(q, details)
        q.client.details = query_data
        q.client.record_data1 = page1_qeury_processor(q, details)
        songs = q.client.record_data1['all_data']['Song']
        if songs != []:
            q.client.page1_song = songs[0]   
        else:
            q.client.page1_song = None    
    elif q.args.page2_search:
        q.args.tabs = 'page2'
        query_data = page2_reader(q, details)
        q.client.details = query_data
        q.client.record_data2 = page2_qeury_processor(q, details)
        songs = q.client.record_data2['all_data']['Song']
        if songs != []:
            q.client.page2_song = songs[0]   
        else:
            q.client.page2_song = None  
    elif q.args.page3_search:
        q.args.tabs = 'page3'
        query_data = page3_reader(q, details)
        q.client.details = query_data
        q.client.record_data3 = page3_qeury_processor(q, details)
        songs = q.client.record_data3['all_data']['Song']
        if songs != []:
            q.client.page3_song = songs[0]   
        else:
            q.client.page3_song = None  
    
    
    if last_q[:3] == 'SP1' :
        page1_song = last_q.split('-')[-1]
        q.args.tabs = 'page1'
        q.client.page1_song = page1_song
    elif last_q[:3] == 'SP2' :
        page2_song = last_q.split('-')[-1]
        q.args.tabs = 'page2'
        q.client.page2_song = page2_song
    elif last_q[:3] == 'SP3' :
        page3_song = last_q.split('-')[-1]
        q.args.tabs = 'page3'
        q.client.page3_song = page3_song


    if q.args.tabs == 'about_tab':
        await about_page(q, details)
    elif q.args.tabs == 'home_tab':
        await home_page(q, details)
    elif q.args.tabs == 'page1':
        await page1_loader(q, details)
    elif q.args.tabs == 'page2':
        await page2_loader(q, details)
    elif q.args.tabs == 'page3':
        await page3_loader(q, details)
    else:
        await home_page(q, details)

    await q.page.save()