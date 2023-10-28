import tkinter
import tkinter.messagebox
import customtkinter
from gopro import GoProManager
from MediaElement import MediaElement


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(1, weight=0)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []
        self.column = 0
        self.row = 0

    def add_item(self, item, image=None):

        self.loadButton = customtkinter.CTkButton(master=self, text="Load", fg_color="gray9",
                                                  border_width=2, text_color=("gray10", "#DCE4EE"),
                                                  width=150, height=100)


        self.loadButton.grid(row=self.row, column=self.column, padx=10, pady=10)
        self.button_list.append(self.loadButton)
        self.column += 1

        if self.column > 5:
            self.column = 0
            self.row += 1




    def remove_item(self, item):
        for label, button in zip(self.label_list, self.button_list):
            if item == label.cget("text"):
                label.destroy()
                button.destroy()
                self.label_list.remove(label)
                self.button_list.remove(button)
                return

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.goproManager = None
        self.title("GoPro Cloud Download Manager")
        self.geometry(f"{1210}x{800}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)



        # sidebar
        self.sidebar_frame = customtkinter.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Credentials",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        self.usernameField = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Email", textvariable=tkinter.StringVar(master=self.sidebar_frame, value="patrick.zilke99@gmail.com"))
        self.usernameField.grid(row=1, column=0, padx=10, pady=10)

        self.passwordField = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Password", textvariable=tkinter.StringVar(master=self.sidebar_frame, value="v310P70aDg99"))
        self.passwordField.grid(row=2, column=0, padx=20, pady=10)

        self.directoryField = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="Directory Path", textvariable=tkinter.StringVar(master=self.sidebar_frame, value="test"))
        self.directoryField.grid(row=3, column=0, padx=20, pady=10)

        self.loadButton = customtkinter.CTkButton(master=self.sidebar_frame, text="Load", command=self.sidebar_button_event, fg_color="transparent", border_width=2,text_color=("gray10", "#DCE4EE"))
        self.loadButton.grid(row=4, column=0, padx=(20, 20), pady=(20, 20), sticky="S")

        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self,
                                                                        corner_radius=0,
                                                                        fg_color="gray5")
        self.scrollable_label_button_frame.grid(row=0, column=1, padx=0, pady=0, rowspan=4, sticky="nsew")
        self.scrollable_label_button_frame.add_item("new item")
        self.scrollable_label_button_frame.add_item("new item")
        self.scrollable_label_button_frame.add_item("new item")
        self.scrollable_label_button_frame.add_item("new item")
        self.scrollable_label_button_frame.add_item("new item")
        self.scrollable_label_button_frame.add_item("new item")
        self.scrollable_label_button_frame.add_item("new item")
        self.scrollable_label_button_frame.add_item("new item")


    def loadMedia(self):
        if len(self.usernameField.get()) > 0 and len(self.passwordField.get()) > 0 and len(self.directoryField.get()) > 0:
            self.goproManager = GoProManager(email=self.usernameField.get(), password=self.passwordField.get(),
                                            path=self.directoryField.get())
            if self.goproManager.checkConnection() == 200:
                mediaList = self.goproManager.getMediaList()

                #for elem in mediaList:



        else:
            print("credentials empty")

    def sidebar_button_event(self):
        self.loadMedia()

if __name__ == "__main__":
    app = App()
    app.mainloop()
