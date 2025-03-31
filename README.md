# CrypTomorrow

## Setup Instructions

### Prerequisites
- Python 3.12.9 (exact version required)
- pip (Python package installer)

### Installing Python 3.12.9

1. **macOS (using Homebrew)**:
```bash
# Install Python 3.12
brew install python@3.12

# Verify the installed version
python3.12 --version


# Or alternatively, you can download directly from Python's website:
# Visit https://www.python.org/downloads/release/python-3129/
# Download and install the macOS installer
```

2. **Windows**:
   - Download Python 3.12.9 installer from [Python's official website](https://www.python.org/downloads/release/python-3129/)
   - Run the installer and make sure to check "Add Python to PATH"

3. **Linux (Ubuntu/Debian)**:
```bash
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.12
```

4. **Verify Installation**:
```bash
python3.12 --version
# Should output: Python 3.12.9
```

### Setting up the Virtual Environment

1. Clone the repository:
```bash
git clone <your-repository-url>
cd CrypTomorrow
```

2. Create a virtual environment with Python 3.12.9:
```bash
# On macOS/Linux
python3.12 -m venv venv

# On Windows
python -m venv venv
```

3. Activate the virtual environment:
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
.\venv\Scripts\activate
```

4. Verify Python version in virtual environment:
```bash
python --version
# Should output: Python 3.12.9
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

### Development Workflow

1. Always activate the virtual environment before working on the project:
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
.\venv\Scripts\activate
```

2. When you're done working:
```bash
deactivate
```

### Adding New Dependencies

If you add new packages to the project:

1. Install the new package:
```bash
pip install <package-name>
```

2. Update requirements.txt:
```bash
pip freeze > requirements.txt
```

3. Commit the updated requirements.txt to the repository.

### Troubleshooting

If you encounter any issues:

1. Make sure you're using Python 3.12.9 (exact version required)
2. Try deleting the venv directory and recreating it
3. Ensure all dependencies are installed correctly
4. Check if you're in the correct directory when running commands