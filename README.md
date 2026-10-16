# Sysroot Export

The script sysroot_export.py extracts the necessary files from a linux rootfs
for cross compiling embedded Linux applications from Windows host.

Currently it is taylored for DQ compiler usage (linking only),
without C hearder files, just the .o, .a, .lib, .so files are copied.

## Creating sysroot

For sysroot creation a Linux host is required, which can be a WSL2 machine too.
For sysroot generation I was using debian trixie trough debootstrap.

### Host preparation
For Ubuntu 26.04 Host
```
apt install qemu-user qemu-user-binfmt debootstrap
```

For Ubuntu 24.04 Host
```
sudo apt install debootstrap qemu-user-static binfmt-support
```
Note: for Ubuntu 24.04, you need to install `qemu-user-static` and later copy `/usr/bin/qemu-aarch64-static`
(or simiar) from the host to `/usr/bin` at the Target sysroot.

### ARM64 Example
```
export TSYSROOT=/lindata/dev_arm/sysroot_arm64_trixie

sudo debootstrap \
  --arch=arm64 \
  --variant=minbase \
  --foreign \
  trixie \
  "$TSYSROOT" \
  https://deb.debian.org/debian

sudo chroot "$TSYSROOT" /debootstrap/debootstrap --second-stage
sudo cp --dereference /etc/resolv.conf "$TSYSROOT/etc/resolv.conf"
```
Ubuntu 24.04 only (not required on Ubuntu 26.04)
```
sudo cp /usr/bin/qemu-aarch64-static "$TSYSROOT/usr/bin/"
```

Enter the target and install the necessary development libraries:
```
sudo chroot "$TSYSROOT" bash
apt update
apt install libc6-dev libstdc++-14-dev pkg-config
apt install default-libmysqlclient-dev
```

### ARMHF Example
```
export TSYSROOT=/lindata/dev_arm/sysroot_armhf_trixie

sudo debootstrap \
  --arch=armhf \
  --variant=minbase \
  --foreign \
  trixie \
  "$TSYSROOT" \
  https://deb.debian.org/debian

sudo chroot "$TSYSROOT" /debootstrap/debootstrap --second-stage
sudo cp --dereference /etc/resolv.conf "$TSYSROOT/etc/resolv.conf"
```
Ubuntu 24.04 only (not required on Ubuntu 26.04)
```
sudo cp /usr/bin/qemu-armhf-static "$TSYSROOT/usr/bin/"
```

Enter the target and install the necessary development libraries:
```
sudo chroot "$TSYSROOT" bash
apt update
apt install libc6-dev libstdc++-14-dev pkg-config
apt install default-libmysqlclient-dev
```

### RISCV64 Example
```
export TSYSROOT=/lindata/dev_riscv/sysroot_riscv64_trixie

sudo debootstrap \
  --arch=riscv64 \
  --variant=minbase \
  --foreign \
  trixie \
  "$TSYSROOT" \
  https://deb.debian.org/debian

sudo chroot "$TSYSROOT" /debootstrap/debootstrap --second-stage
sudo cp --dereference /etc/resolv.conf "$TSYSROOT/etc/resolv.conf"
```
Ubuntu 24.04 only (not required on Ubuntu 26.04)
```
sudo cp /usr/bin/qemu-riscv64-static "$TSYSROOT/usr/bin/"
```
Enter the target and install the necessary development libraries:
```
sudo chroot "$TSYSROOT" bash
apt update
apt install libc6-dev libstdc++-14-dev pkg-config
apt install default-libmysqlclient-dev
```

## Exporting the sysroot for Windows Hosted Cross-Compiling

The previously created sysroots require Linux file system, but the Windows-based dq-comp.exe cannot access theese normally.
(Unless you install ext2fs or similar.) Therefore we need to use this sysroot_export.py script to make the files from Linux sysroot available for dq-comp.exe.

The sysroot_export.py script must be run from Linux environment (so it can access the sysroot files and symlinks propery):

```
python3 sysroot_export.py /lindata/dev_arm/sysroot_armhf_trixie exports/sysroot_armhf_trixie

python3 sysroot_export.py /lindata/dev_arm/sysroot_arm64_trixie exports/sysroot_arm64_trixie

python3 sysroot_export.py /lindata/dev_riscv/sysroot_riscv64_trixie exports/sysroot_riscv64_trixie

```

This repository also contains an `export_all.py` script that creates multiple zip-ed, date-tagged exports.
