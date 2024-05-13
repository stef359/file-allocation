class IndexedAllocation:
    def __init__(self, disk_size):
        self.disk = [None] * disk_size

    def find_free_block(self):
        for i, block in enumerate(self.disk):
            if block is None:
                return i
        return -1

    def create_file(self, file_id, size):
        index_block_index = self.find_free_block()
        if index_block_index == -1:
            print("No space to create index block")
            return None
        
        self.disk[index_block_index] = {'file_id': file_id, 'type': 'index', 'blocks': []}
        for _ in range(size):
            block_index = self.find_free_block()
            if block_index == -1:
                print("Disk is full, not all blocks could be allocated")
                return index_block_index  # Partial file created
            self.disk[block_index] = {'file_id': file_id, 'type': 'data', 'content': 'data'}
            self.disk[index_block_index]['blocks'].append(block_index)
        return index_block_index

    def read_file(self, index_block_index):
        if self.disk[index_block_index] is None or self.disk[index_block_index]['type'] != 'index':
            return "Invalid index block"
        file_content = []
        for block_index in self.disk[index_block_index]['blocks']:
            file_content.append(self.disk[block_index]['content'])
        return file_content

    def delete_file(self, index_block_index):
        if self.disk[index_block_index] and self.disk[index_block_index]['type'] == 'index':
            for block_index in self.disk[index_block_index]['blocks']:
                self.disk[block_index] = None
            self.disk[index_block_index] = None

    def write_file(self, index_block_index, additional_data):
        if self.disk[index_block_index] is None or self.disk[index_block_index]['type'] != 'index':
            return "Invalid index block"
        for data in additional_data:
            block_index = self.find_free_block()
            if block_index == -1:
                print("No space available to expand file")
                return False
            self.disk[block_index] = {'file_id': self.disk[index_block_index]['file_id'], 'type': 'data', 'content': data}
            self.disk[index_block_index]['blocks'].append(block_index)
        return True
