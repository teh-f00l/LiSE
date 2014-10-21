from cProfile import run
from initbold import inittest
from utiltest import mkengine, clear_off, seed, caching


def report_old(engine, n):
    kobold_alive = 'kobold' in engine.character['physical'].thing
    print(
        "On tick {}, the dwarf is at {}, "
        "and the kobold is {}{}{}".format(
            n,
            engine.character['dwarf'].avatar['location'],
            "alive" if kobold_alive else "dead",
            " at " + str(engine.character['kobold'].avatar['location'])
            if kobold_alive else "",
            " (in a shrubbery)" if kobold_alive and len([
                th for th in
                engine.character['kobold'].avatar.location.contents()
                if th.name[:5] == "shrub"
            ]) > 0 else ""
        )
    )


def report(engine, n):
    phys = engine.character['physical']
    kobold_alive = 'kobold' in phys.thing
    print(
        "On tick {}, the dwarf is at {}, "
        "and the kobold is {}{}{}".format(
            n,
            phys.thing['dwarf']['location'],
            "alive" if kobold_alive else "dead",
            " at " + str(phys.thing['kobold']['location'])
            if kobold_alive else "",
            " (in a shrubbery)" if kobold_alive and len([
                th for th in phys.thing['kobold'].location.contents()
                if th.name[:5] == "shrub"
            ]) > 0 else ""
        )
    )


def runtest(engine):
    # run sim for 100 tick
    for n in range(0, 100):
        engine.next_tick()
        report(engine, n)


if __name__ == '__main__':
    clear_off()
    with mkengine(random_seed=seed, caching=caching) as engine:
        inittest(engine)
        engine.commit()
        run('runtest(engine)')
