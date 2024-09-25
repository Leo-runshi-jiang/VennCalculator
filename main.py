import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib_venn import venn2, venn3
import matplotlib.pyplot as plt

import calculator #import own module

class VennDiagramApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Venn Diagram Calculator")
        self.hidden_inputs = True
        self.subsets = () #tuple for all subsets
        self.combinedAreas = {} #dictionary for all calculated combined areas

        # Create a dropdown to select between 2-circle and 3-circle Venn diagram
        self.create_venn_type_selector_and_update_button()

        # Create input fields for user data
        # Frame for user input
        self.inputFrame = ttk.Frame(self.root)
        self.inputFrame.grid(row=1, column=0, padx=10, pady=10)
        self.create_input_fields()

        # Label to display error messages
        self.error_label = ttk.Label(self.inputFrame, text="", foreground="red")
        self.error_label.grid(row=4, columnspan=2)

        # Create a figure for the Venn diagram
        self.fig, self.ax = plt.subplots(figsize=(5, 5))

        # Initial Venn diagram (2 sets)
        venn2(subsets=(1, 1, 1), set_labels=('Set A', 'Set B'), ax=self.ax)

        # Add the plot to tkinter window using grid
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, sticky='nsew')

        # Add frame for displaying calculated results
        self.resultsFrame = ttk.Frame(self.root)
        self.resultsFrame.grid(row = 5, column = 0, padx=10, pady=10)

    def create_venn_type_selector_and_update_button(self):
        #Create a dropdown for selecting 2 or 3 circle Venn diagrams.
        frame_venn_type = ttk.Frame(self.root)
        frame_venn_type.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        ttk.Label(frame_venn_type, text="Select Venn Diagram Type:").pack(side=tk.LEFT)

        # Dropdown menu to choose Venn diagram type
        self.venn_type = ttk.Combobox(frame_venn_type, values=["2 Sets", "3 Sets"], state="readonly")
        self.venn_type.pack(side=tk.LEFT)
        self.venn_type.current(0)  # Default to "2 Sets"
        self.venn_type.bind("<<ComboboxSelected>>", self.update_inputs) #update available inputs

        # Button to update the Venn diagram
        self.update_button = ttk.Button(frame_venn_type, text="Update Venn Diagram", command=self.update_venn) #update diagram plot
        self.update_button.pack()

    def create_input_fields(self):
        #Create input fields for 2-set and 3-set Venn diagrams.

        # Inputs for 2-circle Venn diagram
        ttk.Label(self.inputFrame, text="A Only:").grid(row=0, column=0)
        self.entry_a = ttk.Entry(self.inputFrame, width=5)
        self.entry_a.grid(row=0, column=1)

        ttk.Label(self.inputFrame, text="B Only").grid(row=1, column=0)
        self.entry_b = ttk.Entry(self.inputFrame, width=5)
        self.entry_b.grid(row=1, column=1)

        #intersection sizes

        ttk.Label(self.inputFrame, text="Intersection (A ∩ B):").grid(row=0, column=2)
        self.entry_ab = ttk.Entry(self.inputFrame, width=5)
        self.entry_ab.grid(row=0, column=3)

    def add_venn3_inputs(self):
        if self.hidden_inputs == True:
            self.label_c = ttk.Label(self.inputFrame, text="C Only:")
            self.label_c.grid(row=2, column=0)
            self.entry_c = ttk.Entry(self.inputFrame, width=5)
            self.entry_c.grid(row=2, column=1)
            
            self.label_ac = ttk.Label(self.inputFrame, text="Intersection (A ∩ C):")
            self.label_ac.grid(row=1, column=2)
            self.entry_ac = ttk.Entry(self.inputFrame, width=5)
            self.entry_ac.grid(row=1, column=3)

            self.label_bc = ttk.Label(self.inputFrame, text="Intersection (B ∩ C):")
            self.label_bc.grid(row=2, column=2)
            self.entry_bc = ttk.Entry(self.inputFrame, width=5)
            self.entry_bc.grid(row=2, column=3)

            self.label_abc= ttk.Label(self.inputFrame, text="Intersection (A ∩ B ∩ C):")
            self.label_abc.grid(row=3, column=2)
            self.entry_abc = ttk.Entry(self.inputFrame, width=5)
            self.entry_abc.grid(row=3, column=3)
            
            self.hidden_inputs = False

    def remove_venn3_inputs(self):
        if self.hidden_inputs == False:
            self.entry_c.grid_remove()
            self.entry_ac.grid_remove()
            self.entry_bc.grid_remove()
            self.entry_abc.grid_remove()

            self.label_c.grid_remove()
            self.label_ac.grid_remove()
            self.label_bc.grid_remove()
            self.label_abc.grid_remove()

            self.hidden_inputs = True
    
    def show_calculation_results(self):

        #clear frame
        for widget in self.resultsFrame.winfo_children():
            widget.destroy()

        #case where there are 3 areas
        if len(self.subsets) > 3: 

            self.combinedAreas = calculator.calculate_venn3_sizes(*self.subsets) #unpack subsets, and feed as argument
            #show sizes of each set
            ttk.Label(self.resultsFrame, text=f"Set A: {self.combinedAreas["a_total"]}").grid(row=0, column=0)
            ttk.Label(self.resultsFrame, text=f"Set B: {self.combinedAreas["b_total"]}").grid(row=1, column=0)
            ttk.Label(self.resultsFrame, text=f"Set C: {self.combinedAreas["c_total"]}").grid(row=2, column=0)

            #show size of each combined area
            ttk.Label(self.resultsFrame, text=f"Union (A∪B): {self.combinedAreas["aub"]}").grid(row=0, column=1)
            ttk.Label(self.resultsFrame, text=f"Union (A∪C): {self.combinedAreas["auc"]}").grid(row=1, column=1)
            ttk.Label(self.resultsFrame, text=f"Union (B∪C): {self.combinedAreas["buc"]}").grid(row=2, column=1)
            ttk.Label(self.resultsFrame, text=f"Union (A∪B∪C): {self.combinedAreas["aubuc"]}").grid(row=3, column=1)
        
        elif len(self.subsets) > 0: 

            self.combinedAreas = calculator.calculate_venn2_sizes(*self.subsets) #unpack subsets, and feed as argument
            print("calculating 2 circle areas")
            #show sizes of each set
            ttk.Label(self.resultsFrame, text=f"Set A: {self.combinedAreas["a_total"]}").grid(row=0, column=0)
            ttk.Label(self.resultsFrame, text=f"Set B: {self.combinedAreas["b_total"]}").grid(row=1, column=0)

            #show size of each combined area
            ttk.Label(self.resultsFrame, text=f"Union (A∪B): {self.combinedAreas["aub"]}").grid(row=0, column=1)
    


    def update_venn(self):
        #Update the Venn diagram based on user input and selection.
        try:
            # Clear the previous plot
            self.ax.clear()

            # Get the number of sets from the dropdown
            num_sets = self.venn_type.get()

            if num_sets == "2 Sets":
                # Get values from user inputs for 2-circle Venn diagram
                set_a = int(self.entry_a.get())
                set_b = int(self.entry_b.get())
                set_ab = int(self.entry_ab.get())

                # Plot the updated 2-circle Venn diagram
                self.subsets = (set_a, set_b, set_ab)
                venn2(subsets=self.subsets, set_labels=('Set A', 'Set B'), ax=self.ax)

            elif num_sets == "3 Sets":
                # Get values from user inputs for 3-circle Venn diagram
                set_a = int(self.entry_a.get())
                set_b = int(self.entry_b.get())
                set_c = int(self.entry_c.get())
                set_ab = int(self.entry_ab.get())
                set_bc = int(self.entry_bc.get())
                set_ac = int(self.entry_ac.get())
                set_abc = int(self.entry_abc.get())

                self.subsets = (set_a, set_b, set_c, set_ab, set_ac, set_bc, set_abc)

                # Plot the updated 3-circle Venn diagram
                venn3(subsets=self.subsets, set_labels=('Set A', 'Set B', 'Set C'), ax=self.ax)

            # Refresh the canvas
            self.canvas.draw()
            self.show_calculation_results()

        except ValueError:
            self.error_label.config(text="Please enter valid integers!")

    def update_inputs(self, *args):
        #Show or hide input fields based on the Venn type selected.
        if self.venn_type.get() == "2 Sets":
            self.remove_venn3_inputs()
        elif self.venn_type.get() == "3 Sets":
            self.add_venn3_inputs()

# Initialize the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = VennDiagramApp(root)
    root.mainloop()
