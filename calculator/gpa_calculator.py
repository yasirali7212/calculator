"""
GPA Calculator Module
Manages course grades and calculates GPA with semester tracking
"""

import customtkinter as ctk
import json
import os
from tkinter import filedialog, messagebox


class GPACalculator(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Data storage
        self.semesters = []
        self.current_semester_courses = []
        self.data_file = "gpa_data.json"
        
        # Grade scale (4.0 system)
        self.grade_scale = {
            'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0,
            'F': 0.0
        }
        
        # Configure grid
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)
        
        # Create UI
        self.create_summary_panel()
        self.create_course_entry()
        self.create_action_buttons()
        
        # Load saved data
        self.load_data()
        
    def create_summary_panel(self):
        """Create GPA summary display"""
        summary_frame = ctk.CTkFrame(self, corner_radius=10)
        summary_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        summary_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Current Semester GPA
        semester_frame = ctk.CTkFrame(summary_frame, corner_radius=8)
        semester_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            semester_frame,
            text="Current Semester GPA",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        self.semester_gpa_label = ctk.CTkLabel(
            semester_frame,
            text="0.00",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#4caf50"
        )
        self.semester_gpa_label.pack(pady=(0, 10))
        
        # Cumulative GPA
        cumulative_frame = ctk.CTkFrame(summary_frame, corner_radius=8)
        cumulative_frame.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            cumulative_frame,
            text="Cumulative GPA",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        self.cumulative_gpa_label = ctk.CTkLabel(
            cumulative_frame,
            text="0.00",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#2196f3"
        )
        self.cumulative_gpa_label.pack(pady=(0, 10))
        
        # Total Credits
        credits_frame = ctk.CTkFrame(summary_frame, corner_radius=8)
        credits_frame.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        ctk.CTkLabel(
            credits_frame,
            text="Total Credits",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        self.credits_label = ctk.CTkLabel(
            credits_frame,
            text="0",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#ff9800"
        )
        self.credits_label.pack(pady=(0, 10))
        
    def create_course_entry(self):
        """Create course entry and list"""
        main_frame = ctk.CTkFrame(self, corner_radius=10)
        main_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Entry section
        entry_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        entry_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        entry_frame.grid_columnconfigure(0, weight=2)
        entry_frame.grid_columnconfigure(1, weight=1)
        entry_frame.grid_columnconfigure(2, weight=1)
        
        ctk.CTkLabel(
            entry_frame,
            text="Add Course:",
            font=ctk.CTkFont(size=16, weight="bold")
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))
        
        # Course name
        ctk.CTkLabel(entry_frame, text="Course Name:").grid(row=1, column=0, sticky="w", pady=5)
        self.course_name_entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="e.g., Computer Science 101",
            width=300
        )
        self.course_name_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=(5, 10), pady=5)
        
        # Credits
        ctk.CTkLabel(entry_frame, text="Credits:").grid(row=2, column=0, sticky="w", pady=5)
        self.credits_entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="e.g., 3",
            width=100
        )
        self.credits_entry.grid(row=2, column=1, sticky="w", padx=(5, 10), pady=5)
        
        # Grade
        ctk.CTkLabel(entry_frame, text="Grade:").grid(row=2, column=2, sticky="w", pady=5, padx=(10, 0))
        self.grade_menu = ctk.CTkOptionMenu(
            entry_frame,
            values=list(self.grade_scale.keys()),
            width=100
        )
        self.grade_menu.grid(row=2, column=3, sticky="w", padx=(5, 0), pady=5)
        self.grade_menu.set("A")
        
        # Add button
        add_btn = ctk.CTkButton(
            entry_frame,
            text="➕ Add Course",
            command=self.add_course,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#00897b",
            hover_color="#00695c",
            height=35
        )
        add_btn.grid(row=3, column=0, columnspan=4, pady=(15, 0), sticky="ew")
        
        # Course list
        list_label = ctk.CTkLabel(
            main_frame,
            text="Current Semester Courses:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        list_label.grid(row=1, column=0, padx=15, pady=(0, 5), sticky="w")
        
        # Scrollable frame for courses
        self.courses_frame = ctk.CTkScrollableFrame(main_frame, corner_radius=8)
        self.courses_frame.grid(row=2, column=0, padx=15, pady=(0, 15), sticky="nsew")
        main_frame.grid_rowconfigure(2, weight=1)
        
    def create_action_buttons(self):
        """Create action buttons"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Save Semester
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Semester",
            command=self.save_semester,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1f538d",
            hover_color="#164070",
            height=40
        )
        save_btn.grid(row=0, column=0, padx=5, sticky="ew")
        
        # Clear Current
        clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑️ Clear Current",
            command=self.clear_current,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#f57c00",
            hover_color="#ef6c00",
            height=40
        )
        clear_btn.grid(row=0, column=1, padx=5, sticky="ew")
        
        # View History
        history_btn = ctk.CTkButton(
            button_frame,
            text="📊 View History",
            command=self.view_history,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#6441a5",
            hover_color="#512d8b",
            height=40
        )
        history_btn.grid(row=0, column=2, padx=5, sticky="ew")
        
        # Export Report
        export_btn = ctk.CTkButton(
            button_frame,
            text="📄 Export Report",
            command=self.export_report,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#00695c",
            hover_color="#004d40",
            height=40
        )
        export_btn.grid(row=0, column=3, padx=5, sticky="ew")
        
    def add_course(self):
        """Add a course to current semester"""
        course_name = self.course_name_entry.get().strip()
        credits_str = self.credits_entry.get().strip()
        grade = self.grade_menu.get()
        
        # Validate input
        if not course_name:
            messagebox.showerror("Error", "Please enter a course name")
            return
        
        try:
            credits = float(credits_str)
            if credits <= 0:
                raise ValueError()
        except:
            messagebox.showerror("Error", "Please enter a valid number of credits")
            return
        
        # Add course
        course = {
            'name': course_name,
            'credits': credits,
            'grade': grade,
            'points': self.grade_scale[grade]
        }
        self.current_semester_courses.append(course)
        
        # Clear entries
        self.course_name_entry.delete(0, 'end')
        self.credits_entry.delete(0, 'end')
        self.grade_menu.set("A")
        
        # Update display
        self.update_course_list()
        self.calculate_gpa()
        
    def update_course_list(self):
        """Update the displayed course list"""
        # Clear existing
        for widget in self.courses_frame.winfo_children():
            widget.destroy()
        
        if not self.current_semester_courses:
            ctk.CTkLabel(
                self.courses_frame,
                text="No courses added yet",
                text_color="gray",
                font=ctk.CTkFont(size=14)
            ).pack(pady=20)
            return
        
        # Add header
        header_frame = ctk.CTkFrame(self.courses_frame, fg_color="gray25")
        header_frame.pack(fill="x", pady=(0, 5))
        
        headers = ["Course", "Credits", "Grade", "Points", ""]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=100 if i < 4 else 50
            )
            label.pack(side="left", padx=5, pady=5)
        
        # Add courses
        for idx, course in enumerate(self.current_semester_courses):
            course_frame = ctk.CTkFrame(self.courses_frame, fg_color="gray20")
            course_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(course_frame, text=course['name'], width=100, anchor="w").pack(side="left", padx=5, pady=5)
            ctk.CTkLabel(course_frame, text=str(course['credits']), width=100).pack(side="left", padx=5, pady=5)
            ctk.CTkLabel(course_frame, text=course['grade'], width=100).pack(side="left", padx=5, pady=5)
            ctk.CTkLabel(course_frame, text=f"{course['points']:.1f}", width=100).pack(side="left", padx=5, pady=5)
            
            # Delete button
            delete_btn = ctk.CTkButton(
                course_frame,
                text="✕",
                width=50,
                command=lambda i=idx: self.delete_course(i),
                fg_color="#d32f2f",
                hover_color="#b71c1c"
            )
            delete_btn.pack(side="left", padx=5, pady=5)
    
    def delete_course(self, index):
        """Delete a course"""
        if 0 <= index < len(self.current_semester_courses):
            self.current_semester_courses.pop(index)
            self.update_course_list()
            self.calculate_gpa()
    
    def calculate_gpa(self):
        """Calculate and update GPA displays"""
        # Calculate current semester GPA
        if self.current_semester_courses:
            total_points = sum(c['credits'] * c['points'] for c in self.current_semester_courses)
            total_credits = sum(c['credits'] for c in self.current_semester_courses)
            semester_gpa = total_points / total_credits if total_credits > 0 else 0.0
        else:
            semester_gpa = 0.0
            total_credits = 0
        
        # Calculate cumulative GPA
        all_courses = []
        for semester in self.semesters:
            all_courses.extend(semester['courses'])
        all_courses.extend(self.current_semester_courses)
        
        if all_courses:
            cumulative_points = sum(c['credits'] * c['points'] for c in all_courses)
            cumulative_credits = sum(c['credits'] for c in all_courses)
            cumulative_gpa = cumulative_points / cumulative_credits if cumulative_credits > 0 else 0.0
        else:
            cumulative_gpa = 0.0
            cumulative_credits = 0
        
        # Update labels
        self.semester_gpa_label.configure(text=f"{semester_gpa:.2f}")
        self.cumulative_gpa_label.configure(text=f"{cumulative_gpa:.2f}")
        self.credits_label.configure(text=str(int(cumulative_credits)))
        
        # Update colors based on GPA
        self.semester_gpa_label.configure(text_color=self.get_gpa_color(semester_gpa))
        self.cumulative_gpa_label.configure(text_color=self.get_gpa_color(cumulative_gpa))
    
    def get_gpa_color(self, gpa):
        """Get color based on GPA value"""
        if gpa >= 3.5:
            return "#4caf50"  # Green
        elif gpa >= 3.0:
            return "#00897b"  # Teal
        elif gpa >= 2.5:
            return "#ffa726"  # Orange
        elif gpa >= 2.0:
            return "#ff9800"  # Dark orange
        else:
            return "#f44336"  # Red
    
    def save_semester(self):
        """Save current semester to history"""
        if not self.current_semester_courses:
            messagebox.showwarning("Warning", "No courses to save")
            return
        
        # Create semester dialog
        dialog = ctk.CTkInputDialog(
            text="Enter semester name (e.g., Fall 2024):",
            title="Save Semester"
        )
        semester_name = dialog.get_input()
        
        if semester_name:
            semester = {
                'name': semester_name,
                'courses': self.current_semester_courses.copy()
            }
            self.semesters.append(semester)
            self.current_semester_courses = []
            
            self.update_course_list()
            self.calculate_gpa()
            self.save_data()
            
            messagebox.showinfo("Success", f"Semester '{semester_name}' saved!")
    
    def clear_current(self):
        """Clear current semester courses"""
        if self.current_semester_courses:
            if messagebox.askyesno("Confirm", "Clear all current courses?"):
                self.current_semester_courses = []
                self.update_course_list()
                self.calculate_gpa()
    
    def view_history(self):
        """View semester history"""
        if not self.semesters:
            messagebox.showinfo("History", "No saved semesters yet")
            return
        
        # Create history window
        history_window = ctk.CTkToplevel(self)
        history_window.title("Semester History")
        history_window.geometry("700x500")
        
        # Title
        ctk.CTkLabel(
            history_window,
            text="📚 Semester History",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(history_window)
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Display semesters
        for idx, semester in enumerate(self.semesters):
            semester_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
            semester_frame.pack(fill="x", pady=10)
            
            # Semester header
            header_frame = ctk.CTkFrame(semester_frame, fg_color="gray25")
            header_frame.pack(fill="x", padx=10, pady=10)
            
            ctk.CTkLabel(
                header_frame,
                text=semester['name'],
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(side="left", padx=10, pady=5)
            
            # Calculate semester GPA
            total_points = sum(c['credits'] * c['points'] for c in semester['courses'])
            total_credits = sum(c['credits'] for c in semester['courses'])
            semester_gpa = total_points / total_credits if total_credits > 0 else 0.0
            
            gpa_label = ctk.CTkLabel(
                header_frame,
                text=f"GPA: {semester_gpa:.2f}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=self.get_gpa_color(semester_gpa)
            )
            gpa_label.pack(side="left", padx=10, pady=5)
            
            ctk.CTkLabel(
                header_frame,
                text=f"Credits: {int(total_credits)}",
                font=ctk.CTkFont(size=14)
            ).pack(side="left", padx=10, pady=5)
            
            # Delete button
            delete_btn = ctk.CTkButton(
                header_frame,
                text="Delete",
                width=80,
                command=lambda i=idx: self.delete_semester(i, history_window),
                fg_color="#d32f2f",
                hover_color="#b71c1c"
            )
            delete_btn.pack(side="right", padx=10, pady=5)
            
            # Courses
            for course in semester['courses']:
                course_text = f"  • {course['name']} - {course['credits']} credits - Grade: {course['grade']}"
                ctk.CTkLabel(
                    semester_frame,
                    text=course_text,
                    anchor="w"
                ).pack(fill="x", padx=20, pady=2)
    
    def delete_semester(self, index, window):
        """Delete a semester from history"""
        if messagebox.askyesno("Confirm", f"Delete semester '{self.semesters[index]['name']}'?"):
            self.semesters.pop(index)
            self.calculate_gpa()
            self.save_data()
            window.destroy()
            messagebox.showinfo("Success", "Semester deleted")
    
    def export_report(self):
        """Export GPA report to text file"""
        if not self.current_semester_courses and not self.semesters:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write("=" * 50 + "\n")
                    f.write("GPA REPORT\n")
                    f.write("=" * 50 + "\n\n")
                    
                    # Cumulative stats
                    all_courses = []
                    for semester in self.semesters:
                        all_courses.extend(semester['courses'])
                    all_courses.extend(self.current_semester_courses)
                    
                    if all_courses:
                        cumulative_points = sum(c['credits'] * c['points'] for c in all_courses)
                        cumulative_credits = sum(c['credits'] for c in all_courses)
                        cumulative_gpa = cumulative_points / cumulative_credits
                        
                        f.write(f"Cumulative GPA: {cumulative_gpa:.2f}\n")
                        f.write(f"Total Credits: {int(cumulative_credits)}\n\n")
                    
                    # Semesters
                    for semester in self.semesters:
                        f.write("-" * 50 + "\n")
                        f.write(f"Semester: {semester['name']}\n")
                        f.write("-" * 50 + "\n")
                        
                        total_points = sum(c['credits'] * c['points'] for c in semester['courses'])
                        total_credits = sum(c['credits'] for c in semester['courses'])
                        semester_gpa = total_points / total_credits
                        
                        f.write(f"Semester GPA: {semester_gpa:.2f}\n")
                        f.write(f"Credits: {int(total_credits)}\n\n")
                        
                        for course in semester['courses']:
                            f.write(f"  {course['name']}\n")
                            f.write(f"    Credits: {course['credits']}, Grade: {course['grade']}, Points: {course['points']}\n")
                        f.write("\n")
                    
                    # Current semester
                    if self.current_semester_courses:
                        f.write("-" * 50 + "\n")
                        f.write("Current Semester (Unsaved)\n")
                        f.write("-" * 50 + "\n")
                        
                        total_points = sum(c['credits'] * c['points'] for c in self.current_semester_courses)
                        total_credits = sum(c['credits'] for c in self.current_semester_courses)
                        semester_gpa = total_points / total_credits
                        
                        f.write(f"Semester GPA: {semester_gpa:.2f}\n")
                        f.write(f"Credits: {int(total_credits)}\n\n")
                        
                        for course in self.current_semester_courses:
                            f.write(f"  {course['name']}\n")
                            f.write(f"    Credits: {course['credits']}, Grade: {course['grade']}, Points: {course['points']}\n")
                
                messagebox.showinfo("Success", f"Report exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {str(e)}")
    
    def save_data(self):
        """Save data to JSON file"""
        data = {
            'semesters': self.semesters,
            'current_courses': self.current_semester_courses
        }
        try:
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.semesters = data.get('semesters', [])
                    self.current_semester_courses = data.get('current_courses', [])
                    self.update_course_list()
                    self.calculate_gpa()
            except Exception as e:
                print(f"Error loading data: {e}")
