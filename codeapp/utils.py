# built-in imports
# standard library imports
import csv
import pickle

import requests

# external imports
from flask import current_app

# internal imports
from codeapp import db
from codeapp.models import Dummy


def get_data_list() -> list[Dummy]:
    if db.exists("dataset_list") > 0:
        current_app.logger.info("Dataset allready downloaded")
        dataset_stored: list[Dummy] = []
        raw_dataset: list[bytes] = db.lrange("dataset_list", 0, -1)
        for item in raw_dataset:
            dataset_stored.append(pickle.loads(item))
        return dataset_stored
    response = requests.get(
        "https://onu1.s2.chalmers.se/datasets/IGN_games.csv", timeout=200
    )

    with open("IGN_games.csv", "wb") as new_file:
        new_file.write(response.content)

    with open("IGN_games.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        data: list[dict[str, str]] = list(reader)
        # data: list[dict[str, str]] = [row for row in reader]

    leliste: list[Dummy] = []

    for row in data:
        if "," not in row["genre"]:
            le_game = Dummy(
                title=row["title"],
                score=float(row["score"]),
                score_phrase=row["score_phrase"],
                platform=row["platform"],
                genre=row["genre"],
                release_year=int(row["release_year"]),
                release_month=int(row["release_month"]),
                release_day=int(row["release_day"]),
            )
            db.rpush("dataset_list", pickle.dumps(le_game))
            leliste.append(le_game)
        else:
            duallist = row["genre"].split(", ")
            le_game1 = Dummy(
                title=row["title"],
                score=float(row["score"]),
                score_phrase=row["score_phrase"],
                platform=row["platform"],
                genre=duallist[0],
                release_year=int(row["release_year"]),
                release_month=int(row["release_month"]),
                release_day=int(row["release_day"]),
            )
            le_game2 = Dummy(
                title=row["title"],
                score=float(row["score"]),
                score_phrase=row["score_phrase"],
                platform=row["platform"],
                genre=duallist[1],
                release_year=int(row["release_year"]),
                release_month=int(row["release_month"]),
                release_day=int(row["release_day"]),
            )
            db.rpush("dataset_list", pickle.dumps(le_game1))
            db.rpush("dataset_list", pickle.dumps(le_game2))
            leliste.append(le_game1)
            leliste.append(le_game2)

    # info = response.text
    # infolist = info.split("\r\n")
    # infolist = infolist[1:]

    # leliste: list[Dummy] = []

    # for a in infolist:
    #     b: list[str] = a.split(",")
    #     try:
    #         try:
    #             score = float(b[1])
    #             int1 = int(b[5])
    #             int2 = int(b[6])
    #             int3 = int(b[7])
    #             ca: Dummy = Dummy(b[0], score, b[2], b[3], b[4], int1, int2, int3)
    #             leliste.append(ca)
    #         except ValueError:
    #         try:
    #             b[4] = b[4].replace('"', "")
    #             b[5] = b[5].replace('"', "")
    #             score = float(b[1])
    #             int1 = int(b[6])
    #             int2 = int(b[7])
    #             int3 = int(b[8])
    #             b[5] = b[5].replace(" ", "")
    #             cb: Dummy = Dummy(b[0], score, b[2], b[3], b[4], int1, int2, int3)
    #             cc: Dummy = Dummy(b[0], score, b[2], b[3], b[5], int1, int2, int3)
    #             leliste.append(cb)
    #             leliste.append(cc)
    #         except ValueError:
    #             try:
    #                 score = float(b[3])
    #                 int1 = int(b[7])
    #                 int2 = int(b[8])
    #                 int3 = int(b[9])
    #                 cd: Dummy = Dummy(
    #                     "SusAmungus", score, b[4], b[5], b[6], int1, int2, int3
    #                 )
    #                 leliste.append(cd)
    #             except ValueError:
    #                 try:
    #                     score = float(b[2])
    #                     int1 = int(b[6])
    #                     int2 = int(b[7])
    #                     int3 = int(b[8])
    #                     ce: Dummy = Dummy(
    #                         "SusAmungus", score, b[3], b[4], b[5], int1, int2, int3
    #                     )
    #                     leliste.append(ce)
    #                 except ValueError:
    #                     try:
    #                         b[5] = b[5].replace('"', "")
    #                         b[6] = b[6].replace('"', "")
    #                         score = float(b[2])
    #                         int1 = int(b[7])
    #                         int2 = int(b[8])
    #                         int3 = int(b[9])
    #                         b[6] = b[6].replace(" ", "")
    #                         cf: Dummy = Dummy(
    #                             "SusAmungus",
    #                             score,
    #                             b[3],
    #                             b[4],
    #                             b[5],
    #                             int1,
    #                             int2,
    #                             int3,
    #                         )
    #                         cg: Dummy = Dummy(
    #                             "HalfLife3",
    #                             score,
    #                             b[3],
    #                             b[4],
    #                             b[6],
    #                             int1,
    #                             int2,
    #                             int3,
    #                         )
    #                         leliste.append(cf)
    #                         leliste.append(cg)
    #                     except ValueError:
    #                         score = float(b[4])
    #                         int1 = int(b[8])
    #                         int2 = int(b[9])
    #                         int3 = int(b[10])
    #                         ch: Dummy = Dummy(
    #                             "TheLastOfUS",
    #                             score,
    #                             b[5],
    #                             b[6],
    #                             b[7],
    #                             int1,
    #                             int2,
    #                             int3,
    #                         )
    #                         leliste.append(ch)
    # except IndexError:
    #     pass
    # db.delete("chicken")
    # cow = pickle.dumps(leliste)
    # db.set("chicken", cow)
    return leliste


def calculate_statistics(dataset: list[Dummy]) -> dict[int | str, int]:
    gamedict: dict[int | str, int] = {}

    for entry in dataset:
        if entry.score < 7:
            dataset.remove(entry)

    for cat in dataset:
        if cat.genre in gamedict:
            gamedict[cat.genre] += 1
        else:
            gamedict[cat.genre] = 1

    sorting = sorted(gamedict.items(), key=lambda item: item[1], reverse=True)
    cutted = sorting[:20]
    cutdict: dict[int | str, int] = dict(cutted)
    return cutdict


def prepare_figure(input_figure: str) -> str:
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure
