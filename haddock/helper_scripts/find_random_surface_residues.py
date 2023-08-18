from pymol import cmd
from random import sample

def find_random_surface_residues(file, percentage = 0.25):
    cmd.load(file)
    ## Finds atoms on the surface of a protein
    ## Logic from: https://pymolwiki.org/index.php/FindSurfaceResidues
    cutoff = 2.0
    tmpObj = cmd.get_unused_name("_tmp")
    cmd.create(tmpObj, "(all) and polymer", zoom=0)
    cmd.set("dot_solvent", 1, tmpObj)
    cmd.get_area(selection=tmpObj, load_b=1)
    cmd.remove(tmpObj + " and b < " + str(cutoff))
    cmd.select("exposed_atoms", "(all) in " + tmpObj)
    cmd.delete(tmpObj)
    ## Get a list of residue numbers and then subset it
    surface_residues = set()
    cmd.iterate('exposed_atoms', "surface_residues.add(resi)", space=locals())
    # surface_residues = list(surface_residues)
    k = int(len(surface_residues) * percentage)
    surface_residues_sample = list(sample(surface_residues, k))
    surface_residues_sample = [int(x) for x in surface_residues_sample]
    surface_residues_sample.sort()
    ## Reintialize Everything
    cmd.reinitialize(what='everything')
    return surface_residues_sample