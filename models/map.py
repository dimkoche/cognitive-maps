# coding: utf-8
import config
import hashlib
import random

from helpers.lsat import prepare_data

DB = config.DB


class MapException(Exception):
    pass


class Map():
    id = None
    email = None
    title = None
    hash = None
    passkey = None
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
            passkey = random.randint(10**7, 10**9-1)
            if not title:
                title = 'Model #%s' % hash
            self.id = DB.insert(
                'map',
                email=email,
                hash=hash,
                title=title,
                passkey=passkey
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
        self.passkey = item.passkey
        self.factors = []
        self.relations = {}
        self.koef = {}
        for f in factors:
            self.factors.append({'id': f['id'], 'name': f['name']})
            self.koef[f['name']] = f['koef']

        for r in relations:
            f1 = r['f2_name']
            f2 = r['f1_name']
            effect = r['effect']
            if f1 not in self.relations:
                self.relations[f1] = {}
            self.relations[f1][f2] = {'eff': effect, 'f1': r['f1'], 'f2': r['f2']}

    def get_factors(self):
        return [f for f in self.factors]

    def get_factor(self, factor_id):
        res = DB.select('map_factor', where="map_id=$mid AND id=$fid", vars={'mid': self.id, 'fid': factor_id})
        if res:
            return res[0]
        return None

    def add_factor(self, factor):
        max_len = 32
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

    def edit_factor(self, factor_id, factor_name):
        max_len = 32
        if len(factor_name) > max_len:
            raise MapException('Factor name is too long (Max name length = %d)' % max_len)

        DB.update(
            'map_factor',
            where='map_id=$map_id AND id=$fid',
            vars={
                'map_id': self.id,
                'fid': factor_id
            },
            name=factor_name
        )

        return True

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

    def get_chart_data(self):
        koef = []
        keys = []
        data = []
        for f1 in self.relations:
            keys.append(f1)
            koef.append(self.koef[f1])
            data.append([float(self.relations[f1][f2]['eff']) / 10 for f2 in self.relations[f1]])
        if not data:
            return False
        arr = prepare_data(data, [koef])
        keys.insert(0, 'Steps')
        arr.insert(0, keys)
        arr2 = []
        i = 0
        for a in arr:
            if i:
                a.insert(0, i)
                arr2.append(a)
            i += 1

        return arr