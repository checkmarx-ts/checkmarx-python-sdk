class MemoryInfoRepresentation:
    def __init__(self, free, free_formated, free_percentage, total, total_formated, used, used_formated):
        self.free = free
        self.freeFormated = free_formated
        self.freePercentage = free_percentage
        self.total = total
        self.totalFormated = total_formated
        self.used = used
        self.usedFormated = used_formated

    def __str__(self):
        return f"MemoryInfoRepresentation(" \
               f"free={self.free} " \
               f"freeFormated={self.freeFormated} " \
               f"freePercentage={self.freePercentage} " \
               f"total={self.total} " \
               f"totalFormated={self.totalFormated} " \
               f"used={self.used} " \
               f"usedFormated={self.usedFormated} " \
               f")"

    def to_dict(self):
        return {
            "free": self.free,
            "freeFormated": self.freeFormated,
            "freePercentage": self.freePercentage,
            "total": self.total,
            "totalFormated": self.totalFormated,
            "used": self.used,
            "usedFormated": self.usedFormated,
        }


def construct_memory_info_representation(item):
    return MemoryInfoRepresentation(
        free=item.get("free"),
        free_formated=item.get("freeFormated"),
        free_percentage=item.get("freePercentage"),
        total=item.get("total"),
        total_formated=item.get("totalFormated"),
        used=item.get("used"),
        used_formated=item.get("usedFormated"),
    )
