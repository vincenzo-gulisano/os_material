#! /bin/sh -e

if test -z "$SRCDIR" || test -z "$PINTOSDIR" || test -z "$DSTDIR"; then
    echo "usage: env SRCDIR=<srcdir> PINTOSDIR=<srcdir> DSTDIR=<dstdir> sh $0"
    echo "  where <srcdir> contains bochs-2.3.7.tar.gz"
    echo "    and <pintosdir> is the root of the pintos source tree"
    echo "    and <dstdir> is the installation prefix (e.g. /usr/local)"
    exit 1
fi

cd /tmp
mkdir bochs-pintos-$$
cd bochs-pintos-$$
mkdir bochs-2.3.7
tar xzf $SRCDIR/bochs-2.3.7.tar.gz
cd bochs-2.3.7
cat $PINTOSDIR/src/misc/0001-bochs-2.3.7-jitter.patch | patch -p1
cat $PINTOSDIR/src/misc/0002-bochs-2.3.7-triple-fault.patch | patch -p1
cat $PINTOSDIR/src/misc/0003-bochs-2.3.7-page-fault-segv.patch | patch -p1
cat $PINTOSDIR/src/misc/bochs-2.3.7-gcc43.patch | patch -p1
cat $PINTOSDIR/src/misc/bochs-2.3.7-typos.patch | patch -p1

CFGOPTIONAL="--enable-large-pages --enable-mmx --enable-usb --enable-pci --enable-pcidev --enable-acpi --enable-global-pages --enable-show-ips"
CFGOPTIMIZE="--enable-all-optimizations --enable-guest2host-tlb --enable-repeat-speedups --enable-trace-cache --enable-icache --enable-fast-function-calls --enable-idle-hack "
CFGOPTS="--prefix=$DSTDIR --enable-ignore-bad-msr --enable-disasm --enable-logging --enable-fpu --enable-alignment-check --enable-plugins --enable-cpu-level=6 --enable-readline --without-sdl --without-svga --without-wx --with-x --with-x11 --with-term --with-nogui $CFGOPTIONAL"
mkdir plain &&
        cd plain && 
        ../configure $CFGOPTS --enable-gdb-stub && 
        make -j3 && 
        make install &&
        cd .. &&
mkdir with-dbg &&
        cd with-dbg &&
        ../configure --enable-debugger $CFGOPTS &&
        make -j3 &&
        cp -v bochs $DSTDIR/bin/bochs-dbg &&
        cd .. &&
        echo "SUCCESS"
