import os
from typing import List
from uuid import uuid4

import numpy as np
import pandas as pd
import petl as etl
from django.conf import settings

from data_explorer.models import Collection


class DataHandler:
    def __init__(self, file_name="", file_location=""):
        self.file_name = (file_name or str(uuid4())) + ".csv"
        self.file_location = file_location or os.path.join(settings.BASE_DIR, "csv")
        self.full_path = os.path.join(self.file_location, self.file_name)

    def load_data(self):
        return etl.fromcsv(self.full_path)

    def save_people_data(self, data, planets):
        data = self.parse_people_data(data, planets)
        etl.tocsv(data, self.full_path)
        self._save_metadata()

    def parse_people_data(self, data, planets):
        df = pd.DataFrame(data)
        df["edited"] = pd.to_datetime(df["edited"])
        df["data"] = df.loc[:, "edited"].apply(lambda x: x.strftime("%Y-%m-%d"))
        columns_to_drop = [
            "url",
            "starships",
            "vehicles",
            "species",
            "films",
            "created",
            "edited",
        ]
        df.drop(columns_to_drop, axis=1, inplace=True)
        df["homeworld"] = df["homeworld"].apply(
            lambda x: self._resolve_planets(int(x.split("/")[-2]), planets)  # type: ignore
        )
        parsed_data = df.to_numpy()
        parsed_data = np.insert(parsed_data, 0, df.columns, axis=0)
        return parsed_data.tolist()

    def save_planets_data(self, data):
        data = self._parse_planets_data(data)
        etl.tocsv(data, self.full_path)
        self._save_metadata()

    def _parse_planets_data(self, data: List[dict]):
        headers = data[0].keys()
        parsed_data = [headers]
        for row in data:
            parsed_data.append(row.values())  # type: ignore
        return parsed_data

    def _resolve_planets(self, id, planets):
        try:
            return planets[id - 1]["name"]
        except IndexError:
            return None

    def _save_metadata(self):
        metadata = {
            "id": self.file_name.split(".")[0],
            "file_name": self.file_name.split,
            "file_location": self.file_location,
        }
        collection_metadata = Collection(**metadata)
        collection_metadata.save()

    def _retrive_metadata(self, filename):
        return Collection.objects.get(filename=filename)

    def count_values(self, table, columns):
        return etl.valuecounts(table, *columns).cutout("frequency")
