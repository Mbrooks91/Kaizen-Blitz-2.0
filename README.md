# Kaizen Blitz - Project Management Application

A comprehensive desktop application for managing Kaizen Blitz (rapid improvement) projects using Python and PyQt6.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)

## Features

✨ **Complete Project Management**
- Create and manage multiple Kaizen Blitz projects
- Track project progress and status
- Organize projects by phase (Preparation, Analysis, Improvement, Implementation, Review)

🔍 **Analysis Tools**
- **5 Whys Analysis**: Root cause analysis with unlimited whys
- **Ishikawa (Fishbone) Diagrams**: Categorize causes across 6 categories
- **Action Plans**: Create and track improvement tasks with deadlines and priorities

📊 **Professional Exports**
- PDF reports with comprehensive project summaries
- Editable Word documents
- Excel spreadsheets for action plans
- Email integration for sharing

🎨 **Modern UI**
- Clean, professional interface
- Responsive layouts
- Real-time search and filtering
- Progress tracking and visualization

## Technology Stack

- **Python 3.10+**: Core programming language
- **PyQt6**: Modern desktop GUI framework
- **SQLAlchemy 2.0**: ORM for database management
- **SQLite**: Embedded database
- **ReportLab**: PDF generation
- **python-docx**: Word document creation
- **openpyxl**: Excel file generation
- **matplotlib/seaborn**: Data visualization

## Installation

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)

### Steps

1. **Clone the repository**
   ```bash
   cd /workspaces/Kaizen-Blitz-2.0
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\\Scripts\\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment** (optional)
   ```bash
   cp .env.example .env
   # Edit .env with your preferences
   ```

## Usage

### Running the Application

```bash
python run.py
```

### Quick Start

1. **Create a New Project**
   - Click "+ New Project" button
   - Follow the 5-step wizard
   - Enter project details, team members, and initial phase

2. **Select a Project**
   - Browse projects on the dashboard
   - Use search and filters to find projects
   - Click on a project card to open it

3. **Use Analysis Tools**
   - Navigate using the sidebar
   - **5 Whys**: Identify root causes
   - **Ishikawa**: Categorize contributing factors
   - **Action Plan**: Create improvement tasks

4. **Export Your Work**
   - File → Export to PDF (comprehensive report)
   - File → Export to Word (editable document)
   - Tools → Export to Excel (action plans)

## Project Structure

```
kaizen-blitz-python/
├── src/
│   └── kaizen_blitz/
│       ├── config/          # Configuration and settings
│       ├── models/          # Database models
│       ├── database/        # Repository pattern
│       ├── services/        # Export services (PDF, Word, Excel)
│       ├── ui/              # PyQt6 user interface
│       │   ├── styles/      # UI styling
│       │   ├── widgets/     # Custom widgets
│       │   └── views/       # Application views
│       └── utils/           # Utility functions
├── tests/                   # Unit tests
├── docs/                    # Documentation
└── requirements.txt         # Python dependencies
```

## Features in Detail

### Project Management
- Multi-project workspace
- Status tracking (In Progress, Completed, On Hold, Cancelled)
- Phase management (5 Kaizen phases)
- Team member assignment
- Progress calculation

### 5 Whys Analysis
- Problem statement definition
- Up to 5+ whys (expandable)
- Root cause identification
- PDF export
- Completion tracking

### Ishikawa Diagram
- 6 standard categories (People, Process, Materials, Equipment, Environment, Management)
- Multiple causes per category
- Visual organization
- PDF export support

### Action Plans
- Task management with deadlines
- Priority levels (Low, Medium, High, Critical)
- Status tracking (Not Started, In Progress, Completed, Blocked)
- Responsible person assignment
- Excel export
- Progress visualization

## Configuration

Edit the `.env` file to customize:

```env
DATABASE_URL=sqlite:///kaizen_blitz.db
EXPORT_PATH=~/Documents/KaizenBlitz/Exports
COMPANY_NAME=Your Company
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

This project follows PEP 8 guidelines with:
- Type hints for all function parameters
- Docstrings for classes and methods
- Consistent naming conventions

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the [User Guide](docs/USER_GUIDE.md)
- Contact: info@yourcompany.com

## Acknowledgments

- Kaizen methodology principles
- PyQt6 framework
- SQLAlchemy ORM
- All open-source contributors

---

**Version**: 1.0.0  
**Author**: Your Company  
**Year**: 2026
