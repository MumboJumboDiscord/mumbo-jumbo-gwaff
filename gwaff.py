from scripts import plot, data
import datetime
import json
import argparse
import requests
import os


parser = argparse.ArgumentParser(description="mee6 xp graphing")
parser.add_argument("--plot", help="Use this if you want to plot", action="store_true")
parser.add_argument("--store", help="Use this if you want to store", action="store_true")
parser.add_argument("--save", help="Use this if you want to store the generated plots", action="store_true")
parser.add_argument("--post", help="Use this if you want to post the generated plots, takes a url (str)", type=str)
args = parser.parse_args()


def post(url: str):
    print("Posting...")
    for filename in os.listdir("images/"):
        image = open(f"images/{filename}", "rb")
        requests.post(url=url, json={"embeds": [{"title": "title", "thumbnail": {"url": "https://raw.githubusercontent"
                                                                                        ".com/bwac2517/gwaff/master"
                                                                                        "/assets/icon.png"},
                                                 "image": {"url": "attachment://image.png"}}]}, files={"image.png": image})


def store():
    print("Storing...")
    new_data = data.get()
    time = datetime.datetime.today()

    gwaff = data.generate_gwaff(new_data, time)
    with open("gwaff.json", "w") as out:
        json.dump(gwaff, out, indent=4)


def plot_(save: bool = False):
    print("Plotting...")

    with open("gwaff.json", "r") as outfile:
        gwaff = json.load(outfile)

    if args.save:
        plot.bar(gwaff, save=True)
        plot.line(gwaff, save=True)
    else:
        plot.bar(gwaff)
        plot.line(gwaff)


if args.store:
    store()
if args.plot:
    if args.save:
        plot_(True)
    else:
        plot_()
if type(args.post) == str:
    post(args.post)
else:
    i = input("No flag slected, what do you want to do? (p or s?) >")
    if i == "p":
        plot_()
    elif i == "s":
        store()
    else:
        raise Exception("No flags or valid input")
