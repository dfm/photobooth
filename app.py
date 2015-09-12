#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

__all__ = ["app"]

import glob
import string
import random
import subprocess as sp

import tweepy
from skimage.io import imread, imsave

import flask


ID_CHARS = string.ascii_lowercase + string.digits


app = flask.Flask(__name__)
app.config.from_pyfile("twitter.py", silent=True)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/take")
@app.route("/take/<int:ind>")
def take_photo(ind=0):
    fn = "scratch/out-{0:03d}.jpg".format(ind)
    if app.config["webcam"]:
        job = sp.Popen(["imagesnap", "-w", "1.00", fn])
    else:
        job = sp.Popen([
            "gphoto2", "--capture-image-and-download",
            "--filename", fn,
            "--force-overwrite"
        ])
    job.communicate()
    if job.returncode:
        return flask.abort(500)

    chars = "".join(random.choice(ID_CHARS) for _ in range(10))
    result = dict(filename="{0}?v={1}".format(fn, chars))
    if ind < 3:
        result["next_url"] = flask.url_for(".take_photo", ind=ind+1)
    else:
        pnt, twt = stitch_images(list(map(imread, glob.glob("scratch/*.jpg"))))
        fn = "output/{0}.jpg".format(chars)
        imsave(fn, pnt)
        imsave("output/{0}-twitter.jpg".format(chars), twt)
        result["final"] = fn

    return flask.jsonify(**result)


@app.route("/scratch/<filename>")
def scratch(filename):
    return flask.send_from_directory("scratch", filename)


@app.route("/output/<filename>")
def output(filename):
    return flask.send_from_directory("output", filename)


@app.route("/output/<filename>/print")
def print_photo(filename):
    # Tweet the photo if the credentials are available.
    if ("TWITTER_KEY" in app.config and
            flask.request.args.get("tweet", "no") == "yes"):
        auth = tweepy.OAuthHandler(
            app.config["TWITTER_KEY"],
            app.config["TWITTER_SECRET"],
        )
        auth.set_access_token(
            app.config["TWITTER_USER_KEY"],
            app.config["TWITTER_USER_SECRET"],
        )
        api = tweepy.API(auth)
        api.update_with_media("output/{0}-twitter{1}"
                              .format(*(filename.splitext())),
                              status="Just partyin' #photobooth")

    job = sp.Popen(
        ("lp -o media=4x6,photographic-glossy -o landscape "
         "-o fit-to-page").split() + ["output/" + filename]
    )
    job.communicate()
    if job.returncode:
        return flask.abort(500)

    return flask.jsonify(message="Success")


def stitch_images(images, border=16, bottom=100):
    height = images[0].shape[0]
    full_height = 3*border + bottom + 2*height
    full_width = int(full_height*1.5)
    width = int(0.5 * (full_width - 3*border))
    full_image = imread("static/template.jpg")
    delta = int(0.5 * (images[0].shape[1] - width))

    for i, img in enumerate(images[:4]):
        xi = border + (i // 2) * (border + height)
        yi = border + (i % 2) * (border + width)
        full_image[xi:xi+height, yi:yi+width] = img[:, delta:delta+width]

    return (full_image[border:-border, border:-border],
            full_image[:3*border+2*height, :3*border+2*width])


if __name__ == "__main__":
    import sys

    app.debug = True
    app.config["webcam"] = "--webcam" in sys.argv
    app.run()
