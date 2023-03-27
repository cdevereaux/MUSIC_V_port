'''
Allows Variables and Note Parameters to be indexed within the unit generators
so that they can be used interchangeably with Functions and IO Blocks.
'''

class imposter_list:
    def __init__(self, list, idx):
        self.list = list
        self.idx = idx

    def __getitem__(self, _):
        return self.list[self.idx]
    
    def __setitem__(self, _, value):
        self.list[self.idx] = value
