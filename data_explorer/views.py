import petl as etl
from django import forms
from django.shortcuts import redirect, render

from data_explorer.data_tools import DataHandler
from data_explorer.models import Collection
from data_explorer.swapi import SWAPI

sw = SWAPI("https://swapi.dev/api/")


def update(request, *args, **kwargs):
    planets_handler = DataHandler("planets")
    planets, planets_version = sw.get_planets()
    planets_data = planets_handler.save_planets_data(planets, planets_version)

    people_handler = DataHandler("people")
    people, people_version = sw.get_people()
    people_handler.save_people_data(people, planets_data, people_version)

    return redirect("collecions-view")


def collecion_view(request, sort_by=None, *args, **kwargs):
    _id = request.GET.get("id")
    entries_count = int(request.GET.get("entries_count", 10))
    collection_info = Collection.objects.get(id=_id)

    people = DataHandler("people").load_data(collection_info.full_path)

    people = etl.head(people, entries_count)
    context = {
        "load_more": f"?id={collection_info.id}&entries_count={entries_count +10}",
        "file_name": collection_info.file_name,
        "columns": etl.columns(people),
        "values": etl.toarray(people),
        "entries_count": entries_count,
        "value_counter_url": f"/occurrence-counter/?id={_id}",
    }
    return render(request, "table-view.html", context=context)


def historical_data(request, entries_count=10, *args, **kwargs):
    collections = Collection.objects.all().order_by("-timestamp").values()
    df = etl.fromdicts(collections)
    context = {
        "load_more": f"?entries_count={entries_count +10}",
        "file_name": None,
        "columns": ["timestamp", "file_name"],
        "values": etl.toarray(df),
        "entries_count": entries_count,
    }
    return render(request, "collections-view.html", context=context)


choices = (
    ("name", "name"),
    ("height", "height"),
    ("mass", "mass"),
    ("hair_color", "hair_color"),
    ("skin_color", "skin_color"),
    ("eye_color", "eye_color"),
    ("birth_year", "birth_year"),
    ("gender", "gender"),
    ("date", "date"),
    ("homeworld", "homeworld"),
)


def occurrence_count(request, id, entries_count=10, *args, **kwargs):
    class PickerFields(forms.Form):
        picked_fields = forms.MultipleChoiceField(choices=choices)

    _id = id
    picked_fields = request.GET.getlist("picked_fields", [])
    entries_count = int(request.GET.get("entries_count", 10))

    collection_info = Collection.objects.get(id=_id)
    df = DataHandler("people").load_data(collection_info.full_path)
    columns = etl.columns(df)

    table_columns = None
    table_values = None

    fields_to_count = picked_fields if picked_fields else []

    if fields_to_count:
        df = DataHandler.count_values(df, fields_to_count)
        df = etl.head(df, entries_count)
        table_columns = etl.columns(df)
        table_values = etl.toarray(df)

    picked_fields = "".join(
        ["&picked_fields={}".format(field) for field in picked_fields]
    )

    self_url = f"?id={collection_info.id}{picked_fields}"

    context = {
        "load_more": self_url + f"&entries_count={entries_count +10}",
        "picked_fields_url": self_url,
        "picked_fields": picked_fields,
        "fields": columns,
        "columns": table_columns,
        "values": table_values,
        "form": PickerFields(),
    }
    return render(request, "counter-view.html", context=context)
