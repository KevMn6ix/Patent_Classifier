import pandas as pd
import requests
from io import StringIO

def cpc_to_ipc(cpc_code):
    url = 'https://www.cooperativepatentclassification.org/sites/default/files/cpc/concordances/cpc-ipc-concordance.txt'
    response = requests.get(url)
    response.raise_for_status()
    data = StringIO(response.text)
    df_pandas = pd.read_csv(data, delimiter='\t', header=0)
    filtered_df = df_pandas[df_pandas["CPC Group"] == cpc_code]
    ipc_code = filtered_df["IPC Group"].values[0]
    return ipc_code
