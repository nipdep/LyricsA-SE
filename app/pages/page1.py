from h2o_wave import ui, site, data
from datetime import datetime
from .layout import render_template
from .utilities import *

# ==========================================================================
# ====================== Page-1 Query Handling =============================

def page1_reader(q, details=None):
    data = {'q': q.args._q,
            'domain': q.args._opt1,
            'n': q.args._opt2} 
    return data 


# ==========================================================================
# ======================= Page-1 Rendering =================================

def page1_search_box(q, details=None):
    items = [
        # ui.text_l("Search Query"),
        ui.textbox(name='_q', label='Query', icon='Play', spellcheck=True, placeholder='General Domain used in Metaphor'),
        ui.inline([
            ui.choice_group(name='_opt1', label='Domain Type', choices=[
                ui.choice(name=x, label=x) for x in ['Subject-Domain', 'Object-Domain']
            ], required=True, inline=True, value='Subject-Domain'),
            ui.spinbox(name='_opt2', label='# records ', min=0, max=25, step=1, value=0, width='20px', trigger=False)
        ], justify='around'),
        ui.buttons([ui.button(name='page1_search', label='Search', primary=True, icon='DocumentSearch')], justify='center')
    ]
    card = ui.form_card(
        box=ui.box('content_11', order=0, height='210px'),
        items=items
    )
    return card

def page1_side_bar(q, details=None):
    try:
        # print('record data >> ', q.client.record_data1['all_data'])
        songs = q.client.record_data1['all_data']['Song']
        stat_cards = [
            ui.stat_list_item(label=i, name=f'SP1-{i}', icon='CodeEdit', icon_color='blue')
            for i in songs
        ]
        card = ui.stat_list_card(
            box=ui.box('content_0', order=0),
            title='Songs',
            items = stat_cards
        )
    except:
        card = ui.form_card(box=ui.box('content_0'), items=[])
    return card

def page1_stats(q, details=None):
    try:
        time_s = q.client.record_data1['time']
        card1 = ui.small_stat_card(
            box=ui.box('content_12', order=0, width='214px', height='75px'),
            title='WithIn',
            value=f"{time_s:.2f}s"
        )

        records = q.client.record_data1['#records']
        card2 = ui.small_stat_card(
            box=ui.box('content_12', order=0, width='214px', height='75px'),
            title='Returns',
            value=f"{records} songs"   
        )

        singers = q.client.record_data1['#records']
        card3 = ui.small_stat_card(
            box=ui.box('content_12', order=0, width='214px', height='75px'),
            title='Of',
            value=f"{singers} singers"
        )

        writers = q.client.record_data1['#writers']
        card4 = ui.small_stat_card(
            box=ui.box('content_12', order=0, width='214px', height='75px'),
            title="By",
            value=f"{writers} writers"
        )

        composers = q.client.record_data1['#composers']
        card5 = ui.small_stat_card(
            box=ui.box('content_12', order=0, width='214px', height='75px'),
            title="For",
            value=f"{composers} composers" 
        )

        card_list = [card1, card2, card3, card4, card5]
    except:
        card_list = []
    return card_list
    

def page1_content(q, details=None):
    song_name = q.client.page1_song 
    # print('Song name >> ', song_name)
    if song_name != None:
        song_data = get_song(q, song_name)
        # print('Song data >> ', song_data)
        en_lyrics = song_data['Lyrics in english']
        sh_lyrics = song_data['Lyrics in sinhala']
        html = f"""
<table class="GeneratedTable">
  <thead>
    <tr>
      <th>Lyrics in English : </th>
      <th>Lyrics in Sinhala : </th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>{en_lyrics}</td>
      <td>{sh_lyrics}</td>
    </tr>
  </tbody>
</table>
"""
        card = ui.form_card(
            box=ui.box('content_12', order=1, width='100%'),
            items=[
                ui.inline([
                    ui.text_l('Song Title : '),
                    ui.text_m(song_data['title'])
                ]),
                ui.markup(content=html),
                ui.inline([
                    ui.text_l('Singer : '),
                    ui.text_m(song_data['Singer'] if song_data.get('Singer') != None else '-')
                ]),
                ui.inline([
                    ui.text_l('Writer : '),
                    ui.text_m(song_data['Lyrics'] if song_data.get('Lyrics') != None else '-')
                ]),
                ui.inline([
                    ui.text_l('Composer : '),
                    ui.text_m(song_data['Music'] if song_data.get('Music') != None else '-')
                ]),
            ]
        )
    
    else:
        card = ui.form_card(box=ui.box('content_12'), items=[])

    return card

def page1_topic_corr(q, details=None):
    try:
        # print('All data > ', q.client.record_data1['all_data'])
        all_data = q.client.record_data1['all_data']
        items = []

        query_domain = q.client.details['domain']
        if query_domain == 'Subject-Domain':
            domains = all_data['Object_English']
        else:
            domains = all_data['Subject_English']

        wrt_n = 2
        domain_cards = [
            ui.buttons([ui.button(name=m, label=m, disabled=True, visible=True, width='100%') for m in domains[i:i + wrt_n]], width='100%')
            for i in range(0, len(domains), wrt_n)
        ]
        items.append(ui.text_l("Popular Domains"))
        items.extend(domain_cards)
        items.append(ui.separator(label='+'))

        topics, freq = get_frequency(all_data['Topic'], normalized=True)
        topics_card = [
            ui.slider(name=t, label=t, value=round(freq[i], 2), min=0, max=1, step=0.001, disabled=True, trigger=False, width='100%')
            for i,t in enumerate(topics)
        ]
        items.append(ui.text_l("Topic Popularity"))
        items.extend(topics_card)

        card = ui.form_card(
            box=ui.box('content_0', order=1),
            items=items
        )

        return card
    except:
        return ui.form_card(box=ui.box('content_0'), items=[])

def page1_advance_data(q, details=None):
    try:
        all_data = q.client.record_data1['all_data']
        metaphors = all_data['Metaphor']
        writers = list(set(all_data['Writer']))
        singers = list(set(all_data['Singer']))
        items = []

        meta_n = 2
        metaphor_cards = [ 
            ui.buttons([ui.button(name=m, label=m, disabled=True, visible=True, width='100%', icon='FocalPoint') for m in metaphors[i:i + meta_n]], width='100%')
            for i in range(0, len(metaphors), meta_n)
        ]
        items.append(ui.text_l("Metaphors"))
        items.extend(metaphor_cards)
        items.append(ui.separator(label='+'))

        wrt_n = 3
        writers_cards = [
            ui.buttons([ui.button(name=m, label=m, disabled=True, visible=True, width='100%', icon='EditContact') for m in writers[i:i + wrt_n]], width='100%')
            for i in range(0, len(writers), wrt_n)
        ]
        items.append(ui.text_l("Writers"))
        items.extend(writers_cards)
        items.append(ui.separator(label='+'))

        singers_cards = [
            ui.buttons([ui.button(name=m, label=m, disabled=True, visible=True, width='100%', icon='ContactHeart') for m in singers[i:i + wrt_n]], width='100%')
            for i in range(0, len(writers), wrt_n)
        ]
        items.append(ui.text_l("Singers"))
        items.extend(singers_cards)

        card = ui.form_card(
            box=ui.box('content_12', order=1),
            items=items
        )

        return card
    except:
        return ui.form_card(box=ui.box('content_12'), items=[])


async def page1_loader(q, details=None):

    # get search option
    search_card = page1_search_box(q, details)

    # get side bar card 
    side_card = page1_side_bar(q, details)

    # get query search status cards 
    st_cards = page1_stats(q, details)

    # get advance stats
    adv_card = page1_advance_data(q, details)

    # get topic correlations 
    topic_corr = page1_topic_corr(q, details)

    # get song content 
    content_card = page1_content(q, details)

    cfg = {
        'tag': 'search',
        'side': side_card,
        'head': search_card,
        'st_cards': st_cards,
        'adv_stat': adv_card,
        'topic_freq': topic_corr,
        'content': content_card,
    }
    await render_template(q, cfg)

# ==========================================================================
# ===================== Page-1 Functionalities =============================

def page1_qeury_processor(q, details=None):
    data = q.client.details
    if data['domain'] == 'Subject-Domain':
        opt = 'Annotation.Subject-english'
    else:
        opt = 'Annotation.Object-english'

    q = {"match": {opt: data['q']}}

    t1 = datetime.now()
    resp = query_search(q, data['n'])
    t2 = datetime.now()
    # search information
    delta_t = (t2-t1).total_seconds()
    records = len(resp)

    # response post-processing 
    all_data, all_annotation = get_all_data(resp)

    try:
        singerC = len(set(list(zip(*all_data['Singer']))[0]))
    except:
        singerC = 0
    
    try:
        writerC = len(set(list(zip(*all_data['Writer']))[0]))
    except:
        writerC = 0

    try:
        composerC = len(set(list(zip(*all_data['Musician']))[0]))
    except:
        composerC = 0

    result = {
        # search data
        'time': delta_t,
        '#records': records,
        '#singers': singerC,
        '#writers': writerC,
        '#composers': composerC,
        # search result data
        'primary_data': [i['_source'] for i in resp],
        'all_data': all_data,
        'annotations': all_annotation
    }
    return result

def get_song(q, name):
    data = q.client.record_data1['primary_data']
    for r in data:
        if r['title'] == name:
            return r 
    else:
        return {}
