# encoding: utf-8
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CxScanQueueDetail:
    """
    scan queue detail
    """

    id: Optional[int] = None
    stage: Optional[object] = None
    stage_details: Optional[str] = None
    step_details: Optional[str] = None
    project: Optional[object] = None
    engine: Optional[object] = None
    languages: Optional[List] = None
    team_id: Optional[str] = None
    date_created: Optional[str] = None
    queued_on: Optional[str] = None
    engine_started_on: Optional[str] = None
    completed_on: Optional[str] = None
    loc: Optional[int] = None
    is_incremental: Optional[bool] = None
    is_public: Optional[bool] = None
    origin: Optional[str] = None
    queue_position: Optional[int] = None
    total_percent: Optional[int] = None
    stage_percent: Optional[int] = None
    initiator: Optional[str] = None

    @classmethod
    def from_dict(cls, item: dict) -> "CxScanQueueDetail":
        from .CxScanStage import CxScanStage

        return cls(
            id=item.get("id"),
            stage=CxScanStage.from_dict(item.get("stage") or {}),
            stage_details=item.get("stageDetails"),
            step_details=item.get("stepDetails"),
            project=item.get("project"),
            engine=item.get("engine"),
            languages=item.get("languages"),
            team_id=item.get("teamId"),
            date_created=item.get("dateCreated"),
            queued_on=item.get("queuedOn"),
            engine_started_on=item.get("engineStartedOn"),
            completed_on=item.get("completedOn"),
            loc=item.get("loc"),
            is_incremental=item.get("isIncremental"),
            is_public=item.get("isPublic"),
            origin=item.get("origin"),
            queue_position=item.get("queuePosition"),
            total_percent=item.get("totalPercent"),
            stage_percent=item.get("stagePercent"),
            initiator=item.get("initiator"),
        )
