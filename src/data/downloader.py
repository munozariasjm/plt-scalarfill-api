import pandas as pd
import os
import requests
import re
import glob
from typing import List, Tuple, Dict, Union, Optional
import pathlib
import seaborn as sns
import matplotlib.pyplot as plt


class RemoteDataGetter:
    def __init__(self) -> None:
        """Getter for the data hosted on the remote server
        uploaded by Andres Delannoy as pickle files.
        """
        self.host_path = "https://delannoy.web.cern.ch/plt-scaler/"

    def get_available_fills(self) -> List[str]:
        """
        Returns the list of all the available fills in the host_path.
        """
        r = requests.get(self.host_path)
        fills = list(set(re.findall("\d+.pkl", str(r.content))))
        return fills

    def get_fill_df(self, taget_fill: Union[str, int]) -> pd.DataFrame:
        """Returns the fill dataframe for the given fill.

        Args:
            taget_fill (Union[str, int]): The fill to download

        Returns:
            pd.DataFrame: Dataframe containing all the fill information 
        """
        available_fills = self.get_available_fills()
        if not str(taget_fill).endswith(".pkl"):
            taget_fill = str(taget_fill) + ".pkl"
        assert taget_fill in available_fills, "Fill not found in path: " + taget_fill
        remothe_path = self.host_path + taget_fill
        return pd.read_pickle(remothe_path)
