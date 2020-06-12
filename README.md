# xhc_receiver
This is a python "driver" to use XHC CNC pendants with serial port controlled
CNC machines.

This driver interprets the pendant inputs onto predefined actions
and sends configurable commands over the serial port.

**Notice**: This driver only supports the XHC WHB04B-6/HB04B-6 pendant for now.
The WHB04B-4/HB04B-4 pendant _should_ work with this driver because
it has the same base functionality, **but it's untested**.

# Installation
Download the latest release from the releases section (or clone the 
repository) and extract it to wherever you want it.

## Dependencies
This driver requires [Python 3](https://python.org),
the [_hidapi_](https://github.com/libusb/hidapi) library and
the Python3 _hidapi_ wrapper library [hid](https://github.com/apmorton/pyhidapi)

### Installing the HIDAPI library

#### Linux
On linux search your distribution repos for _hidapi_ or _libhidapi_ and 
install it.

You may find variations like _libhidapi-hidraw_ and _libhidapi-libusb_,
which are wrappers arround different usb libraries. If you choose the 
[_libusb_](https://libusb.info) backend, you'll also need to install it.

#### Windows
On Windows, the easiest way is to download the pre-compiled binaries from
the [releases section](https://github.com/libusb/hidapi/releases) and copy the
_hidapi.dll_ files from the _x64_ and _x86_ directories to C:\Windows\SysWOW64
and C:\Windows\System32, respectively.

#### OSX
There are no current binary distributions of _hidapi_ for OSX, so you'll
have to see the [hidapi's README file](https://github.com/libusb/hidapi#mac)
for instructions on how to build from source.

# Usage
***This driver is still in alpha development, so this information may become
inacurate with further development***

To run this driver simply start the _main.py_ and _actions.py_ scripts.

### Using Linux
On linux you'll need to run the scripts as root, otherwise it
cannot connect to the pendant on use the serial port.

# License
This project is licensed under the MIT license. To view the full license text,
see the [LICENSE](/LICENSE.md) file.
