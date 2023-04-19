
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer

from pathlib import Path
# from tkinter import *
# Explicit imports to satisfy Flake8
# from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Listbox
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from jirasesh import JiraInst

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\ttrol\CodingProjects\Jira_Tool_GUI\GUI_assets\assets\frame0")

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
        self.user = 'Caleb Ho'
        #endregion

        #region  Setting up Background Aesthetics
        window.resizable(False, False)
        window.configure(bg = "#2EB3DD")
        window.geometry("450x500")

        self.canvas = Canvas(
            window,
            bg = "#2EB3DD",
            height = 500,
            width = 450,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.canvas.place(x = 0, y = 0)

        #View and Setup Background rectangle
        self.canvas.create_rectangle(
            206.0,
            32.0,
            413.0,
            92.0,
            fill="#000000",
            outline="")

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
        #Viewbox for queue
        # canvas.create_rectangle(
        #     206.0,
        #     110.0,
        #     413.0,
        #     377.0,
        #     fill="#FFFFFF",
        #     outline="")

        view_frame = Frame(master = window, height = 377-110, width = 413-206)
        view_frame.place(x = 206, y = 110)

        self.scrollbar = Scrollbar(view_frame)
        self.scrollbar.pack( side = RIGHT, fill = Y )

        self.viewbox = Listbox(master = view_frame, bd = 0, bg = 'white', height = 16, width = 31, yscrollcommand = self.scrollbar.set)

        self.viewbox.pack( side = LEFT, fill = BOTH )

        self.scrollbar.config( command = self.viewbox.yview )
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
            command=lambda: self.add_stories,
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
        
        #region Setup and View
        self.up_init_image1 = PhotoImage(
            file=relative_to_assets("button_11.png"))
        self.setup_button = Button(
            image=self.up_init_image1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_11 clicked"),
            relief="flat"
        )
        self.setup_button.place(
            x=314.0,
            y=48.0,
            width=86.0,
            height=29.27777099609375
        )

        self.button_image_6 = PhotoImage(
            file=relative_to_assets("button_6.png"))
        self.view_stories_button = Button(
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            relief="flat"
        )
        self.view_stories_button.place(
            x=218.0,
            y=48.0,
            width=86.0,
            height=29.27777099609375
        )

        #endregion

        #region Result Message box

        # Results View Box
        self.canvas.create_rectangle(
            206.0,
            403.0,
            413.0,
            467.0,
            fill="#FFFFFF",
            outline="")
        
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
        
        # if len(self.states[self.init_state]) > 15:
        #     self.init_state_label["font"] = .1
        # else:
        #     self.init_state_label["font"] = .2

        # if len(self.states[self.final_state]) > 15:
        #     self.final_state_label["font"] = .1
        # else:
        #     self.final_state_label["font"] = .2
    
    def queue_state(self):
        queued_issues = self.jira.get_issues(assignee = self.user, search_state = self.get_current_initial())
        self.display_issues(queued_issues)
        
    def change_state(self):
        if len(self.viewbox.get(0,END)) != 0:
            message = self.get_current_initial() + ' -> ' + self.get_current_final() + "?"
            confirmation = messagebox.askyesno(title = 'Batch Transition Confirmation', 
                    message = message)
            if confirmation:
                success = self.jira.change_state(self.user, self.states[self.final_state])

            if not success:
                self.result_msg = "Error: Transition Failure"
            else:
                self.result_msg = "Success!"

        self.viewbox.delete(0,END)

    def browse_file(self):
        filetypes = (('yaml files', '*.yaml'),('yml files', '*.yml'),('All files', '*.*'))
        f = askopenfilename(title  = 'Open issue file', filetypes = ())
        path = Path(f)
        self.added_stories_filepath = f
        self.file_label["text"] = path.name

    def queue_stories(self):
        self.queued_issues = self.jira.convert_yaml(issues_yml = self.added_stories_filepath)
        self.display_issues(self.queued_issues)

    def add_stories(self):
        self.jira.upload(self.queued_issues)
        self.viewbox.delete(0,END)
        self.queued_issues = []

    #region helper methods
    def get_current_final(self):
        return self.states[self.final_state]
    
    def get_current_initial(self):
        return self.states[self.init_state]

    def display_issues(self, queued_issues):
        self.viewbox.delete(0,END)

        for i in range(len(queued_issues)):
            key = queued_issues[i].key
            summary = queued_issues[i].get_field('summary')
            self.viewbox.insert(i+1, summary + " | " + key)

    #endregion

    #endregion

if __name__ == "__main__":
    window = Tk()
    window.title("Batch Jira Automation")
    a = mainGUI(window)
    window.mainloop()