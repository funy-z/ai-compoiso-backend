with open('requirements.txt', 'r') as file:
    lines = file.readlines()

with open('pip_requirements.txt', 'w') as file:
    for line in lines:
        package_info = line.split('=')
        if len(package_info) >= 2:
            package = package_info[0]
            version = package_info[1]
            file.write(f"{package}=={version}\n")
