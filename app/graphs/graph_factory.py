from abc import ABC
import matplotlib.pyplot as plt
from app.plugins.plugins import DialogsCreated
from app.utils.load_file import load_file
from app.browser import DirectoryBrowser


class GraphBuilder(ABC):
    @staticmethod
    def prepare_data(**kwargs):
        pass


class PlotDataNormalizer(GraphBuilder):
    @staticmethod
    def prepare_data(**kwargs):
        browser = DirectoryBrowser()
        saved_files_list = browser.get_saved_files_list()
        saved_files_list.reverse()
        all_days = []
        plugin_desc = ""
        for file in saved_files_list:
            data = load_file(file)
            analysis = kwargs['plugin'].analyze(data['data'])
            values = list(analysis.values())[0]
            plugin_desc = values['desc']
            all_days.append(values['args'])
        return {
            'x': [filename[:2] for filename in saved_files_list],
            'y': all_days,
            'desc': plugin_desc
        }


class Graph(ABC):
    def create_graph(self, **kwargs):
        pass


class SimplePlotGraph(Graph):
    def build_graph(self, **kwargs):
        xaxis = kwargs['x']
        yaxis = kwargs["y"]
        # plt.plot(xaxis, yaxis)
        # plt.show()
        return plt.plot(xaxis, yaxis)