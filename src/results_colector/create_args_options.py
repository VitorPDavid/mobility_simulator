from optparse import OptionParser


def create_args_options():
    parser = OptionParser()

    parser.add_option(
        "-o",
        "--output-dir",
        type="string",
        dest="output_dir",
        default="output",
        help="path to a directory to save results",
    )
    parser.add_option(
        "-i",
        "--input-file",
        type="string",
        dest="input_file",
        default="cases.txt",
        help="a file with each line with one simulation case",
    )

    parser.add_option(
        "-r",
        "--repeat-count",
        type="int",
        dest="repeat_count",
        default=1,
        help="How much times to repeat each simulation case",
    )

    return parser
