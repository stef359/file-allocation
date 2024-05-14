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
            raise Exception("No space to create index block")
        
        self.disk[index_block_index] = {'file_id': file_id, 'type': 'index', 'blocks': []}
        try:
            for _ in range(size):
                block_index = self.find_free_block()
                if block_index == -1:
                    raise Exception("Disk is full, not all blocks could be allocated")
                self.disk[block_index] = {'file_id': file_id, 'type': 'data', 'content': 'data'}
                self.disk[index_block_index]['blocks'].append(block_index)
        except Exception as e:
            # Cleanup any partial allocation if error occurs
            for block_index in self.disk[index_block_index]['blocks']:
                self.disk[block_index] = None
            self.disk[index_block_index] = None
            raise e  # Re-raise the exception to inform the caller
        return index_block_index

    def read_file(self, index_block_index):
        index_block = self.disk[index_block_index]
        if index_block is None or index_block['type'] != 'index':
            raise Exception("Invalid index block")
        return [self.disk[block_index]['content'] for block_index in index_block['blocks']]

    def delete_file(self, index_block_index):
        index_block = self.disk[index_block_index]
        if index_block and index_block['type'] == 'index':
            for block_index in index_block['blocks']:
                self.disk[block_index] = None
            self.disk[index_block_index] = None
        else:
            raise Exception("Invalid index block or block already deleted")

    def write_file(self, index_block_index, additional_data):
        index_block = self.disk[index_block_index]
        if index_block is None or index_block['type'] != 'index':
            raise Exception("Invalid index block")
        for data in additional_data:
            block_index = self.find_free_block()
            if block_index == -1:
                raise Exception("No space available to expand file")
            self.disk[block_index] = {'file_id': index_block['file_id'], 'type': 'data', 'content': data}
            index_block['blocks'].append(block_index)
        return True
