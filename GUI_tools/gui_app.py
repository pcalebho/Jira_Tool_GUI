from pathlib import Path
from tkinter import messagebox, Canvas, Entry, Label, Button, PhotoImage, Listbox, \
    Frame, Scrollbar, Tk, END, Toplevel
from tkinter.filedialog import askopenfilename, asksaveasfilename
from jirasesh import JiraInst
import yaml

path_parts = Path(__file__).parts
parent_path = '\\'.join(path_parts[0:len(path_parts)-2])+'/GUI_assets/assets/frame0'
ASSETS_PATH = Path(parent_path)

def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

class mainGUI:
    #region GUI layout
    def __init__(self, window):
        #region Instance members
        self.jira = JiraInst()
        self.states = self.jira.get_states()
        self.init_state = 0
        self.final_state = 1
        self.user = "FirstName LastName"
        #endregion

        #region  Setting up Background Aesthetics
        window.resizable(False, False)
        window.configure(bg = "#2EB3DD")
        window.geometry("600x600")

        self.canvas = Canvas(
            window,
            bg = "#2EB3DD",
            height = 600,
            width = 600,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)

        #State change background rectangle
        self.canvas.create_rectangle(
            39.0,
            250.0,
            170.0,
            467.0,
            fill="#531BF3",
            outline="")

        #Adding new stories background rectangle
        self.canvas.create_rectangle(
            39.0,
            32.0,
            170.0,
            204.0,
            fill="#531BF3",
            outline="")
        
        #endregion

        #region Viewbox and selection
        #View and Setup Background rectangle
               
        view_frame = Frame(master = window, height = 377-110, width = 413-206+150)
        view_frame.place(x = 206, y = 130)

        self.scrollbar = Scrollbar(view_frame)
        self.scrollbar.pack( side = 'right', fill = 'y')

        self.viewbox = Listbox(master = view_frame, bd = 0, bg = 'white', height = 24, width = 31+25, yscrollcommand = self.scrollbar.set)
        self.viewbox.pack( side = 'left', fill = 'both' )

        self.scrollbar.config( command = self.viewbox.yview )
        
        # Results View Box
        self.results_message_box = Label(
            master = window,
            bg = 'white',
            bd = 0,
            height=2,
            width = 50
        )
        
        self.results_message_box.place(x=207, y = 537.5)
        
        #endregion

        #region State changing stories

        #Inital View
        self.init_state_label = Label(
            window,
            bg = '#FFFFFF',
            bd = 0,
            height = 2,
            width = 10,
            text = self.states[self.init_state])
        self.init_state_label.place(x= 55, y=274)
        
        #Final View
        self.final_state_label = Label(
            window,
            bg = '#FFFFFF',
            bd = 0,
            height = 2,
            width = 10,
            text = self.states[self.final_state])
        self.final_state_label.place(x= 55, y=330)


        self.up_init_image = PhotoImage(file=relative_to_assets("button_1.png"))
    
        self.up_init_state_button = Button(
            image=self.up_init_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.inc_dec_state(1, 'initial'),
            relief="flat"
        )
        self.up_init_state_button.place(
            x=133.0,
            y=274.0,
            width=20.0,
            height=12.0
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        self.down_init_state_button = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command= lambda: self.inc_dec_state(-1, 'initial'),
            relief="flat"
        )
        self.down_init_state_button.place(
            x=133.0,
            y=295.0,
            width=20.0,
            height=12.0
        )

        self.button_image_3 = PhotoImage(file=relative_to_assets("button_3.png"))

        self.up_final_state_button = Button(
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.inc_dec_state(1, 'final'),
            relief="flat"
        )
        self.up_final_state_button.place(
            x=133.0,
            y=330.0,
            width=20.0,
            height=12.0
        )

        self.button_image_4 = PhotoImage(file=relative_to_assets("button_4.png"))

        self.down_final_state_button = Button(
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.inc_dec_state(1, 'final'),
            relief="flat"
        )
        self.down_final_state_button.place(
            x=133.0,
            y=351.0,
            width=20.0,
            height=12.0
        )

        self.canvas.create_text(
            77,
            259.0,
            anchor="nw",
            text="Initial",
            fill="#FFFFFF",
            font=("Inter Bold", 12 * -1)
        )

        self.canvas.create_text(
            78,
            315.0,
            anchor="nw",
            text="Final",
            fill="#FFFFFF",
            font=("Inter Bold", 12 * -1)
        )

        self.up_init_image0 = PhotoImage(
            file=relative_to_assets("button_10.png"))
        self.change_state_button = Button(
            image=self.up_init_image0,
            borderwidth=0,
            highlightthickness=0,
            command=self.change_state,
            relief="flat"
        )
        self.change_state_button.place(
            x=55.0,
            y=418.0,
            width=98.0,
            height=29.27777862548828
        )

        self.button_image_8 = PhotoImage(
            file=relative_to_assets("button_8.png"))
        self.queue_state_button = Button(
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command= self.queue_state,
            relief="flat"
        )
        self.queue_state_button.place(
            x=55.0,
            y=375.0,
            width=98.0,
            height=29.27777099609375
        )

        #endregion

        #region Add stories
        self.button_image_5 = PhotoImage(
            file=relative_to_assets("button_5.png"))
        self.browse_button = Button(
            window,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command= self.browse_file,
            relief="flat"
        )
        self.browse_button.place(
            x=64.0,
            y=48.0,
            width=81.0,
            height=29.27777099609375
        )


        self.button_image_7 = PhotoImage(
            file=relative_to_assets("button_7.png"))
        self.add_stories_button = Button(
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=self.add_stories,
            relief="flat"
        )
        self.add_stories_button.place(
            x=64.0,
            y=157.0,
            width=81.0,
            height=29.27777099609375
        )

        self.file_label = Label(
            anchor="n",
            width = 16,
            text="file.yaml",
            font=("Inter Bold", 12 * -1),
            bg = "#531BF3",
            fg = 'white'
        )
        self.file_label.place(x=46, y = 77.0,)

        self.button_image_9 = PhotoImage(
            file=relative_to_assets("button_9.png"))
        self.queue_stories_button = Button(
            image=self.button_image_9,
            borderwidth=0,
            highlightthickness=0,
            command= self.queue_stories,
            relief="flat"
        )
        self.queue_stories_button.place(
            x=55.0,
            y=110.0,
            width=98.0,
            height=29.27777099609375
        )
        #endregion
        
        #region Name Entry
        name_frame = Frame(height = 72-32, bg = "black",padx = 10, pady= 5)
        name_frame.place(x= 206, y = 32)
        
        self.user_label = Label(master= name_frame, justify = 'left', text = "name:", fg = "white", bg = "black", font = "Inter 11 bold")
        self.user_label.pack(side = 'left')
        
        #ttk.Style().configure('pad.TEntry', padding='0 0 10 0')
        
        self.username_entry = Entry(
            master = name_frame,
            width = 34,
            font = "Inter 9",
        )
        self.username_entry.pack(side = 'right')
        self.username_entry.insert(0, self.user)

       
        #endregion

        #region Exporting yaml
        export_frame = Frame(height = 60, width = 200, bg ="#2EB3DD")
        export_frame.place(x = 245, y = 80)

        self.view_stories_btn_image = PhotoImage(file=relative_to_assets("ViewStories_button.png"))
        
        self.view_stories_button = Button(
            master = export_frame,
            image = self.view_stories_btn_image,
            # borderwidth= 15,
            highlightthickness=0,
            relief="flat",
            background= "#2EB3DD",
            command = lambda: self.view_stories()
        )

        self.view_stories_button.pack(side='left',anchor='w',padx= 40)
        
        self.export_yaml_btn_image = PhotoImage(file=relative_to_assets("ExportYaml_button.png"))
        self.export_yaml_button = Button(
            master = export_frame,
            image = self.export_yaml_btn_image,
            # borderwidth = 15,
            highlightthickness=0,
            relief = "flat",
            background="#2EB3DD",
            command = self.export_to_yaml,
            padx = 20
        )
        
        self.export_yaml_button.pack(side='right', anchor='e')
        #endregion
        
        #region Log 0h 
        log_frame = Frame(height = 70, width = 131, bg = "#531BF3")
        log_frame.place(x = 39, y = 500)

        self.log_btn_image = PhotoImage(file=relative_to_assets("log0h.png"))
        
        self.log_button = Button(
            master = log_frame,
            image = self.log_btn_image,
            borderwidth= 0,
            highlightthickness=0,
            relief="flat",
            background= "#531BF3",
            command = self.log_time
        )

        self.log_button.place(x = 10, y = 20)
        
        self.log_later_btn_image = PhotoImage(file=relative_to_assets("log0h_later.png"))
        self.log_later_button = Button(
            master = log_frame,
            image = self.log_later_btn_image,
            borderwidth = 0,
            highlightthickness=0,
            relief = "flat",
            background="#531BF3"
            # command = lambda:self.log_time
        )
        
        self.log_later_button.place(x =70, y = 20)
        
        #endregion

    #endregion
    #region Methods
    def inc_dec_state(self, direction, chosen_state):
        #Necessary for finding number available states
        max = len(self.states)-1

        #Used to make sure the state doesn't go out of bounds but insteads loops around
        #Nested loops are not very readable sorry
        if chosen_state == "initial":
            if direction < 0:
                if self.init_state == 0:
                    self.init_state = max
                else:
                    self.init_state -= 1
            else:
                if self.init_state == max:
                    self.init_state = 0
                else:
                    self.init_state += 1
            self.init_state_label["text"] = self.states[self.init_state]
        elif chosen_state == "final":
            if direction < 0:
                if self.final_state == 0:
                    self.final_state = max
                else:
                    self.final_state -= 1
            else:
                if self.final_state == max:
                    self.final_state = 0
                else:
                    self.final_state += 1
            self.final_state_label["text"] = self.states[self.final_state]
    
    def queue_state(self):
        self._set_user_from_entry()
        queued_issues = self.jira.get_issues(assignee = self.user, search_state = self._get_current_initial())[self._get_current_initial()]
        self._display_issues(queued_issues, is_jira_object = True)
        self._display_message('Queuing stories in ' + '\"' + self._get_current_initial() + '\"')
        
    def change_state(self):
        self._set_user_from_entry()
        success = False
        if len(self.viewbox.get(0, END)) != 0:
            message = self._get_current_initial() + ' -> ' + self._get_current_final() + "?"
            confirmation = messagebox.askyesno(title = 'Batch Transition Confirmation', 
                    message = message)
            if confirmation:
                success = self.jira.change_state(self.user, initial_state = self.states[self.init_state], final_state = self.states[self.final_state])

            if not success:
                self._display_message("Error: Transition Failure", 'green')
            else:
                self._display_message('Success!','green')
        
        self.viewbox.delete(0, END)
        
    def view_stories(self):
        self._reset()
        self.viewbox.delete(0,END)
        issue_list = []
        try:
            self.results_message_box["text"] = "Working..."
            stories = self.jira.get_issues(self.user)
            for status in stories:
                if len(stories[status]) != 0:
                    for issue in stories[status]:
                        issue_list.append(issue)
        except:
            self._display_message('Error: Could not get issues','red')
            return
        
        if len(issue_list) != 0:
            self._display_issues(issue_list,is_jira_object= True)
            self._display_message("Viewing stories for " + self.user, 'green')
        else:
            self._display_message('No issues found', 'red')


    def browse_file(self):
        filetypes = (('yaml files', '*.yaml'),('yml files', '*.yml'),('txt files','.*txt'),('All files', '*.*'))
        f = askopenfilename(title  = 'Open issue file', filetypes = ())
        path = Path(f)
        self.added_stories_filepath = f
        self.file_label["text"] = path.name

    def queue_stories(self):
        self._reset()
        self.dialog = Toplevel()
        big_frame = Frame(self.dialog)
        big_frame.pack(side = 'top', fill='both', expand=True)
        button_frame = Frame(self.dialog)
        button_frame.pack(side = 'bottom')

        label = Label(big_frame, text="Are you uploading to an\nactive or future sprint?")
        label.place(relx=0.5, rely=0.3, anchor='center')

        option1_button = Button(button_frame, text = 'Active', command = lambda: self._assign_attribute('active'))
        option1_button.pack(side= 'left', padx = 10)
        
        option2_button = Button(button_frame, text = 'Future', command = lambda: self._assign_attribute('future'))
        option2_button.pack(side= 'right', padx = 10)
        
        ext = Path(self.added_stories_filepath).suffix
        self._display_message('Working...')
        self.dialog.transient(window)
        self.dialog.geometry('200x100')
        self.dialog.wait_window()
        
        try:
            if ext == '.yml' or ext == '.yaml':
                self.queued_issues = self.jira.convert_file(issues_file= self.added_stories_filepath, assignee = self.user, search_state= self.sprint_search_state)
            elif ext == '.txt':
                self.queued_issues = self.jira.convert_file(issues_file= self.added_stories_filepath, assignee = self.user, search_state= self.sprint_search_state)
            else:
                self._display_message("Error: Wrong file type",'red')
        except:
            self._display_message("Error: Cannot read stories from file",'red')
            return
        try:
            if self.queued_issues == []:
                self._display_message("Error with story validation. Check if fields are correct.", 'red')
        except:
            self._display_message("Error with story validation. Check if fields are correct.", 'red')
            
        self._display_issues(self.queued_issues, is_jira_object=False)
        self._display_message('Ready to add', 'green')

    def add_stories(self):
        self._reset()
        
        try:
            confirmation = messagebox.askokcancel('Confirmation','Are you sure you would like to upload stories?')
            if confirmation:
                self.jira.upload(self.queued_issues)
                self.viewbox.delete(0, END)
                self.queued_issues = []
                self._display_message('Successfully added stories', 'green')
        except:
            self._display_message('Error uploading issues')


    def log_time(self):
        self._reset()
        issues = self.jira.get_issues(self.user, search_state = 'In Progress')['In Progress']
        if len(issues) == 0:
            self._display_message('No In progress issues to log', 'red')
            return
        else:
            try:
                for issue in issues:
                    self.jira.log_hours(0, issue)
                self._display_message('Successfully added 0 hours','green')
            except:
                self._display_message('Error logging hours','red')

    def export_to_yaml(self):
        self._reset()
        self._display_message("Working...")
        try:
            stories = self.jira.get_issues(self.user)
            defaults = {'sprint': 'active', 'assignee': self.user, 'issuetype': 'Story'}
            issues = []
            for status in stories:
                if len(stories[status]) != 0:
                    for issue in stories[status]:
                        dict = {}
                        dict['project'] = issue.get_field('project').key
                        dict['summary'] = issue.get_field('summary')
                        dict['description'] = issue.get_field('description')
                        dict['epic'] = issue.get_field('customfield_10014')
                        temp = issue.get_field('components')
                        dict['components'] = '[' + temp[0].name + ']'
                        dict['customfield_10051'] = issue.get_field('customfield_10051')
                        dict['timetracking'] = {'originalEsimate': issue.get_field('timetracking').originalEstimate}
                        issues.append(dict)
            
            files = [('YAML files','*.yaml')]
            output = asksaveasfilename(filetypes = files,defaultextension = '.yaml')

            with open(output, 'w') as outfile:
                yaml.dump({'defaults': defaults, 'issues':issues}, outfile)
            self._display_message('Export Success', 'green')
        except:
            self._display_message('Export Failure', 'red')
    
    #region helper methods
    def _get_current_final(self):
        return self.states[self.final_state]
    
    def _get_current_initial(self):
        return self.states[self.init_state]

    def _display_issues(self, queued_issues, is_jira_object = False):
        self.viewbox.delete(0,END)

        for i in range(len(queued_issues)):
            if is_jira_object:
                assignee = self.user
                summary = queued_issues[i].get_field('summary')
            else:
                assignee = queued_issues[i]['assignee_name']
                summary = queued_issues[i]['summary']
            str = assignee + ' | ' + summary
            self.viewbox.insert(i+1, str)
    
    def _set_user_from_entry(self):
        self.user = self.username_entry.get()
    
    def _reset(self):
        self._set_user_from_entry()
        self._display_message('')
        self.sprint_search_state = ''
    
    def _display_message(self, message, color = 'black'):
        self.results_message_box["text"] = message
        self.results_message_box["fg"] = color
    
    def _assign_attribute(self,state):
        self.sprint_search_state = state
        self.dialog.destroy()

    #endregion

    #endregion

if __name__ == "__main__":
    window = Tk()
    window.title("Batch Jira Automation")
    a = mainGUI(window)
    window.mainloop()