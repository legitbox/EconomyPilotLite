import tomllib
import tomlkit
import os

def check_config():
    config = {
        "currency_symbol": "$"
    }

    directory = 'config'
    filename = 'economy-pilot-lite.toml'
    file_path = os.path.join(directory, filename)

    os.makedirs(directory, exist_ok=True)

    if not os.path.isfile(file_path):
        toml_doc = tomlkit.document()
        toml_doc.update(config)

        with open(file_path, 'w') as file:
            file.write(tomlkit.dumps(toml_doc))


def load_config():
    directory = 'config'
    filename = 'economy-pilot-lite.toml'
    file_path = os.path.join(directory, filename)
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'rb') as file:
        toml_data = tomllib.load(file)
        currency_symbol = toml_data.get("currency_symbol")
    return currency_symbol