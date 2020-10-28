# encoding: utf-8


class CxPolicyFindingResponse(object):
    """
    policy finding response
    """
    def __init__(self, policy_finding_id, link):
        """

        Args:
            policy_finding_id (int):
            link (:obj:`CxLink`):
        """
        self.id = policy_finding_id
        self.link = link

    def __str__(self):
        return "CxPolicyFindingResponse(id={}, link={})".format(
            self.id, self.link
        )
