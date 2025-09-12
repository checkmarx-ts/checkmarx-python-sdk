from dataclasses import dataclass
from typing import List
from .CloudInsightAccount import CloudInsightAccount, construct_cloud_insight_account


@dataclass
class PaginatedAccountsListResponse(object):
    data: List[CloudInsightAccount] = None
    total: int = None
    current_page: int = None
    last_page: int = None


def construct_paginated_accounts_list_response(item):
    return {
            "data": [
                construct_cloud_insight_account(account) for account in item.get("data", []) or []
            ],
            "total": item.get("total"),
            "currentPage": item.get("currentPage"),
            "lastPage": item.get("lastPage")
        }
