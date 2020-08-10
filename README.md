# Factoring Jupyter Notebook

This notebook explains the quantum processing unit (QPU) programming model used 
for factoring, and shows how to implement it using D-Wave Ocean's stack of 
tools.

By the end of this notebook you will have seen how to convert a problem into 
a binary quadratic model for submission to the D-Wave system and be able to modify 
its parameters.

## Usage

To enable notebook extensions:

```bash
jupyter contrib nbextension install --sys-prefix
jupyter nbextension enable toc2/main
jupyter nbextension enable exercise/main
jupyter nbextension enable exercise2/main
jupyter nbextension enable python-markdown/main

```

To run the notebook:

```bash
jupyter notebook
```

## License

Released under the Apache License 2.0. See LICENSE file.
