from scripts import plot, data
import datetime
import json
import argparse


parser = argparse.ArgumentParser(description="mee6 xp graphing")
parser.add_argument("-p", help="Use this if you want to plot", action="store_true")
parser.add_argument("-s", help="Use this if you want to store", action="store_true")
args = parser.parse_args()


def save():
    print("Saving...")
    new_data = data.get()
    time = datetime.datetime.today()

    gwaff = data.generate_gwaff(new_data, time)
    with open("gwaff.json", "w") as out:
        json.dump(gwaff, out, indent=4)


def plot_():
    print("Plotting...")

    with open("gwaff.json", "r") as outfile:
        gwaff = json.load(outfile)

    plot.bar(gwaff)
    plot.line(gwaff)


if parser.parse_args().s:
    save()
elif parser.parse_args().p:
    plot_()
else:
    i = input("No flag slected, what do you want to do? (p or s?) >")
    if i == "p":
        plot_()
    elif i == "s":
        save()
    else:
        raise Exception("No flags or valid input")
