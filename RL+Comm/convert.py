import IPython.nbformat.current as nbf
nb = nbf.read(open('Resource_alloc.py3', 'r'), 'py')
nbf.write(nb, open('Resource_alloc.py3.ipynb', 'w'), 'ipynb')