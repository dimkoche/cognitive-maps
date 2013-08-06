# coding: utf-8
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


class Index:
    def GET(self):
        return render.base(render.main())


class MapAdd:
    def POST(self):
        data = web.input()
        email = data.mapEmail
        title = data.mapTitle
        if not email:
            raise web.seeother('/')

        m = Map(email=email, title=title)
        raise web.seeother('/map/show/%s' % m.hash)


class MapShow:
    def GET(self, hash):
        try:
            m = Map(hash=hash)
        except MapException:
            raise web.seeother('/')
        if not m.id:
            raise web.seeother('/')
        return render.base(render.map.show(m))


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
            raise web.seeother('/map/show/%s' % m.hash)

        m.add_factor(factor)
        raise web.seeother('/map/show/%s' % m.hash)


class MapChangeFactor:
    def POST(self):
        data = web.input()
        hash = data.map
        f1 = data.f1
        f2 = data.f2
        effect = data.effect
        if not hash:
            raise web.seeother('/')

        try:
            m = Map(hash=hash)
        except MapException:
            raise web.seeother('/')

        if not f1 or not f2:
            raise web.seeother('/map/show/%s' % m.hash)

        m.change_factor_effect(f1, f2, effect)
        raise web.seeother('/map/show/%s' % m.hash)


class MapUpdateImage:
    def GET(self):
        data = web.input()
        hash = data.mapHash
        if not hash:
            raise web.seeother('/')

        try:
            m = Map(hash=hash)
        except MapException:
            raise web.seeother('/')

        koef = []
        keys = []
        data = []
        for f1 in m.relations:
            keys.append(f1)
            koef.append(m.koef[f1])
            data.append([float(m.relations[f1][f2]['eff']) / 10 for f2 in m.relations[f1]])

        draw(data, keys, [koef], 'static/maps/%s.png' % m.hash)
        #return keys, data, koef
        raise web.seeother('/map/show/%s' % m.hash)


class MapChangeKoef:
    def POST(self):
        data = web.input()
        hash = data.map
        f = data.f
        koef = data.koef
        if not hash:
            raise web.seeother('/')

        try:
            m = Map(hash=hash)
        except MapException:
            raise web.seeother('/')

        if not f:
            raise web.seeother('/map/show/%s' % m.hash)

        m.change_koef(f, koef)
        raise web.seeother('/map/show/%s' % m.hash)
