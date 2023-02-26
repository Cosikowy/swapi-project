import os
from datetime import datetime
from uuid import uuid4

import petl as etl
from django.conf import settings

from data_explorer.models import Collection
from data_explorer.swapi import ENDPOINTS


class DataHandler:
    def __init__(self, file_name="", file_location=""):
        self.file_name = f"{str(uuid4().hex)}.{file_name}.csv"
        self.file_location = file_location or os.path.join(settings.BASE_DIR, "csv")
        self.full_path = os.path.join(self.file_location, self.file_name)

    def load_data(self, full_path):
        return etl.fromcsv(full_path)

    def save_people_data(self, data, planets, version_tag):
        data = self.parse_people_data(data, planets)
        etl.tocsv(data, self.full_path)
        self._save_metadata(version_tag, ENDPOINTS.people)
        return data

    def parse_people_data(self, data, planets):
        df = etl.fromdicts(data)
        df = etl.addfield(
            df,
            "date",
            lambda x: datetime.fromisoformat(x["edited"]).strftime("%Y-%m-%d"),
        )
        columns_to_drop = [
            "url",
            "starships",
            "vehicles",
            "species",
            "films",
            "created",
            "edited",
            "homeworld_url",
        ]
        df = etl.rename(df, "homeworld", "homeworld_url")
        df = etl.addfield(
            df,
            "homeworld",
            lambda x: self._resolve_planets(
                int(x["homeworld_url"].split("/")[-2]), planets
            ),
        )
        df = etl.cutout(df, *columns_to_drop)
        return df

    def save_planets_data(self, data, version_tag):
        data = self._parse_planets_data(data)
        etl.tocsv(data, self.full_path)
        self._save_metadata(version_tag, ENDPOINTS.planets)
        return data

    def _parse_planets_data(self, data):
        df = etl.fromdicts(data)
        return df

    def _resolve_planets(self, id, planets):
        p = etl.cut(planets, "name")
        return p[id][0]

    def _save_metadata(self, version_tag, endpoint):
        metadata = {
            "id": self.file_name.split(".")[0],
            "file_name": self.file_name,
            "file_location": self.file_location,
            "etag": version_tag,
            "endpoint": endpoint,
        }
        collection_metadata = Collection(**metadata)
        collection_metadata.save()

    def _retrive_metadata(self, filename):
        return Collection.objects.get(filename=filename)

    @staticmethod
    def count_values(table, columns):
        df = etl.valuecounts(table, *columns)
        return etl.cutout(df, "frequency")
