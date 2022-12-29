from .Result import Result


class Query:
    def __init__(self, query_id, categories, cwe_id, query_name, query_group, severity, language, language_hash,
                 language_change_date, severity_index, query_path, query_version_code, results=None):
        """

        Args:
            query_id (int):
            categories (str):
            cwe_id (int):
            query_name (str):
            query_group (str):
            severity (str):
            language (str):
            language_hash (str):
            language_change_date (str):
            severity_index (int):
            query_path (str):
            query_version_code (int):
            results (list of Result):
        """
        self.Id = query_id
        self.Categories = categories
        self.CweId = cwe_id
        self.Name = query_name
        self.Group = query_group
        self.Severity = severity
        self.Language = language
        self.LanguageHash = language_hash
        self.LanguageChangeDate = language_change_date
        self.SeverityIndex = severity_index
        self.QueryPath = query_path
        self.QueryVersionCode = query_version_code
        self.Results = results

    def __str__(self):
        return "Query(query_id={query_id}, categories={categories}, cwe_id={cwe_id}, query_name={query_name}, "\
               "query_group={query_group}, severity={severity}, language={language}, language_hash={language_hash}, "\
               "language_change_date={language_change_date}, severity_index={severity_index}, "\
               "query_path={query_path}, query_version_code={query_version_code}, results={results})".format(
                    query_id=self.Id,
                    categories=self.Categories,
                    cwe_id=self.CweId,
                    query_name=self.Name,
                    query_group=self.Group,
                    severity=self.Severity,
                    language=self.Language,
                    language_hash=self.LanguageHash,
                    language_change_date=self.LanguageChangeDate,
                    severity_index=self.SeverityIndex,
                    query_path=self.QueryPath,
                    query_version_code=self.QueryVersionCode,
                    results=self.Results
                )


def construct_query(item, results=None):
    return Query(
        query_id=int(item.get("id")),
        categories=item.get("categories"),
        cwe_id=int(item.get('cweId')),
        query_name=item.get("name"),
        query_group=item.get("group"),
        severity=item.get("Severity"),
        language=item.get("Language"),
        language_hash=item.get("LanguageHash"),
        language_change_date=item.get("LanguageChangeDate"),
        severity_index=int(item.get("SeverityIndex")),
        query_path=item.get("QueryPath"),
        query_version_code=int(item.get("QueryVersionCode")),
        results=results
    )
