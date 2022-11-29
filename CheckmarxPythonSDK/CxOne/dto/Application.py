# encoding: utf-8
class Application(object):
    def __init__(self, application_id, name, description, criticality, rules, project_ids, created_at,
                 updated_at, tags):
        """

        Args:
            application_id (str):
            name (str):
            description (str):
            criticality (int):
            rules (`list` of `Rule`):
            project_ids (`list` of str):
            created_at (str):
            updated_at (str):
            tags (dict):
        """
        self.id = application_id
        self.name = name
        self.description = description
        self.criticality = criticality
        self.rules = rules
        self.projectIds = project_ids
        self.createdAt = created_at
        self.updatedAt = updated_at
        self.tags = tags

    def __str__(self):
        return """Application(id={id}, name={name}, description={description}, 
        criticality={criticality}, rules={rules}, projectIds={projectIds}, 
        createdAt={createdAt}, updatedAt={updatedAt}, tags={tags})""".format(
            id=self.id, name=self.name, description=self.description,
            criticality=self.criticality, rules=self.rules, projectIds=self.projectIds,
            createdAt=self.createdAt, updatedAt=self.updatedAt, tags=self.tags
        )
