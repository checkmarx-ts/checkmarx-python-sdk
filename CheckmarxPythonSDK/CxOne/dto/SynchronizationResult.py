class SynchronizationResult:
    def __init__(self, added, failed, ignored, removed, status, updated):
        self.added = added
        self.failed = failed
        self.ignored = ignored
        self.removed = removed
        self.status = status
        self.updated = updated

    def __str__(self):
        return f"SynchronizationResult(" \
               f"added={self.added} " \
               f"failed={self.failed} " \
               f"ignored={self.ignored} " \
               f"removed={self.removed} " \
               f"status={self.status} " \
               f"updated={self.updated} " \
               f")"

    def to_dict(self):
        return {
            "added": self.added,
            "failed": self.failed,
            "ignored": self.ignored,
            "removed": self.removed,
            "status": self.status,
            "updated": self.updated,
        }


def construct_synchronization_result(item):
    return SynchronizationResult(
        added=item.get("added"),
        failed=item.get("failed"),
        ignored=item.get("ignored"),
        removed=item.get("removed"),
        status=item.get("status"),
        updated=item.get("updated"),
    )
