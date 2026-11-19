#!/usr/bin/env python3
"""Regenerate the osipov.uk preview pages from the shared template.

Shared inputs:  template.html, hub-template.html, styles.css, writing.json,
                content/<version>.html
Outputs:        index.html (hub) and <version>/index.html for each entry below.

Add a variant: add an entry to VERSIONS and a content/<name>.html fragment,
run `python3 build.py`, commit the result. Update writing: edit writing.json
(verified public records only: canonical URL, exact displayed title and date),
run `python3 build.py`, commit.
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
ORDER = ['advisory', 'corporate', 'executive', 'media']

VERSIONS = {'advisory': {'title': 'Igor Osipov — Technology adviser to boards and executive teams', 'description': 'Independent technology advice for boards and executive teams: investment decisions, transformation and AI, from a former global systems head, board director and deputy CEO.', 'nav': '\n      <a href="#experience">Experience</a>\n      <a href="#writing">Writing</a>\n      <a href="#interviews">Interviews</a>\n      <a href="#contact">Contact</a>\n    ', 'kicker': 'Board and executive technology advice', 'lede': 'I help boards and executive teams decide where technology investment will improve the business, what needs to change, and what should be left alone.', 'proof': 'I act as a non-executive director and adviser for corporations under NDA. Earlier, board director and deputy CEO of an international logistics group, and Global Head of System Development for Contract Logistics at Kuehne+Nagel, responsible for the systems used by 25,000 people across 370 sites in 51 countries.', 'ctas': '\n        <a class="btn" href="mailto:consult@osipov.uk">Discuss a business challenge</a>\n        <a class="btn ghost" href="#experience">See my experience</a>\n      ', 'banner': '<div class="highlight">\n  <div class="wrap">\n    <span class="tag">Latest</span>\n    <span>New interview: NVIDIA, Anthropic and whether AI is a bubble, on И Грянул Грэм (in Russian). <a href="{{ROOT}}media/">Watch and read more</a></span>\n  </div>\n</div>', 'label': 'Version 1 · default', 'hub_title': 'Board and executive advisory', 'hub_blurb': 'For chairs, board members and CEOs who need independent judgement on technology investment, transformation and AI.', 'writing': {'heading': 'Writing', 'sub': 'Recent articles and posts. New pieces appear first on <a href="https://www.linkedin.com/in/igorosipov/">LinkedIn</a>.', 'items': ['nvidia', 'pl', 'data', 'post'], 'blurb': True}}, 'corporate': {'title': 'Igor Osipov — Technology advisory for CIOs, CTOs and their sponsors', 'description': 'Independent advice for technology leaders and their sponsors: delivery improvement, programme review, integration and practical AI adoption.', 'nav': '\n      <a href="#experience">Experience</a>\n      <a href="#writing">Writing</a>\n      <a href="#interviews">Interviews</a>\n      <a href="#contact">Contact</a>\n    ', 'kicker': 'Technology advisory for CIOs, CTOs and their sponsors', 'lede': 'I work with technology leaders, and the executives who fund them, when delivery needs to improve or a programme needs an honest review.', 'proof': 'Former Global Head of System Development for Contract Logistics at Kuehne+Nagel, board director and deputy CEO of an international logistics group. Now an adviser to corporations under NDA.', 'ctas': '\n        <a class="btn" href="mailto:consult@osipov.uk">Start a conversation</a>\n        <a class="btn ghost" href="#experience">See my experience</a>\n      ', 'banner': '<div class="highlight">\n  <div class="wrap">\n    <span class="tag">Latest</span>\n    <span>New interview: NVIDIA, Anthropic and whether AI is a bubble, on И Грянул Грэм (in Russian). <a href="{{ROOT}}media/">Watch and read more</a></span>\n  </div>\n</div>', 'label': 'Version 2', 'hub_title': 'Corporate technology advisory', 'hub_blurb': 'For CIOs, CTOs and their sponsors: delivery that needs to improve, programmes that need an honest review, AI that needs a business case.', 'writing': {'heading': 'Writing', 'sub': 'Recent articles and posts. New pieces appear first on <a href="https://www.linkedin.com/in/igorosipov/">LinkedIn</a>.', 'items': ['nvidia', 'pl', 'data', 'post'], 'blurb': True}}, 'executive': {'title': 'Igor Osipov — Executive profile', 'description': 'Technology and transformation executive: formerly Global Head of System Development at Kuehne+Nagel, then board director and deputy CEO of an international logistics group.', 'nav': '\n      <a href="#scope">Leadership scope</a>\n      <a href="#history">Career history</a>\n      <a href="#writing">Writing</a>\n      <a href="#contact">Contact</a>\n    ', 'kicker': 'Executive profile', 'lede': 'Technology and transformation executive. I lead the systems, budgets and teams that complex operations depend on, and the change programmes that replace them.', 'proof': 'Non-executive director and adviser for corporations under NDA. Former Global Head of System Development for Contract Logistics at Kuehne+Nagel, then board director and deputy CEO of an international logistics group. More than twenty years in enterprise technology, from hands-on engineering to the boardroom.', 'ctas': '\n        <a class="btn" href="mailto:consult@osipov.uk">Get in touch</a>\n        <a class="btn ghost" href="https://www.linkedin.com/in/igorosipov/">LinkedIn profile</a>\n      ', 'banner': '<div class="highlight">\n  <div class="wrap">\n    <span class="tag">Latest</span>\n    <span>New interview: NVIDIA, Anthropic and whether AI is a bubble, on И Грянул Грэм (in Russian). <a href="{{ROOT}}media/">Watch and read more</a></span>\n  </div>\n</div>', 'label': 'Version 3', 'hub_title': 'Executive appointments', 'hub_blurb': 'For executive search and hiring leaders: profile, leadership scope and career history, with a CV route.', 'writing': {'heading': 'Writing and interviews', 'sub': 'How I think, in my own words. New pieces appear first on <a href="https://www.linkedin.com/in/igorosipov/">LinkedIn</a>.', 'items': ['nvidia', 'pl', 'data', 'grem'], 'blurb': False}}, 'media': {'title': 'Igor Osipov — Interviews and commentary', 'description': 'Interviews, writing and commentary from Igor Osipov on AI, technology investment and enterprise transformation.', 'nav': '\n      <a href="#interviews">Interviews</a>\n      <a href="#topics">Topics</a>\n      <a href="#writing">Writing</a>\n      <a href="#contact">Contact</a>\n    ', 'kicker': 'Interviews and commentary', 'lede': 'I explain what technology decisions actually mean for businesses: AI investment, platform change, and where the money really goes.', 'proof': 'Non-executive director and adviser for corporations under NDA. Former Global Head of System Development for Contract Logistics at Kuehne+Nagel and deputy CEO of an international logistics group. More than twenty years in enterprise technology.', 'ctas': '\n        <a class="btn" href="mailto:consult@osipov.uk">Invite for an interview or comment</a>\n        <a class="btn ghost" href="https://www.linkedin.com/in/igorosipov/">LinkedIn</a>\n      ', 'banner': '<div class="highlight">\n  <div class="wrap">\n    <span class="tag">Latest</span>\n    <span>New interview: NVIDIA, Anthropic and whether AI is a bubble, on И Грянул Грэм (in Russian). <a href="#interviews">Watch below</a></span>\n  </div>\n</div>', 'label': 'Version 4', 'hub_title': 'Media and commentary', 'hub_blurb': 'Interviews, writing and speaking topics, anchored on the latest И Грянул Грэм interview.', 'writing': {'heading': 'Writing', 'sub': 'Recent articles and posts. New pieces appear first on <a href="https://www.linkedin.com/in/igorosipov/">LinkedIn</a>.', 'items': ['nvidia', 'pl', 'data', 'post'], 'blurb': True}}}
def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

def render_writing(cfg, items_by_id, vname):
    L = ['<section id="writing">', '  <div class="wrap">',
         f'    <h2>{cfg["heading"]}</h2>',
         f'    <p class="sub">{cfg["sub"]}</p>']
    for iid in cfg['items']:
        it = items_by_id[iid]
        L.append('    <div class="item">')
        L.append(f'      <p class="meta">{esc(it["kind"])} · {esc(it["date"])}</p>')
        L.append(f'      <a class="title" href="{it["url"]}">{esc(it["title"])}</a>')
        if cfg['blurb']:
            b = it.get('blurb', {}).get(vname) or it.get('blurb', {}).get('default')
            if b:
                L.append(f'      <p>{esc(b)}</p>')
        L.append('    </div>')
    L += ['  </div>', '</section>']
    return '\n'.join(L)

def main():
    template = (ROOT / 'template.html').read_text()
    hub_tpl = (ROOT / 'hub-template.html').read_text()
    feed = json.loads((ROOT / 'writing.json').read_text())
    items_by_id = {it['id']: it for it in feed['items']}
    cards = []
    for name in ORDER:
        v = VERSIONS[name]
        page = template
        for key in ('TITLE', 'DESCRIPTION', 'NAV', 'KICKER', 'LEDE', 'PROOF',
                    'CTAS', 'BANNER'):
            page = page.replace('{{' + key + '}}', v[key.lower()])
        frag = (ROOT / 'content' / f'{name}.html').read_text()
        writing = render_writing(v['writing'], items_by_id, name)
        page = page.replace('{{SECTIONS}}', frag.replace('{{WRITING}}', writing))
        page = page.replace('{{ROOT}}', '../')
        d = ROOT / name
        d.mkdir(exist_ok=True)
        (d / 'index.html').write_text(page)
        cards.append((name, v))
    card_html = '\n' + '\n'.join(
        '      <a class="card version-card" href="%s/">\n'
        '        <p class="live">%s</p>\n'
        '        <h3>%s</h3>\n'
        '        <p>%s</p>\n'
        '      </a>' % (name, v['label'], v['hub_title'], v['hub_blurb'])
        for name, v in cards) + '\n    '
    (ROOT / 'index.html').write_text(hub_tpl.replace('{{CARDS}}', card_html))
    print('built:', ', '.join(['index.html'] + [n + '/index.html' for n in ORDER]))

if __name__ == '__main__':
    main()
