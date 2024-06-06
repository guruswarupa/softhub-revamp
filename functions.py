import subprocess

def checkpack(packtype):
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    if packtype == "🌐 Winget": 
        packages = str(subprocess.run(["winget", "list", "--source", "winget"], check=True, capture_output=True,startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW))
    elif packtype == "🌐 Chocolatey":
        choco_list = subprocess.run(["choco","list"], capture_output=True, text=True,startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW)
        packages = choco_list.stdout
    elif packtype == "🌐 Scoop":
        packages = str(subprocess.check_output("scoop list", shell=True,startupinfo=startupinfo, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NO_WINDOW))
    return packages

