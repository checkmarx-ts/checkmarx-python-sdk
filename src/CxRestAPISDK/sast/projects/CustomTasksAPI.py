# encoding: utf-8
import http

import requests

from src.CxRestAPISDK.config import CxConfig
from src.CxRestAPISDK.auth import AuthenticationAPI

from src.CxRestAPISDK.sast.projects.dto.customTasks import CxCustomTask
from src.CxRestAPISDK.sast.projects.dto import CxLink


class CustomTasksAPI(object):
    """
    REST API: custom tasks
    """
    base_url = CxConfig.CxConfig.config.url
    custom_tasks_url = base_url + "/customTasks"
    custom_task_url = base_url + "/customTasks/{id}"
    custom_tasks = []

    def __init__(self):
        self.retry = 0

    def get_all_custom_tasks(self):
        """
        REST API: get all custom tasks
        :return:
        """
        custom_tasks = []
        r = requests.get(
            url=CustomTasksAPI.custom_tasks_url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers
        )
        if r.status_code == http.HTTPStatus.OK:
            a_list = r.json()
            custom_tasks = [
                CxCustomTask.CxCustomTask(
                    id=item.get("id"),
                    name=item.get("name"),
                    type=item.get("type"),
                    data=item.get("data"),
                    link=CxLink.CxLink(
                        (item.get("link", {}) or {}).get("rel"),
                        (item.get("link", {}) or {}).get("uri")
                    )
                ) for item in a_list
            ]
            CustomTasksAPI.custom_tasks = custom_tasks
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise Exception("Not Found")
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < 3):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_custom_tasks()
        else:
            raise Exception("Network Error")
        return custom_tasks

    def get_custom_task_id_by_name(self, task_name):
        custom_tasks = self.get_all_custom_tasks()
        a_dict = {
            item.name: item.id for item in custom_tasks
        }
        return a_dict.get(task_name)

    def get_custom_task_by_id(self, task_id):
        """

        :param task_id:
        :return:
        """
        custom_task = None
        custom_task_url = self.custom_task_url.format(id=task_id)
        r = requests.get(
            url=custom_task_url,
            headers=AuthenticationAPI.AuthenticationAPI.auth_headers
        )
        if r.status_code == http.HTTPStatus.OK:
            a_dict = r.json()
            custom_task = CxCustomTask.CxCustomTask(
                id=a_dict.get("id"),
                name=a_dict.get("name"),
                type=a_dict.get("type"),
                data=a_dict.get("data"),
                link=CxLink.CxLink(
                    (a_dict.get("link", {}) or {}).get("rel"),
                    (a_dict.get("link", {}) or {}).get("uri")
                )
            )
        elif r.status_code == http.HTTPStatus.BAD_REQUEST:
            raise Exception("Bad Request")
        elif r.status_code == http.HTTPStatus.NOT_FOUND:
            raise Exception("Not Found")
        elif (r.status_code == http.HTTPStatus.UNAUTHORIZED) and (self.retry < 3):
            AuthenticationAPI.AuthenticationAPI.reset_auth_headers()
            self.retry += 1
            self.get_all_custom_tasks()
        else:
            raise Exception("Network Error")
        return custom_task
