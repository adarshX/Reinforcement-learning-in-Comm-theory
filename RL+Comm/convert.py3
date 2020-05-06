from nbformat import current 
nb = current.read(open('Resource_alloc.py3', 'r'), 'py')
current.write(nb, open('Resource_alloc.py3.ipynb', 'w'), 'ipynb')