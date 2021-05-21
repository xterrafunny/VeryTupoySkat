class KeyValueStore:
    def _read(self, file):
        for line in file.readlines():
            if line.count(self.sep) != 1:
                raise KeyError
            key, value = line.split(self.sep)
            key = self.key_type(key.strip())
            value = self.value_type(value.strip())
            self.data[key] = value

    def __init__(self,
                 file_name: str,
                 key_type=str,
                 value_type=str,
                 sep=','):
        self.file_name = file_name
        self.key_type = key_type
        self.value_type = value_type
        self.sep = sep
        self.data = dict()
        try:
            open(self.file_name, 'r')
        except FileNotFoundError:
            open(self.file_name, 'w')

        with open(self.file_name, 'r') as file:
            self._read(file)

    def store(self, key, value):
        assert isinstance(key, self.key_type)
        assert isinstance(value, self.value_type)

        self.data[key] = value

    def load(self, key):
        assert isinstance(key, self.key_type)
        if key not in self.data:
            raise KeyError
        return self.data[key]

    def __contains__(self, key):
        assert isinstance(key, self.key_type)
        return key in self.data

    def __del__(self):
        with open(self.file_name, "w") as file:
            for key, value in self.data.items():
                file.write(f"{key}{self.sep}{value}\n")


class KeyStore:
    def __init__(self,
                 file_name: str,
                 key_type=str,
                 sep=','):
        self.kv = KeyValueStore(file_name, key_type, bool, sep)

    def store(self, key):
        self.kv.store(key, True)

    def __contains__(self, key):
        return key in self.kv

    def __del__(self):
        del self.kv
