from dataclasses import dataclass


@dataclass
class CloudInsightContainer:
    container_id: str = None
    cluster_name: str = None
    container_name: str = None
    public_exposed: str = None
    image: str = None
    image_short_name: str = None
    project: str = None


def construct_cloud_insight_container(item):
    return CloudInsightContainer(
        container_id=item.get("containerId"),
        cluster_name=item.get("clusterName"),
        container_name=item.get("containerName"),
        public_exposed=item.get("publicExposed"),
        image=item.get("image"),
        image_short_name=item.get("imageShortname"),
        project=item.get("project")
    )
