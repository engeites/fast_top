
class CLI:

    def render_divider(self):
        print("\n\n" + "*" * 30 + "\n\n")

    def render_message(self, message: str):
        print("\n\n" + "*" * 30 + "\n\n")
        print(message)
        print("\n\n" + "*" * 30 + "\n\n")

    def print_welcome(self):
        print("Welcome to the CLI!")

    def print_goodbye(self):
        print("Goodbye!")

    def display_main_menu(self, options: list):
        for index, option in enumerate(options):
            print(f"{index + 1}: {option}")

        user_input = input("Please enter the following commands: ")
        try:
            return options[int(user_input) - 1]
        except (ValueError, IndexError):
            return None

    def display_analyzer_menu(self, desc_list: list, command_list: list):
        print("\n\nList of all analysis tools:\n")
        for index, command in enumerate(desc_list):
            print(f"{index + 1}: {command}")

        user_input = input("Please enter the following commands or any other symbol to return to main menu: ")
        try:
            command = command_list[int(user_input) - 1]
            return command
        except (IndexError, ValueError):
            self.render_message("No such command. Returning to main menu")
            return None

    def display_choose_file_menu(self, file_list: list) -> str|None:
        print("\nThis is a list of files with saved data:\n")
        for index, file in enumerate(file_list):
            print(f"{index + 1}: {file}")

        user_input = input("Please choose file: ")
        try:
            file = file_list[int(user_input) - 1]
            return file
        except (IndexError, ValueError):
            self.render_message("No such command")
            return None

    def display_graph_menu(self, plugin_list: dict):
        for counter, desc in enumerate(plugin_list.keys()):
            print(f"{counter}: {desc}")

        user_input = input("Choose tool to build graph: ")

        options = [desc for desc in plugin_list.keys()]
        chosen_plugin = options[int(user_input)]
        return chosen_plugin
