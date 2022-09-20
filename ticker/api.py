class API:
    key: str
    def __init__(self) -> None:
        try:
            self.key = self.get_key()
        except OSError:
            self.key = ""
        pass
        
    def key_exists(self)->bool:
        key = self.get_key()
        return len(key) > 0
    
    def get_key(self) -> str:
        try:
            api_key = ""
            with (open("api.txt","r") as api_file):
                api_key = api_file.read()
            return api_key
        except OSError:
            raise OSError("File api.txt does not exist")

    def set_key(self,key: str)->None:
        with(open("api.txt", "x") as api_file):
            api_file.write(key)
        return