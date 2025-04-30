import sys
import os
import ctypes.util
import subprocess
from mpi4py import MPI
from lammps import lammps

errors = []

# [1] Check mpi4py version and MPI vendor
try:
    ver = MPI.Get_version()
    lib = MPI.Get_library_version()
    if "Open MPI" not in lib:
        errors.append("mpi4py not linked with Open MPI")
except Exception as e:
    errors.append(f"mpi4py load error: {e}")

# [2] Check linked libmpi.so
try:
    ldd_out = subprocess.run(["ldd", MPI.__file__], capture_output=True, text=True).stdout
    if "/openmpi_" not in ldd_out:
        errors.append("libmpi.so not from expected OpenMPI install")
except Exception as e:
    errors.append(f"libmpi ldd check failed: {e}")

# [3] Check mpicc location
mpicc = subprocess.run(["which", "mpicc"], capture_output=True, text=True).stdout.strip()
if "openmpi" not in mpicc:
    errors.append("mpicc is not from OpenMPI module")

# [4] Check MPI.COMM_WORLD rank/size
try:
    comm = MPI.COMM_WORLD
    _ = comm.Get_rank()
    _ = comm.Get_size()
except Exception as e:
    errors.append(f"MPI.COMM_WORLD error: {e}")

# [5] Check LAMMPS + GPU + Kokkos
try:
    lmp = lammps(cmdargs=['-k','on','g','1','-sf','kk'])
    lmp.close()
    lmp.finalize()
except Exception as e:
    errors.append(f"LAMMPS GPU init failed: {e}")

# Final report
print("\n===== MPI/LAMMPS SANITY CHECK =====")
if errors:
    print("❌ Issues found:")
    for err in errors:
        print(f"   - {err}")
    sys.exit(1)
else:
    print("✅ All checks passed: MPI, mpi4py, mpicc, and LAMMPS GPU interface are OK.")
