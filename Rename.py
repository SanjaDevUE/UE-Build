import os
import shutil

def rename_project_files(old_name, new_name, project_path):
    if old_name in os.path.basename(project_path):
        new_project_path = project_path.replace(old_name, new_name)
        shutil.move(project_path, new_project_path)
        project_path = new_project_path

    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.uproject'):
                old_project_file = os.path.join(root, file)
                new_project_file = old_project_file.replace(old_name, new_name)
                os.rename(old_project_file, new_project_file)

                update_file_references(new_project_file, old_name, new_name)

    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(('.cpp', '.h', '.cs', '.ini', '.uplugin')):
                file_path = os.path.join(root, file)
                update_file_references(file_path, old_name, new_name)

def update_file_references(file_path, old_name, new_name):
    with open(file_path, 'r') as file:
        content = file.read()

    content = content.replace(old_name, new_name)

    old_api_name = f"{old_name.upper()}_API"
    new_api_name = f"{new_name.upper()}_API"
    content = content.replace(old_api_name, new_api_name)

    with open(file_path, 'w') as file:
        file.write(content)

def main():
    old_project_name = input("Enter the old project name: ")
    new_project_name = input("Enter the new project name: ")
    project_directory = input("Enter the path to the Unreal Engine project directory: ")

    rename_project_files(old_project_name, new_project_name, project_directory)
    print(f"Project renamed from {old_project_name} to {new_project_name}, including API changes.")

if __name__ == "__main__":
    main()