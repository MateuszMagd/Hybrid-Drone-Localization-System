import os

def print_tree(startpath, indent=''):
    """
    Rekurencyjnie drukuje strukturę folderów i plików w formacie drzewa.
    """
    for item in os.listdir(startpath):
        path = os.path.join(startpath, item)
        print(indent + "|-- " + item)
        if os.path.isdir(path):
            print_tree(path, indent + "|   ")

# Podaj ścieżkę do folderu, który chcesz wyświetlić
root_folder = "G:\project\Thesis"
print_tree(root_folder)
