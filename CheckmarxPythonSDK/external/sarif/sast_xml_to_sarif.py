from uuid import uuid4
from typing import List
from CheckmarxPythonSDK.external.sarif.dto import (
    CxSarifCategory,
    SarifArtifactLocation,
    SarifDescription,
    SarifDriver,
    SarifDriverRule,
    SarifLocation,
    SarifMessage,
    SarifPhysicalLocation,
    SarifPhysicalLocationPropertyBag,
    SarifRegion,
    SarifResultPropertyBag,
    SarifResultsCollection,
    SarifRun,
    SarifScanResult,
    SarifTaxa,
    SarifTaxaPropertyBag,
    SarifTaxaRelationship,
    SarifTaxaRelationshipTarget,
    SarifTaxonomy,
    SarifTool,
    SarifToolComponent,
    SarifMultiFormatMessageString,
)
from CheckmarxPythonSDK.external.sarif.stig_mapping import stig_mapping
from CheckmarxPythonSDK.CxPortalSoapApiSDK.CxPortalWebService import get_query_collection
from CheckmarxPythonSDK.CxRestAPISDK.CxSastXML.xml_results import get_xml_results
from CheckmarxPythonSDK.CxRestAPISDK.CxSastXML.dto import (
    CxXMLResults
)


def create_sarif_report_from_sast_xml(xml_path, xml_string=None, query_risk_dict=None, query_recommendation_dict=None) \
        -> SarifResultsCollection:
    xml_report = get_xml_results(xml_path, xml_string)
    return create_sarif_results(xml_report, query_risk_dict=query_risk_dict,
                                query_recommendation_dict=query_recommendation_dict)


def create_sarif_results(xml_report, query_risk_dict, query_recommendation_dict) -> SarifResultsCollection:
    sarif_runs = [
        create_sarif_run(xml_report,
                         query_risk_dict=query_risk_dict,
                         query_recommendation_dict=query_recommendation_dict)
    ]
    return SarifResultsCollection(
        schema="https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
        version="2.1.0",
        runs=sarif_runs
    )


def create_sarif_run(xml_report: CxXMLResults, query_risk_dict, query_recommendation_dict) -> SarifRun:
    taxonomies = create_taxonomies(xml_report)
    tool = SarifTool(driver=SarifDriver(
        name="Checkmarx CxSAST",
        full_name="Checkmarx CxSAST",
        version="1.0",
        information_uri="https://checkmarx.com",
        rules=convert_cx_results_to_sarif_rules(xml_report, taxonomies, query_risk_dict=query_risk_dict)
    ))
    results = convert_cx_results_to_sarif_results(xml_report, taxonomies, query_recommendation_dict)
    return SarifRun(tool=tool, results=results, taxonomies=taxonomies)


def convert_cx_results_to_sarif_rules(xml_report: CxXMLResults, taxonomies, query_risk_dict) -> List[SarifDriverRule]:
    queries = xml_report.Queries
    category_taxa: List[SarifTaxa] = taxonomies[0].taxa

    return [
        SarifDriverRule(
            rule_id=str(query.Name),
            name=query.Name,
            short_description=SarifDescription(text=""),
            full_description=SarifDescription(text=""),
            help_uri=f"https://cwe.mitre.org/data/definitions/{query.CweId}.html",
            help=SarifMultiFormatMessageString(
                general="",
                text=query_risk_dict.get(query.Id),
                markdown="",
            ),
            relation_ships=[
                SarifTaxaRelationship(
                    target=SarifTaxaRelationshipTarget(
                        target_id=get_id_of_sarif_tool_component(query.Name, category_taxa),
                        index=0,
                        tool_component=SarifToolComponent(
                            name=taxonomies[0].name,
                            guid=taxonomies[0].guid,
                            index=get_index_of_sarif_tool_component(query.Name, category_taxa)
                        )
                    )
                )
            ]
        ) for query in queries
    ]


def get_id_of_sarif_tool_component(query_name, category_taxa):
    for item in category_taxa:
        if item.name == query_name:
            return item.id
    return 0


def get_index_of_sarif_tool_component(query_name, category_taxa):
    for index, item in enumerate(category_taxa):
        if item.name == query_name:
            return index
    return None


def convert_cx_results_to_sarif_results(xml_report: CxXMLResults, taxonomies, query_recommendation_dict) -> List[SarifScanResult]:
    sarif_result = []

    category_taxa: List[SarifTaxa] = taxonomies[0].taxa

    for query in xml_report.Queries:
        for result in query.Results:
            sarif_result.append(
                SarifScanResult(
                    rule_id=str(query.Name),
                    kind=get_sarif_scan_result_kind(query.Severity),
                    level=get_sarif_scan_result_level(query.Severity),
                    message=SarifMessage(text=query.Name),
                    properties=SarifResultPropertyBag(
                        tags=["similarityId", "cxCwe", "cxStigID", "cxStigRuleID"],
                        similarity_id=int(result.Path.SimilarityId),
                        cx_cwe=str(query.CweId),
                        cx_stig_id=get_stig_id_from_category_taxa_by_query_id(category_taxa, query.Id),
                        cx_stig_rule_id=get_stig_rule_id_from_category_taxa_by_query_id(category_taxa, query.Id)
                    ),
                    locations=[
                        SarifLocation(
                            physical_location=SarifPhysicalLocation(
                                artifact_location=SarifArtifactLocation(uri=node.FileName),
                                region=SarifRegion(
                                    start_line=int(node.Line),
                                    start_column=int(node.Column),
                                    end_column=int(node.Column) + int(node.Length)
                                ),
                                properties=SarifPhysicalLocationPropertyBag(
                                    tags=["snippet"],
                                    snippet=node.Snippet.Line.Code if node.Snippet else ""
                                )
                            )
                        ) for node in result.Path.PathNodes
                    ],
                    fixes=[{
                        "description": {
                            "text": query_recommendation_dict.get(query.Id)
                        }
                    }]
                )
            )
    return sarif_result


def get_stig_id_from_category_taxa_by_query_id(category_taxa: List[SarifTaxa], query_id):
    for sarif_taxa in category_taxa:
        if sarif_taxa.id == str(query_id):
            return sarif_taxa.properties.cxStigID


def get_stig_rule_id_from_category_taxa_by_query_id(category_taxa: List[SarifTaxa], query_id):
    for sarif_taxa in category_taxa:
        if sarif_taxa.id == str(query_id):
            return sarif_taxa.properties.cxStigRuleID


def get_sarif_scan_result_kind(query_severity) -> str:
    if query_severity == "Information":
        return "informational"
    else:
        return "fail"


def get_sarif_scan_result_level(query_severity) -> str:
    if query_severity == "Information":
        return "none"
    elif query_severity == "Low":
        return "note"
    elif query_severity == "Medium":
        return "warning"
    elif query_severity == "High":
        return "error"


def create_taxonomies(xml_report: CxXMLResults) -> List[SarifTaxonomy]:
    return [create_category_taxonomy(xml_report)]


def create_category_taxonomy(xml_report: CxXMLResults) -> SarifTaxonomy:
    guid = str(uuid4())
    name = "Cx Result Categories"
    full_description = SarifDescription(text="Checkmarx SAST categories")
    short_description = SarifDescription(text="Checkmarx SAST categories")
    taxa = []

    query_ids = [query.Id for query in xml_report.Queries]
    response = get_query_collection()
    query_groups = response.get("QueryGroups")

    for query_group in query_groups:
        query_group_name = query_group.get("Name")
        if "General" in query_group_name or "Quality" in query_group_name or "Best" in query_group_name:
            continue
        for query in query_group.get("Queries"):
            categories = query.get('Categories')
            if categories is None:
                categories = []

            query_id = query.get('QueryId')
            # ignore query that is not in the XML report
            if query_id not in query_ids:
                continue

            taxa_id = str(query_id)
            name = query.get('Name')
            full_description = SarifDescription(text="")
            short_description = SarifDescription(text="")
            stig_id = find_stig_id(categories)
            properties = SarifTaxaPropertyBag(
                tags=["cxCwe", "cxSeverity", "cxCategoryName", "cxCategoryType", "cxQueryGroupName", "cxLanguageName",
                      "cxPackageTypeName", "cxStigID", "cxStigRuleID"],
                cx_cwe=query.get('Cwe'),
                cx_severity=convert_cx_severity_to_string(query.get('Severity')),
                cx_category=[
                    CxSarifCategory(
                        cx_category_name=category.get("CategoryName"),
                        cx_category_type=category.get("CategoryType")
                    ) for category in categories
                ],
                cx_query_group_name=query_group.get('Name'),
                cx_language_name=query_group.get('LanguageName'),
                cx_package_type_name=query_group.get('PackageTypeName'),
                cx_stig_id=find_stig_id(categories),
                cx_stig_rule_id=find_stig_rule_id(stig_id)
            )
            taxa.append(SarifTaxa(
                taxa_id=taxa_id,
                name=name,
                full_description=full_description,
                short_description=short_description,
                properties=properties
            ))
    return SarifTaxonomy(
        guid=guid, name=name, full_description=full_description, short_description=short_description,
        taxa=taxa
    )


def convert_cx_severity_to_string(severity: int) -> str:
    if severity == 0:
        return "Information"
    elif severity == 1:
        return "Low"
    elif severity == 2:
        return "Medium"
    elif severity == 3:
        return "High"
    else:
        return ""


def find_stig_id(categories) -> str:
    for category in categories:
        category_name = category.get("CategoryName")
        if category_name.startswith("APSC"):
            stig_id = category_name.split(" ")[0]
            return stig_id
    return ""


def find_stig_rule_id(stig_id) -> str:
    return stig_mapping.get(stig_id)
