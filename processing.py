import pandas as pd
import re
import numpy as np
from datetime import datetime
from typing import Optional

def join_and_clean(board_file : str, jobs_file : str, output_path : Optional[str] = None) -> pd.DataFrame:
    df1 = pd.read_json(board_file)
    df2 = pd.read_json(jobs_file)
    result = pd.merge(df1, df2, on='unique_id')
    pattern = re.compile(r"[0-9]+", re.IGNORECASE)
    experiences = [np.array(pattern.findall(result.loc[i, "experience"]), dtype=int).mean() for i in range(result.shape[0])]
    result_processed = result.copy()
    result_processed["experience"] = experiences
    pattern = re.compile(r"Mis à jour le ([0-9]+(/[0-9]+)+)", re.IGNORECASE)
    dates = [datetime.strptime(pattern.findall(result_processed.loc[i, "date"])[0][0], "%d/%m/%Y") for i in range(result_processed.shape[0])]
    result_processed["date"] = dates
    result_processed['starting_date'] = result_processed['starting_date'].fillna(datetime.today().strftime("%d/%m/%Y"))
    pattern = re.compile(r"([0-9]+(/[0-9]+)+)", re.IGNORECASE)
    starting_dates = [datetime.strptime(pattern.findall(result_processed.loc[i, "starting_date"])[0][0], "%d/%m/%Y") for i in range(result_processed.shape[0])]
    result_processed["starting_date"] = starting_dates
    result_processed = result_processed.drop('link', axis=1)
    result_processed['description'] = result_processed['description'].transform(lambda s : s[21:])
    if output_path:
        result_processed.to_json(orient="records", path_or_buf=output_path)
    return result_processed
