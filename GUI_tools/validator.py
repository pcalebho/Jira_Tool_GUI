#!/usr/bin/env python3
import yaml
import pdb
from copy import deepcopy
import pprint
import re
from jira import JIRA, JIRAError


class ValidationError(Exception):
    pass


class Validator(object):
    issuetypes = ('Story', 'Task')

    def __init__(self, jira, fatal_errors=True, duplicates=False,
                 closed_sprints=False, prepend_sprint=False):
        self.jira = jira
        self.fatal_errors = fatal_errors
        self.duplicates = duplicates
        self.closed_sprints = closed_sprints
        self.prepend_sprint = prepend_sprint
        self.initialize()

    def initialize(self):
        self.projects = {proj.key: proj for proj in self.jira.projects()}

        self.project_components = {}
        self.boards = {}

    def validate_name_to_single_user(self, name):
        if name == 'self':
            user = self.jira.user(self.jira.current_user())
        else:
            users = self.jira.search_users(query=name)

            if len(users) == 0:
                raise ValidationError("No user found for '{}'".format(name))
            elif len(users) > 1:
                raise ValidationError("Multiple users found for '{}': {}"
                                      .format(name, users))
            user = users[0]

        return {'id': user.accountId}

    def validate_project_key(self, key):
        if key not in self.projects:
            raise ValidationError("project key '{}' not found"
                                  .format(key))
        return key

    def validate_board_name_to_board(self, board_name):
        if board_name not in self.boards:
            self.boards.update({board.name: board for board in self.jira.boards()})
            if board_name not in self.boards:
                raise ValidationError("board name '{}' not found"
                                      .format(board_name))

        return self.boards[board_name]

    def validate_sprint_desc_to_sprint(self, sprint_desc, board):
        sprints = self.jira.sprints(board.id, state='active')
        sprints += self.jira.sprints(board.id, state='future')

        if self.closed_sprints:
            sprints += self.jira.sprints(board.id, state='closed', startAt=50)  # for testing with closed sprints

        filtered = [s for s in sprints if s.state == sprint_desc]
        if len(filtered) == 0:
            filtered = [s for s in sprints if sprint_desc in s.name]
            if len(filtered) == 0:
                raise ValidationError("No matching sprint for board '{}' with either state or name '{}'"
                                      .format(board.name, sprint_desc))
        if len(filtered) > 1:
            raise ValidationError("Multiple matching sprints for board '{}' and sprint desc '{}'"
                                  .format(board.name, sprint_desc))

        return filtered[0]

    def validate_project_components(self, project_key, components):
        project_key = self.validate_project_key(project_key)
        if project_key not in self.project_components:
            self.project_components[project_key] = self.jira.project_components(project_key)

        output = []
        for component in components:
            if component not in (comp.name for comp in self.project_components[project_key]):
                raise ValidationError("Component '{}' not found in project {}"
                                      .format(component, project_key))
            output.append({'name': component})
        return output

    def validate_epic_id_to_epic(self, epic_id):
        """Currently only epic ID is supported"""
        if epic_id is None:
            return None
        epic = self.jira.issue(epic_id)
        return epic

    def validate(self, issue_descriptions, assignee = None):
        issues = []
        for desc in issue_descriptions:
            try:
                issue = deepcopy(desc)
                issue['project'] = self.validate_project_key(desc['project'])

                # validate optional assignee field
                if assignee is None:
                    user = self.validate_name_to_single_user(name= desc['assignee'])
                    issue['assignee_name'] = desc['assignee']
                else:
                    user = self.validate_name_to_single_user(name = assignee)
                    issue['assignee_name'] = assignee
                
                issue['assignee'] = user

                if desc['issuetype'] not in self.issuetypes:
                    raise ValidationError("issuetype '{}' not in {}"
                                          .format(desc['issuetype'],
                                                  self.issuetypes))
                issue['issuetype'] = {'name': desc['issuetype']}

                issue['board'] = self.validate_board_name_to_board(desc['board'])
                issue['sprint'] = self.validate_sprint_desc_to_sprint(desc['sprint'],
                                                                 issue['board'])
                issue['components'] = self.validate_project_components(issue['project'],
                                                                       desc['components'])
                issue['epic'] = self.validate_epic_id_to_epic(desc['epic'])
                

                if self.prepend_sprint:
                    match = re.search(r"IR\d+", issue['sprint'].name)
                    if match is not None:
                        issue['summary'] =  match[0] + " - " + desc['summary']
                    else:
                        raise ValidationError("Illegal sprint name."
                                              " Cannot prepend to issue summaries.")

                issues.append(issue)
            except KeyError as err:
                if self.fatal_errors:
                    return []
            except ValidationError as err:
                if self.fatal_errors:
                    return []
            except JIRAError as err:
                if self.fatal_errors:
                    return []

        return issues
