import os
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Notes Application")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        
        self.notes_file = "notes.txt"
        self.initialize_notes_file()
        
        self.create_widgets()
        
        self.load_notes()
    
    def get_current_datetime(self):
        """Return current date and time in YYYY-MM-DD HH:MM:SS format"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def initialize_notes_file(self):
        """Create notes file if it doesn't exist with creation date"""
        if not os.path.exists(self.notes_file):
            with open(self.notes_file, "w") as file:
                file.write(f"Notes File - Created: {self.get_current_datetime()}\n")
                file.write("="*50 + "\n\n")
    
    def create_widgets(self):
        """Create all GUI widgets"""
        main_frame = tk.Frame(self.root, bg="#f0f0f0", padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = tk.Label(
            main_frame, 
            text="Notes Application", 
            font=("Arial", 18, "bold"), 
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=(0, 20))
        
        entry_frame = tk.LabelFrame(
            main_frame, 
            text="New Note", 
            bg="#f0f0f0", 
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        entry_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.note_text = scrolledtext.ScrolledText(
            entry_frame, 
            wrap=tk.WORD, 
            width=60, 
            height=10,
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        self.note_text.pack(fill=tk.BOTH, expand=True)
        
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        save_button = tk.Button(
            button_frame,
            text="Save Note",
            command=self.save_note,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
            padx=15,
            pady=5
        )
        save_button.pack(side=tk.LEFT, padx=(0, 10))
        
        clear_button = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_note,
            bg="#f44336",
            fg="white",
            font=("Arial", 12),
            padx=15,
            pady=5
        )
        clear_button.pack(side=tk.LEFT)
        
        display_frame = tk.LabelFrame(
            main_frame, 
            text="Your Notes", 
            bg="#f0f0f0", 
            font=("Arial", 12),
            padx=10,
            pady=10
        )
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        self.notes_display = scrolledtext.ScrolledText(
            display_frame, 
            wrap=tk.WORD, 
            width=60, 
            height=15,
            font=("Arial", 12),
            padx=10,
            pady=10,
            state=tk.DISABLED
        )
        self.notes_display.pack(fill=tk.BOTH, expand=True)
        
        export_button = tk.Button(
            main_frame,
            text="Export Notes",
            command=self.export_notes,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12),
            padx=15,
            pady=5
        )
        export_button.pack(side=tk.RIGHT, pady=(10, 0))
    
    def save_note(self):
        """Save the current note to the file"""
        note_content = self.note_text.get("1.0", tk.END).strip()
        
        if not note_content:
            messagebox.showwarning("Empty Note", "Please enter some text before saving.")
            return
        
        try:
            with open(self.notes_file, "a") as file:
                file.write(f"[{self.get_current_datetime()}]\n")
                file.write(note_content + "\n")
                file.write("-"*50 + "\n\n")
            
            messagebox.showinfo("Success", "Note saved successfully!")
            self.clear_note()
            self.load_notes()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save note: {str(e)}")
    
    def clear_note(self):
        """Clear the note entry area"""
        self.note_text.delete("1.0", tk.END)
    
    def load_notes(self):
        """Load all notes from the file into the display area"""
        try:
            with open(self.notes_file, "r") as file:
                content = file.read()
            
            self.notes_display.config(state=tk.NORMAL)
            self.notes_display.delete("1.0", tk.END)
            self.notes_display.insert(tk.END, content)
            self.notes_display.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load notes: {str(e)}")
    
    def export_notes(self):
        """Export notes to a user-selected location"""
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                initialfile="my_notes_export.txt"
            )
            
            if file_path:
                with open(self.notes_file, "r") as source_file:
                    content = source_file.read()
                
                with open(file_path, "w") as dest_file:
                    dest_file.write(content)
                
                messagebox.showinfo("Success", f"Notes exported successfully to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export notes: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()