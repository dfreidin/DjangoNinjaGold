# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from random import randint
from time import strftime

# Create your views here.
def index(request):
    return render(request, "ninja_gold/index.html")

def reset(request):
    request.session["gold"] = 0
    request.session["activities"] = []
    return redirect(index)

def process(request, building):
    if not "gold" in request.session:
        request.session["gold"] = 0
    if not "activities" in request.session:
        request.session["activities"] = []
    gold = int(request.session["gold"])
    if building == "farm":
        earnings = randint(10, 20)
    elif building == "cave":
        earnings = randint(5, 10)
    elif building == "house":
        earnings = randint(2, 5)
    elif building == "casino":
        earnings = randint(-50, 50)
        if gold + earnings < 0:
            earnings = -1 * gold
    else:
        return redirect(index)
    activity = "Earned {} gold from the {}! ({})".format(earnings, building, strftime("%c"))
    if earnings > 0:
        color = "pos"
    elif earnings < 0:
        color = "neg"
        activity = "Entered a casino and lost {} gold... Ouch... ({})".format(-1 * earnings, strftime("%c"))
    else:
        color = ""
    request.session["activities"].append({"activity": activity, "class": color})
    request.session["gold"] = gold + earnings
    return redirect(index)