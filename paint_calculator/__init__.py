import os
from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# Load the config file - handle both direct run and pytest scenarios
try:
    # First try importing config as a module (works when run from project root)
    app.config.from_object('config')
except (ImportError, ModuleNotFoundError):
    # If that fails, try loading from file path (works in all scenarios)
    # Get the project root directory (parent of paint_calculator)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(project_root, 'config.py')
    
    if os.path.exists(config_path):
        app.config.from_pyfile(config_path)
    else:
        # Fallback to default config if config.py not found
        app.config['DEBUG'] = True
