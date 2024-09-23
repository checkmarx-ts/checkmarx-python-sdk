"""Compares two CxSAST presets.

This script compares two CxSAST presets, listing the queries that are
in one of the presets but not in the other.

"""

import sys
from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI
from CheckmarxPythonSDK.CxPortalSoapApiSDK import get_query_collection

projects_api = ProjectsAPI()


def compare_preset_details(preset_a, preset_b, query_map):
    """Compares the details (i.e., the queries) of two CxSAST presets.

    Parameters:
    preset_a (CxPreset): the first preset
    preset_b (CxPreset): the second preset
    """

    a_queries = set(preset_a.query_ids)
    b_queries = set(preset_b.query_ids)

    queries = []
    for query_id in a_queries - b_queries:
        queries.append(query_map[query_id])

    for q in sorted(queries):
        print(q)


def compare_presets(preset_a_name, preset_b_name):
    """Compares two CxSAST presets.

    Parameters:
    preset_a_name (str): the name of the first preset
    preset_b_name (str): the name of the second preset
    """

    all_presets = projects_api.get_all_preset_details()
    preset_a = None
    preset_b = None
    for preset in all_presets:
        if preset.name.lower() == preset_a_name.lower():
            if preset_a:
                print(f'Warning: multiple presets match "{preset_a_name}"')
            preset_a = projects_api.get_preset_details_by_preset_id(preset.id)
        elif preset.name.lower() == preset_b_name.lower():
            if preset_b:
                print(f'Warning: multiple presets match "{preset_b_name}"')
            preset_b = projects_api.get_preset_details_by_preset_id(preset.id)

    if not preset_a:
        raise Exception(f'{preset_a_name}: cannot find preset details')

    if not preset_b:
        raise Exception(f'{preset_b_name}: cannot find preset details')

    resp = get_query_collection()
    if not resp['IsSuccesfull']:
        raise Exception('Error retrieving queries')

    query_map = {}
    query_groups = resp['QueryGroups']
    for qg in query_groups:
        queries = qg['Queries']
        for q in queries:
            query_map[q['QueryId']] = f'{qg["PackageFullName"]}:{q["Name"]}'

    print(f'Queries in {preset_a.name} but not in {preset_b.name}:')
    compare_preset_details(preset_a, preset_b, query_map)

    print()

    print(f'Queries in {preset_b.name} but not in {preset_a.name}:')
    compare_preset_details(preset_b, preset_a, query_map)


if __name__ == '__main__':

    if len(sys.argv) < 3:
        print(f'usage: py {sys.argv[0]} <preset A> <preset B>',
              file=sys.stderr)
        sys.exit(1)

    preset_a = sys.argv[1]
    preset_b = sys.argv[2]

    try:
        compare_presets(preset_a, preset_b)
    except Exception as e:
        print(f'Error: {e}', file=sys.stderr)
        sys.exit(2)
