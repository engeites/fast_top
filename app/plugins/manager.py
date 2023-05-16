from app.plugins.plugins import PluginInterface


class PluginManager():
    def __init__(self, plugins: list[PluginInterface]):
        self.plugins = plugins

    def analyse_data(self, data: dict):
        analysis_result = {}
        for plugin in self.plugins:
            analysis_result.update(plugin.analyze(data))
        return analysis_result

