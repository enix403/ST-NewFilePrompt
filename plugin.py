import os
import sublime
import sublime_plugin

from . import bracex
 
def reveal_in_sidebar(self):
    self.window.run_command("reveal_in_side_bar")

class MakeNewFileCommand(sublime_plugin.WindowCommand):
    def on_path_entered(self, location_str):

        locations_str = location_str.rstrip("/")
        locations = bracex.expand(location_str)

        for location in locations:
            if os.path.exists(location):
                sublime.error_message("NewFilePrompt: Path already exists")
                return

            base, _ = os.path.split(location)
            if not os.path.exists(base):
                os.makedirs(base)
            

        for location in locations:
            # create the file
            open(location, "a").close()

        self.window.run_command('hide_panel')
        self.window.open_file(locations[0])
        sublime.set_timeout_async(lambda: reveal_in_sidebar(self), 250)

    def run(self, dirs):
        self.window.show_input_panel("File Location:", dirs[0] + "/", self.on_path_entered, None, None)


class MakeNewFolderCommand(sublime_plugin.WindowCommand):
    def on_path_entered(self, location_str):
        locations = bracex.expand(location_str)

        for location in locations:
            if os.path.exists(location):
                sublime.error_message("NewFilePrompt: Path already exists")
                return

        for location in locations:
            # create the folder
            os.makedirs(location)

        self.window.run_command('hide_panel')

    def run(self, dirs):
        self.window.show_input_panel("Folder Location:", dirs[0] + "/", self.on_path_entered, None, None)
