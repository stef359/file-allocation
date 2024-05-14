class ContiguousAllocation:
    def __init__(self, disk_size):
        self.disk = [None] * disk_size  # None represents free space

    def find_free_block(self, size):
        # Improved search method for finding contiguous blocks
        for start in range(len(self.disk) - size + 1):
            if all(self.disk[i] is None for i in range(start, start + size)):
                return start
        return None

    def create_file(self, file_id, size):
        start = self.find_free_block(size)
        if start is not None:
            for i in range(start, start + size):
                self.disk[i] = file_id
            return True
        else:
            raise Exception("Not enough contiguous space to create file")

    def read_file(self, file_id):
        file_content = []
        for block in self.disk:
            if block == file_id:
                file_content.append(block)
        return file_content

    def delete_file(self, file_id):
        freed = False
        for i in range(len(self.disk)):
            if self.disk[i] == file_id:
                self.disk[i] = None
                freed = True
        if not freed:
            raise Exception("File not found")

    def write_file(self, file_id, additional_size):
        end_pos = None
        # Find the end position of the file
        for i in range(len(self.disk) - 1, -1, -1):
            if self.disk[i] == file_id:
                end_pos = i
                break
        if end_pos is not None and all(self.disk[i] is None for i in range(end_pos + 1, end_pos + 1 + additional_size)):
            for i in range(end_pos + 1, end_pos + 1 + additional_size):
                self.disk[i] = file_id
            return True
        else:
            raise Exception("Not enough contiguous space to expand file or file does not exist")