# encoding: utf-8
import json
from ..utilities import (type_check)


class BranchInput(object):
    def __init__(self, name, isDefaultBranch):
        """

        Args:
            name (str): name of branch
            isDefaultBranch (bool): is default - should be true
        """
        type_check(name, str)
        type_check(isDefaultBranch, bool)
        self.name = name
        self.isDefaultBranch = isDefaultBranch

    def __str__(self):
        return """BranchInput(name={name}, isDefaultBranch={isDefaultBranch})""".format(
            name=self.name, isDefaultBranch=self.isDefaultBranch
        )

    def get_post_data(self):
        return json.dumps(
            {
                "name": self.name,
                "isDefaultBranch": self.isDefaultBranch,
            }
        )
