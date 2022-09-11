"""
Nicholas Ly (lynichol@msu.edu)
ShellHacks 2022
September 11, 2022
"""

from security_data import SecurityData
import constants as const

import tkinter as tk
from tkinter import font, messagebox

class SearchApp(tk.Tk):
    """
    A class which represents the search engine user interface.
    """

    def __init__(self):
        """
        Initializes the user interface with neccessary widgets and functions.
        """
        super().__init__()

        self.securities = SecurityData()
        self.results = []
        segoe12 = font.Font(family="Segoe UI", size="12")

        self.title("Security Identifier Search")
        self.geometry(f"1200x225")
        self.resizable(False, False)

        search_label = tk.Label(self, text="Search:", font=segoe12)
        search_label.place(x=450, y=10)

        self.query = tk.StringVar()
        query_entry = tk.Entry(self, textvariable=self.query, font=segoe12)
        query_entry.place(x=510, y=10)
        query_entry.focus()

        search_btn = tk.Button(self, text="Enter", font=segoe12)
        search_btn.config(command=self.search)
        search_btn.place(x=700, y=5)

        scrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        scrollbar.place(x=10, y=159, width=1180)

        self.result_box = tk.Listbox(self, listvariable=self.results, height=5, selectmode=tk.SINGLE, font=segoe12, width=131, xscrollcommand=scrollbar.set)
        self.result_box.place(x=9, y=45)
        scrollbar.config(command=self.result_box.xview)

        mark_btn = tk.Button(self, text="Save street ID as high priority", font=segoe12)
        mark_btn["command"] = self.update_priorities
        mark_btn.place(x=495, y=180)

    def search(self):
        """
        Given a query, creates a sorted copy of the database from most to least
        relevant/similar.
        """
        global results
        q = self.query.get()

        if len(q) > 0:
            self.result_box.delete(0, tk.END)  # Clears list of results
            results = self.securities.get_search_results(q)
            for i in range(const.RESULT_DISPLAY):
                self.result_box.insert('end', self.securities.data[results[i][0]])

    def update_priorities(self):
        """
        Refreshes priority order, moving the street ID of the specified index to
        the front of the list and updating the priority.txt file likewise.
        """
        if self.result_box.size() > 0:
            results_in_box = self.result_box.get(0, tk.END)
            selected_result = self.result_box.get(tk.ANCHOR)

            # Calculates the index of the selected security's most relevant
            # street ID in the priority list.
            p_index = len(self.securities.priorities) - results[
                int(results_in_box.index(selected_result))][1][1]

            self.securities.refresh_priorities(p_index)
            messagebox.showinfo("Priority Order Update", \
                f"{self.securities.priorities[0]} is now of highest priority!")
            
def main():
    app = SearchApp()
    app.mainloop()

if __name__ == "__main__":
    main()
