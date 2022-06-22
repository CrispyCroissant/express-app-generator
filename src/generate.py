import os
import sys
import funcs

rootPath: str = ""

if len(sys.argv) != 2:
    print("Usage: python gen.py pathToFolder")
    quit(0)
else:
    rootPath = sys.argv[1]

os.makedirs(rootPath)
os.chdir(rootPath)

funcs.install_deps()
funcs.configure_tsconfig()
funcs.configure_jest_config()
funcs.configure_scripts()
funcs.create_folder_struct(rootPath)

print("Finished!")
