"""GUI for the BIPY using Flexx module to make it platform independent

Author: Ajeet Singh
Date: 06/22/2019
"""
from flexx import flx, ui


class MainWindow(flx.Widget):
    """The main window class for the application. It will define the
    init layout for the whole GUI system
    """

    def init(self):
        with flx.VSplit():
            with ui.TabLayout() as self.t:
                self.home_tab = ui.Widget(title="Home")
                self.edit_tab = ui.Widget(title="Edit")
                self.project_tab = ui.Widget(title="Project")
                self.wh_browser_tab = ui.Widget(title="Warehouse Browser")
                self.repository_tab = ui.Widget(title="Repository")
                self.analysis_tab = ui.Widget(title="Analysis")
                self.help_tab = ui.Widget(title="Help")
            flx.Widget(style='background:blue', flex=8)


if __name__ == "__main__":
    app = flx.App(MainWindow)
    app.launch('app')
    flx.run()
