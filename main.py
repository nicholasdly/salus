
import tkinter as tk
import tkinter.ttk as ttk
from numpy import vectorize
from pandas import DataFrame, read_csv
from difflib import SequenceMatcher
from time import perf_counter

# TODO: Using numpy/pandas to calculate longest common substring might be faster
# than using difflib; will need to do some testing.

PATH_SECURITIES = "assets/securities.csv"
PATH_PRIORITIES = "assets/priorities.txt"
MAX_RESULTS = 5

class SISE:
    """
    Represents the Security Identifier Search Engine.
    """

    def __init__(self):
        """
        Initializes security data and user interface.
        """
        print("Reading input data...")
        with open(PATH_SECURITIES) as database:
            next(database)
            data = (line for line in database)
            self.search_strings = DataFrame(data, columns=["line"])

        print("Establishing a bit of logic...")
        self.data = read_csv(PATH_SECURITIES)
        self.sm = SequenceMatcher()
        self.lcs_vectorized = vectorize(self.get_lcs)

        print("Making user interface...")
        self.window = tk.Tk()
        self.window.title("SISE Search")
        self.window.resizable(width=False, height=False)

        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.window.rowconfigure(1, weight=4)
        self.window.rowconfigure(2, weight=1)

        self.search_frame = self.create_search_frame()
        self.search_frame.grid(column=0, row=0, padx=5, pady=3)

        self.results_frame = self.create_results_frame()
        self.results_frame.grid(column=0, row=1, padx=5, sticky="EW")

        self.tip_frame = self.create_tip_frame()
        self.tip_frame.grid(column=0, row=2, padx=5, pady=5)

        self.window.mainloop()

    ############################################################################
    # WINDOW RELATED FUNCTIONS
    ############################################################################

    def create_search_frame(self):
        """
        Creates the frame where the search bar exists.
        """
        frame = ttk.Frame(master=self.window)

        # Establishes frame layout
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=3)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.rowconfigure(0, weight=1)

        # Creates search label
        lbl_search = ttk.Label(frame, text="Search:")
        lbl_search.grid(column=0, row=0, padx=3)

        # Creates search bar
        ent_search = ttk.Entry(frame)
        ent_search.focus()
        ent_search.grid(column=1, row=0)

        # Creates search button
        btn_search = ttk.Button(
            frame,
            text="Search",
            command=lambda: self.on_search(ent_search.get().lower())
        )
        btn_search.grid(column=2, row=0, padx=5, pady=5)
        ent_search.bind("<Return>",
            lambda _: self.on_search(ent_search.get().lower())
        )

        # Creates filters button
        btn_filters = ttk.Button(frame, text="Filters", command=self.on_filters)
        btn_filters.grid(column=3, row=0, padx=5, pady=5)

        return frame

    def create_results_frame(self):
        """
        Creates the frame where the search results exist.
        """
        frame = ttk.Frame(master=self.window, relief=tk.RAISED, borderwidth=1)

        # Establishes frame layout
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Creates search results list box
        lbx_results = tk.Listbox(frame, height=MAX_RESULTS, selectmode="SINGLE")
        lbx_results.grid(column=0, row=0, sticky="EW")
        lbx_results.bind("<Double-1>", lambda _: self.on_select(lbx_results))

        return frame

    def create_tip_frame(self):
        """
        Creates the frame where the tip text exists.
        """
        frame = ttk.Frame(master=self.window)

        # Establishes frame layout
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        # Creates search results list box
        lbl_tip = ttk.Label(frame, text="Made by Nicholas Ly!")
        lbl_tip.grid(column=0, row=0)

        return frame

    ############################################################################
    # EVENT RELATED FUNCTIONS
    ############################################################################

    def on_search(self, query):
        """
        Submits search query.
        """
        lbl_tip = self.tip_frame.winfo_children()[0]
        lbl_tip.config(text="Loading, please wait...")
        lbl_tip.update()

        lbx_results = self.results_frame.winfo_children()[0]

        if query:
            self.set_relevancy_values(query)
            results = self.get_top_results()
            print(results)

            # TODO: Display search results on UI!
            lbx_results.delete(0, "end")
            for i, result in enumerate(results):
                lbx_results.insert(i, self.get_relevant_id(int(result)))

        else:
            print("Empty query!")

        lbl_tip.config(
            text="Search complete! Double click on a result for details."
        )

    def on_filters(self):
        """
        Opens filters menu.
        """

        # TODO: Implement filters!

        window = tk.Toplevel()
        print("ON FILTERS")


    def on_select(self, lbx):
        """
        Opens details menu.
        """

        # TODO: Implement result selection!
        print(f"ON SELECT: {lbx.curselection()[0]}")

        window = tk.Toplevel()

    ############################################################################
    # LOGIC RELATED FUNCTIONS
    ############################################################################

    def get_lcs(self, col):
        """
        Returns the length of the longest common substring between the query and
        a second string.
        """
        self.sm.set_seq2(str(col).lower())
        return self.sm.find_longest_match()[2]

    def set_relevancy_values(self, query):
        """
        Adds relevancy data to dataframe based off of longest common substring
        (LCS).
        """
        print("Computing relevant results...")
        start = perf_counter()
        self.sm.set_seq1(query)

        self.search_strings["LCS"] = self.lcs_vectorized(
            self.search_strings["line"]
        )
        self.search_strings = self.search_strings.sort_values(
            "LCS", ascending=False
        )
        
        stop = perf_counter()
        print("Query term {} took {} seconds to sift through {} entries."\
            .format(repr(query), round(stop-start, 3), len(self.data))
        )

    def get_top_results(self):
        """
        Returns the security IDs of the securities with the longest common
        substring to the query.
        """
        results = self.search_strings[
            self.search_strings["LCS"] == self.search_strings["LCS"].max()
        ]
        return list(results.index.values)[:MAX_RESULTS]
        
    def get_relevant_id(self, index):
        """
        """
        security = list(self.data.iloc[index])
        similarity_data = []

        for id in security:
            if isinstance(id, str):
                self.sm.set_seq2(str(id).lower())
                similarity_data.append(self.sm.quick_ratio())
            else:
                similarity_data.append(0)

        return security[similarity_data.index(max(similarity_data))]


def main():
    sise = SISE()

if __name__ == "__main__":
    main()
