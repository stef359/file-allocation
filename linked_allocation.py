class LinkedAllocation:
    def __init__(self, disk_size):
        self.disk = [None] * disk_size

    def find_free_block(self):
        for i, block in enumerate(self.disk):
            if block is None:
                return i
        return -1

    def create_file(self, file_id, size):
        last_index = None
        first_index = None
        for _ in range(size):
            free_index = self.find_free_block()
            if free_index == -1:
                raise Exception("Disk is full, cannot create file")
            self.disk[free_index] = {'file_id': file_id, 'next': None}
            if last_index is not None:
                self.disk[last_index]['next'] = free_index
            last_index = free_index
            if first_index is None:
                first_index = free_index
        return first_index

    def read_file(self, start_index):
        file_content = []
        current_index = start_index
        while current_index is not None:
            block = self.disk[current_index]
            file_content.append(block['file_id'])
            current_index = block['next']
        return file_content

    def delete_file(self, start_index):
        current_index = start_index
        while current_index is not None:
            next_index = self.disk[current_index]['next']
            self.disk[current_index] = None
            current_index = next_index

    def write_file(self, start_index, additional_size):
        current_index = start_index
        while self.disk[current_index]['next'] is not None:
            current_index = self.disk[current_index]['next']
        
        for _ in range(additional_size):
            free_index = self.find_free_block()
            if free_index == -1:
                raise Exception("No free blocks available, cannot expand file")
            self.disk[free_index] = {'file_id': self.disk[current_index]['file_id'], 'next': None}
            self.disk[current_index]['next'] = free_index
            current_index = free_index
        return True
