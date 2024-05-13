class Disk:
    def __init__(self, size):
        self.size = size
        self.blocks = [None] * size  # None means the block is free

    def allocate(self, file_name, start, length):
        if self.check_space(start, length):
            for i in range(start, start + length):
                self.blocks[i] = file_name
            return True
        else:
            return False

    def deallocate(self, file_name):
        for i in range(self.size):
            if self.blocks[i] == file_name:
                self.blocks[i] = None

    def check_space(self, start, length):
        return all(self.blocks[i] is None for i in range(start, start + length))

    def __str__(self):
        return ' | '.join([str(i) if i is not None else '_' for i in self.blocks])

class Directory:
    def __init__(self):
        self.entries = {}  # key: file_name, value: (start, length)

    def add_file(self, file_name, start, length):
        self.entries[file_name] = (start, length)

    def remove_file(self, file_name):
        if file_name in self.entries:
            del self.entries[file_name]

    def __str__(self):
        return '\n'.join([f"{file}: start={start}, length={length}" for file, (start, length) in self.entries.items()])
