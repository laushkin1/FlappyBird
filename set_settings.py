import sys

if len(sys.argv) > 1:
    try:
        new_scale = int(sys.argv[1])
        with open("settings.py", "r") as f:
            lines = f.readlines()

        with open("settings.py", "w") as f:
            for line in lines:
                if line.startswith("SCALE ="):
                    f.write(f"SCALE = {new_scale}\n")
                else:
                    f.write(line)

    except ValueError:
        print("Ошибка: SCALE должен быть целым числом")
        sys.exit(1)


