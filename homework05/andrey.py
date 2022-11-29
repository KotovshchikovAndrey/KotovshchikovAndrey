import math
import time
import typing as tp

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
        query_params.offset = query_params.offset + responseItems.length;
    }
    return items;
"""


class PostVkAdapter:
    _query_params: tp.Dict[str, tp.Any]
    _total_requests_count_in_second: int

    def __init__(self, total_requests_count_in_second: int, **kwargs: str) -> None:
        self._total_requests_count_in_second = total_requests_count_in_second
        self._query_params = kwargs

    def get_posts_execute(
        self, count: int, max_count: int
    ) -> tp.List[tp.Dict[str, tp.Any]]:
        offset = self._query_params.get("offset", 0)
        posts_execute_data = []
        iter_count = math.ceil(count / max_count)
        start = time.time()
        i, send_request_count = 0, 0
        while (i < iter_count) and (count > 0):
            if count >= max_count:
                posts_list = self._get_posts_from_api()
                posts_execute_data += posts_list
                count -= 1000
                offset += 1000
            else:
                posts_list = self._get_posts_from_api(count)
                posts_execute_data += posts_list
                break

            send_request_count += 1
            request_delta_time = time.time() - start
            if (request_delta_time < 1) and (
                send_request_count >= self._total_requests_count_in_second
            ):
                time.sleep(1 - request_delta_time)
                start, send_request_count = time.time(), 0

        return posts_execute_data

    def _get_posts_from_api(self, count: int = 1000) -> tp.List[tp.Dict[str, tp.Any]]:
        self._query_params["count"] = count
        code_data = code % self._query_params
        request_data = {
            "access_token": config.VK_CONFIG["access_token"],
            "v": config.VK_CONFIG["version"],
            "code": code_data,
        }

        response = session.post("execute", **request_data)
        try:
            response_data = response.json()["response"]
        except Exception as e:
            raise APIError.bad_request(message=str(e))

        posts_execute_list = []
        for posts in response_data:
            posts_execute_list += posts

        return posts_execute_list


p = {
    "owner_id": "",
    "domain": "itmoru",
    "offset": 150,
    "filter": "owner",
    "extended": 0,
    "fields": "",
}

post_adapter = PostVkAdapter(total_requests_count_in_second=3, **p)
r = post_adapter.get_posts_execute(count=7500, max_count=1000)
print(len(r))
