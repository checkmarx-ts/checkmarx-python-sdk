# encoding: utf-8


class CxCustomTask(object):
    """
    custom tasks
    """

    def __init__(self, custom_task_id, name, custom_task_type, data, link):
        """

        Args:
            custom_task_id (int):
            name (str):
            custom_task_type (str):
            data (str):
            link (CxLink):
        """
        self.id = custom_task_id
        self.name = name
        self.type = custom_task_type
        self.data = data
        self.link = link

    def __str__(self):
        return "CxCustomTask(id={], name={}, type={}, data={}, link={})".format(
            self.id, self.name, self.type, self.data, self.link
        )
