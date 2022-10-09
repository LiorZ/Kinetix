import yaml

class KinetixParser:
    def __init__(self, filename):
        self.filename = filename
        self.data = None

    def parse(self):
        with open(self.filename, 'r') as f:
            self.data = yaml.load(f)

    def get_data(self):
        return self.data
