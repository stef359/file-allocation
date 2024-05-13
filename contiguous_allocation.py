class ContiguousAllocation:
    def __init__(self, disk_size):
        self.disk = [None] * disk_size  # None represents free space

    def create_file(self, file_id, size):
        start = None
        # Search for a contiguous block of free space
        for i in range(len(self.disk) - size + 1):
            if all(block is None for block in self.disk[i:i + size]):
                start = i
                break

        if start is not None:
            for i in range(start, start + size):
                self.disk[i] = file_id
            return True
        else:
            print("Not enough contiguous space to create file")
            return False

    def read_file(self, file_id):
        file_content = []
        for block in self.disk:
            if block == file_id:
                file_content.append(block)
        return file_content

    def delete_file(self, file_id):
        for i in range(len(self.disk)):
            if self.disk[i] == file_id:
                self.disk[i] = None

    def write_file(self, file_id, additional_size):
        # Check the end position of the file
        end_pos = None
        for i in range(len(self.disk)):
            if self.disk[i] == file_id:
                end_pos = i

        # Try to expand the file in the contiguous space
        if all(block is None for block in self.disk[end_pos + 1:end_pos + 1 + additional_size]):
            for i in range(end_pos + 1, end_pos + 1 + additional_size):
                self.disk[i] = file_id
        else:
            print("Not enough contiguous space to expand file")
            # File needs to be moved or cannot be expanded
            return False
        return True