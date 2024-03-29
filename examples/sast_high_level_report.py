"""Generate a simple summary of result evolution across a range of dates."""
import argparse
import csv
from datetime import date
from datetime import datetime
import logging
import sys

from CheckmarxPythonSDK.CxODataApiSDK.HttpRequests import get_request
from CheckmarxPythonSDK.CxPortalSoapApiSDK import get_compare_scan_results
from CheckmarxPythonSDK.CxRestAPISDK import AccessControlAPI
from CheckmarxPythonSDK.CxRestAPISDK import CustomFieldsAPI
from CheckmarxPythonSDK.CxRestAPISDK import ProjectsAPI

access_control_api = AccessControlAPI()
custom_fields_api = CustomFieldsAPI()
projects_api = ProjectsAPI()

class Summary:
    """A summary of the differences across two scans."""

    def __init__(self, project_name, fixed, not_exploitable, new,
                 recurrent, custom_fields):

        self.project_name = project_name
        self.fixed = fixed
        self.not_exploitable = not_exploitable
        self.new = new
        self.recurrent = recurrent
        self.custom_fields = custom_fields

    def add(self, other):
        """Add the figures from other to this summary."""

        self.fixed += other.fixed
        self.not_exploitable += other.not_exploitable
        self.new += other.new
        self.recurrent += other.recurrent

    def write_csv(self, writer):

        writer.writerow([self.project_name, self.fixed,self.not_exploitable,
                         self.new, self.recurrent, *self.custom_fields])

    def __repr__(self):

        return f'Summary({self.project_name},{self.fixed},' \
            f'{self.not_exploitable},' \
            f'{self.new},{self.recurrent})'

    def __str__(self):

        return f'Summary[project_name={self.project_name},' \
            f'fixed={self.fixed},' \
            f'not_exploitable={self.not_exploitable},' \
            f'new={self.new},recurrent={self.recurrent},' \
            f'custom_fields={self.custom_fields}]'


def get_all_scans_in_date_range(args):

    team = None
    team_filter = ''
    if args.team_name:
        team = get_team_by_name(args.team_name)
        team_filter = f'%20and%20OwningTeamId%20eq%20{team.id}'

    project_filter = ''
    if args.project_name:
        project = get_project_by_name(args.project_name, team)
        project_filter = f'%20and%20ProjectId%20eq%20{project.project_id}'

    url = f'/Cxwebinterface/odata/v1/Scans?' \
        '$select=Id,ProjectId,ProjectName,OwningTeamId,IsIncremental,ScanRequestedOn,EngineFinishedOn' \
        f'&$filter=ScanRequestedOn%20ge%20{args.start_date}' \
        f'%20and%20ScanRequestedOn%20lt%20{args.end_date}' \
        f'{project_filter}' \
        f'{team_filter}' \
        f'&$orderby=ScanRequestedOn%20desc'

    logging.debug(f'url: {url}')
    return get_request(relative_url=url)


def get_scan_with_results(scan_id):

    url = f'/Cxwebinterface/odata/v1/Scans({scan_id})?' \
        '&$expand=Results($expand=State)'

    logging.debug(f'url: {url}')
    scan = get_request(relative_url=url)[0]
    logging.debug(f'scan: id={scan["Id"]}' \
                  f',project_name={scan["ProjectName"]}' \
                  f',total_vulnerabilities={scan["TotalVulnerabilities"]}' \
                  f',high={scan["High"]}' \
                  f',medium={scan["Medium"]}' \
                  f',low={scan["Low"]}' \
                  f',info={scan["Info"]}')
    return scan


def make_result_map(results):

    result_map = {}
    for result in results:
        similarity_id = result['SimilarityId']
        if similarity_id in result_map:
            logging.debug(f'Similarity ID {similarity_id} already in result map')
            log_result('Old', result_map[similarity_id])
            log_result('New', result)
        result_map[similarity_id] = result

    return result_map


def log_result(msg, result):

    logging.debug(f'{msg}: id={result["Id"]},result_id={result["ResultId"]},scan_id={result["ScanId"]},similarity_id={result["SimilarityId"]},path_id={result["PathId"]},query_id={result["QueryId"]}')


def count_not_exploitable(results):

    not_exploitable = 0
    for result in results:
        if result['StateId'] == 1:
            not_exploitable = not_exploitable + 1

    return not_exploitable


def filter_not_exploitable(similarity_ids, result_map):

    return [si for si in similarity_ids if result_map[si]['StateId'] != 1]


def get_project_by_name(project_name, team=None):

    if team:
        return projects_api.get_project_id_by_project_name_and_team_full_name(project_name, team.full_name)
    else:
        for p in projects_api.get_all_project_details():
            if p.name == project_name:
                return p

        raise ValueError(f'{project_name}: no such project')


def get_team_by_name(team_name):

    if team_name.find('/') >= 0:
        team_id = access_control_api.get_team_id_by_full_name(team_name)
        return access_control_api.get_team_by_id(team_id)
    else:
        team = None
        for t in access_control_api.get_all_teams():
            if t.name == team_name:
                if team:
                    raise ValueError(f'{team_name}: name is not unique')
                else:
                    team = t

        if team:
            return team
        else:
            raise ValueError(f'{team_name}: no such team')


class Project:

    def __init__(self, project_id, project_name, custom_field_names):

        self.project_id = project_id
        self.project_name = project_name
        self.first_scan_date = None
        self.first_scan_id = None
        self.last_scan_date = None
        self.last_scan_id = None
        self.custom_fields = []

        if custom_field_names:
            logging.debug(f'Getting details of project {self.project_id}')
            cx_project = projects_api.get_project_details_by_id(self.project_id)
            for field_name in custom_field_names:
                found = False
                for cx_custom_field in cx_project.custom_fields:
                    if field_name == cx_custom_field.name:
                        self.custom_fields.append(cx_custom_field.value)
                        found = True
                        break
                if not found:
                    self.custom_fields.append('')

    def add_scan(self, scan):

        scan_id = scan['Id']
        t = scan['ScanRequestedOn'].split('.')[0]
        scan_requested_on = datetime.fromisoformat(t).astimezone()
        logging.debug(f'scan_requested_on: {scan_requested_on}, self.first_scan_date: {self.first_scan_date}, self.last_scan_date: {self.last_scan_date}')
        if self.first_scan_date:
            if scan_requested_on <= self.first_scan_date:
                self.first_scan_date = scan_requested_on
                self.first_scan_id = scan_id
            elif scan_requested_on > self.last_scan_date:
                self.last_scan_date = scan_requested_on
                self.last_scan_id = scan_id
        else:
            self.first_scan_date = scan_requested_on
            self.first_scan_id = scan_id
            self.last_scan_date = scan_requested_on
            self.last_scan_id = scan_id

    def compare_scans(self):

        if not self.first_scan_date:
            raise Exception

        if self.first_scan_id != self.last_scan_id:
            logging.debug(f'Comparing scans {self.first_scan_id} and {self.last_scan_id} for project {self.project_name}')

            first_scan_data = get_scan_with_results(self.first_scan_id)
            first_results = first_scan_data['Results']
            first_result_map = make_result_map(first_results)
            last_scan_data = get_scan_with_results(self.last_scan_id)
            last_results = last_scan_data['Results']
            last_result_map = make_result_map(last_results)

            first_similarity_ids = set(first_result_map.keys())
            last_similarity_ids = set(last_result_map.keys())

            fixed_similarity_ids = first_similarity_ids - last_similarity_ids
            new_similarity_ids = last_similarity_ids - first_similarity_ids
            recurring_similarity_ids = first_similarity_ids & last_similarity_ids

            return Summary(self.project_name, len(fixed_similarity_ids),
                           count_not_exploitable(last_results),
                           len(filter_not_exploitable(new_similarity_ids,
                                                      last_result_map)),
                           len(filter_not_exploitable(recurring_similarity_ids,
                                                      last_result_map)),
                           self.custom_fields)

        else:
            logging.debug(f'First and last scan ids are the same ({self.first_scan_id})')
            return None

    def __str__(self):

        return f'Project({self.project_id}, {self.project_name}, {self.first_scan_date}, {self.first_scan_id}, {self.last_scan_date}, {self.last_scan_id})'


def compare(args):

    scans = get_all_scans_in_date_range(args)
    projects = {}
    for scan in scans:
        if scan['IsIncremental']:
            logging.debug(f'Scan {scan["Id"]}: skipping incremental scan')
            continue
        project_id = scan['ProjectId']
        project_name = scan['ProjectName']
        logging.debug(f'project_id: {project_id}, project_name: {project_name}')
        if project_name not in projects:
            logging.debug('Creating new project object')
            projects[project_name] = Project(project_id, project_name,
                                             args.custom_fields)
        project = projects[project_name]
        project.add_scan(scan)
        projects[project_name] = project

    total = Summary('Total', 0, 0, 0, 0, ['' for cf in args.custom_fields])
    writer = csv.writer(sys.stdout)
    header = ['Project Name', 'Fixed', 'Not Exploitable',
              'New', 'Recurrent']
    header.extend(args.custom_fields)
    writer.writerow(header)

    for project in projects.values():
        summary = project.compare_scans()
        if summary:
            total.add(summary)
            summary.write_csv(writer)

    total.write_csv(writer)
    sys.stdout.flush()


def valid_date(s):
    # Adapted from https://stackoverflow.com/questions/25470844/specify-date-format-for-python-argparse-input-arguments
    try:
        return date.fromisoformat(s)
    except ValueError:
        msg = f'{s}: dates must be in YYYY-MM-DD format'
        raise argparse.ArgumentTypeError(msg)


def check_custom_fields(args):
    ''' Check that the specified custom fields are valid.'''

    logging.debug('Checking custom fields')
    if not args.custom_fields:
        args.custom_fields = []
        return

    custom_fields = args.custom_fields.split(',')
    for custom_field in custom_fields:
        if not custom_fields_api.get_custom_field_id_by_name(custom_field):
            raise ValueError(f'{custom_field}: unknown custom field')

    args.custom_fields = custom_fields


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--custom_fields',
                        help='A comma-separated list of custom fields to include in the report')
    parser.add_argument('-l', '--log_level', default='INFO', metavar='LEVEL',
                        help='Set the logging level to LEVEL')
    parser.add_argument('-p', '--project_name',
                        help='Restrict report to the specified project')
    parser.add_argument('-t', '--team_name',
                        help='Restrict report to the specified team')
    parser.add_argument('start_date', type=valid_date,
                        help='Start date of report period')
    parser.add_argument('end_date', type=valid_date,
                        help='End date of report period')
    args = parser.parse_args()

    logging.basicConfig(level=args.log_level)
    check_custom_fields(args)
    compare(args)
