# txt4print

`txt4print` is a minimalistic tool that is meant for printing small important 
text files recoverable (e.g., private keys).

It creates a pdf file that can be printed out to have an offline copy of 
important files, that can be stores securely and safely (e.g., a bank's safe).
The resulting paper should be recoverable with a basic texteditor by anyone 
with a basic understanding of computers (e.g., a sysop, or a programmer).

**Test your recovery process!**

The script is designed to work on a limited linux system with no network 
connection (for keeping secrets safe).

## Single file binary
This is meant to be used as a single file binary. You can create that using 
`pyinstaller`. On my x86_64 Linux the binary is about 7 MiB big.

    $ pip install pyinstaller
    $ pyinstaller -F txt4print


## Limitations
The script was written for a certain purpose and will not be very useful for 
other files.  It will only work with very small text files with short lines (for longer 
files you will want a different solution anyways, as typing this back is annoying).

Long lines will not be wrapped and be cut of (at about 80 chars). Having many 
unprintable chars will make lines much longer. 
Long files will wrap on multiple pages with no indication on any 
page but the first, which file it is part of.

There is no error correction for single lines, so detecting an error is 
possible by using the checksum, but finding it will be difficult for long files.

This script  will not work on Windows, since the font inclusion trick will not work there.
