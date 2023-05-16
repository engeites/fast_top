from datetime import datetime, timedelta
from app.browser import DirectoryBrowser
from .factory import FileLoaderFactory, APILoaderFactory,  LoaderFactory
from .loaders import Loader


def convert_day_to_date(day_str) -> str:
    current_date = datetime.today()
    day_of_week = current_date.strftime('%A')

    while day_of_week.lower() != day_str.lower():
        current_date += timedelta(days=1)
        day_of_week = current_date.strftime('%A')

    return current_date.strftime('%d.%m.%Y')


def determine_loader(command: str) -> str:
    if command.endswith(".json"):
        date_string = command[:-5]
        datetime.strptime(date_string, "%d.%m.%Y")
        return "file"

    try:
        datetime.strptime(command, "%d.%m.%Y")
        return "file"
    except ValueError:
        return "api"


def load_data(day_to_load: str, with_save: bool = False) -> dict:

    factories = {
        'file': FileLoaderFactory(),
        'api': APILoaderFactory()
    }

    factory_type = determine_loader(day_to_load)

    if factory_type in factories:
        factory: LoaderFactory = factories[factory_type]
        print(f"Chosen loader: {factory}. Starting...\n\n")

        loader: Loader = factory.get_loader()
        if with_save:
            browser = DirectoryBrowser()
            browser.save_new_file(convert_day_to_date(day_to_load), loader.load_data(day_to_load))
        return loader.load_data(day_to_load)['data']