import random

class Disk:
    def __init__(self, size):
        self.size = size
        self.blocks = [None] * size  # None means the block is free

    def allocate(self, file_name, start, length):
        # Allocate blocks contiguously.
        if self.check_space(start, length):
            for i in range(start, start + length):
                self.blocks[i] = file_name
            return True
        return False

    def allocate_randomly(self, file_name, size):
        # Allocate blocks in a non-contiguous manner and record the next block index.
        indices = []
        for _ in range(size):
            if all(block is not None for block in self.blocks):
                raise Exception("Disk is full, cannot allocate more files.")
            index = random.choice([i for i, block in enumerate(self.blocks) if block is None])
            self.blocks[index] = (file_name, -1)
            indices.append(index)
        for i in range(len(indices) - 1):
            self.blocks[indices[i]] = (indices[i], file_name, indices[i + 1])
        return indices

    def deallocate(self, file_name):
        # Deallocate all blocks occupied by a file.
        for i in range(self.size):
            if self.blocks[i] == file_name:
                self.blocks[i] = None

    def check_space(self, start, length):
        # Check if the specified range of blocks is free.
        return all(self.blocks[i] is None for i in range(start, start + length))

    def __str__(self):
        # Display the current state of the disk.
        return ' | '.join([str(i) if i is not None else '_' for i in self.blocks])

class Directory:
    def __init__(self):
        self.entries = {}  # key: file_name, value: (start, length)

    def add_file(self, file_name, start, length):
        # Add a file to the directory with contiguous allocation details.
        self.entries[file_name] = (start, length)

    def add_file_non_contiguous(self, file_name, indices):
        # Add a file to the directory with non-contiguous allocation details.
        self.entries[file_name] = indices

    def remove_file(self, file_name):
        # Remove a file from the directory.
        if file_name in self.entries:
            del self.entries[file_name]

    def __str__(self):
        # Display the directory entries.
        return '\n'.join([f"{file}: blocks={details}" for file, details in self.entries.items()])
