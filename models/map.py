# coding: utf-8
import config
import hashlib
import random

DB = config.DB


class MapException(Exception):
    pass


class Map():
    id = None
    email = None
    title = None
    hash = None
    factors = None
    relations = None
    koef = None

    def __init__(self, mid=None, hash=None, email=None, title=None):
        if mid:
            self.id = mid
            self._load_attrs()
        elif hash:
            self.hash = hash
            self._load_attrs()
        elif email:
            m = hashlib.md5('%s' % random.random())
            hash = m.hexdigest()
            if not title:
                title = 'Model #%s' % hash
            self.id = DB.insert(
                'map',
                email=email,
                hash=hash,
                title=title
            )
            if self.id:
                self._load_attrs()
            else:
                raise MapException('Unable to add map')

    def _load_attrs(self):
        if not self.id and not self.hash:
            raise MapException("Can't load map without Id or Hash")

        if self.id:
            vars = {'mid': self.id}
            info = DB.select('map', where="id=$mid", vars=vars)
        else:
            vars = {'hash': self.hash}
            info = DB.select('map', where="hash=$hash", vars=vars)

        if info:
            info = info[0]
            map_id = info['id']
        else:
            raise MapException("Can't load map with vars=%s" % vars)
        factors = DB.select('map_factor', where="map_id=$mid", vars={'mid': map_id})
        sql = """
            SELECT f1, mf1.`name` f1_name,  f2, mf2.`name` f2_name, md.effect FROM map_data md
            JOIN map_factor mf1 ON mf1.id=md.f1
            JOIN map_factor mf2 ON mf2.id=md.f2
            WHERE md.map_id=$mid
        """
        relations = DB.query(sql, vars={'mid': map_id})
        self._set_attrs(info, factors, relations)

    def _set_attrs(self, item, factors, relations):
        self.id = item.id
        self.hash = item.hash
        self.email = item.email
        self.title = item.title
        self.factors = []
        self.relations = {}
        self.koef = {}
        for f in factors:
            self.factors.append(f['name'])
            self.koef[f['name']] = f['koef']
        print self.factors, self.koef
        for r in relations:
            f1 = r['f2_name']
            f2 = r['f1_name']
            effect = r['effect']
            if f1 not in self.relations:
                self.relations[f1] = {}
            self.relations[f1][f2] = {'eff': effect, 'f1': r['f1'], 'f2': r['f2']}

    def get_factors(self):
        return [f for f in self.factors]

    def add_factor(self, factor):
        max_len = 64
        if len(factor) > max_len:
            raise MapException('Factor name is too long (Max name length = %d)' % max_len)

        factor_id = DB.insert(
            'map_factor',
            map_id=self.id,
            name=factor
        )
        self._load_attrs()

        factors = DB.select('map_factor', where="map_id=$mid", vars={'mid': self.id})
        for f in factors:
            if factor_id != f['id']:
                DB.insert(
                    'map_data',
                    map_id=self.id,
                    f1=f['id'],
                    f2=factor_id

                )
            DB.insert(
                'map_data',
                map_id=self.id,
                f1=factor_id,
                f2=f['id']
            )
        return factor_id

    def change_factor_effect(self, f1, f2, effect):
        effect = int(effect)
        if effect < -9 or effect > 9:
            return False
        print DB.update(
            'map_data',
            where='map_id=$map_id AND f1=$f1 AND f2=$f2',
            vars={
                'map_id': self.id,
                'f1': f1,
                'f2': f2
            },
            effect=effect
        )

    def change_koef(self, f, koef):
        koef = int(koef)
        if koef < -99 or koef > 99:
            return False
        print DB.update(
            'map_factor',
            where='map_id=$map_id AND id=$f',
            vars={
                'map_id': self.id,
                'f': f
            },
            koef=koef
        )