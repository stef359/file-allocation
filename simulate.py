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
        return ContiguousAllocation(100)  # Assuming 100 blocks for simplicity
    elif choice == '2':
        return LinkedAllocation(100)
    elif choice == '3':
        return IndexedAllocation(100)
    else:
        print("Invalid choice. Defaulting to Contiguous Allocation.")
        return ContiguousAllocation(100)

def main():
    disk_size = 32  # Adjust based on your disk size requirements
    disk = Disk(disk_size)
    directory = Directory()
    allocation_method = select_allocation_method()

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
            file_name = input("Enter file name: ")
            start = int(input("Enter start block: "))
            length = int(input("Enter length of the file: "))
            if disk.allocate(file_name, start, length):
                directory.add_file(file_name, start, length)
                print(f"File '{file_name}' added successfully.")
            else:
                print("Failed to add file. Please check disk space.")
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
            # Example: Create a file using the selected allocation method
            file_name = input("Enter file name for method-specific operation: ")
            size = int(input("Enter the size of the file in blocks: "))
            if isinstance(allocation_method, ContiguousAllocation):
                allocation_method.create_file(file_name, size)
            elif isinstance(allocation_method, LinkedAllocation):
                start_index = allocation_method.create_file(file_name, size)
                print(f"File created starting at block {start_index}")
            elif isinstance(allocation_method, IndexedAllocation):
                index_block = allocation_method.create_file(file_name, size)
                print(f"File created with index block at {index_block}")
            else:
                print("Unsupported operation.")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
