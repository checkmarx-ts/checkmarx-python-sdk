# encoding: utf-8

"""
    tests.test_custom_tasks_api

    :copyright Checkmarx
    :license MIT

"""

from CheckmarxPythonSDK.CxRestAPISDK.sast.projects.CustomTasksAPI import CustomTasksAPI


def test_get_all_custom_tasks():
    custom_tasks_api = CustomTasksAPI()
    custom_tasks = custom_tasks_api.get_all_custom_tasks()
    assert custom_tasks is not None


def test_get_custom_task_id_by_name():
    custom_task_name = "git"
    custom_tasks_api = CustomTasksAPI()
    task_id = custom_tasks_api.get_custom_task_id_by_name(custom_task_name)
    assert task_id is not None


def test_get_custom_task_by_id():
    custom_task_name = "git"
    custom_tasks_api = CustomTasksAPI()
    task_id = custom_tasks_api.get_custom_task_id_by_name(custom_task_name)
    custom_task = custom_tasks_api.get_custom_task_by_id(task_id)
    assert custom_task is not None
