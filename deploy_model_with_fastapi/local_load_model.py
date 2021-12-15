import warnings
from typing import List

import joblib
import mlflow
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

pokemon_app = FastAPI()


class Pokemon(BaseModel):
    hp: int
    attack: int
    defence: int
    special_attack: int
    special_defense: int
    speed: int


@pokemon_app.get("/pokemon-type")
def get_pokemon_type(hp: int, attack: int, defence: int, special_attack: int, special_defense: int, speed: int):
    df = pd.DataFrame(columns=["hp", "attack", "defence", "special_attack", "special_defense", "speed"])
    df.loc[0] = pd.Series({'hp': hp, 'attack': attack, 'defence': defence, 'special_attack': special_attack,
                           'special_defense': special_defense, 'speed': speed})
    model = get_model("../models/model2.pkl")
    res = bool(model.predict(df)[0])
    return {"is_legendary": res}


@pokemon_app.post("/pokemon-type")
def post_pokemon_type(pokemon: Pokemon):
    df = pd.DataFrame(columns=["hp", "attack", "defence", "special_attack", "special_defense", "speed"])
    df.loc[0] = pd.Series({'hp': pokemon.hp, 'attack': pokemon.attack, 'defence': pokemon.defence,
                           'special_attack': pokemon.special_attack,
                           'special_defense': pokemon.special_defense, 'speed': pokemon.speed})
    model = get_model("../models/model2.pkl")
    res = bool(model.predict(df)[0])
    return {"is_legendary": res}


@pokemon_app.post("/pokemon-types")
def get_pokemon_types(pokemons: List[Pokemon]):
    i = 0
    df = pd.DataFrame(columns=["hp", "attack", "defence", "special_attack", "special_defense", "speed"])
    for pokemon in pokemons:
        df.loc[i] = pd.Series({'hp': pokemon.hp, 'attack': pokemon.attack, 'defence': pokemon.defence,
                               'special_attack': pokemon.special_attack,
                               'special_defense': pokemon.special_defense, 'speed': pokemon.speed})
        i += 1
    model = get_model("../models/model2.pkl")
    results = []
    for r in model.predict(df):
        results.append(bool(r))
    return {"is_legendary": results}


def get_model(model_path: str):
    # if model_path starts with a mlflow model path, use mlflow pyfunc to get the model
    # mlflow model must have blow formats:
    # - f"models:/{model_name}/{version}"
    # - f"models:/{model_name}/{stage}"
    if model_path.startswith("models"):
        model = mlflow.pyfunc.load_model(
            model_uri=model_path
        )
    # if it's a local fs path, use joblib to get the model
    else:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=UserWarning)
            model = joblib.load(open(model_path, 'rb'))
    return model


def main():
    # result1 = get_pokemon_type(79, 115, 70, 125, 80, 111)
    # print(result1)
    full_dict = {"columns": ["hp", "attack", "defense", "special_attack", "special_defense", "speed"],
                 "index": [272, 293, 414, 263, 49],
                 "data": [[80, 70, 70, 90, 100, 70], [64, 51, 23, 51, 23, 28], [70, 94, 50, 94, 50, 66],
                          [38, 30, 41, 30, 41, 60],
                          [70, 65, 60, 90, 75, 90]]}
    p1 = Pokemon(hp=79, attack=115, defence=70, special_attack=125, special_defense=80, speed=111)
    p2 = Pokemon(hp=89, attack=115, defence=70, special_attack=125, special_defense=80, speed=111)
    p_list = [p1, p2]
    result2 = get_pokemon_types(p_list)
    print(result2)


if __name__ == "__main__":
    main()
