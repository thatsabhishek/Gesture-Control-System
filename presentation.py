import os
import comtypes.client
import time

class PresentationControl:
    def __init__(self):
        self.ppt_app = comtypes.client.CreateObject("PowerPoint.Application")
        self.presentation = None

    def start_presentation(self):
        # Search for files with the .pptx extension in the current directory
        files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.pptx')]

        # If there are .pptx files, open the first one found
        if files:
            file_to_open = os.path.abspath(files[0])  # Get the absolute path
            print(f"Opening presentation file: {file_to_open}")
            self.presentation = self.ppt_app.Presentations.Open(file_to_open)
            self.ppt_app.Visible = True
            self.presentation.SlideShowSettings.Run()
        else:
            print("No presentation file (.pptx) found in the directory.")

    def stop_presentation(self):
        if self.presentation:
            self.presentation.SlideShowWindow.View.Exit()
            self.presentation.Close()
            self.ppt_app.Quit()
        print("Exiting presentation mode.")

    def next_slide(self):
        if self.presentation:
            self.presentation.SlideShowWindow.View.Next()
            time.sleep(0.20)

    def previous_slide(self):
        if self.presentation:
            time.sleep(0.20)
            self.presentation.SlideShowWindow.View.Previous()

# Instantiate the control
presentation_control = PresentationControl()
