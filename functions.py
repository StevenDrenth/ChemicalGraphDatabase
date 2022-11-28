from rxnmapper import RXNMapper
from rdkit import Chem
import itertools
from rdkit.Chem import rdChemReactions

def ringinfo(rdmol):
    """
    This function checks if there are rings in the given molecule. If there are any, it checks if they are aromatic,
    if there are aromatic rings with overlapping atoms they're identified as aromatic systems.
    
    The function returns the following:
    ringlst: a list with all ring names and their size in amount of atoms
    asys: a dictionary of the aromatic systems, where the key is the ring/system name and the value the atoms that are in it.
    arings: a dictionary of the aromatic rings, where the key is the ring/system name and the value the atoms that are in it.
    rings: a dictionary of the rings, where the key is the ring/system name and the value the atoms that are in it.
    
    Parameters
    --------------
    rdmol: RDkit format, created from a MOLfile
    """
    
    # Get a list of all aromatic atoms in the molecule
    arom = []
    for m in rdmol.GetAromaticAtoms():
        arom.append(m.GetIdx())

    # Create a list of lists of all rings in the molecule     
    allring = list(list(n) for n in Chem.GetSymmSSSR(rdmol)) 

    # Create initial variables
    asys = {} # Dict for all aromatic rings
    arings = {} # Dict for all aromatic systems
    rings = {} # Dict for all other rings
    skip = [] # All rings in this list are skipped
    ringlst = [] # List of created ringnames and size (number of atoms)
    acnt = 1 # Counts the number of created aromatic rings
    rcnt = 1 # Counts the number of created other rings
    ascnt = 1 # Counts the number of created aromatic systems

    # The first for loop loops over all rings
    for ring in Chem.GetSymmSSSR(rdmol):
        ring = list(ring)

        # Remove the current ring from the allring list
        if ring in allring:
            allring.remove(ring)
            
        # Create one list of the allring list of lists
        rest = list(itertools.chain.from_iterable(allring)) 

        # Checks if the atoms in the current ring overlap with atoms of all other rings and if it's aromatic
        if (len(set(ring) & set(rest)) > 0) & set(ring).issubset(arom):
            for r in allring:
                
                # Checks if the current ring and ring r have shared atoms and if they're both aromatic
                if set(ring).issubset(arom) & set(r).issubset(arom) & ((len(set(ring) & set(r)) > 0)):
                    check = 0 
                    
                    # Loop over all rings in the asys dictionary
                    for name in asys:
                        # If the current ring is part of an existing aromatic system it is added to this
                        if (len(set(ring) & set(asys[name])) > 0):
                            check = 1
                            asys.update({name:asys[name]+ring})
                            
                    # If the ring is part of a new aromatic system, it is created
                    if check == 0:
                        name = 'aromaticsystem'+'_'+str(ascnt) # Create system name
                        asys.update({name:ring+r}) # Add system name + atoms to the dict
                        skip = skip + r # the ring r is added to the skip list (cannot be a (aromatic) ring because it is in a system)
                        ringlst.append(name) # Name of the system is appended
                        ascnt += 1

        # If the ring is already part of an aromatic system, it cannot be part of a (aromatic) ring and it is skipped
        elif set(ring).issubset(skip):
            pass

        # Checks if the current ring is aromatic
        elif set(ring).issubset(arom):
            check = 0
        
            # If the current ring is in an existing aromatic system, it is added to it
            for name in asys:
                if (len(set(ring) & set(asys[name])) > 0):
                    check = 1
                    asys.update({name:asys[name]+ring})
        
            # If the current ring is not part of an aromatic system it is added as aromatic ring
            if check == 0:
                name = 'aromatic'+'_'+str(acnt) # Create ring name
                ringlst.append([name, len(ring)]) # Name of the ring + size is appended
                arings.update({name:ring}) # Add ring name + atoms to the dict
                acnt += 1

        # If the ring isn't aromatic, it is a regular ring
        else:
            name = 'ring'+'_'+str(rcnt) # Create ring name
            ringlst.append([name, len(ring)]) # Name of the ring + size is appended
            rings.update({name:ring}) # Add ring name + atoms to the dict
            rcnt += 1

    # For loop to calculate the size of the aromatic systems
    rlst = ringlst.copy() # Copy the ringlst, as the ringlst will be altered
    for n_r in rlst:
        if 'aromaticsystem' in n_r:
            name = n_r
            # Remove the aromatic system name and add the name+size
            ringlst.remove(name)
            asys.update({name:list(set(asys[name]))})
            ringlst.append([name, len(asys[name])])

    return ringlst, asys, arings, rings

def to_int(df):
    """
    For each column of the dataframe, check if it's a string, if so, replace by numbers
    """
    for col in df.columns:
        first = df[col].dropna().unique()[0]
        if type(first) == str:
            lst = [i for i in range(1, df[col].dropna().nunique()+1)] # Create list of integer
            df[col] = df[col].replace(list(df[col].dropna().unique()), lst) # Replace string by integers
    return df