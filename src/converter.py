import yaml


class YamlConverter:

    # main
    def drone2woodpecker(drone_yaml: str) -> str:
        woodpecker_yaml: str
        woodpecker: dict = {}
        drone: dict

        # Load drone.io yaml
        drone = yaml.load(drone_yaml, Loader=yaml.Loader)

        # This is where the magic happen
        kind = drone['kind']
        steps = drone['steps']
        for step in steps:
            step_name = step['name']
            step_image = step['image']
            step_commands = step['commands'] # not change

            step_name_dict = {}
            step_name_dict['image'] = step_image
            step_name_dict['commands'] = step_commands
            pipe = {}
            pipe[step_name] = step_name_dict

        woodpecker[kind] = pipe
        # TODO
        # 


        # Dump the woodpecler yaml format
        woodpecker_yaml = yaml.dump(woodpecker, allow_unicode=True)
        return woodpecker_yaml

    def woodpecker2drone(rawData: str) -> str:
        jsonData = yaml.safe_load(rawData, Loader=yaml.Loader)
        yamlData = yaml.dump(jsonData, allow_unicode=True)
        return yamlData


if __name__ == "__main__":
    data: str
    file_path = input('File path: ')

    # read data from file and feed the fuction
    with open(file_path, 'r') as f:
        data = f.read()
    print(YamlConverter.drone2woodpecker(data))
