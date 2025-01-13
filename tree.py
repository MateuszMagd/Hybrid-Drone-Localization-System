import os

def print_tree(startpath, indent=''):
    """
    Show folder and file structure
    """
    for item in os.listdir(startpath):
        path = os.path.join(startpath, item)
        print(indent + "|-- " + item)
        if os.path.isdir(path):
            print_tree(path, indent + "|   ")

# Change it to your path
root_folder = "G:\project\Thesis"
print_tree(root_folder)
