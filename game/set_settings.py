import sys
import os

if len(sys.argv) > 1:
    try:
        new_scale = int(sys.argv[1])
        settings_path = os.path.join(os.path.dirname(__file__), "settings.py")
        with open(settings_path, "r") as f:
            lines = f.readlines()

        with open(settings_path, "w") as f:
            for line in lines:
                if line.startswith("SCALE ="):
                    f.write(f"SCALE = {new_scale}\n")
                else:
                    f.write(line)

    except ValueError:
        print("Error: SCALE must be an integer.")
        sys.exit(1)
