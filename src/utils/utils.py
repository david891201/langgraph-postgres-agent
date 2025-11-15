import os
import configparser
import logging
from typing import Dict, Any

def load_config(config_path: str, env: str) -> Dict[str, Any]:
    """
    Load configuration from .conf file for the specified environment
    """
    config = {}
    try:
        parser = configparser.ConfigParser()
        parser.read(config_path)
        
        if env in parser.sections():
            for key, value in parser.items(env):
                try:
                    if value.isdigit():
                        config[key] = int(value)
                    elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
                        config[key] = float(value)
                    elif value.lower() == 'true':
                        config[key] = True
                    elif value.lower() == 'false':
                        config[key] = False
                    else:
                        config[key] = value
                except ValueError:
                    config[key] = value
        else:
            print(f"Environment section '{env}' not found in config file")
        
        return config
    except FileNotFoundError:
        print(f"Config file not found: {config_path}")
        return {}
    except Exception as e:
        print(f"Error parsing config file: {e}")
        return {}
    
    
def setup_logger(log_file: str = None):
    """
    Set up logging system
    """
    # Configure root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Clear existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)
    
    # Add file handler (if provided)
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
    
    return logger