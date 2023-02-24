from django.http import HttpResponse

from data_explorer.data_tools import DataHandler
from data_explorer.swapi import SWAPI

sw = SWAPI("https://swapi.dev/api/")


def update(request, *args, **kwargs):
    planets_handler = DataHandler("planets")
    planets, planets_version = sw.get_planets()
    planets_data = planets_handler.save_planets_data(planets, planets_version)

    people_handler = DataHandler("people")
    people, people_version = sw.get_people()
    people_handler.save_people_data(people, planets_data, people_version)

    return HttpResponse("success")


def collecions_view(request, *args, **kwargs):
    return HttpResponse({"status": 200})
