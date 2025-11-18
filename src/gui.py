# src/gui.py

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox

# Import the core logic functions
from strength_analyzer import analyze_password
from wordlist_generator import generate_and_export_wordlist

# Set the overall appearance mode (Dark, Light, System)
ctk.set_appearance_mode("System")  
# Set the color theme (blue, dark-blue, green)
ctk.set_default_color_theme("blue") 

class PasswordToolApp(ctk.CTk):
    """
    Main application class for the Password Strength Analyzer and 
    Custom Wordlist Generator using CustomTkinter.
    """
    def __init__(self):
        super().__init__()

        # --- Basic Setup ---
        self.title("CyberSec Tool Suite: Password & Wordlist")
        self.geometry("800x650")

        # Configure grid layout (2x1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Create Tabview for dynamic switching ---
        self.tabview = ctk.CTkTabview(self, width=750, height=600)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Add Tabs
        self.tabview.add("Analyzer")
        self.tabview.add("Wordlist Generator")

        # Configure Tab content
        self.tabview.tab("Analyzer").grid_columnconfigure(0, weight=1)
        self.tabview.tab("Wordlist Generator").grid_columnconfigure(0, weight=1)

        # Initialize the two core tool sections
        self.known_data_entry = None # Initialize for analyzer tab
        self.password_entry = None # Initialize for analyzer tab
        self.score_label = None # Initialize for analyzer tab
        self.time_label = None # Initialize for analyzer tab
        self.feedback_text = None # Initialize for analyzer tab
        self.wordlist_inputs = None # Initialize for wordlist tab
        self.wordlist_status_label = None # Initialize for wordlist tab

        self._setup_analyzer_tab(self.tabview.tab("Analyzer"))
        self._setup_wordlist_tab(self.tabview.tab("Wordlist Generator"))

    # =================================================================
    #                      PASSWORD ANALYZER TAB
    # =================================================================

    def _setup_analyzer_tab(self, tab):
        """Sets up the Password Analyzer interface."""
        
        # Title
        ctk.CTkLabel(tab, text="Password Strength Analyzer (zxcvbn)", 
                     font=ctk.CTkFont(size=20, weight="bold")).grid(
            row=0, column=0, padx=20, pady=(20, 10), sticky="w"
        )

        # Input Frame (Password and Known Data)
        input_frame = ctk.CTkFrame(tab)
        input_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        input_frame.columnconfigure(1, weight=1)
        
        # Password Input
        ctk.CTkLabel(input_frame, text="Password to Analyze:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = ctk.CTkEntry(input_frame, show="*")
        self.password_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Known Data Input
        ctk.CTkLabel(input_frame, text="Known Data (comma-separated):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.known_data_entry = ctk.CTkEntry(input_frame, placeholder_text="e.g., John, 1995, Sparky")
        self.known_data_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Analyze Button
        self.analyze_button = ctk.CTkButton(tab, text="Analyze Strength", 
                                            command=self._analyze_password_click)
        self.analyze_button.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Output Frame
        output_frame = ctk.CTkFrame(tab)
        output_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        output_frame.columnconfigure(1, weight=1)
        
        # Output Labels
        self.score_label = ctk.CTkLabel(output_frame, text="Score: N/A")
        self.score_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.time_label = ctk.CTkLabel(output_frame, text="Crack Time: N/A")
        self.time_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        ctk.CTkLabel(output_frame, text="Feedback/Suggestions:", 
                     font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, padx=10, pady=(10, 0), sticky="w")
        
        self.feedback_text = ctk.CTkTextbox(output_frame, height=150, width=500, wrap="word")
        self.feedback_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
    
    def _analyze_password_click(self):
        """Handler for the Analyze Strength button."""
        password = self.password_entry.get()
        known_data_str = self.known_data_entry.get()
        
        if not password:
            messagebox.showerror("Input Error", "Please enter a password to analyze.")
            return

        # Prepare known data list
        known_data = [d.strip() for d in known_data_str.split(',') if d.strip()]
        
        # Call the core function
        results = analyze_password(password, known_data)
        
        # Update GUI elements
        score = results.get('score', 0)
        crack_time = results.get('crack_time_display', 'N/A')
        warning = results.get('warning', '')
        suggestions = "\n- " + "\n- ".join(results.get('suggestions', [])) if results.get('suggestions') else ""

        # Color code the score
        if score == 4:
            color = "green"
        elif score >= 2:
            color = "yellow"
        else:
            color = "red"

        self.score_label.configure(text=f"Score: {score} / 4", text_color=color)
        self.time_label.configure(text=f"Crack Time: {crack_time}")
        
        self.feedback_text.delete("1.0", "end")
        self.feedback_text.insert("1.0", f"Warning: {warning}\n\nSuggestions: {suggestions}")


    # =================================================================
    #                      WORDLIST GENERATOR TAB
    # =================================================================

    def _setup_wordlist_tab(self, tab):
        """Sets up the Custom Wordlist Generator interface."""
        
        # Title
        ctk.CTkLabel(tab, text="Custom Attack Wordlist Generator", 
                     font=ctk.CTkFont(size=20, weight="bold")).grid(
            row=0, column=0, padx=20, pady=(20, 10), sticky="w"
        )
        
        # Instructions
        ctk.CTkLabel(tab, text="Enter base words/phrases (separated by a new line or comma):", 
                     wraplength=700).grid(row=1, column=0, padx=20, pady=5, sticky="w")

        # Input Textbox (FIX: Removed unsupported 'placeholder_text' argument)
        self.wordlist_inputs = ctk.CTkTextbox(tab, height=150, width=700, wrap="word")
        self.wordlist_inputs.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        # Optional: Manually insert placeholder-like text after creation
        self.wordlist_inputs.insert("0.0", "Enter Name, Pet, Date, Favorite Word, etc.")


        # Generate Button
        self.generate_button = ctk.CTkButton(tab, text="Generate & Export Wordlist", 
                                             command=self._generate_wordlist_click)
        self.generate_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        # Status Label
        self.wordlist_status_label = ctk.CTkLabel(tab, text="Status: Ready to generate.")
        self.wordlist_status_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")

    def _generate_wordlist_click(self):
        """Handler for the Generate & Export Wordlist button."""
        input_data_raw = self.wordlist_inputs.get("1.0", "end-1c")
        
        # Check and strip the default placeholder text if the user didn't enter anything
        placeholder = "Enter Name, Pet, Date, Favorite Word, etc."
        if input_data_raw.strip() == placeholder or not input_data_raw.strip():
            messagebox.showerror("Input Error", "Please provide inputs (name, date, etc.) for wordlist generation.")
            return

        # 1. Process inputs: split by newline or comma
        inputs = [line.strip() for line in input_data_raw.replace(',', '\n').split('\n') if line.strip()]

        # 2. Open file dialog to choose save location
        output_filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save Wordlist As"
        )
        
        if not output_filename:
            self.wordlist_status_label.configure(text="Status: Generation cancelled.")
            return

        try:
            self.wordlist_status_label.configure(text="Status: Generating... Please wait.")
            self.update_idletasks() # Force update the GUI status

            # 3. Call the core function
            generate_and_export_wordlist(inputs, output_filename)
            
            # 4. Update status
            messagebox.showinfo("Success", f"Wordlist successfully exported to:\n{output_filename}")
            self.wordlist_status_label.configure(text=f"Status: Exported to {output_filename}")
            
        except Exception as e:
            messagebox.showerror("Generation Error", f"An error occurred during generation: {e}")
            self.wordlist_status_label.configure(text="Status: Generation failed.")


if __name__ == "__main__":
    app = PasswordToolApp()
    app.mainloop()
