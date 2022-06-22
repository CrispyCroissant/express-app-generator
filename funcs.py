import subprocess
import os
import json


def install_deps() -> None:
    try:
        print("Initializing npm...")
        subprocess.run(["npm", "init", "--y"],
                       check=True,
                       stdout=subprocess.DEVNULL)
    except Exception as e:
        print(e)
        print("ERROR: npm init failed to run...")
        quit(-1)

    try:
        print("Installing Express...")
        subprocess.run(["npm", "i", "express"],
                       check=True,
                       stdout=subprocess.DEVNULL)
    except Exception as e:
        print(e)
        print("ERROR: npm failed to install express...")
        quit(-1)

    try:
        print("Installing dev dependencies...")
        subprocess.run(["npm", "i", "-D", "dotenv", "typescript",
                        "@types/express", "@types/node",
                        "@types/jest", "@types/supertest",
                        "concurrently", "nodemon", "supertest",
                        "jest", "ts-jest", "ts-node"],
                       check=True,
                       stdout=subprocess.DEVNULL)
    except Exception as e:
        print(e)
        print("ERROR: npm failed to dev dependencies...")
        quit(-1)

    try:
        print("Generating tsconfig...")
        subprocess.run(["npx", "tsc", "--init"],
                       check=True,
                       stdout=subprocess.DEVNULL)
    except:
        print("ERROR: Failed to generate tsconfig.json")
        exit(-1)

    try:
        print("Generating jest.config...")
        subprocess.run(["npx", "ts-jest", "config:init"],
                       check=True,
                       stdout=subprocess.DEVNULL)
    except:
        print("ERROR: Failed to generate jest.config.js")
        exit(-1)


def configure_tsconfig() -> None:
    print("Configuring tsconfig...")
    file = open("tsconfig.json", "r")
    new_file_content = ""

    for line in file:
        line = line.strip()
        new_line = line

        if '// "outDir": "./"' in line:
            new_line = line.replace('// "outDir": "./"',
                                   '"outDir": "./dist"')

        if'// "sourceMap": true' in line:
            new_line = line.replace('// "sourceMap": true',
                                   '"sourceMap": true')

        new_file_content += new_line + "\n"

    file.close()

    file = open("tsconfig.json", "w")
    file.write(new_file_content)
    file.close()


def configure_jest_config() -> None:
    print("Configuring jest...")
    filename = "jest.config.js"

    with open(filename, "r") as file:
        lines = file.readlines()

    lines[-1] = '  modulePathIgnorePatterns: ["<rootDir>/dist/"],\n};'

    with open(filename, "w") as file:
        file.writelines(lines)


def configure_scripts() -> None:
    print("Configuring scripts...")
    filename = "package.json"

    with open(filename, "r") as file:
        data = json.load(file)
        del data["scripts"]["test"]

        data["scripts"]["build"] = "npx tsc"
        data["scripts"]["start"] = "node dist/server.ts"
        data["scripts"]["dev"] = "concurrently \"npx tsc --watch\" \"nodemon -q dist/server.js\""

    os.remove(filename)
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)


def create_folder_struct(path: str) -> None:
    print("Creating folder structure...")
    folders = ["config", "controllers",
               "helpers", "routers", "services", "types"]

    for folder_name in folders:
        new_path = os.path.join(path, folder_name)

        os.makedirs(new_path)
        # Create empty file for git recognition.
        try:
            open(os.path.join(new_path, "skeleton"), "a").close()
        except Exception as e:
            print(e)
            print("ERROR: Couldn't create skeleton files")
