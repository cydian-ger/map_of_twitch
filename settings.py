import yaml

YAML = None
try:
    with open("settings.yaml", "r") as settings:
        YAML = yaml.load(settings, Loader=yaml.FullLoader)
except FileNotFoundError or OSError or IOError:
    raise IOError("settings.yaml is missing")

if YAML is None:
    raise IOError("couldn't open settings.yaml")

if YAML.__contains__("Timeout_Time"):
    try:
        Timeout_Time = int(YAML.get("Timeout_Time"))
    except ValueError:
        raise TypeError("Timeout time must be INT type")
else:
    raise ImportError("Field 'Timeout_Time' not provided")

if YAML.__contains__("Max_Workers"):
    try:
        Max_Workers = int(YAML.get("Max_Workers"))
    except ValueError:
        raise TypeError("Max workers must be INT type")
else:
    raise ImportError("Field 'Max_Workers' not provided")

if YAML.__contains__("Overlap_Multiplier"):
    try:
        Overlap_Multiplier = float(YAML.get("Overlap_Multiplier"))
    except ValueError:
        raise TypeError("Overlap multiplier must be float")
else:
    raise ImportError("Field 'Overlap_Multiplier' not provided")

if YAML.__contains__("Viewer_Dir"):
    try:
        Viewer_Dir = str(YAML.get("Viewer_Dir"))
    except ValueError:
        raise TypeError("Viewer Dir must be str")
else:
    raise ImportError("Field 'Viewer_Dir' not provided")

if YAML.__contains__("Set_Size"):
    try:
        Set_Size = int(YAML.get("Set_Size"))
        if Set_Size < 1:
            raise IndexError("Set size can not be below 1")
    except ValueError:
        raise TypeError("Set size must be int")
else:
    raise ImportError("Field 'Set_Size' not provided")

if YAML.__contains__("Streamer_List"):
    try:
        Streamer_List = str(YAML.get("Streamer_List"))
    except ValueError:
        raise TypeError("Streamer List must be str")
else:
    raise ImportError("Field 'Streamer_List' not provided")
