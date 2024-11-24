from optparse import OptionParser


def create_args_options():
    parser = OptionParser()

    parser.add_option(
        "-i",
        "--input-dir",
        type="string",
        dest="inputdir",
        default="../data",
        help="input from where to read data",
    )
    parser.add_option(
        "-o",
        "--output-dir",
        type="string",
        dest="outputdir",
        default="../output",
        help="input from where to write the data",
    )
    parser.add_option(
        "-p",
        "--population",
        type="int",
        dest="population",
        default=10,
        help="size of population",
    )
    parser.add_option(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        default=False,
        help="print debug messages to stdout",
    )
    parser.add_option("-d", "--days", type="int", dest="days", default=7, help="days to simulate")
    parser.add_option(
        "--stay",
        type="float",
        dest="stay",
        default=10.0,
        help="Not in use, maximum stay time in place",
    )
    parser.add_option("-s", "--seed", type="int", dest="seed", default=1, help="simulation seed")

    return parser
