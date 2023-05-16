from matplotlib import pyplot as plt

from app.graphs.graph_factory import PlotDataNormalizer, SimplePlotGraph


def build_plot(chosen_tool):
    normalizer = PlotDataNormalizer()
    if isinstance(chosen_tool, list):

        # Calculate the number of plots
        try:
            num_plots = len(chosen_tool)
        except TypeError:
            num_plots = 1

        # Determine the number of rows and columns for subplots
        num_rows = int(num_plots ** 0.5)
        num_cols = int((num_plots + num_rows - 1) / num_rows)

        # Create the subplots
        fig, axes = plt.subplots(nrows=num_rows, ncols=num_cols)

        # Flatten the axes array if necessary
        if num_plots == 1:
            axes = [axes]

        # Iterate over the data and create plots
        for i, ax in enumerate(axes.flat):
            if i < num_plots:
                data_ready = normalizer.prepare_data(plugin=chosen_tool[i])
                ax.plot(data_ready['x'], data_ready['y'])
                ax.set_title(f'{data_ready["desc"]}')

        # Adjust spacing between subplots
        plt.tight_layout()

        # Display the plots
        plt.show()
        return

    data_ready = normalizer.prepare_data(plugin=chosen_tool)

    graph = SimplePlotGraph()
    graph.build_graph(**data_ready)
    plt.show()