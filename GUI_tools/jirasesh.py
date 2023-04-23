#!/usr/bin/env python3
import sys
import yaml
import pprint
from copy import deepcopy
from jira import JIRA
from validator import Validator
from pathlib import Path
import re

class JiraInst():
    #Constructor
    def __init__(self, auth_filename_yaml = None):
        #import configure varibles
        with open('config_files/config.yaml', 'r') as file:
            config = yaml.safe_load(file)
            self._states = config["states"]

        #import authentication variables
        if auth_filename_yaml is None:
            auth_filename_yaml = 'config_files/default_authentication.yml'
        
        with open(auth_filename_yaml, 'r') as file:
            auth = yaml.safe_load(file)

        #Connect to jira and initiate session
        self.jira_session = JIRA(auth['site'], basic_auth=(auth['email'], auth['token']))

        
    #Gets JIRA open or future issues for a given user
    def get_issues(self, assignee, search_state = None):
        issue_list = {}

        if search_state is None:
            for s in self._states:
                state_in_JQL = '\"' + s + '\"'
                query_JQL = 'assignee = \"' + assignee + '\" and sprint in (openSprints(),futureSprints()) and status = ' + state_in_JQL
                try:
                    issue_list[s] = self.jira_session.search_issues(query_JQL)
                except:
                    issue_list[s] = []
        else:
            state_in_JQL = '\"' + search_state + '\"'
            query_JQL = 'assignee = \"' + assignee + '\" and sprint in (openSprints(),futureSprints()) and status = ' + state_in_JQL
            issue_list = self.jira_session.search_issues(query_JQL)

        return issue_list
    
    #Get states of jira instance
    def get_states(self):
        return self._states
    
    #Changes states of issues for a given user. 
    def change_state(self, assignee, final_state, initial_state = None, issues_2_change = None):            
        if initial_state is None:
            initial_state = self._states[0]

        if issues_2_change is None:
            issue_list = self.get_issues(assignee,initial_state)
        else:
            issue_list = issues_2_change

        try:
            if len(issue_list) == 0:
                return False
            for issue in issue_list:    
                self.jira_session.transition_issue(issue.key, final_state)
            return True
        except:
            return False
            
    def  log_hours(self, hours, user, issue, started = None):
        hours_JQL = hours + "h"    
        try:
            if started is None:
                self.jira_session.add_worklog(issue.key, timeSpent = hours_JQL)
            else:
                self.jira_session.add_worklog(issue.key, timeSpent = hours_JQL, started = started)
        except:
            pass

    def convert_file(self, issues_file, assignee):
        filepath = Path(issues_file)

        v = Validator(self.jira_session)

        # parse yaml into list of story, task, bugs
        if filepath.suffix == '.yml' or filepath.suffix == '.yaml':
            issues = self.parse_yaml_file(yml_file = issues_file)
            vissues = v.validate(issues, assignee)
        elif filepath.suffix == '.txt':
            issues = self.parse_txt_file(txt_file = issues_file)
            vissues = v.validate(issues)
        else:
            return

        #check if issues are empty
        if len(vissues) == 0:
            return

        return vissues 
    
    def parse_yaml_file(self, yml_file):
        issues = []
        with open(yml_file, 'r') as file:
            config = yaml.safe_load(file)

        for issue_cfg in config['issues']:
            issue = deepcopy(config['defaults'])
            issue.update(issue_cfg)
            issues.append(issue)

        return issues

    def parse_txt_file(self, txt_file):
        with open(txt_file, 'r') as file:
            raw_txt = file.read()

        assignee_escape_char = '['
        assignee_escape_char_end =']'
        action_item_escape_char = '%%'
        project_escape_char = '###'
        board_escape_char = '^^'

        #Defaults to all
        defaults = {}
        defaults['sprint'] = 'future'
        defaults['issuetype'] = 'Story'
        defaults['description'] = '-'
        defaults['customfield_10051'] = '-' 
        defaults['epic'] = None
        defaults['components'] = ['OTHER']

        #Search for escape characters
        action_items_indices = [_.start() for _ in re.finditer(re.escape(action_item_escape_char), raw_txt)]
        assignee_indices = ([_.start() for _ in re.finditer(re.escape(assignee_escape_char), raw_txt)], \
            [_.start() for _ in re.finditer(re.escape(assignee_escape_char_end), raw_txt)])
        project_indices = [_.start() for _ in re.finditer(re.escape(project_escape_char), raw_txt)]
        board_indices = [_.start() for _ in re.finditer(re.escape(board_escape_char), raw_txt)]

        #Parse text
        project_id = raw_txt[project_indices[0]+len(project_escape_char):project_indices[1]]
        board_id = raw_txt[board_indices[0]+len(board_escape_char):board_indices[1]]
        issues = []

        for i in range(len(action_items_indices)):
            issue = deepcopy(defaults)
            summary = raw_txt[action_items_indices[i]+len(action_item_escape_char):assignee_indices[0][i]]
            assignee = raw_txt[assignee_indices[0][i]+1 : assignee_indices[1][i]]
            # component = 
            issue.update({'summary': summary, 'assignee': assignee, 'project': project_id, 'board':board_id})
            issues.append(issue)

        return issues

    def upload(self, issues):
        #Add issues to sprint and epic
       
        for issue in issues:
            sprint_id = issue.pop('sprint').id
            if issue['epic'] is not None:
                epic_id = issue.pop('epic').id
            else:
                issue.pop('epic')
                no_epic = True
            board = issue.pop('board')
            issue.pop('assignee_name')

            res = self.jira_session.create_issue(issue)         
            
            self.jira_session.add_issues_to_sprint(sprint_id=sprint_id,
                                            issue_keys=[res.key])

            # the add_issues_to_epic API appears to be deprecated
            if not no_epic:
                try:
                    self.jira_session.add_issues_to_epic(epic_id=epic_id,
                                            issue_keys=[res.key])
                except NotImplementedError:
                    res.update(fields={'parent': {'id': epic_id}})
                
    
    def export_to_yaml(self):
        pass

if __name__ == "__main__":
    a = JiraInst()
    a.parse_yaml_file(yml_file= 'C:/Users/ttrol/CodingProjects/Jira_Tool_GUI/templates/overhead2.yaml')
    
