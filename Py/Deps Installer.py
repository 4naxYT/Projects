def installdepsfunc(content):
    """
    Install dependencies for the project.
    
    pass in a raw string literal as file content.
    """
    import os
    import subprocess
    content = "python -m pip install " + content

    def makefile(path, name, contents):
        """
        Create a .bat file with the given contents.
        path     : directory where the file will be created
        name     : filename (without extension, or with .bat)
        contents : string containing batch commands

        also returns path to the new file
        """
        # Ensure the directory exists
        os.makedirs(path, exist_ok=True)
        
        # Add .bat extension if not present
        if not name.endswith('.bat'):
            name += '.bat'
        
        full_path = os.path.join(path, name)
        
        with open(full_path, 'w') as f:
            f.write("python -m pip install --upgrade pip\n" + contents)
        
        return full_path
    def runfile(full_path):
        """
        Executes a file from "path" given
        """
        if not os.path.isfile(full_path):
            raise FileNotFoundError(f"File not found: {full_path}")
        
        # Run the batch file and wait for completion
        result = subprocess.run(full_path, shell=True, capture_output=True, text=True)
        return result
    def delfile(full_path):
        """
        Deletes a file from "path" given
        """
        if os.path.isfile(full_path):
            os.remove(full_path)
        else:
            print(f"Warning: {full_path} dosen't exist.")

    # 1. Create file
    print("[Deps Installer] Creating File...")
    file_path = makefile(r"C:\Users\Public\Temp", "install_deps.bat", content)

    # 2. run dat
    print("[Deps Installer] Running File...")
    try:
        result = runfile(file_path)
        if result.stderr:
            print("Errors:", result.stderr)
    except Exception as e:
        print(f"Error running batch: {e}")
        
    # 3. delete it :3
    print("[Deps Installer] Finished.")
    delfile(file_path)
    subprocess.call('cls', shell=True) # cls for windwos

installdepsfunc(r"")
