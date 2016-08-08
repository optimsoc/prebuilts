Built in place on Ubuntu 14.04 using:

    ./configure --prefix=/opt/verilator-<version>
    make
    make installdata

We distribute the source tree (recommended method), but need to
install the data into the proper place. We add the relocate script to
allow moving this to another place.

Relocate to a different path:

    /path/to/extracted/verilator-<version>/relocate.sh
