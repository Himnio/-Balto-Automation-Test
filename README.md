## Prerequisites

- Python 3.8+
- pip (Python package installer)

## Installation

1. **Create and activate a virtual environment** (recommended):
   ```bash
   # Create a virtual environment
   python -m venv venv or use python3 -m venv venv
   
   # Activate the virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   # .\venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the development server**:
   ```bash
   python3 paint_calculator/run.py
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:9200
   ```

## Running Tests

1. **Unit Tests**:
   ```bash
   pytest tests/unit/
   ```

2. **End-to-End Tests**:
   ```bash
   pytest tests/e2e/
   ```

## Common Issues and Solutions

### 1. Secret Key Error
**Error**: `RuntimeError: The session is unavailable because no secret key was set`

**Solution**:
- Create a `.env` file in the project root
- Add `FLASK_SECRET_KEY=your-secret-key-here`
- Make sure `python-dotenv` is installed and properly loading the environment variables

### 2. Home Button Not Redirecting
**Issue**: The home button on the results page wasn't working due to incorrect form method.

**Solution**:
- Changed form method from `post` to `get` in `results.html`

### 3. Dependency Issues
If you encounter dependency conflicts:
1. Make sure you're using a virtual environment
2. Try updating pip: `pip install --upgrade pip`
3. Reinstall requirements: `pip install -r requirements.txt --force-reinstall`

### 4. CSRF Issues 
solution - For testing csrf issues is to disable it in the config file

## Project Structure

```
Balto-automation-test/
├── paint_calculator/
│   ├── __init__.py
│   ├── run.py          # Main application file
│   ├── api.py          # API endpoints and calculations
│   └── config.py       # Configuration settings
├── tests/
│   ├── unit/           # Unit tests
│   └── e2e/            # End-to-end tests
├── templates/          # HTML templates
├── .env.example       # Example environment variables
├── requirements.txt   # Project dependencies
└── README.md          # This file
```