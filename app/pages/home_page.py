from h2o_wave import ui, Q
from .layout import render_template
from .utilities import *

async def home_page(q, details=None):

    # build registered user card 
    # user_details = get_handles()
    # personas = [ui.inline([ui.persona(title=r[0], subtitle=r[2], size='s', name=str(r[1]), image=r[3]),
    #                         ui.button(name='view_user', label='view', icon='View', value=r[1])], justify='between') for r in user_details]
    # search_box = [ui.inline([ui.textbox(name='searching_user', label='Search User' ), ui.button(name='search', label='Search')], justify='around')]
    # handles_card = ui.form_card(
    #     box=ui.box('content_1', order=1, width='100%', height='700px'),
    #     items=search_box+[ui.text_m(content='Select User :'),]+personas,
    # )
    page1_frame = gen_card({
        'topic': 'Search Option #1',
        'desc': 'Search by Concept & Object that used for Metaphors To get popular use in metaphor and form of interpretation ...',
        'btn_name': 'go_page1',
        'btn_label': 'Search'
    })

    page2_frame = gen_card({
        'topic': 'Search Option #2',
        'desc': 'Search by your Song-Idea To get popular Songs written with similar focus ...',
        'btn_name': 'go_page2',
        'btn_label': 'Search'
    })

    page3_frame = gen_card({
        'topic': 'Search Option #3',
        'desc': 'Search by a Word or a Phrase to get all the songs that composites of the word ... ',
        'btn_name': 'go_page3',
        'btn_label': 'Search'
    })

    cfg = {
        'tag': 'home',
        'items': [ui.text("Home Page")],
        'page1_frame': page1_frame,
        'page2_frame': page2_frame,
        'page3_frame': page3_frame,
    }
    await render_template(q, cfg)

def gen_card(cfg):
    frame = ui.form_card(
        box=ui.box('content_1', order=1, width='100%', height='195px'),
        items=[
            ui.text_xl(cfg['topic']),
            ui.text(cfg['desc']),
            ui.buttons([ui.button(name=cfg['btn_name'], label=cfg['btn_label'], primary=True, icon='Search')], justify='end'),
        ]
    )
    return frame



