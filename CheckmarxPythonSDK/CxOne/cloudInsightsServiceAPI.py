# encoding: utf-8
import json
from .httpRequests import get_request, post_request, delete_request
from CheckmarxPythonSDK.utilities.compat import OK
from .utilities import type_check
from .dto import (
    CreateEnrichAccount,
    EnrichAccount,
    Account,
    StartEnrich,
    Container,
)

api_url = "/api/cnas"


def create_enrich_account(data):
    """

    Args:
        data (CreateEnrichAccount):

    Returns:
        EnrichAccount
    """
    type_check(data, CreateEnrichAccount)
    relative_url = api_url + "/accounts/enrich"
    data = json.dumps(data.to_dict())
    response = post_request(relative_url=relative_url, data=data)
    item = response.json()
    return EnrichAccount(
        name=item.get("name"),
        account_id=item.get("accountID"),
    )


def get_enrich_account_by_external_id(external_id, offset=0, limit=100):
    """

    Args:
        external_id (str): A unique identifier provided by Checkmarx
        offset (int): Offset the results Default value : 0
        limit (int): Limit the number of results

    Returns:

    """
    type_check(external_id, str)
    type_check(offset, int)
    type_check(limit, int)
    relative_url = api_url + "/accounts/enrich?external-id={}&offset={}&limit={}".format(
        external_id, offset, limit
    )
    response = get_request(relative_url=relative_url)
    item = response.json()
    return {
        "data": [
            Account(
                account_id=account.get("id"),
                name=account.get("name"),
                credentials=account.get("credentials"),
                account_type=account.get("accountType"),
                tenant_id=account.get("tenantId"),
                created_at=account.get("createdAt"),
                updated_at=account.get("updatedAt"),
                last_scan_date=account.get("lastScanDate"),
            ) for account in item.get("data", []) or []
        ],
        "total": item.get("total"),
        "currentPage": item.get("currentPage"),
        "lastPage": item.get("lastPage")
    }


def start_enrichment(cloud_insights_account_id, start_enrich):
    """

    Args:
        cloud_insights_account_id (str):   uuid4
        start_enrich (StartEnrich)

    Returns:
        message (str)
    """
    type_check(cloud_insights_account_id, str)
    type_check(start_enrich, StartEnrich)

    relative_url = api_url + "/accounts/{id}/enrich".format(id=cloud_insights_account_id)
    post_data = json.dumps(start_enrich.to_dict())
    response = post_request(relative_url=relative_url, data=post_data)
    item = response.json()
    return item.get("message")


def get_cloud_insight_account(account_id):
    """

    Args:
        account_id (str): Cloud Insights account ID

    Returns:
        Account
    """
    type_check(account_id, str)
    relative_url = api_url + "/accounts/{id}".format(id=account_id)
    response = get_request(relative_url=relative_url)
    account = response.json()
    return Account(
        account_id=account.get("id"),
        name=account.get("name"),
        credentials=account.get("credentials"),
        account_type=account.get("accountType"),
        tenant_id=account.get("tenantId"),
        created_at=account.get("createdAt"),
        updated_at=account.get("updatedAt"),
        last_scan_date=account.get("lastScanDate"),
    )


def delete_cloud_insight_account(account_id):
    """

      Args:
          account_id (str): Cloud Insights account ID

      Returns:
          bool
      """
    is_successful = False
    relative_url = api_url + "/accounts/{id}".format(id=account_id)
    response = delete_request(relative_url=relative_url)
    if response.status_code == OK:
        is_successful = True
    return is_successful


def get_all_containers_for_an_account_id(account_id, limit=100, offset=0, image_name=None, image_short_name=None,
                                         project_name=None, repo_url=None, cluster_name=None, public_exposed=None,
                                         search=None, cluster_id=None, order_column=None, order_direction=None):
    """

    Args:
        account_id (str): Cloud Insights account ID
        limit (int): Limit the number of results
        offset (int): Offset the results Default value : 0
        image_name (str):
        image_short_name (str):
        project_name (str):
        repo_url (str):
        cluster_name (str):
        public_exposed (str):
        search (str):
        cluster_id (str):
        order_column (str):
        order_direction (str):

    Returns:

    """
    type_check(account_id, str)
    type_check(limit, int)
    type_check(offset, int)
    type_check(image_name, str)
    type_check(image_short_name, str)
    type_check(project_name, str)
    type_check(repo_url, str)
    type_check(cluster_name, str)
    type_check(public_exposed, str)
    type_check(search, str)
    type_check(cluster_id, str)
    type_check(order_column, str)
    type_check(order_direction, str)
    relative_url = api_url + "/accounts/{id}/containers?limit={limit}&offset={offset}".format(
        id=account_id, limit=limit, offset=offset
    )
    if image_name:
        relative_url += "&image-name={}".format(image_name)
    if image_short_name:
        relative_url += "&image-short-name={}".format(image_short_name)
    if project_name:
        relative_url += "&project-name={}".format(project_name)
    if repo_url:
        relative_url += "&repo-url={}".format(repo_url)
    if cluster_name:
        relative_url += "&cluster-name={}".format(cluster_name)
    if public_exposed:
        relative_url += "&public-exposed={}".format(public_exposed)
    if search:
        relative_url += "&search={}".format(search)
    if cluster_id:
        relative_url += "&cluster-id={}".format(cluster_id)
    if order_column:
        relative_url += "&order-column={}".format(order_column)
    if order_direction:
        relative_url += "&order-direction={}".format(order_direction)
    response = get_request(relative_url=relative_url)
    item = response.json()
    return {
        "data": [
            Container(
                container_id=container.get("containerId"),
                cluster_name=container.get("clusterName"),
                container_name=container.get("containerName"),
                public_exposed=container.get("publicExposed"),
                image=container.get("image"),
                image_short_name=container.get("imageShortname"),
                project=container.get("project")
            ) for container in item.get("data", []) or []
        ],
        "total": item.get("total"),
        "currentPage": item.get("currentPage"),
        "lastPage": item.get("lastPage")
    }
