from dataclasses import dataclass


@dataclass
class ByorJobPatchRequest:
    status: str = None  # Canceled is the only valid input.

    def to_dict(self):
        return {
            "status": self.status
        }


def construct_byor_job_patch_request(item):
    return ByorJobPatchRequest(
        status=item.get("status")
    )
