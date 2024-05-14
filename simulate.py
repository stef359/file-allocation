import random
from disk_management import Disk, Directory
from contiguous_allocation import ContiguousAllocation
from linked_allocation import LinkedAllocation
from indexed_allocation import IndexedAllocation

def select_allocation_method():
    print("Select an allocation method:")
    print("1: Contiguous Allocation")
    print("2: Linked Allocation")
    print("3: Indexed Allocation")
    choice = input("Enter choice (1-3): ")
    if choice == '1':
        return ContiguousAllocation(500)
    elif choice == '2':
        return LinkedAllocation(500)
    elif choice == '3':
        return IndexedAllocation(500)
    else:
        print("Invalid choice. Defaulting to Contiguous Allocation.")
        return ContiguousAllocation(500)

def main():
    disk_size = 500
    disk = Disk(disk_size)
    directory = Directory()
    allocation_method = select_allocation_method()
    next_free_block = 0  # For contiguous allocation

    while True:
        print("\nCommands:")
        print("1: Add file")
        print("2: Remove file")
        print("3: Show disk state")
        print("4: Show directory listing")
        print("5: Perform allocation method-specific operation")
        print("0: Exit")
        command = input("Enter command number: ")

        if command == '0':
            print("Exiting simulator.")
            break
        elif command == '1':
            num_files = int(input("How many files do you want to add? "))
            base_file_name = input("Enter base file name: ")
            for i in range(num_files):
                file_name = f"{base_file_name}{i+1}"
                length = random.randint(1, 10)
                if isinstance(allocation_method, ContiguousAllocation):
                    start = next_free_block
                else:
                    start = random.randint(0, disk_size - 1)

                if disk.allocate(file_name, start, length):
                    directory.add_file(file_name, start, length)
                    print(f"File '{file_name}' added successfully at start block {start}.")
                    if isinstance(allocation_method, ContiguousAllocation):
                        next_free_block = start + length
                else:
                    print(f"Failed to add file '{file_name}'. Please check disk space.")
        elif command == '2':
            file_name = input("Enter file name to remove: ")
            if file_name in directory.entries:
                disk.deallocate(file_name)
                directory.remove_file(file_name)
                print(f"File '{file_name}' removed successfully.")
            else:
                print("File not found in directory.")
        elif command == '3':
            print("Disk State:")
            print(disk)
        elif command == '4':
            print("Directory Listing:")
            print(directory)
        elif command == '5':
            print("Performing method-specific operation:")
            file_name = input("Enter file name for method-specific operation: ")
            size = random.randint(1, disk_size)
            try:
                if isinstance(allocation_method, ContiguousAllocation):
                    result = allocation_method.create_file(file_name, size)
                    print("File created successfully.")
                elif isinstance(allocation_method, LinkedAllocation):
                    start_index = allocation_method.create_file(file_name, size)
                    print(f"File created starting at block {start_index}")
                elif isinstance(allocation_method, IndexedAllocation):
                    index_block = allocation_method.create_file(file_name, size)
                    print(f"File created with index block at {index_block}")
                else:
                    print("Unsupported operation.")
            except Exception as e:
                print(f"Error: {str(e)}")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
