import json

from app.browser import DirectoryBrowser
from app.graphs.graph_factory import SimplePlotGraph, PlotDataNormalizer
from app.loaders.get_loader import load_data
from app.clients.CLI import CLI
from app.plugins import plugins, PluginManager
from app.utils.plot_builder import build_plot
from app.plugins.plugins import DialogsCreated, SuccessRechargePlugin, RechargedAmountPlugin, ChannelEffectiveness


def open_file():
    with open('data_example.txt', 'r') as f:
        return json.load(f)


def analyze_new_data_piece(data: dict) -> dict[dict]:
    manager = PluginManager(plugins=plugins)
    return manager.analyse_data(data)


class AnalyzerApp:
    def __init__(self, prepared_data: dict, client: CLI):
        self.current_day: str = ''
        self.analysis_results = prepared_data
        self.client = client

    def run_main_menu(self):
        submenus = {
            'Show basic daily info': self.display_basic_daily_info,
            'All analysis tools': self.run_analysis_menu,
            'Load more data from API': self.run_loader_menu,
            'Load previously saved file': self.run_browser_menu,
            'Save current data to file': self.save_data_to_file,
            'Build Graph': self.build_graph,
            'Exit': self.exit_app
        }

        self.client.render_message("Welcome to CLI interface!")

        while True:
            command = self.client.display_main_menu([key for key in submenus.keys()])
            if not command:
                self.client.render_message("I do not have such command!")
                continue
            submenus[command]()

    def run_analysis_menu(self):
        while True:
            analysis_to_show = self.client.display_analyzer_menu(
                [analyzer['desc'] for analyzer in self.analysis_results.values()],
                [analyzer for analyzer in self.analysis_results]
            )

            if not analysis_to_show:
                break

            self.client.render_divider()
            self.analysis_results[analysis_to_show]['func'](self.analysis_results[analysis_to_show]['args'])
            self.client.render_divider()

    def run_loader_menu(self):
        day_to_load = input("Enter day to load\nShould be weekday capitalized: ")
        success = self.load_from_source(day_to_load)
        if success:
            self.current_day = day_to_load

    def run_browser_menu(self):
        browser = DirectoryBrowser()
        saved_files_list = browser.get_saved_files_list()
        # print(saved_files_list)
        file_to_load = self.client.display_choose_file_menu(saved_files_list)
        if not file_to_load:
            return None
        self.load_from_source(file_to_load)

    def load_from_source(self, file: str, with_save: bool = False) -> bool:
        print(f"Starting loading process for source: {file}")
        if with_save:
            print(f"Plan to save loaded data to file")
            new_data = load_data(file, with_save=True)
        else:
            new_data = load_data(file)
            if not new_data['started']:
                self.client.render_message("Could not fetch data!")
                return False

        self.analysis_results = analyze_new_data_piece(new_data)
        return True

    def exit_app(self):
        self.client.render_message("Goodbye!")
        exit()

    def save_data_to_file(self):
        self.load_from_source(self.current_day, with_save=True)

    def display_basic_daily_info(self):
        basic_entries = {k: v for k, v in self.analysis_results.items() if v.get('type') == 'basic'}
        print("\n\nDaily results\n\n")
        for desc, entry in basic_entries.items():
            func = entry['func']
            args = entry['args']
            func(args)
        print("\n\n")

    def build_graph(self):

        available_plugins = {
            "Total dialogs created": DialogsCreated,
            "Successful recharges": SuccessRechargePlugin,
            "Total recharges": RechargedAmountPlugin,
            "ChannelEffectiveness": ChannelEffectiveness,
            "All graphs": [DialogsCreated, SuccessRechargePlugin, RechargedAmountPlugin, ChannelEffectiveness]
        }

        chosen_plugin = self.client.display_graph_menu(available_plugins)
        if isinstance(chosen_plugin, list):
            build_plot(available_plugins[chosen_plugin])
            return
        build_plot(available_plugins[chosen_plugin])


if __name__ == '__main__':
    data = open_file()
    manager = PluginManager(plugins=plugins)

    result = manager.analyse_data(data['data'])

    app = AnalyzerApp(prepared_data=result, client=CLI())
    app.run_main_menu()

