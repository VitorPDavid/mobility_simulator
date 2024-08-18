from scipy.stats import expon, norm


# class Person:
#     def __init__(
#         self, env, rnd, i, occupation, places, groups, groupprob, aparam, dparam, stay_data, tprob, verbose
#     ) -> None:
#         self.env = env
#         self.i = i
#         self.occupation = occupation
#         self.places = places
#         self.groups = groups
#         self.groupprob = groupprob
#         self.aparam = aparam
#         self.dparam = dparam
#         self.stay_data = stay_data
#         self.tprob = tprob
#         self.rnd = rnd
#         self.verbose = verbose

#     def run(self):
#         grp = self.rnd.choice(self.groups, size=1, p=self.groupprob)[0]  # choose a group
#         place = None
#         self.occupation[place] += 1
#         day = 1

#         # Day loop
#         while True:
#             # User arrival
#             arrival = norm.rvs(size=1, *self.aparam[grp][:-2], loc=self.aparam[grp][-2], scale=self.aparam[grp][-1])[0]
#             departure = norm.rvs(size=1, *self.dparam[grp][:-2], loc=self.dparam[grp][-2], scale=self.dparam[grp][-1])[
#                 0
#             ]
#             while departure < arrival:
#                 departure = norm.rvs(
#                     size=1, *self.dparam[grp][:-2], loc=self.dparam[grp][-2], scale=self.dparam[grp][-1]
#                 )[0]
#             if departure > 1440:
#                 departure = 1440.0
#             departure += self.env.now
#             yield self.env.timeout(arrival)
#             self.occupation[place] -= 1
#             place = rnd.choice(self.places, size=1, p=self.tprob[place])[
#                 0
#             ]  # TODO: place of arrival needs to be obtained from data... using tprob from None is wrong
#             stay = expon.rvs(
#                 size=1, *self.stay_data[place][:-2], loc=self.stay_data[place][-2], scale=self.stay_data[place][-1]
#             )[0]
#             self.occupation[place] += 1
#             if self.verbose:
#                 print("[{:10.5f}]\tUser {:02d} arrived at {}".format(self.env.now, self.i, place))

#             # Dinamica de jornada de trabalho
#             while self.env.now + stay < departure:
#                 yield self.env.timeout(stay)
#                 self.occupation[place] -= 1
#                 place = rnd.choice(self.places, size=1, p=self.tprob[place])[0]
#                 self.occupation[place] += 1
#                 if self.verbose:
#                     print("[{:10.5f}]\tUser {:02d} switched to {}".format(self.env.now, self.i, place))

#                 stay = expon.rvs(
#                     size=1, *self.stay_data[place][:-2], loc=self.stay_data[place][-2], scale=self.stay_data[place][-1]
#                 )[0]

#             yield self.env.timeout(departure - self.env.now)

#             place = None

#             if self.verbose:
#                 print("[{:10.5f}]\tUser {:02d} leaved".format(self.env.now, self.i))

#             yield self.env.timeout(day * 1440 - self.env.now)

#             if self.verbose:
#                 print("[{:10.5f}]\tUser {:02d} day {} endded".format(self.env.now, self.i, day))

#             day += 1


# individual behavior
def person(env, rnd, i, occupation, places, groups, groupprob, aparam, dparam, stay_data, tprob, verbose):
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
        stay = expon.rvs(size=1, *stay_data[place][:-2], loc=stay_data[place][-2], scale=stay_data[place][-1])[0]
        occupation[place] += 1
        if verbose:
            print("[{:10.5f}]\tUser {:02d} arrived at {}".format(env.now, i, place))

        # Dinamica de jornada de trabalho
        while env.now + stay < departure:
            yield env.timeout(stay)
            occupation[place] -= 1
            place = rnd.choice(places, size=1, p=tprob[place])[0]
            occupation[place] += 1
            if verbose:
                print("[{:10.5f}]\tUser {:02d} switched to {}".format(env.now, i, place))
            # fout[place].write("{}\t{}\n".format(env.now, occupation[place]))
            stay = expon.rvs(size=1, *stay_data[place][:-2], loc=stay_data[place][-2], scale=stay_data[place][-1])[0]
            # if env.now+stay > departure:
            #    break

        yield env.timeout(departure - env.now)
        occupation[place] -= 1
        place = None
        occupation[place] += 1
        if verbose:
            print("[{:10.5f}]\tUser {:02d} leaved".format(env.now, i))

        yield env.timeout(day * 1440 - env.now)
        if verbose:
            print("[{:10.5f}]\tUser {:02d} day {} endded".format(env.now, i, day))
        day += 1
