from datetime import datetime
class Logs():
    def __init__(self, path='', name = "", tabs=1):
        self.path = f"{path}logs.log"
        self.name = f"<{name}> " if name else ""
        self.tabs = tabs

    def log(self, action, printCmd = False, type = "Info", saveInLog = True, name = '__default__', author = "Bot"):
        """Create new log"""
        try:
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        except Exception as e:
            print(f"(Logs can not run) Please make sure datetime is installed!\n{e}")
            return False

        name = self.name if name == '__default__' else name

        # log format
        tab = []
        for _ in range(self.tabs):
            tab.append("\t")
        tab = "".join(tab)
        action = f"{name}{tab}{dt_string} | {type} | {author} | {action}"

        # Save action to log file
        if saveInLog:
            try:
                f = open(self.path, "a", encoding="utf-8")
                f.write(f"{action}\n")
                f.close()
            except Exception as e:
                print(f"(Logs can not run) Make sure you select correct path\n{e}")
                return False

        if printCmd:
            print(action)
        return True
    
    def newLine(self, text = "\n"):
        """Add new line in log file"""
        try:
            f = open(self.path, "a")
            f.write(f"{text}")
            f.close()
        except Exception as e:
            print(f"(Logs can not run) Make sure you select correct path\n{e}")
            return False
        return True