class ResourceRepresentation:
    def __init__(self, resource_representation_id, attributes, display_name, icon_uri, name, owner_managed_access,
                 scopes, resource_representation_type, uris):
        self.id = resource_representation_id
        self.attributes = attributes
        self.displayName = display_name
        self.icon_uri = icon_uri
        self.name = name
        self.ownerManagedAccess = owner_managed_access
        self.scopes = scopes
        self.type = resource_representation_type
        self.uris = uris

    def __str__(self):
        return f"ResourceRepresentation(" \
               f"id={self.id} " \
               f"attributes={self.attributes} " \
               f"displayName={self.displayName} " \
               f"icon_uri={self.icon_uri} " \
               f"name={self.name} " \
               f"ownerManagedAccess={self.ownerManagedAccess} " \
               f"scopes={self.scopes} " \
               f"type={self.type} " \
               f"uris={self.uris} " \
               f")"

    def to_dict(self):
        return {
            "id": self.id,
            "attributes": self.attributes,
            "displayName": self.displayName,
            "icon_uri": self.icon_uri,
            "name": self.name,
            "ownerManagedAccess": self.ownerManagedAccess,
            "scopes": self.scopes,
            "type": self.type,
            "uris": self.uris,
        }


def construct_resource_representation(item):
    return ResourceRepresentation(
        resource_representation_id=item.get("id"),
        attributes=item.get("attributes"),
        display_name=item.get("displayName"),
        icon_uri=item.get("icon_uri"),
        name=item.get("name"),
        owner_managed_access=item.get("ownerManagedAccess"),
        scopes=item.get("scopes"),
        resource_representation_type=item.get("type"),
        uris=item.get("uris"),
    )
