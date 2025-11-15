import argparse
from datetime import datetime

def parse_args():
    """
    Parse command line arguments
    
    Returns:
        Parsed arguments with extra unknown args as args.extra dictionary
    """
    parser = argparse.ArgumentParser(description='SageMaker AI Framework')
    parser.add_argument('--config', type=str, default='conf/job.conf',
                        help='Path to config file')
    parser.add_argument('--env', type=str, default='dev',
                        help='Environment (ut, uat, prod, dev)')
    parser.add_argument('--date', type=str, default=datetime.now().strftime('%Y-%m-%d'),
                        help='Execution date (YYYY-MM-DD)')
    parser.add_argument('--model_source', type=str, default='Azure',
                        help='Using Guardrail or Azure')
    
    
    # Parse all arguments including unknown ones
    args, unknown = parser.parse_known_args()
    
    # Convert unknown args to a dictionary for easy access
    extra_args = {}
    i = 0
    while i < len(unknown):
        if unknown[i].startswith('--'):
            param = unknown[i][2:]
            if i + 1 < len(unknown) and not unknown[i+1].startswith('--'):
                extra_args[param] = unknown[i+1]
                i += 2
            else:
                extra_args[param] = True
                i += 1
        else:
            i += 1
    
    args.extra = extra_args
    return args