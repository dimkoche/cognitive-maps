# coding: utf-8
import json
import web

import config

from helpers.lsat import draw
from models.map import Map, MapException

t_globals = dict(
    datestr=web.datestr,
    str=str,
    sort=sorted,
    xrange=xrange,
    ctx=web.web_session
)
render = web.template.render('templates/', cache=config.cache, globals=t_globals)
render._keywords['globals']['render'] = render


def is_editable(map, data):
    if 'map' in web.web_session and web.web_session.map == map.hash:
        return True
    if 'key' in data.keys():
        if data.key == str(map.passkey):
            web.web_session.map = map.hash
            return True
    return False


def show_map(map, editable=False):
    if editable:
        raise web.seeother('/map/show/%s?key=%s' % (map.hash, map.passkey))
    raise web.seeother('/map/show/%s' % map.hash)


class Index:
    def GET(self):
        return render.base(render.main(), 'home')


class About:
    def GET(self):
        return render.base(render.about(), 'about')


class MapAdd:
    def POST(self):
        data = web.input()
        email = data.mapEmail
        title = data.mapTitle
        if not email:
            raise web.seeother('/')

        m = Map(email=email, title=title)
        show_map(m, editable=True)


class MapShow:
    def GET(self, hash):
        data = web.input()
        try:
            m = Map(hash=hash)
        except MapException:
            raise web.seeother('/')
        if not m.id:
            raise web.seeother('/')
        enabled = is_editable(m, data)
        return render.base(render.map.show(m, enabled))


class MapAddFactor:
    def POST(self):
        data = web.input()
        hash = data.mapHash
        factor = data.factorName
        if not hash:
            raise web.seeother('/')

        try:
            m = Map(hash=hash)
        except MapException:
            raise web.seeother('/')

        if not factor:
            show_map(m)

        editable = is_editable(m, data)
        if editable:
            m.add_factor(factor)
        show_map(m, editable)


class MapChangeFactor:
    def POST(self):
        data = web.input()
        hash = data.map
        f1 = data.f1
        f2 = data.f2
        effect = data.effect
        if not hash:
            return json.dumps({'success': False, 'error': 'Incorrect data'})

        try:
            m = Map(hash=hash)
        except MapException:
            return json.dumps({'success': False, 'error': 'Incorrect data'})

        if not f1 or not f2:
            return json.dumps({'success': False, 'error': 'Incorrect data'})

        editable = is_editable(m, data)
        if editable:
            m.change_factor_effect(f1, f2, effect)
            return json.dumps({'success': True})
        return json.dumps({'success': False, 'error': 'Access denied'})


class MapChangeKoef:
    def POST(self):
        data = web.input()
        hash = data.map
        f = data.f
        koef = data.koef
        if not hash:
            return json.dumps({'success': False, 'error': 'Incorrect data'})

        try:
            m = Map(hash=hash)
        except MapException:
            return json.dumps({'success': False, 'error': 'Incorrect data'})

        if not f:
            return json.dumps({'success': False, 'error': 'Incorrect data'})

        editable = is_editable(m, data)
        if editable:
            m.change_koef(f, koef)
            return json.dumps({'success': True})
        return json.dumps({'success': False, 'error': 'Access denied'})


class MapGetChartData:
    def GET(self):
        data = web.input()
        hash = data.map
        if not hash:
            raise web.seeother('/')

        try:
            m = Map(hash=hash)
        except MapException:
            raise web.seeother('/')

        data = m.get_chart_data()
        if not data:
            return json.dumps({'success': False})
        return json.dumps({'success': True, 'data': data})
