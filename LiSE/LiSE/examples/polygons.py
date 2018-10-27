# Parable of the Polygons is public domain.
# This implementation is part of LiSE, a framework for life simulation games.
# Copyright (c) Zachary Spector, public@zacharyspector.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Implementation of Parable of the Polygons http://ncase.me/polygons/"""


def install(eng):
    @eng.function
    def cmp_neighbor_shapes(poly, cmp, stat):
        """Compare the proportion of neighboring polys with the same shape as this one

        Count the neighboring polys that are the same shape as this one, and return how that compares with
        some stat on the poly's user.

        """
        from operator import attrgetter
        home = poly.location
        similar = 0
        n = 0
        for n, neighbor_home in enumerate(map(attrgetter('destination'), home.portal.values()), 1):
            # assume only 1 poly per home for now; this is faithful to the original
            try:
                neighbor = next(iter(neighbor_home.contents()))
            except StopIteration:
                continue
            if neighbor.user is poly.user:
                similar += 1
        return cmp(poly.character.stat[stat], similar / n)

    @eng.rule
    def relocate(poly):
        """Move to a random unoccupied place"""
        unoccupied = [place for place in poly.character.place.values() if not place.content]
        poly.location = poly.engine.choice(unoccupied)

    @relocate.trigger
    def similar_neighbors(poly):
        """Trigger when my neighborhood fails to be enough like me"""
        from operator import ge
        return poly.engine.function.cmp_neighbor_shapes(poly, ge, 'min_sameness')

    @relocate.trigger
    def dissimilar_neighbors(poly):
        """Trigger when my neighborhood gets too much like me"""
        from operator import lt
        return poly.engine.function.cmp_neighbor_shapes(poly, lt, 'max_sameness')


    eng.rulebook['parable'] = [relocate]


    physical = eng.new_character(
        'physical', min_sameness=.1, max_sameness=.9,
        _config={
            'min_sameness': {'control': 'slider', 'min': 0.0, 'max': 1.0},
            'max_sameness': {'control': 'slider', 'min': 0.0, 'max': 1.0}
        }
    )
    square = eng.new_character('square')
    triangle = eng.new_character('triangle')
    square.avatar.rulebook = triangle.avatar.rulebook = 'parable'


    # make an 8-way-connected grid
    physical.grid_2d_8graph(20, 20)
    empty = list(physical.place.values())
    eng.shuffle(empty)
    # distribute 30 of each shape randomly among the empty places
    for i in range(1, 31):
        square.add_avatar(empty.pop().new_thing('square%i' % i, _image_paths=['atlas://polygons/meh_square']))
    for i in range(1, 31):
        triangle.add_avatar(empty.pop().new_thing('triangle%i' % i, _image_paths=['atlas://polygons/meh_triangle']))


if __name__ == '__main__':
    import os
    from LiSE import Engine
    for stale in ('LiSEworld.db', 'trigger.py', 'prereq.py', 'action.py', 'function.py', 'method.py'):
        if os.path.exists(stale):
            os.remove(stale)
    with Engine('LiSEworld.db') as eng:
        with eng.batch():
            install(eng)
    import sys
    if '--profile' in sys.argv:
        import cProfile

        def test():
            with Engine('LiSEworld.db') as eng:
                for n in range(10):
                    eng.next_turn()

        cProfile.run('test()', 'polygons.prof')