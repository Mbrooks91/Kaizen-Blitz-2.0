# Kaizen Blitz - User Guide

Complete guide for using the Kaizen Blitz project management application.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Creating a Project](#creating-a-project)
3. [Using the 5 Whys Tool](#using-the-5-whys-tool)
4. [Creating Ishikawa Diagrams](#creating-ishikawa-diagrams)
5. [Managing Action Plans](#managing-action-plans)
6. [Exporting and Sharing](#exporting-and-sharing)
7. [Keyboard Shortcuts](#keyboard-shortcuts)
8. [Troubleshooting](#troubleshooting)

---

## Getting Started

### First Launch

When you first launch Kaizen Blitz, you'll see:
- **Dashboard**: Overview of all your projects
- **Sidebar**: Navigation menu on the left
- **Toolbar**: Quick access to common actions
- **Menu Bar**: Full application menu

### Interface Overview

**Sidebar Navigation:**
- Dashboard - View all projects
- New Project - Create a new project
- 5 Whys - Root cause analysis
- Ishikawa Diagram - Fishbone analysis
- Action Plan - Task management

**Color Coding:**
- 🔵 Blue - Primary actions
- 🟢 Green - Success/Complete
- 🟠 Orange - Warning/On Hold
- 🔴 Red - Error/Cancelled

---

## Creating a Project

### Step-by-Step Guide

1. **Click "+ New Project"** (Dashboard or Sidebar)

2. **Step 1: Basic Information**
   - Enter project name (required)
   - Add a description
   - Click "Next"

3. **Step 2: Project Details**
   - Specify target area (e.g., "Assembly Line A")
   - Set start date
   - Set expected completion date
   - Click "Next"

4. **Step 3: Team Members**
   - Enter team member names (one per line)
   - Example:
     ```
     John Smith
     Sarah Johnson
     Michael Chen
     ```
   - Click "Next"

5. **Step 4: Initial Phase**
   - Select starting phase:
     - Preparation
     - Analysis
     - Improvement
     - Implementation
     - Review
   - Click "Next"

6. **Step 5: Review & Confirm**
   - Review all entered information
   - Click "Finish" to create the project
   - Click "Previous" to make changes
   - Click "Cancel" to abort

### Tips
- Use descriptive project names
- Include measurable goals in descriptions
- Start in "Preparation" phase for new projects

---

## Using the 5 Whys Tool

### Purpose
Identify the root cause of a problem by asking "why" repeatedly.

### How to Use

1. **Select a Project** from the dashboard

2. **Navigate to 5 Whys** (Sidebar or Menu → Tools → 5 Whys)

3. **Enter Problem Statement**
   - Describe the problem clearly
   - Be specific and measurable
   - Example: "Production output decreased by 20%"

4. **Complete the 5 Whys**
   - Why 1: Answer why the problem occurred
   - Why 2: Ask why that answer is true
   - Why 3: Continue drilling down
   - Why 4: Keep asking why
   - Why 5: Usually reveals root cause

5. **Add More Whys** (Optional)
   - Click "+ Add Another Why" if needed
   - Sometimes requires 6, 7, or more whys

6. **Identify Root Cause**
   - Enter the ultimate root cause
   - This should be actionable
   - Example: "No preventive maintenance schedule exists"

7. **Save Your Work**
   - Click "Save" button
   - Analysis is saved to the project

8. **Mark as Complete**
   - Click "Mark as Complete" when done
   - Contributes to project progress

9. **Export to PDF**
   - Click "Export to PDF"
   - Choose save location
   - Share with stakeholders

### Best Practices
- Focus on processes, not people
- Use facts, not opinions
- Stop when you reach an actionable root cause
- Verify the root cause with data

---

## Creating Ishikawa Diagrams

### Purpose
Categorize potential causes of a problem using the fishbone structure.

### The 6 Categories

1. **People** - Human factors
2. **Process** - Procedures and methods
3. **Materials** - Raw materials and supplies
4. **Equipment** - Machines and tools
5. **Environment** - Work conditions
6. **Management** - Policies and leadership

### How to Use

1. **Select a Project** from the dashboard

2. **Navigate to Ishikawa** (Sidebar or Menu → Tools → Ishikawa Diagram)

3. **Enter Problem Statement**
   - Describe the effect/problem
   - Example: "High defect rate in final products"

4. **Add Causes to Each Category**
   - Click on each tab (People, Process, etc.)
   - Enter a cause in the text field
   - Click "Add Cause"
   - Repeat for all relevant causes

5. **Example Causes**

   **People:**
   - Insufficient training
   - High turnover rate
   - Lack of experience

   **Process:**
   - Unclear procedures
   - No quality checks
   - Rushed production

   **Materials:**
   - Poor quality raw materials
   - Inconsistent suppliers
   - Incorrect specifications

   **Equipment:**
   - Outdated machinery
   - Lack of maintenance
   - Calibration issues

   **Environment:**
   - Temperature fluctuations
   - Poor lighting
   - Noise distractions

   **Management:**
   - No quality goals
   - Insufficient resources
   - Lack of accountability

6. **Remove Causes**
   - Select a cause from the list
   - Click "Remove Selected"

7. **Save Your Work**
   - Click "Save" button

8. **Mark as Complete**
   - Click "Mark as Complete"

9. **Export**
   - Use File → Export to include in project PDF

### Tips
- Brainstorm with your team
- Don't filter ideas initially
- Group similar causes
- Prioritize causes for action

---

## Managing Action Plans

### Purpose
Create concrete action items with deadlines, responsibilities, and priorities.

### How to Use

1. **Select a Project** from the dashboard

2. **Navigate to Action Plan** (Sidebar or Menu → Tools → Action Plan)

3. **Add Tasks**
   - Click "+ Add Task"
   - A new row appears in the table

4. **Fill in Task Details**

   **Task Description:**
   - What needs to be done
   - Be specific and actionable
   - Example: "Implement weekly maintenance schedule"

   **Responsible Person:**
   - Who will do it
   - Enter name or role

   **Deadline:**
   - Click the date field
   - Select target completion date

   **Status:**
   - Not Started (default)
   - In Progress
   - Completed
   - Blocked

   **Priority:**
   - Low
   - Medium
   - High
   - Critical

   **Notes:**
   - Additional information
   - Dependencies
   - Resources needed

5. **Delete Tasks**
   - Click "Delete" button in the Actions column
   - Confirm deletion

6. **Filter Tasks**
   - Use the Filter dropdown
   - Show only: All, Not Started, In Progress, Completed, Blocked

7. **Track Progress**
   - Progress bar shows % of completed tasks
   - Updates automatically

8. **Save Your Work**
   - Click "Save" button
   - All tasks are saved

9. **Export to Excel**
   - Click "Export to Excel"
   - Choose save location
   - Opens in spreadsheet software

10. **Mark as Complete**
    - Click "Mark as Complete"
    - Locks the action plan

### Best Practices
- Set realistic deadlines
- Assign clear ownership
- Update status regularly
- Use priority levels effectively
- Review and adjust weekly

---

## Exporting and Sharing

### Export Options

#### 1. Project Summary PDF
**What it includes:**
- Cover page
- Project overview
- All completed 5 Whys analyses
- All completed Ishikawa diagrams
- All completed action plans

**How to export:**
- File → Export to PDF
- Choose save location
- Professional report ready to share

#### 2. Word Document
**What it includes:**
- Same content as PDF
- Fully editable format

**How to export:**
- File → Export to Word
- Choose save location
- Edit and customize as needed

#### 3. Excel Spreadsheet (Action Plans)
**What it includes:**
- Task table with all details
- Summary statistics
- Completion tracking

**How to export:**
- Open Action Plan view
- Click "Export to Excel"
- Choose save location

#### 4. Individual Tool PDFs
**How to export:**
- Open specific tool (5 Whys, etc.)
- Click "Export to PDF"
- Standalone report for that tool

### Sharing Reports

**Email:**
- Export to PDF
- Attach to email
- Share with stakeholders

**Print:**
- Open PDF
- Print from PDF viewer
- Distribute hard copies

**Cloud Storage:**
- Save exports to cloud folders
- Share links with team

---

## Keyboard Shortcuts

### Global Shortcuts
- `Ctrl+N` - New Project
- `Ctrl+S` - Save Current View
- `Ctrl+Q` - Quit Application

### Navigation
- Use sidebar to switch between views
- Click project cards to open projects

### Tips
- Most actions have button alternatives
- Tooltips appear on hover

---

## Troubleshooting

### Application Won't Start

**Problem:** Error on launch

**Solutions:**
1. Check Python version (3.10+)
   ```bash
   python --version
   ```

2. Reinstall dependencies
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```

3. Check for error messages in terminal

### Database Errors

**Problem:** "Database locked" or connection errors

**Solutions:**
1. Close all instances of the application
2. Check file permissions on database file
3. Delete `kaizen_blitz.db` to start fresh (loses data)

### Export Failures

**Problem:** PDF/Word/Excel export fails

**Solutions:**
1. Check export path exists and is writable
2. Ensure sufficient disk space
3. Close any open exported files
4. Check permissions on export directory

### Missing Data

**Problem:** Projects or data disappeared

**Solutions:**
1. Check database file location
2. Verify you're not running multiple instances
3. Look for `.db` backup files
4. Check filters on dashboard (may be hiding projects)

### Performance Issues

**Problem:** Application is slow

**Solutions:**
1. Close other applications
2. Reduce number of projects displayed
3. Clear old completed projects
4. Check system resources (RAM, CPU)

### UI Display Problems

**Problem:** UI elements misaligned or missing

**Solutions:**
1. Restart application
2. Update PyQt6
   ```bash
   pip install --upgrade PyQt6
   ```
3. Check screen resolution and scaling

---

## Getting Help

### Resources
- **README.md** - Installation and setup
- **This Guide** - Detailed usage instructions
- **GitHub Issues** - Report bugs
- **Email Support** - info@yourcompany.com

### Tips for Better Support
- Describe the problem clearly
- Include error messages
- Note steps to reproduce
- Mention your operating system

---

## Appendix: Kaizen Methodology

### What is Kaizen?
- Japanese philosophy of continuous improvement
- Small, incremental changes
- Involve everyone
- Focus on processes

### Kaizen Blitz
- Rapid improvement event
- Usually 3-5 days
- Focused team effort
- Immediate results

### The 5 Phases

1. **Preparation**
   - Define scope
   - Assemble team
   - Gather data

2. **Analysis**
   - Identify problems
   - Use 5 Whys
   - Create Ishikawa diagrams

3. **Improvement**
   - Brainstorm solutions
   - Prioritize actions
   - Plan implementation

4. **Implementation**
   - Execute action plan
   - Track progress
   - Adjust as needed

5. **Review**
   - Measure results
   - Document learnings
   - Standardize improvements

---

**Version:** 1.0.0  
**Last Updated:** January 2026

For questions or feedback, please contact support.
