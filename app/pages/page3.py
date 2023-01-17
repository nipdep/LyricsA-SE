from h2o_wave import ui, site, data
from .layout import render_template

from .utilities import *

# ==========================================================================
# ====================== Page-2 Query Handling =============================

def page3_reader(q, details=None):
    data = {'q': q.args._q,
            'lang': q.args._opt1} 
    return data 


# ==========================================================================
# ======================= Page-2 Rendering =================================

def page3_search_box(q, details=None):
    items = [
        # ui.text_l("Search Query"),
        ui.textbox(name='_q', label='Search by Word', icon='Play', spellcheck=True, placeholder='A Word or a Phrase', value='ආදරේ'),
        ui.choice_group(name='_opt1', label='Language', choices=[
            ui.choice(name=x, label=x) for x in ['English', 'Sinhala']
        ], required=True, inline=True, value='Sinhala'),
        ui.buttons([ui.button(name='page3_search', label='Search', primary=True, icon='DocumentSearch')], justify='center')
    ]
    card = ui.form_card(
        box=ui.box('content_11', order=0, height='210px'),
        items=items
    )
    return card

def page3_side_bar(q, details=None):
    try:
        # print('record data >> ', q.client.record_data1['all_data'])  # falling love with distance girl, but don't know how to talk to her at least.
        songs = q.client.record_data3['all_data']['Song']
        stat_cards = [
            ui.stat_list_item(label=i, name=f'SP3-{i}', icon='CodeEdit', icon_color='blue')
            for i in songs
        ]
        card = ui.stat_list_card(
            box=ui.box('content_0', order=0),
            title='Song',
            items = stat_cards
        )
    except:
        card = ui.form_card(box=ui.box('content_0'), items=[])
    return card

def page3_stats(q, details=None):
    try:
        time_s = q.client.record_data3['time']
        card1 = ui.small_stat_card(
            box=ui.box('content_12', order=0, width='214px', height='75px'),
            title='WithIn',
            value=f"{time_s:.2f}s"
        )

        records = q.client.record_data3['#records']
        card2 = ui.small_stat_card(
            box=ui.box('content_12', order=0, width='214px', height='75px'),
            title='Returns',
            value=f"{records} songs"   
        )

        singers = q.client.record_data3['#records']
        card3 = ui.small_stat_card(
            box=ui.box('content_12', order=0, width='214px', height='75px'),
            title='Of',
            value=f"{singers} singers"
        )

        writers = q.client.record_data3['#writers']
        card4 = ui.small_stat_card(
            box=ui.box('content_12', order=0, width='214px', height='75px'),
            title="By",
            value=f"{writers} writers"
        )

        composers = q.client.record_data3['#composers']
        card5 = ui.small_stat_card(
            box=ui.box('content_12', order=0, width='214px', height='75px'),
            title="For",
            value=f"{composers} composers"
        )

        card_list = [card1, card2, card3, card4, card5]
    except:
        card_list = []
    return card_list

def page3_content(q, details=None):
    song_name = q.client.page3_song 
    if song_name != None:
        song_data = get_song(q, song_name)
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
            box=ui.box('content_12', order=1),
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

def page3_topic_corr(q, details=None):
    try:
        # print('All data > ', q.client.record_data1['all_data'])
        all_data = q.client.record_data3['all_data']
        object_dom = list(set(all_data['Object_English']))
        subject_dom = list(set(all_data['Subject_English']))
        items = []

        wrt_n = 2
        objects_cards = [
            ui.buttons([ui.button(name=m, label=m, disabled=True, visible=True, width='100%') for m in object_dom[i:i + wrt_n]], width='100%')
            for i in range(0, len(object_dom), wrt_n)
        ]
        items.append(ui.text_l("Object Domains"))
        items.extend(objects_cards)
        items.append(ui.separator(label='+'))

        subject_cards = [
            ui.buttons([ui.button(name=m, label=m, disabled=True, visible=True, width='100%') for m in subject_dom[i:i + wrt_n]], width='100%')
            for i in range(0, len(subject_dom), wrt_n)
        ]
        items.append(ui.text_l("Subject Domains"))
        items.extend(subject_cards)
        items.append(ui.separator(label='+'))

        topics, freq = get_frequency(all_data['Topic'], normalized=True)
        topics_card = [
            ui.slider(name=t, label=t, value=freq[i], min=0, max=1, step=0.001, disabled=True, trigger=False, width='100%')
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

def page3_advance_data(q, details=None):
    try:
        all_data = q.client.record_data3['all_data']
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

async def page3_loader(q, details=None):
    # get search option
    search_card = page3_search_box(q, details)

    # get side bar card 
    side_card = page3_side_bar(q, details)

    # get query search status cards 
    st_cards = page3_stats(q, details)

    # get advance stats
    adv_card = page3_advance_data(q, details)

    # get topic correlations 
    topic_corr = page3_topic_corr(q, details)

    # get song content 
    content_card = page3_content(q, details)

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

def page3_qeury_processor(q, details=None):
    data = q.client.details
    if data['lang'] == 'English':
        opt = 'Lyrics in english'
    else:
        opt = 'Lyrics in sinhala'

    q = {"match": {opt: data['q']}}
    t1 = datetime.now()
    resp = query_search(q)
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
    data = q.client.record_data3['primary_data']
    for r in data:
        if r['title'] == name:
            return r 
    else:
        return {}