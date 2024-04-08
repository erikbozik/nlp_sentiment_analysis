import os
from functools import partial

import numpy as np
import pandas as pd
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks
from hf_hub_ctranslate2 import MultiLingualTranslatorCT2fromHfHub
from pydantic import BaseModel
from transformers import AutoTokenizer

load_dotenv()


class TranslateInput(BaseModel):
    target_column: str
    source_file: str
    batches: int


model = MultiLingualTranslatorCT2fromHfHub(
    model_name_or_path=os.environ["translator_path"], device="cuda", compute_type="int8_float16",
    tokenizer=AutoTokenizer.from_pretrained(os.environ["encoder_path"])
)

app = FastAPI()


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def translate_text(text: TranslateInput):
    df_list = np.array_split(pd.read_csv(text.source_file, on_bad_lines='warn'), text.batches)
    for index, chunk in enumerate(df_list):
        chunk[text.target_column] = model.generate(
            list(chunk[text.target_column]),
            src_lang=["en"] * len(chunk[text.target_column]),
            tgt_lang=["sk"] * len(chunk[text.target_column]),
        )
        if index % 100 == 0:
            print(f"Chunk {index} translated.")
            pd.concat(df_list[:index]).to_csv(f"{text.source_file}_translated_{index}_after_crash.csv")

    pd.concat(df_list).to_csv(f"{text.source_file}_translated.csv")


@app.post("/translate")
def translate(text: TranslateInput, background_task: BackgroundTasks) -> str:
    trans = partial(translate_text, text)
    background_task.add_task(trans)
    return f"Started the translation"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
