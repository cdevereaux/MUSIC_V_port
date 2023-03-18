class imposter_list:
    def __init__(self, list, idx):
        self.list = list
        self.idx = idx

    def __getitem__(self, _):
        return self.list[self.idx]
    
    def __setitem__(self, _, value):
        self.list[self.idx] = value
