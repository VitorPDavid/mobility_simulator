import os
import pickle

import numpy as np
import simpy
from numpy.random import default_rng
from scipy.stats import expon, norm


def run_simulation(options):
    population = options.population
    env = simpy.Environment()
    whfile = os.path.join(options.inputdir, "workhours")
    transitionsfile = os.path.join(options.inputdir, "transitions")
    staydistfile = os.path.join(options.inputdir, "staydist")
    rnd = default_rng(options.run)
    np.random.seed(seed=options.run)

    places = [None, "adm", "inf", "mul", "bib", "pos"]

    # read input data from files
    file = open(whfile, "rb")
    data = pickle.load(file)
    groupfreq = data["group_freq"]
    groupparam = data["group_param"]
    # print(groupfreq)
    # print(groupparam)
    # exit()
    file.close()
    file = open(transitionsfile, "rb")
    transitions = (pickle.load(file))["transitions"]
    file.close()
    file = open(staydistfile, "rb")
    stayparam = (pickle.load(file))["staydist"]
    file.close()

    # initialization
    focp = open("occupation", "w")
    occupation = {}
    # fout = {}
    tprob = {}
    # transitions
    for place in places:
        occupation[place] = 0
        # fout[place] = open(str(place), "w")
        tprob[place] = []
        total = sum(list(transitions[place].values()))
        for nextplace in places:
            if place != nextplace:
                tprob[place].append(transitions[place][nextplace] / total)
            else:
                tprob[place].append(0.0)
        print(tprob[place])
    print(stayparam)

    # groups
    groups = []
    groupprob = []
    aparam = {}
    dparam = {}
    for grp in groupfreq:
        groups.append(grp)
        groupprob.append(groupfreq[grp] / sum(list(groupfreq.values())))  # amount in grp/total
        aparam[grp] = groupparam[grp][0]
        dparam[grp] = groupparam[grp][1]

    # individual behavior
    def person(env, i, occupation, places):
        grp = rnd.choice(groups, size=1, p=groupprob)[0]  # choose a group
        place = None
        occupation[place] += 1
        day = 1

        # Day loop
        while True:
            # User arrival
            arrival = norm.rvs(size=1, *aparam[grp][:-2], loc=aparam[grp][-2], scale=aparam[grp][-1])[0]
            departure = norm.rvs(size=1, *dparam[grp][:-2], loc=dparam[grp][-2], scale=dparam[grp][-1])[0]
            while departure < arrival:
                departure = norm.rvs(size=1, *dparam[grp][:-2], loc=dparam[grp][-2], scale=dparam[grp][-1])[0]
            if departure > 1440:
                departure = 1440.0
            departure += env.now
            yield env.timeout(arrival)
            occupation[place] -= 1
            place = rnd.choice(places, size=1, p=tprob[place])[
                0
            ]  # TODO: place of arrival needs to be obtained from data... using tprob from None is wrong
            stay = expon.rvs(size=1, *stayparam[place][:-2], loc=stayparam[place][-2], scale=stayparam[place][-1])[0]
            occupation[place] += 1
            if options.verbose:
                print("[{:10.5f}]\tUser {:02d} arrived at {}".format(env.now, i, place))

            # Dinamica de jornada de trabalho
            while env.now + stay < departure:
                yield env.timeout(stay)
                occupation[place] -= 1
                place = rnd.choice(places, size=1, p=tprob[place])[0]
                occupation[place] += 1
                if options.verbose:
                    print("[{:10.5f}]\tUser {:02d} switched to {}".format(env.now, i, place))
                # fout[place].write("{}\t{}\n".format(env.now, occupation[place]))
                stay = expon.rvs(size=1, *stayparam[place][:-2], loc=stayparam[place][-2], scale=stayparam[place][-1])[
                    0
                ]
                # if env.now+stay > departure:
                #    break

            yield env.timeout(departure - env.now)
            occupation[place] -= 1
            place = None
            occupation[place] += 1
            if options.verbose:
                print("[{:10.5f}]\tUser {:02d} leaved".format(env.now, i))

            yield env.timeout(day * 1440 - env.now)
            if options.verbose:
                print("[{:10.5f}]\tUser {:02d} day {} endded".format(env.now, i, day))
            day += 1

    # trace occupation
    def trace(env, occupation):
        step = 5.0

        while True:
            yield env.timeout(step)
            total = 0
            focp.write("{} ".format(env.now))
            print("{} ".format(env.now), end="")
            for place in places:
                if place == None:
                    continue
                focp.write("{} ".format(occupation[place]))
                print("{} ".format(occupation[place]), end="")
                total += occupation[place]
            focp.write("{}\n".format(total))
            print("{}".format(total))

    for i in range(population):
        env.process(person(env, i, occupation, places))

    env.process(trace(env, occupation))

    env.run(until=options.days * 1440)
