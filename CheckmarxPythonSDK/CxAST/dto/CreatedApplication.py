# encoding: utf-8
from .Rule import Rule


class CreatedApplication(object):
    def __init__(self, application_id, name, description, criticality, rules, tags,
                 created_at, updated_at):
        """

        Args:
            application_id (str):
            name (str):
            description (str):
            criticality (int):
            rules (`list` of `Rule`):
            tags (dict):
            created_at (str):
            updated_at (str):
        """
        self.id = application_id
        self.name = name
        self.description = description
        self.criticality = criticality
        self.rules = rules
        self.tags = tags
        self.createdAt = created_at
        self.updatedAt = updated_at

    def __str__(self):
        return """CreatedApplication(id={id}, name={name}, description={description}, 
        criticality={criticality}, rules={rules}, tags={tags}, createdAt={createdAt}, 
        updatedAt={updatedAt})""".format(
            id=self.id, name=self.name, description=self.description,
            criticality=self.criticality, rules=self.rules, tags=self.tags,
            createdAt=self.createdAt, updatedAt=self.updatedAt
        )
