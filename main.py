
import tkinter as tk  # Classic widgets
import tkinter.ttk as ttk  # Themed widgets
import numpy as np
import pandas as pd
from difflib import SequenceMatcher
from time import perf_counter

PATH_SECURITIES = "assets/securities.csv"
PATH_PRIORITIES = "assets/priorities.txt"
MAX_RESULTS = 10
REFRESH_RATE = 5000

class SISE:
    """
    Represents the Security Identifier Search Engine.
    """

    def __init__(self):
        """
        Initializes security data and user interface.
        """
        self.columns = []
        self.data = []

        # TODO: Start using numpy and pandas to really speed up computation!

        # Reads financial security data from file
        with open(PATH_SECURITIES) as database:
            self.columns = database.readline()[:-1].split(',')
            self.data = [row[:-1] for row in database]

        # Creates primary UI window
        self.window = tk.Tk()
        self.window.title("SISE Search")
        # window.geometry("")
        # window.resizable(width=False, height=False)

        # Establishes window layout
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=4)
        self.window.rowconfigure(2, weight=1)
        self.window.rowconfigure(3, weight=1)

        self.search_frame = self.create_search_frame()
        self.search_frame.grid(column=0, row=0, padx=5, pady=5)

        self.results_frame = self.create_results_frame()
        self.results_frame.grid(column=0, row=1, sticky="EW")

        self.tip_frame = self.create_tip_frame()
        self.tip_frame.grid(column=0, row=2, sticky="EW")

        self.progress_frame = self.create_progress_frame()
        self.progress_frame.grid(column=0, row=3, sticky="EW")

        self.window.mainloop()

    ############################################################################
    # WINDOW RELATED FUNCTIONS
    ############################################################################

    def create_search_frame(self):
        """
        Creates the frame where the search bar exists.
        """
        frame = ttk.Frame(
            master=self.window,
            relief=tk.RAISED,
            borderwidth=1
        )

        # Establishes frame layout
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.rowconfigure(0, weight=1)

        # Creates search label
        lbl_search = ttk.Label(frame, text="Search:")
        lbl_search.grid(column=0, row=0)

        # Creates search bar
        ent_search = ttk.Entry(frame)
        ent_search.focus()
        ent_search.grid(column=1, row=0)

        # Creates search button
        btn_search = ttk.Button(frame, text="Search", command=lambda: self.on_search(ent_search))
        btn_search.grid(
            column=2,
            row=0,
            padx=5,
            pady=5
        )
        self.window.bind("<Return>", lambda event: self.on_search(ent_search))

        # Creates filters button
        btn_filters = ttk.Button(frame, text="Filters", command=self.on_filters)
        btn_filters.grid(
            column=3,
            row=0,
            padx=5,
            pady=5
        )

        return frame

    def create_results_frame(self):
        """
        Creates the frame where the search results exist.
        """
        frame = ttk.Frame(
            master=self.window,
            relief=tk.RAISED,
            borderwidth=1
        )

        # Establishes frame layout
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Creates search results list box
        lbx_results = tk.Listbox(frame)
        lbx_results.grid(column=0, row=0, sticky="NESW")
        lbx_results.bind("<Double-1>", lambda event: self.on_select(lbx_results))

        return frame

    def create_tip_frame(self):
        """
        Creates the frame where the tip text exists.
        """
        frame = ttk.Frame(
            master=self.window,
            relief=tk.RAISED,
            borderwidth=1
        )

        # Establishes frame layout
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Creates search results list box
        lbl_tip = ttk.Label(frame, text="Tip: Double-click on a result for more information!")
        lbl_tip.grid(column=0, row=0, sticky="NESW")

        return frame

    def create_progress_frame(self):
        """
        Creates the frame where the progress bar exists.
        """
        frame = ttk.Frame(
            master=self.window,
            relief=tk.RAISED,
            borderwidth=1
        )

        # Establishes frame layout
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Creates progress bar
        pb = ttk.Progressbar(frame, orient="horizontal", mode="determinate", maximum=len(self.data))
        pb.grid(column=0, row=0, sticky="NESW")

        return frame

    ############################################################################
    # EVENT RELATED FUNCTIONS
    ############################################################################

    def on_search(self, ent):
        """
        Submits search query.
        """
        query = ent.get()
        if query:
            relevancy_data = self.get_all_relevancy(query)
            print(relevancy_data[:MAX_RESULTS])
        else:
            print("Empty query")

    def on_filters(self):
        """
        Opens filters menu.
        """
        window = tk.Toplevel()
        print("ON FILTERS")

    def on_select(self, lbx):
        """
        Opens details menu.
        """
        window = tk.Toplevel()
        print("ON SELECT")

    ############################################################################
    # LOGIC RELATED FUNCTIONS
    ############################################################################

    def get_relevancy(self, security):
        """
        """
        pass

    def get_all_relevancy(self, query):
        """
        Returns sorted relevancy data based off of longest common substring
        (LCS), in a list of tuples containing the length of the LCS and the
        index of the security.
        """
        start = perf_counter()
        pb = self.progress_frame.winfo_children()[0]
        seqm = SequenceMatcher(a=query.lower())

        results = []
        for index, security in enumerate(self.data):
            seqm.set_seq2(str(security).lower())
            lcs = seqm.find_longest_match()[2]
            results.append((lcs, index))

            if index % REFRESH_RATE == 0:
                pb.step(REFRESH_RATE)
                pb.update_idletasks()
        
        stop = perf_counter()
        print(f"Query term {repr(query)} took {round(stop-start, 5)} seconds.")
        return sorted(results, reverse=True)

def main():
    sise = SISE()

if __name__ == "__main__":
    main()
