import time
import typing as tp
import math

import pandas as pd

from vkapi import config, session
from vkapi.exceptions import APIError

code = """
    var query_params = %s;
    var items = [];
    var iterCount = 25;
    var i = 0;
    while (i < iterCount && query_params.count > 0) {
        var responseItems = API.wall.get(query_params).items;
        items.push(responseItems);
        i = i + 1;
        query_params.count = query_params.count - 100;
        query_params.offset = query_params.offset + 100;
    }
    return items;
"""


def get_posts_2500(
    query_params: tp.Dict[str, tp.Any],
    count: int = 1000
) -> tp.List[tp.Dict[str, tp.Any]]:
    query_params["count"] = count
    code_data = code % query_params
    request_data = {
        "access_token": config.VK_CONFIG["access_token"],
        "v": config.VK_CONFIG["version"],
        "code": code_data,
    }

    response = session.post(
        "execute", **request_data)

    if response.status_code == 200:
        response_data = []
        for posts in response.json()["response"]:
            response_data += posts

        return response_data


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 1000,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    query_params = {
        "owner_id": owner_id,
        "domain": domain,
        "offset": offset,
        "filter": filter,
        "extended": extended,
        "fields": fields,
        "v": "5.126"
    }

    wall_execute_data = []
    iter_count = math.ceil(count / max_count)
    i = 0
    while (i < iter_count) and (count > 0):
        if count >= max_count:
            posts_list = get_posts_2500(query_params)
            wall_execute_data += posts_list
            count -= 1000
            query_params["offset"] += 1000
        else:
            posts_list = get_posts_2500(query_params, count)
            wall_execute_data += posts_list
            break

    return pd.json_normalize(wall_execute_data)
