from azure.identity import DefaultAzureCredential
from omnia_timeseries import TimeseriesAPI, TimeseriesEnvironment
import pandas as pd
from typing import Union

# Python SDK documentation
# https://github.com/equinor/omnia-timeseries-python


TENANT_ID = "3aa4a235-b6e2-48d5-9195-7fcf05b459b0"

credential_1 = DefaultAzureCredential()

ims_tag = "GFC.13-AE___938_.Sand_Raw"
ims_collective = "GFC"


def get_id_from_tag(
    api: TimeseriesAPI, ims_tag: str, ims_collective: str
) -> Union[str, None]:
    """Simple function to determine timeseries ID from a given ims- tag and collective"""
    try:
        tag_search = api.search_timeseries(name=ims_tag, assetId=ims_collective)
        if not tag_search["data"]["items"]:
            raise Exception(f"Unable to find or access {ims_tag}")
        return tag_search["data"]["items"][0]["id"]
    except Exception as e:
        print(f"Error: {e}")
        return None


for cred in credential_1.credentials:
    api = TimeseriesAPI(azure_credential=cred, environment=TimeseriesEnvironment.Test())

    tag_ts_id = get_id_from_tag(api, ims_tag, ims_collective)

    if tag_ts_id:
        print(f"Getting data with {type(cred)}")
        data = api.get_datapoints(id=tag_ts_id, startTime=None, endTime=None, limit=500)
        datapoints = data["data"]["items"][0]["datapoints"]
        time_values = [(dp["time"], dp["value"]) for dp in datapoints]

        df = pd.DataFrame(time_values, columns=["time", "value"])
        print(df)
    else:
        print(f"{type(cred)} did not work")
