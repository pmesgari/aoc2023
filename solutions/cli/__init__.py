import sys
import os

args = sys.argv

def set_filepath():
    if len(args) < 2:
        print("Missing filename argument.")
        sys.exit(1)
    
    
    day = ''.join([c for c in args[0][args[0].find('day'):] if c.isdigit()])
    filename = args[1]

    cli_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(cli_dir)

    filepath = os.path.join(base_dir, f'inputs/day{day}/{filename}.txt')
    if os.path.exists(filepath):
        return filepath
    else:
        print("Input file missing.")
        sys.exit(1)

filepath = set_filepath()
