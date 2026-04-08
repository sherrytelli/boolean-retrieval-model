import model
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.boolean_model = model.Boolean_model()
        
        #setting the application title and window size
        self.title("Boolean Retrieval model")
        self.geometry("720x400") 

        #frame to store query results
        self.result_frame = tk.Frame(self, highlightbackground="black", highlightthickness=1, width=110, height=320)
        self.result_frame.pack(fill="x", padx=15, pady=15)
        self.result_frame.pack_propagate(False)

        #scrollbar for results widget
        self.scrollbar = tk.Scrollbar(self.result_frame)
        self.scrollbar.pack(side="right", fill="y")

        #error/initial text
        self.ini_text = "operators: [and, or, andnot]\n\nk: distance between two words. must be a number\n\nQuery: w\nResult:[]\n\nQuery: w1 operator w2\nResult:[]\n\nQuery: w1 operator w2 operator w3\nResult:[]\n\nQuery: w1 w2 /k\nResult:[]"
        
        #text widget for displaying results
        self.result_text = tk.Text(self.result_frame, wrap="word", height=10, yscrollcommand=self.scrollbar.set)
        self.result_text.pack(fill="both", expand=True, padx=5, pady=5)
        self.result_text.insert(tk.END, self.ini_text)
        self.result_text.config(state="disabled") #disable text editing

        #linking scrollbar to text widget
        self.scrollbar.config(command=self.result_text.yview)

        #frame to store query input and enter button
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(side="bottom", fill="x", padx=10, pady=10)

        #entry box for query input
        self.query_entry = tk.Entry(self.input_frame, width=100, fg="grey")
        self.query_entry.pack(side="left", padx=5, pady=5)
        
        #adding placeholder
        self.placeholder_text = "Enter your query or ""!help"" for help"
        self.query_entry.insert(0, self.placeholder_text)
        self.query_entry.bind("<FocusIn>", self.remove_placeholder)
        self.query_entry.bind("<FocusOut>", self.add_placeholder)

        #enter button
        self.enter_button = tk.Button(self.input_frame, text="Enter", width=10, height=1, command=self.process_query)
        self.enter_button.pack(side="left", padx=5, pady=5)
        
    def remove_placeholder(self, event):
        """Remove placeholder text when the user clicks inside the entry box."""
        if self.query_entry.get() == self.placeholder_text:
            self.query_entry.delete(0, tk.END)
            self.query_entry.config(fg="black")  #change text color to black

    def add_placeholder(self, event):
        """Restore placeholder text if the entry box is empty when the user leaves."""
        if self.query_entry.get() == "":
            self.query_entry.insert(0, self.placeholder_text)
            self.query_entry.config(fg="gray")  #change text color back to gray
            
    def process_query(self):
        """Fetch query from entry box and display results."""
        try:
            query = self.query_entry.get()
            if query and query != self.placeholder_text:  #ignore placeholder text
                if(query == "!help"):
                    #update text box with result
                    self.result_text.config(state="normal")
                    self.result_text.delete("1.0", tk.END)
                    self.result_text.insert(tk.END, self.ini_text)
                    self.result_text.config(state="disabled")
                else:
                    result = self.boolean_model.run_query(query)
                    if((result == "Invalid Query Operator") or (result == "Invalid Query")):
                        #update text box with result
                        self.result_text.config(state="normal")
                        self.result_text.delete("1.0", tk.END)
                        self.result_text.insert(tk.END, f"Query: {query}\n\nResults: {result}\n\n{self.ini_text}")
                        self.result_text.config(state="disabled") 
                    else:
                        #update text box with result
                        self.result_text.config(state="normal")
                        self.result_text.delete("1.0", tk.END)
                        self.result_text.insert(tk.END, f"Query: {query}\n\nResults: {result}")
                        self.result_text.config(state="disabled")
        except KeyError: #handle any dictionary key errors
            #update text box with result
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Query: {query}\n\nResults: Word(s) not found.")
            self.result_text.config(state="disabled")
        except: #handle any other types of exceptions
            #update text box with result
            self.result_text.config(state="normal")
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"Query: {query}\n\nResults: Invalid Query\n\n{self.ini_text}")
            self.result_text.config(state="disabled")
            
        #clear query box and restore placeholder
        self.query_entry.delete(0, tk.END)
        self.focus()
        self.query_entry.config(fg="gray")  
        
if __name__ == "__main__":
    app = App()
    app.mainloop()