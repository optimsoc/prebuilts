Built on Ubuntu 14.04 using:

    ./configure --prefix=/opt/verilator-3.880

As we distribute the source tree (recommended method), we needed to
workaround the package config part. Hence verilator.pc is copied to
pkgconfig/ and the include dir replaced for the non-installed version.

Relocate to a different path:

    /path/to/extracted/verilator-3.880/relocate.sh