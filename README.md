# Chemical Graph Database
In this folder, the code and the accompanying files for the master thesis project 'Design of a Chemical Graph Database : Query on an Atom-Specific Level' of Steven Drenth can be found.

The different parts of the code and their accompanying files are numbered. A number can be followed by ‘-MOLfiles’ or ‘-SMILES’, which indicates the starting dataset that was used. The numbers have the following meaning:
-	A file starting with the number 1 means that this is part of transforming to the Neo4J graph database. 1.1 means that the input is a MOLfile format, 1.2 SMILES format.
-	A file starting with the number 2 means that this is part of querying useful data for Pytorch Geometric out of the graph database of Neo4j. 2.1 and 2.2 are for the transformation to work with the TUData dataloader, 2.3 for working with the heterogeneous dataloader (not done with SMILES set) and 2.4 for working with the MoleculeNet dataloader (not done with SMILES set).
-	A file starting with the number 3 means that this is part of the tests with Pytorch Geometric, using the data output of the previous point. 3.1 and 3.2 are for the TUData, 3.3 for the heterogeneous data (not done with SMILES set) and 3.4 for the MoleculeNet data (not done with SMILES set).

**When running the code, make sure that you run the MOLfiles and SMILES notebooks on DIFFERENT Neo4j databases and that these databases are cleaned and restarted before running the code.**

Below, an explanation of the files that do not start with a number is given:
-	functions.py: python file with additional functions that are called in different notebooks
-	MOL_to_cypher.cypher: cypher file that is written to Neo4j, this is automatically deleted and changed by the Jupyter Notebooks starting with number 1.
-	SMILES.csv: csv file with the SMILES strings and additional information. This is not the original file, as it cannot be shown due to confidential issues
