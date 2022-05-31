import yaml
from server_log import write_log

class YamlConverter:

    def trigger():
        ...

    def cloning():
        ...

    def plugins():
        ...

    def routing():
        ...

    def environment(env):
        new_env = []
        for k, v in env.items():
            new_env.append(f'{k}={v}')
        return new_env

    def platform(s: str) -> str:
        return f'{s.get("os")}/{s.get("arch")}'

    def workspaces(s: str) -> str:
        return f'path: {s.get("path")}'

    # convert each step
    # require a dict of steps, and a list of host volumes
    # the fuction should return a dictionay of image name as key
    # and an other dictionary as the item
    def steps(steps, host_volumes=[]) -> dict:
        # the dictionary for result
        woodpecker_steps = {}

        # for each step in drone step
        # convert it into woodpecker
        # and store the result into
        # the result dictionary

        for drone_step in steps:
            # elements in each step
            each_step = {}

            name = drone_step.get('name')

            depends_on = drone_step.get('depends_on')
            # secrets
            trigger = drone_step.get('trigger')

            # image
            image = drone_step.get('image')
            if image:
                each_step['image'] = image

            # Commands
            commands = drone_step.get('commands')  # not change
            if commands:
                each_step['commands'] = commands

            # Condition
            when = drone_step.get('when')
            if when:
                when = YamlConverter.conditions(when)
                each_step['when'] = when

            # environment
            environment = drone_step.get('environment')
            if environment:
                environment = YamlConverter.environment(environment)
                each_step['environment'] = environment

            # Volumes
            volumes = drone_step.get('volumes')
            if host_volumes and volumes:
                volumes = YamlConverter.volumes(volumes, host_volumes)
                each_step['volumes'] = volumes

            # there is more

            # more

            woodpecker_steps[name] = each_step

        return woodpecker_steps

    def conditions(condition):
        woodpecker_condition = {}

        # these three are in drone.io, but
        # i dont see them in woodpecker
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
            platform = YamlConverter.platform(platform)

            woodpecker_condition["platform"] = platform

        # endregion

        # region Convert instance
        instance = condition.get('instance')
        if instance:
            if type(instance) is dict:
                if 'include' in instance:
                    instance['include'] = str(
                        instance['include']).replace("'", '')
                if 'exclude' in instance:
                    instance['exclude'] = str(
                        instance['exclude']).replace("'", '')
            else:
                instance = str(instance).replace("'", '')

            woodpecker_condition['instance'] = instance

        # endregion

        return woodpecker_condition

    def services(services):
        woodpecker_services = {}
        for service in services:
            name = service.get('name')
            image = service.get('image')
            woodpecker_services[name] = {'image': image}
            env = service.get('environment')
            if env:
                env = YamlConverter.environment(env)
                woodpecker_services[name]['environment'] = env
        return woodpecker_services

    def volumes(volumes, host_volumes):
        woodpecker_volumes = []

        for volume in volumes:
            volume_name = volume.get('name')
            volume_path = volume.get('path')
            for host_volume in host_volumes:
                if host_volume.get('name') == volume_name:
                    host_path = host_volume.get('host').get('path')
                    woodpecker_volumes.append(f'{host_path}:{volume_path}')
        return woodpecker_volumes

    # main

    def drone2woodpecker(drone_data: str) -> str:

        write_log(2, f'Converter - Recieved \n{drone_data}')

        woodpecker = {}

        # Load drone.io yaml
        drone = yaml.safe_load(drone_data)

        # This is where the magic happen
        if type(drone) is dict:
            kind = drone.get('kind')
        else:
            kind = []
        
        if kind:

            steps = drone.get('steps')
            volumes = drone.get('volumes')
            if steps:
                woodpecker_steps = YamlConverter.steps(steps, volumes)
                woodpecker[kind] = woodpecker_steps

            platform = drone.get('platform')
            if platform:
                woodpecker_platform = YamlConverter.platform(platform)
                woodpecker['platform'] = woodpecker_platform


            services = drone.get('services')
            if services:
                woodpecker_services = YamlConverter.services(services)
                woodpecker['services'] = woodpecker_services
            
            
            # woodpecker['branches'] = drone.io does not have this
            # woodpecker['workspace'] = i dont see this in drone.io
            # woodpecker['clone'] = this is quite complicate
            
            woodpecker_yaml = yaml.dump(woodpecker, allow_unicode=True).replace("'", "")
            
            write_log(2, f'Returned {woodpecker}')
            
            return woodpecker_yaml
        
        write_log(2, f'Data is Woodpecker-ci format, nothing to convert!')

        return drone_data

# For testing
if __name__ == "__main__":
    with open('test.yaml', 'r') as f:
        data = yaml.safe_load(f)
        steps = data.get('steps')
        volumes = data.get('volmues')

        the_steps = YamlConverter.steps(steps, volumes)

        the_return = yaml.dump(the_steps, allow_unicode=True).replace("'",'')

        print(the_return)
