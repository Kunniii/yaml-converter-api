from os import environ
from platform import python_branch
import yaml
import json


class YamlConverter:
    def __trigger():
        ...

    def __platform(s: str) -> str:
        return f'{s.get("os")}/{s.get("arch")}'

    def __workspaces(s: str) -> str:
        return f'path: {s.get("path")}'

    def __cloning():
        ...

    # convert each step
    def __steps(self, s) -> dict:
        # the fuction should return a dictionay of image name as key
        # and an other dictionary as the item

        # the dictionary for result
        woodpecker_steps = {}

        # for each step in drone step
        # convert in to woodpecker
        # and store the result in to
        # the result dictionanry

        for drone_step in s:
            # split get value
            name = drone_step.get('name')
            image = drone_step.get('image')
            commands = drone_step.get('commands')  # not change
            environment = drone_step.get('environment')
            # secrets

            when = drone_step.get('when')
            # when is nested, need a fuction to convert.
            # this conditions
            when = self.__conditions(when)

            trigger = drone_step.get('trigger')
            depends_on = drone_step.get('depends_on')

            # there is more  :)

            # elements in each step
            each_step = {}
            each_step["image"] = image
            each_step["commands"] = commands
            # more

            woodpecker_steps[name] = each_step

        return woodpecker_steps

    # function to convert when in step:
    def __conditions(self, condition) -> dict:
        woodpecker_condition = {}

        cron = condition.get('cron')
        ref = condition.get('ref')
        matrix = condition.get('matrix')

        # region Convert branch
        branch = condition.get('branch')
        if branch:
            # if branch is dict, then it has include, exclude
            if type(branch) is dict:
                # if branch has 'include'
                if "include" in branch:
                    branch["include"] = str(branch['include']).replace("'", '')
                # if branch has 'exclude'
                if "exclude" in branch:
                    branch["exclude"] = str(branch['exclude']).replace("'", '')
            # else branch is a list
            else:
                branch = str(branch).replace("'", '')

            woodpecker_condition["branch"] = branch

        # endregion

        # region Convert event
        # if event is dict, then it has include, exclude
        event = condition.get('event')
        if event:
            if type(event) is dict:
                if "include" in event:
                    event["include"] = str(event['include']).replace("'", '')
                if "exclude" in event:
                    event["exclude"] = str(event['exclude']).replace("'", '')
            else:
                event = str(event).replace("'", '')

            woodpecker_condition['event'] = event
        # endregion

        # region Convert status
        status = condition.get('status')
        if status:
            # if status is dict, then it has include, exclude
            if type(status) is dict:
                if "include" in status:
                    status["include"] = str(status['include']).replace("'", '')
                if "exclude" in status:
                    status["exclude"] = str(status['exclude']).replace("'", '')
            else:
                status = str(status).replace("'", '')

            woodpecker_condition['status'] = status

        # endregion

        # region Convert repo
        # drone.io has multiple repo support with include and exclude
        # but Woodpecker has only one repo support
        # so, let's see if it can work in drone.io format
        repo = condition.get('repo')
        if repo:
            if type(repo) is dict:
                if "include" in repo:
                    repo["include"] = str(repo['include']).replace("'", "")
                if "exclude" in repo:
                    repo["exclude"] = str(repo['exclude']).replace("'", "")
            else:
                repo = str(repo).replace("'", '')
            woodpecker_condition['repo'] = repo

        # endregion

        # region Convert platform
        platform = condition.get('platform')
        if platform:
            platform = self.__platform(platform)

            woodpecker_condition["platform"] = platform

        # endregion

        # region Convert environment
        environment = condition.get('environment')
        if environment:
            new_env = []
            for k, v in environment.items():
                new_env.append(f'{k}={v}')
            environment = new_env
            woodpecker_condition["environment"] = environment

        # endregion

        # region Convert instance
        instance = condition.get('instance')
        if instance:
            if type(instance) is dict:
                if 'include' in instance:
                    instance['include'] = str(instance['include']).replace("'",'')
                if 'exclude' in instance:
                    instance['exclude'] = str(instance['exclude']).replace("'",'')
            else:
                instance = str(instance).replace("'",'')
                
            woodpecker_condition['instance'] = instance

        # endregion

        return woodpecker_condition

    def __plugins():
        ...

    def __services(s):
        woodpecker_services = {}
        for service in s:
            name = service.get('name')
            image = service.get('image')
            woodpecker_services[name] = {'image': image}
        return woodpecker_services

    def __parallelism():
        ...

    def __routing():
        ...

    def __volumes():
        ...

    # main

    def drone2woodpecker(raw_data: str) -> str:
        woodpecker_yaml: str
        woodpecker: dict = {}
        drone: dict

        # Load drone.io yaml
        drone = yaml.load(raw_data, Loader=yaml.Loader)

        # This is where the magic happen
        kind = drone['kind']
        steps = drone['steps']
        for step in steps:
            step_name = step['name']
            step_image = step['image']
            step_commands = step['commands']  # not change

            step_name_dict = {}
            step_name_dict['image'] = step_image
            step_name_dict['commands'] = step_commands
            pipe = {}
            pipe[step_name] = step_name_dict

        woodpecker[kind] = pipe
        # TODO
        #

        # Dump the woodpecker yaml format
        woodpecker_yaml = yaml.dump(woodpecker, allow_unicode=True).replace("'","")
        return woodpecker_yaml

    def woodpecker2drone(rawData: str) -> str:
        jsonData = yaml.safe_load(rawData, Loader=yaml.Loader)
        yamlData = yaml.dump(jsonData, allow_unicode=True)
        return yamlData


# For testing
if __name__ == "__main__":
    data: str
    file_path = input('File path: ')

    # read data from file and feed the fuction
    with open(file_path, 'r') as f:
        data = f.read()
        print(YamlConverter.drone2woodpecker(data))
