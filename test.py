import json
import sys
with open("tasks.json", 'r') as f:
    data = json.load(f)
    


print(type(str(sys.argv[1].lower())))