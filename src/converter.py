from unittest import loader
import yaml


class YamlConverter:
    
    # main
    def drone2woodpecker(rawData: str) -> str:
        jsonData = yaml.load(rawData, Loader=yaml.Loader)
        print(jsonData)
        yamlData = yaml.dump(jsonData, allow_unicode=True)
        return yamlData

    def woodpecker2drone(rawData: str) -> str:
        jsonData = yaml.safe_load(rawData, Loader=yaml.Loader)
        yamlData = yaml.dump(jsonData, allow_unicode=True)
        return yamlData


if __name__ == "__main__":
    data = ""
    file_path = input('File path: ')
    with open(file_path, 'r') as f:
        data = f.read()
    print(YamlConverter.drone2woodpecker(data))

