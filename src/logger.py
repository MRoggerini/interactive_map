import tkinter as tk
from datetime import datetime


class MapLogger(tk.Label):
    """
        Logger class. Displays logs for different events
        Extends tk.label
    """
    def __init__(
            self,
            root_tk,
            builder
            anchor='w',
            bg='black',
            fg='white',
            ps1='$ '):
        super(self).__init__(root_tk)

        self.builder = builder
        self.root_tk = root_tk
        self.ps1 = ps1


    def log(self, input_text):
        """
            Action used to log something on the logging label.
            Input:
                - input_text: what to log
            Action:
                - set the logging label to the input text, prepended by the ps1
                - the log priority is set to "log"
        """
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.config(
                text=f'[{curr_time}] {self.ps1}{input_text}'
                fg='white'
            )


    def warning(self, input_text):
        """
            action used to log something on the logging label.
            Input:
                - input_text: what to log
            Action:
                - set the logging label to the input text, prepended by the ps1
                - the log priority is set to "warning"
        """
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.config(
                text=f'[{curr_time}] {self.ps1}{input_text}'
                fg='yellow'
            )


    def error(self, input_text):
        """
            action used to log something on the logging label.
            Input:
                - input_text: what to log
            Action:
                - set the logging label to the input text, prepended by the ps1
                - the log priority is set to "error"
        """
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.config(
                text=f'[{curr_time}] {self.ps1}{input_text}',
                fg='red'
            )



