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

    def convert_file(self, issues_file, assignee, validation = True):
        filepath = Path(issues_file)
    
        # parse yaml into list of story, task, bugs
        if filepath.suffix == '.yml' or filepath.suffix == '.yaml':
            with open(issues_yml, 'r') as file:
                config = yaml.safe_load(file)
        elif filepath.suffix == '.txt':
            pass
        else:
            return
        
        issues = []

        try:
            for issue_cfg in config['issues']:
                issue = deepcopy(config['defaults'])
                issue.update(issue_cfg)
                issues.append(issue)
        except KeyError as err:
            #add error handling
            pass

        # validate issues
        if validation:
            v = Validator(self.jira_session)
            vissues = v.validate(issues, assignee)
        else:
            vissues = issues

        #check if issues are empty
        if len(vissues) == 0:
            return

        return vissues 
    
    def parse_txt_file(self, txt_file, assignee):
        with open(txt_file, 'r') as file:
            raw_txt = file.read()

        assignee_escape_char = '[' 
        action_item_escape_char = '%'
        project_escape_char = '%'     

        #Search for escape characters
        action_items_indices = [_.start() for _ in re.finditer(re.escape(action_item_escape_char), raw_txt)]
        assignee_indices = [_.start() for _ in re.finditer(re.escape(assignee_escape_char), raw_txt)]



    def upload(self, issues):
        #Add issues to sprint and epic
        results = []
        issue_info = []
        
        for issue in issues:
            sprint_id = issue.pop('sprint').id
            epic_id = issue.pop('epic').id
            board = issue.pop('board')

            res = self.jira_session.create_issue(issue)
            results.append(res)           
            
            self.jira_session.add_issues_to_sprint(sprint_id=sprint_id,
                                            issue_keys=[res.key])

            # the add_issues_to_epic API appears to be deprecated
            try:
                self.jira_session.add_issues_to_epic(epic_id=epic_id,
                                        issue_keys=[res.key])
            except NotImplementedError:
                res.update(fields={'parent': {'id': epic_id}})
                
    
    def export_to_yaml(self):
        pass

if __name__ == "__main__":
    a = JiraInst()
    a.parse_txt_file(txt_file= 'C:/Users/ttrol/CodingProjects/Jira_Tool_GUI/templates/Ztrash.txt', assignee='Caleb Ho')
