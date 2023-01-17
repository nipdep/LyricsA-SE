from heapq import nsmallest
from turtle import width
from h2o_wave import Q, app, ui, data

config = {
    "app_title": "LyricsA`SE",
    "sub_title": "Metaphor based Advance Songs' Lyrics Search Engine",
    "footer_text": 'Copyright 2023 @nipdep',
}


async def initialize_app(q):
    q.user.font_color = '#fec827'
    q.user.primary_color = '#fec827'
    q.page['meta'] = ui.meta_card(box='')
    if q.user.config is None:
        q.user.config = config
        q.user.default_config = config
        q.client.selected_tab = 'home_tab'

    if q.user.logo is None:
        q.user.logo, = await q.site.upload(['static/logo.jpg'])
        q.user.logo_height = '50'

    if q.app.illustration is None:
        q.app.illustration, = await q.site.upload(['static/ill3.jpg'])
        q.user.logo_height = '50'

    q.user.init = True


def create_layout(q: Q, tag=None):
    config = q.user.config
    q.page.drop()

    q.page['header'] = ui.header_card(
        box='header',
        title=config['app_title'],
        subtitle=config['sub_title'],
        icon='TFVCLogo',
        icon_color='#222',
        items=[
            ui.button(name='home_tab', label=' ', icon='Home', primary=True, width='40px'),
            ui.button(name='about_tab', label=' ', icon='info', primary=True, width='40px'),
            ui.button(name='setting_tab', label=' ', icon='Settings', primary=True, width='40px'),
            ui.text(
                """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">
                """
            ),
            # ui.text("<img src='"+q.user.logo+"' width='" + str(q.user.logo_height)+"px'>"),
        ],
    )
    # nav_items = 
    if q.client.generate_dashboard:
        nav_items += [
            ui.tab(name='#', label='', icon='BulletedListBulletMirrored'),
            ui.tab(name='dashboard_tab', label='Dashboard', icon='Processing'),
        ]

    q.page['footer'] = ui.footer_card(
        box='footer', caption=config['footer_text'])

    zones = ui.zone(name='content', zones=[ui.zone(
        name='content_0', size='650px', direction='row')])
    if tag in ['feature']:
        zones = ui.zone(name='content', zones=[
            ui.zone(name='content_0', size='600px', direction='row'),
            ui.zone(name='content_1', size='500px', direction='row'),

        ])
    elif tag == 'setting':
        zones = ui.zone(name='content', zones=[
            ui.zone(name='content_1', size='300px', direction='row'),
            ui.zone(name='content_0', size='80px', direction='row'),

        ])
    elif tag in 'search':
        zones = ui.zone(name='content', direction='row', #size='560px', 
            zones=[
                ui.zone(name='content_0', size='25%', direction='column'),
                ui.zone(name='content_1', size='75%', direction='column', zones=[
                    ui.zone(name='content_11'),
                    ui.zone(name='content_12', direction='row', wrap='between')
                ])
            ])

    elif tag == 'home':
        # zones = ui.zone(name='content_0', size='650px')
        zones = ui.zone(name='content', direction='row', #size='560px', 
            zones=[
                ui.zone(name='content_0', size='70%', direction='column',),
                ui.zone(name='content_1', size='30%', direction='row', wrap='between')
            ])

    else:
        print(tag)
        pass

    inline_styling = """
table.GeneratedTable {
  width: 100%;
  background-color: #e9f5f7;
  border-collapse: collapse;
  border-width: 2px;
  border-color: #e9f5f7;
  border-style: dotted;
  color: #000000;
}

table.GeneratedTable td, table.GeneratedTable th {
  border-width: 2px;
  border-color: #91bbf2;
  border-style: dotted;
  padding: 3px;
  font-weight: 400;
  white-space: pre-line;
}

table.GeneratedTable thead {
  background-color: #e9f5f7;
  font-family: Inter;
  font-size: 18px;
  font-weight: 400;
  color: rgb(0, 0, 0);
}    
"""

    q.page['meta'] = ui.meta_card(box='',
                                  themes=[
                                    ui.theme(
                                        name='cdark',
                                        primary=q.user.primary_color,
                                        text=q.user.font_color,
                                        card='#000',
                                        page='#1b1d1f',
                                    ),
                                    ui.theme(
                                        name='ixdlabs_twitter',
                                        primary='#0c0882',
                                        text='#000000',
                                        card='#e9f5f7',
                                        page='#cbd4d3',
                                    )
                                  ],
                                  theme='ixdlabs_twitter',
                                  stylesheet=ui.inline_stylesheet(inline_styling),
                                  title=config['app_title'] + '| H2O Wave',
                                  # stylesheet=ui.inline_stylesheet(style),
                                  layouts=[
                                      ui.layout(
                                          breakpoint='l',
                                          width='1600px',
                                          zones=[
                                              ui.zone(name='header', size='75px', direction='row'),
                                            #   ui.zone(
                                                #   name='navbar', size='90px', direction='row'),
                                              zones,
                                              ui.zone('footer'),
                                          ])
                                  ])

async def render_template(q: Q, page_cfg):
    create_layout(q, tag=page_cfg['tag'])

    if page_cfg['tag'] == 'home':
        caption = """<div style='width:70%;margin-left:15%'>"""
        caption += """Search Engine designed for Song Writers to improve the elocution and fluidity of poetry.
        Advance Metaphor based searching results influence beauty of the poem.
		"""
        # caption += f"<br><br><img src='{q.app.caption}' width='80%' height='200px'>"
        caption += "<br><hr></div>"
        q.page['content_left'] = ui.tall_info_card(
            box=ui.box(zone='content_0', height='620px'),
            name='launch_app',
            title=config["app_title"],
            caption=caption,
            category=config["sub_title"],
            label='',
            image=q.app.illustration,
            image_height='280px'
        )
        # q.page['content_01'] = page_cfg['handles_card']
        q.page['content_01'] = page_cfg['page1_frame']
        q.page['content_02'] = page_cfg['page2_frame']
        q.page['content_03'] = page_cfg['page3_frame']
    elif page_cfg['tag'] == 'about':
        q.page['content_00'] = ui.form_card(box=ui.box(
            zone='content_0', width='100%', order=1), title='', items=[])

    elif page_cfg['tag'] == 'dashboard':
        q.page['content_00'] = ui.form_card(box=ui.box(
            zone='content_0', width='100%', order=1), title='', items=[])

    elif page_cfg['tag'] == 'setting':
        q.page['content_01'] = ui.section_card(box=ui.box(
            zone='content_0'), title='', subtitle='', items=page_cfg['save_buttons'])
        q.page['content_10'] = ui.form_card(box=ui.box(
            zone='content_1', width='40%', order=1), title='', items=page_cfg['setting_items'])
        q.page['content_11'] = ui.form_card(box=ui.box(
            zone='content_1', width='30%', order=2), title='', items=page_cfg['upload_items'])
        q.page['content_12'] = ui.form_card(box=ui.box(
            zone='content_1', width='30%', order=3), title='', items=page_cfg['color_picker_items'])

    elif page_cfg['tag'] == 'search':
        q.page['block_0'] = page_cfg['side']
        q.page['block_1'] = page_cfg['head']
        for i, c in enumerate(page_cfg['st_cards'],1):
            q.page[f'block_{i*21}'] = c
        q.page['block_2'] = page_cfg['content']
        q.page['block_3'] = page_cfg['adv_stat']
        q.page['block_4'] = page_cfg['topic_freq']
    await q.page.save()