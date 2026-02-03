"""
Scientific Calculator Module
Provides advanced mathematical calculations with a beautiful UI
"""

import customtkinter as ctk
import math
from typing import Optional


class ScientificCalculator(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Calculator state
        self.current_value = "0"
        self.previous_value = ""
        self.operation = None
        self.new_number = True
        self.memory = 0
        self.angle_mode = "deg"  # deg or rad
        self.history = []
        
        # Configure grid
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Create UI
        self.create_display()
        self.create_mode_toggle()
        self.create_buttons()
        
        # Bind keyboard
        self.winfo_toplevel().bind('<Key>', self.on_key_press)
        
    def create_display(self):
        """Create the calculator display"""
        display_frame = ctk.CTkFrame(self, corner_radius=10)
        display_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        display_frame.grid_columnconfigure(0, weight=1)
        
        # History display (small)
        self.history_label = ctk.CTkLabel(
            display_frame,
            text="",
            font=ctk.CTkFont(size=14),
            text_color=("gray50", "gray60"),
            anchor="e"
        )
        self.history_label.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="ew")
        
        # Main display
        self.display = ctk.CTkLabel(
            display_frame,
            text="0",
            font=ctk.CTkFont(size=42, weight="bold"),
            anchor="e"
        )
        self.display.grid(row=1, column=0, padx=20, pady=(5, 15), sticky="ew")
        
    def create_mode_toggle(self):
        """Create angle mode toggle"""
        mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        mode_frame.grid(row=1, column=0, padx=10, pady=(0, 5), sticky="ew")
        
        self.mode_label = ctk.CTkLabel(
            mode_frame,
            text="Angle Mode:",
            font=ctk.CTkFont(size=12)
        )
        self.mode_label.pack(side="left", padx=(10, 5))
        
        self.mode_switch = ctk.CTkSegmentedButton(
            mode_frame,
            values=["Degrees", "Radians"],
            command=self.toggle_mode,
            font=ctk.CTkFont(size=12)
        )
        self.mode_switch.pack(side="left")
        self.mode_switch.set("Degrees")
        
    def create_buttons(self):
        """Create calculator button grid"""
        button_frame = ctk.CTkFrame(self, corner_radius=10)
        button_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        # Configure grid to be responsive
        for i in range(7):
            button_frame.grid_rowconfigure(i, weight=1)
        for i in range(6):
            button_frame.grid_columnconfigure(i, weight=1)
        
        # Button configurations: (text, row, col, colspan, command, color)
        buttons = [
            # Row 0 - Memory and special functions
            ("MC", 0, 0, 1, lambda: self.memory_clear(), "gray30"),
            ("MR", 0, 1, 1, lambda: self.memory_recall(), "gray30"),
            ("M+", 0, 2, 1, lambda: self.memory_add(), "gray30"),
            ("M-", 0, 3, 1, lambda: self.memory_subtract(), "gray30"),
            ("MS", 0, 4, 1, lambda: self.memory_store(), "gray30"),
            ("C", 0, 5, 1, lambda: self.clear(), "#d32f2f"),
            
            # Row 1 - Advanced functions
            ("sin", 1, 0, 1, lambda: self.scientific_function('sin'), "#6441a5"),
            ("cos", 1, 1, 1, lambda: self.scientific_function('cos'), "#6441a5"),
            ("tan", 1, 2, 1, lambda: self.scientific_function('tan'), "#6441a5"),
            ("log", 1, 3, 1, lambda: self.scientific_function('log'), "#6441a5"),
            ("ln", 1, 4, 1, lambda: self.scientific_function('ln'), "#6441a5"),
            ("AC", 1, 5, 1, lambda: self.all_clear(), "#b71c1c"),
            
            # Row 2 - More functions
            ("x²", 2, 0, 1, lambda: self.scientific_function('square'), "#6441a5"),
            ("x³", 2, 1, 1, lambda: self.scientific_function('cube'), "#6441a5"),
            ("xʸ", 2, 2, 1, lambda: self.operation_pressed('^'), "#1f538d"),
            ("√", 2, 3, 1, lambda: self.scientific_function('sqrt'), "#6441a5"),
            ("∛", 2, 4, 1, lambda: self.scientific_function('cbrt'), "#6441a5"),
            ("⌫", 2, 5, 1, lambda: self.backspace(), "#f57c00"),
            
            # Row 3 - More functions and operations
            ("1/x", 3, 0, 1, lambda: self.scientific_function('reciprocal'), "#6441a5"),
            ("n!", 3, 1, 1, lambda: self.scientific_function('factorial'), "#6441a5"),
            ("|x|", 3, 2, 1, lambda: self.scientific_function('abs'), "#6441a5"),
            ("mod", 3, 3, 1, lambda: self.operation_pressed('%'), "#1f538d"),
            ("(", 3, 4, 1, lambda: self.append_char('('), "gray30"),
            (")", 3, 5, 1, lambda: self.append_char(')'), "gray30"),
            
            # Row 4 - Numbers and operations
            ("7", 4, 0, 1, lambda: self.number_pressed('7'), "gray25"),
            ("8", 4, 1, 1, lambda: self.number_pressed('8'), "gray25"),
            ("9", 4, 2, 1, lambda: self.number_pressed('9'), "gray25"),
            ("÷", 4, 3, 1, lambda: self.operation_pressed('/'), "#1f538d"),
            ("π", 4, 4, 1, lambda: self.constant_pressed('pi'), "#6441a5"),
            ("e", 4, 5, 1, lambda: self.constant_pressed('e'), "#6441a5"),
            
            # Row 5
            ("4", 5, 0, 1, lambda: self.number_pressed('4'), "gray25"),
            ("5", 5, 1, 1, lambda: self.number_pressed('5'), "gray25"),
            ("6", 5, 2, 1, lambda: self.number_pressed('6'), "gray25"),
            ("×", 5, 3, 1, lambda: self.operation_pressed('*'), "#1f538d"),
            ("10ˣ", 5, 4, 1, lambda: self.scientific_function('10x'), "#6441a5"),
            ("2ˣ", 5, 5, 1, lambda: self.scientific_function('2x'), "#6441a5"),
            
            # Row 6
            ("1", 6, 0, 1, lambda: self.number_pressed('1'), "gray25"),
            ("2", 6, 1, 1, lambda: self.number_pressed('2'), "gray25"),
            ("3", 6, 2, 1, lambda: self.number_pressed('3'), "gray25"),
            ("-", 6, 3, 1, lambda: self.operation_pressed('-'), "#1f538d"),
            ("0", 6, 4, 1, lambda: self.number_pressed('0'), "gray25"),
            (".", 6, 5, 1, lambda: self.decimal_pressed(), "gray25"),
            
            # Row 7 (last row, centered)
            ("+/-", 7, 0, 1, lambda: self.toggle_sign(), "gray30"),
            ("+", 7, 1, 1, lambda: self.operation_pressed('+'), "#1f538d"),
            ("=", 7, 2, 4, lambda: self.equals_pressed(), "#00897b"),
        ]
        
        # Create buttons
        for btn_config in buttons:
            text, row, col, colspan, command, color = btn_config
            btn = ctk.CTkButton(
                button_frame,
                text=text,
                command=command,
                font=ctk.CTkFont(size=16, weight="bold"),
                fg_color=color,
                hover_color=self.adjust_color(color, 1.2),
                corner_radius=8,
                height=50
            )
            btn.grid(row=row, column=col, columnspan=colspan, 
                    padx=3, pady=3, sticky="nsew")
    
    def adjust_color(self, color, factor):
        """Adjust color brightness for hover effect"""
        if color.startswith('#'):
            # Convert hex to RGB, adjust, and convert back
            r, g, b = int(color[1:3], 16), int(color[4:6], 16), int(color[6:8], 16)
            r = min(255, int(r * factor))
            g = min(255, int(g * factor))
            b = min(255, int(b * factor))
            return f'#{r:02x}{g:02x}{b:02x}'
        return color
    
    def toggle_mode(self, value):
        """Toggle between degrees and radians"""
        self.angle_mode = "deg" if value == "Degrees" else "rad"
    
    def number_pressed(self, number):
        """Handle number button press"""
        if self.new_number:
            self.current_value = number
            self.new_number = False
        else:
            if self.current_value == "0":
                self.current_value = number
            else:
                self.current_value += number
        self.update_display()
    
    def decimal_pressed(self):
        """Handle decimal point"""
        if '.' not in self.current_value:
            if self.new_number:
                self.current_value = "0."
                self.new_number = False
            else:
                self.current_value += '.'
            self.update_display()
    
    def operation_pressed(self, op):
        """Handle operation button"""
        if self.operation and not self.new_number:
            self.equals_pressed()
        
        self.previous_value = self.current_value
        self.operation = op
        self.new_number = True
        self.update_history(f"{self.current_value} {self.operation}")
    
    def equals_pressed(self):
        """Calculate result"""
        if not self.operation:
            return
        
        try:
            prev = float(self.previous_value)
            current = float(self.current_value)
            
            if self.operation == '+':
                result = prev + current
            elif self.operation == '-':
                result = prev - current
            elif self.operation == '*':
                result = prev * current
            elif self.operation == '/':
                if current == 0:
                    self.current_value = "Error: Div by 0"
                    self.new_number = True
                    self.update_display()
                    return
                result = prev / current
            elif self.operation == '^':
                result = prev ** current
            elif self.operation == '%':
                result = prev % current
            else:
                return
            
            # Format result
            self.current_value = self.format_number(result)
            self.operation = None
            self.new_number = True
            self.update_display()
            self.history_label.configure(text="")
            
        except Exception as e:
            self.current_value = "Error"
            self.new_number = True
            self.update_display()
    
    def scientific_function(self, func):
        """Apply scientific function"""
        try:
            value = float(self.current_value)
            
            if func == 'sin':
                result = math.sin(math.radians(value) if self.angle_mode == 'deg' else value)
            elif func == 'cos':
                result = math.cos(math.radians(value) if self.angle_mode == 'deg' else value)
            elif func == 'tan':
                result = math.tan(math.radians(value) if self.angle_mode == 'deg' else value)
            elif func == 'log':
                result = math.log10(value)
            elif func == 'ln':
                result = math.log(value)
            elif func == 'sqrt':
                result = math.sqrt(value)
            elif func == 'cbrt':
                result = value ** (1/3)
            elif func == 'square':
                result = value ** 2
            elif func == 'cube':
                result = value ** 3
            elif func == 'reciprocal':
                result = 1 / value
            elif func == 'factorial':
                result = math.factorial(int(value))
            elif func == 'abs':
                result = abs(value)
            elif func == '10x':
                result = 10 ** value
            elif func == '2x':
                result = 2 ** value
            else:
                return
            
            self.current_value = self.format_number(result)
            self.new_number = True
            self.update_display()
            
        except Exception as e:
            self.current_value = "Error"
            self.new_number = True
            self.update_display()
    
    def constant_pressed(self, constant):
        """Insert mathematical constant"""
        if constant == 'pi':
            value = math.pi
        elif constant == 'e':
            value = math.e
        else:
            return
        
        self.current_value = self.format_number(value)
        self.new_number = True
        self.update_display()
    
    def toggle_sign(self):
        """Toggle positive/negative"""
        try:
            value = float(self.current_value)
            self.current_value = self.format_number(-value)
            self.update_display()
        except:
            pass
    
    def backspace(self):
        """Remove last character"""
        if not self.new_number and len(self.current_value) > 1:
            self.current_value = self.current_value[:-1]
            self.update_display()
        elif not self.new_number:
            self.current_value = "0"
            self.new_number = True
            self.update_display()
    
    def clear(self):
        """Clear current value"""
        self.current_value = "0"
        self.new_number = True
        self.update_display()
    
    def all_clear(self):
        """Clear everything"""
        self.current_value = "0"
        self.previous_value = ""
        self.operation = None
        self.new_number = True
        self.history_label.configure(text="")
        self.update_display()
    
    def append_char(self, char):
        """Append character (for parentheses)"""
        if self.new_number:
            self.current_value = char
            self.new_number = False
        else:
            self.current_value += char
        self.update_display()
    
    # Memory functions
    def memory_clear(self):
        """Clear memory"""
        self.memory = 0
    
    def memory_recall(self):
        """Recall memory"""
        self.current_value = self.format_number(self.memory)
        self.new_number = True
        self.update_display()
    
    def memory_add(self):
        """Add to memory"""
        try:
            self.memory += float(self.current_value)
        except:
            pass
    
    def memory_subtract(self):
        """Subtract from memory"""
        try:
            self.memory -= float(self.current_value)
        except:
            pass
    
    def memory_store(self):
        """Store in memory"""
        try:
            self.memory = float(self.current_value)
        except:
            pass
    
    def format_number(self, num):
        """Format number for display"""
        if isinstance(num, int) or (isinstance(num, float) and num.is_integer()):
            return str(int(num))
        else:
            # Round to 10 decimal places and remove trailing zeros
            formatted = f"{num:.10f}".rstrip('0').rstrip('.')
            return formatted
    
    def update_display(self):
        """Update the display"""
        self.display.configure(text=self.current_value)
    
    def update_history(self, text):
        """Update history display"""
        self.history_label.configure(text=text)
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        
        # Numbers
        if key.isdigit():
            self.number_pressed(key)
        # Operations
        elif key == '+':
            self.operation_pressed('+')
        elif key == '-':
            self.operation_pressed('-')
        elif key == '*':
            self.operation_pressed('*')
        elif key == '/':
            self.operation_pressed('/')
        elif key == '.':
            self.decimal_pressed()
        elif key == '\r' or key == '=':  # Enter or equals
            self.equals_pressed()
        elif event.keysym == 'BackSpace':
            self.backspace()
        elif event.keysym == 'Escape':
            self.all_clear()
