from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
    "excludes": ["tkinter", "unittest"],
    "packages": ['cv2','numpy','autopy','handtracking','time','pyautogui','presentation','keyboard','os','comtypes.client'],
    "zip_include_packages": ["encodings", "PySide6", "shiboken6"],
}

setup(
    name="Gesture Control System",
    version="0.1",
    description="Cusrsor Control using Hand gestures",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base="gui", icon="icon.ico")],
)