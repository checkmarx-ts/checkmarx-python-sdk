from dataclasses import dataclass
from typing import List
from .CloudInsightAccountLog import CloudInsightAccountLog, construct_cloud_insight_account_log


@dataclass
class PaginatedAccountLogsListResponse:
    data: List[CloudInsightAccountLog] = None
    total: int = None
    current_page: int = None
    last_page: int = None


def construct_paginated_account_logs_list_response(item):
    return PaginatedAccountLogsListResponse(
        data=[
            construct_cloud_insight_account_log(account_log) for account_log in item.get("data", [])
        ],
        total=item.get("total"),
        current_page=item.get("currentPage"),
        last_page=item.get("lastPage"),
    )
