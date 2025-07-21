# Using DARWIN

First, `ssh` into DARWIN.

    ssh <email>@darwin.hpc.udel.edu

Then, go into the `knot` workgroup.

    workgroup -g knot

Then, request a partition.

    salloc --partition=standard --nodes=<# of nodes>

You should see something along the following:

    salloc: Granted job allocation 5573675
    salloc: Waiting for resource configuration
    <small pause>
    salloc: Nodes r1n03 are ready for job

Now, make sure that Python is set to 3.13.1.

    vpkg_require python/3.13.1

You should be in the home `~` directory. Enter `ls` to check if
the `unknotter` directory exists. If not, pull the git repository
from GitHub.

    git clone https://github.com/wh-taylor/unknotter.git

You can now run Python files normally.

    python3 <file>

To utilize DARWIN's nodes, use `srun` before your desired command.

    srun python3 <file>

To use `generate.py` with DARWIN effectively, use the following format:

    srun python3 generate.py <# knots> <# crossings> <data size> >> <csv file name>

Note that running this on `n` nodes will result in a total of
`<data size> * n` diagrams being generated. So, if you are running
12 nodes and want to generate 300,000 knot diagrams, use a data size
of 25,000.

Also. note the use of `>>`. Since multiple nodes are running this
command simultaneously, we want each of them to append onto the same
file one after another instead of overwriting.