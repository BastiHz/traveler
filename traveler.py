import argparse
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

from src import run


parser = argparse.ArgumentParser()
parser.add_argument(
    "n",
    type=int,
    help="Number of points."
)
parser.add_argument(
    "-w",
    "--window-size",
    metavar=("<width>", "<height>"),
    nargs=2,
    type=int,
    help="Specify the window width and height in pixels.",
    default=(800, 600)
)
parser.add_argument(
    "-m",
    "--min-distance",
    metavar="<min-distance>",
    type=int,
    help="Minimum distance between points.",
    default=15
)
args = parser.parse_args()
run.run(args.n, args.window_size, args.min_distance)
