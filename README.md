# 🧮 Scientific & GPA Calculator

A beautiful, full-featured dual-purpose calculator application built with Python and CustomTkinter. Features both a comprehensive scientific calculator with advanced mathematical functions and a GPA calculator with semester management.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔬 Scientific Calculator

- **Basic Operations**: Addition, subtraction, multiplication, division
- **Scientific Functions**:
  - Trigonometric: sin, cos, tan (with degree/radian mode)
  - Logarithmic: log, ln, log₂
  - Power functions: x², x³, xʸ, √x, ∛x
  - Exponentials: 10ˣ, 2ˣ
  - Special: factorial, absolute value, modulo, reciprocal
- **Mathematical Constants**: π (pi), e
- **Memory Functions**: MC, MR, M+, M-, MS
- **Advanced Features**:
  - Parentheses support for complex expressions
  - Calculation history display
  - Keyboard input support
  - Backspace for editing
  - Clear (C) and All Clear (AC) functions
- **Beautiful UI**: Color-coded buttons with smooth hover effects

### 📊 GPA Calculator

- **Course Management**:
  - Add courses with name, credit hours, and grade
  - Edit and delete courses
  - Scrollable course list display
- **GPA Calculations**:
  - Current semester GPA
  - Cumulative GPA across all semesters
  - Weighted by credit hours
  - Standard 4.0 scale (A=4.0, A-=3.7, B+=3.3, etc.)
- **Semester Features**:
  - Save multiple semesters
  - View semester history
  - Delete old semesters
  - Semester-by-semester breakdown
- **Data Persistence**:
  - Automatic save/load of GPA data
  - Export reports as text files
- **Visual Feedback**:
  - Color-coded GPA display (green for high, red for low)
  - Clean, organized table layout

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Clone or download this repository**

   ```bash
   cd calculator
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python calculator_app.py
   ```

## 📖 Usage

### Scientific Calculator

#### Mouse/Touch Input

- Click any button to perform operations
- Use the number pad for digits
- Click operators (+, -, ×, ÷) for basic math
- Use scientific function buttons for advanced calculations
- Toggle between Degrees and Radians for trigonometric functions

#### Keyboard Shortcuts

- **Numbers**: 0-9
- **Operations**: +, -, \*, /
- **Decimal**: .
- **Calculate**: Enter or =
- **Backspace**: Delete last character
- **Escape**: All Clear (AC)

#### Memory Functions

- **MC**: Clear memory
- **MR**: Recall memory value
- **M+**: Add current value to memory
- **M-**: Subtract current value from memory
- **MS**: Store current value in memory

### GPA Calculator

1. **Add Courses**:
   - Enter course name
   - Enter credit hours (e.g., 3)
   - Select grade from dropdown
   - Click "Add Course"

2. **Manage Courses**:
   - View all courses in the scrollable list
   - Click ✕ to delete a course
   - Current semester GPA updates automatically

3. **Save Semester**:
   - Click "Save Semester"
   - Enter semester name (e.g., "Fall 2024")
   - Courses are saved to history

4. **View History**:
   - Click "View History" to see all saved semesters
   - View GPA and courses for each semester
   - Delete old semesters if needed

5. **Export Report**:
   - Click "Export Report"
   - Choose location to save
   - Get a detailed text file with all GPA data

## 🎨 UI Design

The application features a modern, dark-themed interface with:

- **Color Scheme**:
  - Deep blues and purples for a professional look
  - Color-coded buttons (operators in blue, numbers in gray, functions in purple)
  - GPA color coding (green for high grades, red for low)
- **Smooth Animations**: Hover effects on all buttons
- **Responsive Layout**: Adapts to different window sizes
- **Clear Typography**: Large, readable fonts
- **Intuitive Organization**: Tabbed interface for easy navigation

## 📊 Grade Scale

The GPA calculator uses the standard 4.0 scale:

| Grade | Points |
| ----- | ------ |
| A     | 4.0    |
| A-    | 3.7    |
| B+    | 3.3    |
| B     | 3.0    |
| B-    | 2.7    |
| C+    | 2.3    |
| C     | 2.0    |
| C-    | 1.7    |
| D+    | 1.3    |
| D     | 1.0    |
| F     | 0.0    |

## 💾 Data Storage

- GPA data is automatically saved to `gpa_data.json` in the application directory
- Data persists between sessions
- You can manually backup this file to preserve your GPA history

## 🛠️ Technical Details

- **Framework**: CustomTkinter (modern UI framework based on Tkinter)
- **Language**: Python 3.8+
- **Dependencies**:
  - customtkinter >= 5.2.0
  - Pillow >= 10.0.0
- **Architecture**: Modular design with separate calculator components

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!

## 📝 License

This project is open source and available under the MIT License.

## 🎯 Future Enhancements

Potential features for future versions:

- Graph plotting for functions
- Unit conversions
- Statistical calculations
- Support for different GPA scales
- Data visualization charts
- Cloud sync for GPA data
- Mobile app version

## 👨‍💻 Author

Built with ❤️ using Python and CustomTkinter

---

**Enjoy calculating! 🧮📊**
