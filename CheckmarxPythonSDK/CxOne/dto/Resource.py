from dataclasses import dataclass


@dataclass
class Resource:
    id: str = None
    name: str = None
    type: str = None
    cluster_name: str = None
    asset_type: str = None
    public_exposed: bool = None
    image: str = None
    image_short_name: str = None
    image_sha: str = None
    replica_count: int = None
    tags: dict = None


def construct_resource(item):
    return Resource(
        id=item.get("id"),
        name=item.get("name"),
        type=item.get("type"),
        cluster_name=item.get("clusterName"),
        asset_type=item.get("assetType"),
        public_exposed=item.get("publicExposed"),
        image=item.get("image"),
        image_short_name=item.get("imageShortname"),
        image_sha=item.get("imageSha"),
        replica_count=item.get("replicaCount"),
        tags=item.get("tags"),
    )
