from datetime import datetime
class Logs():
    def __init__(self, path='', name = "", tabs=1):
        self.path = f"{path}logs.log"
        self.name = f"<{name}> " if name else ""
        self.tabs = tabs

    def log(self, action, printCmd = False, type = "Info ", saveInLog = True, name = '__default__', author = "Bot"):
        """Create new log"""
        try:
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        except Exception as e:
            print(f"(Logs can not run) Please make sure datetime is installed!\n{e}")
            return False

        name = self.name if name == '__default__' else name

        # log format
        tab = ["\t" for _ in range(self.tabs)]
        tab = "".join(tab)
        action = f"{dt_string} {name}{tab}{type} | {author} | {action}"

        # Save action to log file
        if saveInLog:
            try:
                with open(self.path, "a", encoding="utf-8") as f:
                    f.write(f"{action}\n")
            except Exception as e:
                print(f'(Logs can not run) Make sure you select correct path\n{e}')
                return False
        if printCmd:
            print(action)
        return True
    
    def newLine(self, text = "\n"):
        """Add new line in log file"""
        try:
            with open(self.path, "a") as f:
                f.write(f"{text}")
        except Exception as e:
            print(f"(Logs can not run) Make sure you select correct path\n{e}")
            return False
        return True