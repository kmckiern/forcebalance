import numpy as np
import os
from forcebalance.nifty import _exec
from forcebalance.gmxio import GMX
from forcebalance.gmxio import rm_gmx_baks
from forcebalance.gmxio import write_ndx

# I can't figure out how to import, and then use this function without creating a GMX object (which would need to run an MD sim, etc).  I already have the trjs, and simply want to use gmx analysis tools in an automated way.
def callgmx(command, stdin=None, print_to_screen=False, print_command=False, **kwargs):
    """ Call GROMACS; prepend the gmxpath to the call to the GROMACS program. """
    ## Always, always remove backup files.
    rm_gmx_baks(os.getcwd())
    ## Call a GROMACS program as you would from the command line.
    csplit = command.split()
    prog = os.path.join(self.gmxpath, csplit[0])
    csplit[0] = prog + self.gmxsuffix
    return _exec(' '.join(csplit), stdin=stdin, print_to_screen=print_to_screen, print_command=print_command, **kwargs) 

def valid8():
    # Remove jumps in trajectory due to pbc.
    callgmx("trjconv -s lipid-md.tpr -f lipid-md.trr -pbc mol -o trjout_pbcmol.gro", stdin="System\n")

    # Lateral lipid diffusion
    # Requires p8.ndx file to already exist in dir.
    # self.write_ndx(p8.ndx, "P8")
    callgmx("g_msd -s lipid-md.tpr -f trjout.gro -n p8.ndx -lateral z -o lld.dat", stdin="P8\n")

    # Membrane density
    # Requires headgroup and tail index files.
    callgmx("g_density -s lipid-md.tpr -f trjout.gro -n dppc_density_groups.ndx -o rho_hg.xvg", stdin="Headgroups\n")
    callgmx("g_density -s lipid-md.tpr -f trjout.gro -n dppc_density_groups.ndx -o rho_t.xvg", stdin="Tails\n")
    callgmx("g_density -s lipid-md.tpr -f trjout.gro -o rho_water.xvg", stdin="Water\n")

    # Electron Density Profile
    # Requires electrons.dat (file which describes the number of electrons for each type of atom).
    callgmx("g_density -s lipid-md.tpr -f trjout.gro -ei elec.dat -dens electron -d z -symm -o rhoelec.xvg", stdin="System\n")
    callgmx("g_density -s lipid-md.tpr -f trjout.gro -ei elec.dat -dens electron -d z -symm -n dppc_density_groups.ndx -o rhoelec_hg.xvg", stdin="Headgroups\n")
    callgmx("g_density -s lipid-md.tpr -f trjout.gro -ei elec.dat -dens electron -d z -symm -n dppc_density_groups.ndx -o rhoelec_t.xvg", stdin="Tails\n")
    callgmx("g_density -s lipid-md.tpr -f trjout.gro -ei elec.dat -dens electron -d z -symm -o rhoelec_water.xvg", stdin="Water\n")

    # I think all of the following distances are found from the EDP/structure factor.
    # Luzzati thickness
    # Hydrophobic thickness
    # Headgroup distances
    # Thermal area expansivity
    # Thermal contractivity

if __name__ == '__main__':
    valid8()
