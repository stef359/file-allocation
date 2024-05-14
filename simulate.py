import random
from disk_management import Disk, Directory

def select_allocation_method(disk):
    print("Select an allocation method:")
    print("1: Contiguous Allocation")
    print("2: Linked Allocation")
    print("3: Exit Selection")
    choice = input("Enter choice (1-3): ")
    if choice == '1':
        return lambda file_name, start, length: disk.allocate(file_name, start, length)
    elif choice == '2':
        return lambda file_name, size: disk.allocate_randomly(file_name, size)
    else:
        print("Exiting allocation selection.")
        return None

def main():
    disk_size = 500
    disk = Disk(disk_size)
    directory = Directory()
    allocation_method = select_allocation_method(disk)
    next_free_block = 0  # For contiguous allocation

    if allocation_method is None:
        return

    while True:
        print("\nCommands:")
        print("1: Add file")
        print("2: Remove file")
        print("3: Show disk state")
        print("4: Show directory listing")
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
                size = random.randint(1, 10)  # Random size for the file
                if allocation_method.__code__.co_argcount == 3:  # Contiguous allocation
                    start = next_free_block
                    if disk.allocate(file_name, start, size):
                        directory.add_file(file_name, start, size)
                        print(f"File '{file_name}' added successfully at start block {start}.")
                        next_free_block = start + size
                    else:
                        print(f"Failed to add file '{file_name}'. Please check disk space.")
                else:  # Random allocation
                    indices = allocation_method(file_name, size)
                    directory.add_file_non_contiguous(file_name, indices)
                    print(f"File '{file_name}' added successfully across blocks: {indices}")
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
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()