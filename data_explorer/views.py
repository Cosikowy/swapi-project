import petl as etl
from django.shortcuts import redirect, render

from data_explorer.data_tools import DataHandler
from data_explorer.forms import PickerFields, SortForm
from data_explorer.models import Collection
from data_explorer.swapi import SWAPI

sw = SWAPI("https://swapi.dev/api/")


def update(request, *args, **kwargs):
    print("Updating data...")
    planets_handler = DataHandler("planets")
    planets, planets_version = sw.get_planets()
    planets_data = planets_handler.save_planets_data(planets, planets_version)
    print("Updating people...")

    people_handler = DataHandler("people")
    people, people_version = sw.get_people()
    people_handler.save_people_data(people, planets_data, people_version)

    return redirect("collecions-view")


def collecion_view(request, id, sort_by=None, *args, **kwargs):
    _id = id
    entries_count = int(request.GET.get("entries_count", 10))
    sort_by = request.GET.get("sort_by", None)
    collection_info = Collection.objects.get(id=_id)
    people = DataHandler("people").load_data(collection_info.full_path)
    load_more_url = f"?entries_count={entries_count +10}"
    if sort_by:
        load_more_url += f"&sort_by={sort_by}"
        reverse = False if sort_by.startswith("-") else True
        sort_by = sort_by.strip("-")
        people = etl.sort(people, sort_by, reverse)

    people = etl.head(people, entries_count)
    context = {
        "load_more": load_more_url,
        "file_name": collection_info.file_name,
        "columns": etl.columns(people),
        "values": etl.toarray(people),
        "entries_count": entries_count,
        "value_counter_url": f"/occurrence-counter/{_id}",
        "sort_form": SortForm(),
    }
    return render(request, "table-view.html", context=context)


def historical_data(request, entries_count=10, *args, **kwargs):
    values = []
    collections = Collection.objects.all().order_by("-timestamp").values()
    if len(collections):
        df = etl.fromdicts(collections)
        values = etl.toarray(df)

    context = {
        "load_more": f"?entries_count={entries_count +10}",
        "file_name": None,
        "columns": ["timestamp", "file_name"],
        "values": values,
        "entries_count": entries_count,
    }
    return render(request, "collections-view.html", context=context)


def occurrence_count(request, id, entries_count=10, *args, **kwargs):
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

    self_url = f"?{picked_fields}"

    context = {
        "load_more": self_url + f"&entries_count={entries_count+10}",
        "picked_fields_url": self_url,
        "picked_fields": picked_fields,
        "fields": columns,
        "columns": table_columns,
        "values": table_values,
        "form": PickerFields(),
    }
    return render(request, "counter-view.html", context=context)
