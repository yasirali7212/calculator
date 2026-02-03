"""
Scientific & GPA Calculator Application
A modern dual-purpose calculator with beautiful UI
"""

import customtkinter as ctk
from scientific_calculator import ScientificCalculator
from gpa_calculator import GPACalculator

# Set appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class CalculatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Scientific & GPA Calculator")
        self.geometry("900x700")
        self.minsize(800, 600)
        
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create header
        self.create_header()
        
        # Create tabview
        self.tabview = ctk.CTkTabview(self, corner_radius=15)
        self.tabview.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Add tabs
        self.tabview.add("Scientific Calculator")
        self.tabview.add("GPA Calculator")
        
        # Configure tab grid
        self.tabview.tab("Scientific Calculator").grid_rowconfigure(0, weight=1)
        self.tabview.tab("Scientific Calculator").grid_columnconfigure(0, weight=1)
        self.tabview.tab("GPA Calculator").grid_rowconfigure(0, weight=1)
        self.tabview.tab("GPA Calculator").grid_columnconfigure(0, weight=1)
        
        # Create calculator instances
        self.scientific_calc = ScientificCalculator(self.tabview.tab("Scientific Calculator"))
        self.scientific_calc.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.gpa_calc = GPACalculator(self.tabview.tab("GPA Calculator"))
        self.gpa_calc.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # Set default tab
        self.tabview.set("Scientific Calculator")
        
    def create_header(self):
        """Create the application header"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        # Title
        title = ctk.CTkLabel(
            header_frame,
            text="🧮 Advanced Calculator Suite",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(side="left")
        
        # Subtitle
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Scientific & GPA Calculations Made Beautiful",
            font=ctk.CTkFont(size=14),
            text_color=("gray60", "gray40")
        )
        subtitle.pack(side="left", padx=15)


def main():
    """Main application entry point"""
    app = CalculatorApp()
    app.mainloop()


if __name__ == "__main__":
    main()
