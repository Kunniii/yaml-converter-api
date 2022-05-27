def __steps(s: str) -> dict:
    for step in s:
        step_name = step['name']
        step_image = step['image']
        step_commands = step['commands'] # not change

        step_name_dict = {}
        step_name_dict['image'] = step_image
        step_name_dict['commands'] = step_commands
        steps = {}
        steps[step_name] = step_name_dict
        
    return steps
        
