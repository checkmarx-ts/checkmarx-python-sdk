from .QueryDescriptionSampleCode import QueryDescriptionSampleCode


class QueryDescription(object):
    def __init__(self, query_description_id, result_description, risk, cause, general_recommendations, samples,
                 example=None, best_fix_location=None):
        """

        Args:
            query_description_id (str):
            result_description (str):
            risk (str):
            cause (str):
            general_recommendations (str):
            samples (list of QueryDescriptionSampleCode):
            example (str):
            best_fix_location (str):
        """
        self.queryDescriptionId = query_description_id
        self.resultDescription = result_description
        self.risk = risk
        self.cause = cause
        self.generalRecommendations = general_recommendations
        self.sample = samples
        self.example = example
        self.bestFixLocation = best_fix_location

    def __str__(self):
        return """QueryDescription(queryDescriptionId={}, resultDescription={}, risk={}, cause={}, 
        generalRecommendations={}, sample={}, example={}, bestFixLocation={})""".format(
            self.queryDescriptionId,
            self.resultDescription,
            self.risk,
            self.cause,
            self.generalRecommendations,
            self.sample,
            self.example,
            self.bestFixLocation,
        )
