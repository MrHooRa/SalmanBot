from datetime import datetime
class Logs():
    def __init__(self, path='', name = ""):
        self.path = f"{path}logs.txt"
        self.name = f"<{name}> " if name else ""

    def log(self, action, printCmd = False, type = "Info", name = '__defaultName__'):
        try:
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        except Exception as e:
            print(f"(Logs can not run) Please make sure datetime is installed!\n{e}")
            return False

        name = self.name if name == '__defaultName__' else name

        # log format
        action = f"{name}{dt_string} | {type} | {action}"

        # Save action to log file
        try:
            f = open(self.path, "a")
            f.write(f"{action}\n")
            f.close()
        except Exception as e:
            print(f"(Logs can not run) Make sure you select correct path\n{e}")
            return False

        if printCmd:
            print(action)
        return True