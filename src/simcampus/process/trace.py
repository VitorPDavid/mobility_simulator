# trace occupation
def trace(env, occupation, places, focp):
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
