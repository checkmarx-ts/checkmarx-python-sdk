class ProviderRepresentation:
    def __init__(self, operational_info, order):
        self.operationalInfo = operational_info
        self.order = order

    def __str__(self):
        return f"ProviderRepresentation(" \
               f"operationalInfo={self.operationalInfo} " \
               f"order={self.order} " \
               f")"

    def to_dict(self):
        return {
            "operationalInfo": self.operationalInfo,
            "order": self.order,
        }


def construct_provider_representation(item):
    return ProviderRepresentation(
        operational_info=item.get("operationalInfo"),
        order=item.get("order"),
    )
