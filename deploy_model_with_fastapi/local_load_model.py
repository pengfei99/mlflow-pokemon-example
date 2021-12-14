import warnings

import joblib
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


@pokemon_app.post("/pokemon-types")
def get_pokemon_types(pokemon: Pokemon):
    dic=pokemon.dict()
    print(dic)
    df = pd.DataFrame.from_dict(pokemon.dict())
    df.head()


def get_model(file_name: str):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        model = joblib.load(open(file_name, 'rb'))
        # pickle.load(open(file_name, 'rb'))
    return model


def main():
    result1 = get_pokemon_type(79, 115, 70, 125, 80, 111)
    print(result1)
    p1 = Pokemon(hp=79, attack=115, defence=70, special_attack=125, special_defense=80, speed=111)
    result2 = get_pokemon_types(p1)
    print(result2)


if __name__ == "__main__":
    main()
