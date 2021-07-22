# txt4print

`txt4print` is a minimalistic tool that is meant for printing small important 
text files recoverable (e.g., private keys).

It creates a pdf file that can be printed out to have an offline copy of 
important files, that can be stores securely and safely (e.g., a bank's safe).
The resulting paper should be recoverable with a basic texteditor by anyone 
with a basic understanding of computers (e.g., a sysop, or a programmer).

We do not guaranty anything, if you use this software! There is no warranty!

**Test your recovery process!**

The script is designed to work on a limited linux system with no network 
connection (for keeping secrets safe).

## How does it work?
The script takes a textfile as input and creates a pdf file to be printed 
(yes, on paper). You store that in a safe place.
Should you ever lose all of your digital copies of that file, you take that 
paper from your safe location and type it back into a computer using your keyboard.

On the pdf there are all bytes of the input file printed in a way that they 
can be typed back into a computer using any text editor. Care is taken, so 
that all bytes can be identified. It uses a font with distinctive letters 
(Number zero 0 versus letter O, Number 1 versus lower case L: l and upper case i: I).
Spaces and newlines are printed explicitly. All other non-printable bytes are 
printed as hex numbers. No byte is ignored. For each line a CRC checksum is 
included, so that mistakes can be spotted easily in files with many lines.

The printout contains the name of the file printed, it's size in bytes, and a 
sha256 checksum, so that you can verify you do not make any mistakes typing.
It also has the date and time of printing and a 4 byte random ID. The ID is 
printed on enery page, next to the page number, so that you can easily sort 
pages of multiple printouts if they ever get mixed up.

The printout also contains brief instructions on what it is and how data 
is represented on it. This should allow recreation of the files from the 
printout alone, even when this documentation will no longer be available 
online.

## Examples
Get a feel for what it looks like, here are some examples:
* [An example CA Certificate](examples/example-ca-cert.crt.pdf) ([original file](examples/example-ca-cert.crt)).
* [The CA Certificate's private key](examples/example-ca-cert.key.pdf) ([original file](examples/example-ca-cert.key)) &ndash; encrypted with passphrase "unsecure".
* [The source code of txt4print](examples/txt4print.py.pdf)
* [The source of this README](examples/README.md.pdf)

## Single file binary
This is meant to be used as a single file binary. You can create that using 
`pyinstaller`. On my x86_64 Linux the binary is about 7 MiB big.

    $ pip install pyinstaller
    $ pyinstaller -F txt4print.py

## Advice
* **Do not trust anything I say here!** I am no expert in this area, I just 
  want to solve this problem for myself. If you really depend on what is in 
  your data - go on, read this, fine. Those are thoughts I came up with when 
  thinking about that problem, maybe they help you. **But do not rely on 
  this!** If it is so important, you should seek professional advice.
* **Test your recovery process!** Yes, really. Type the file back into your 
  computer, using only the print out, and a freshly set up computer without 
  any other data from your infrastructure. That is the case you are preparing 
  for here, so make sure that you have everything for that.
* Use a laser printer! Seriously, try printing a page with a laser printer and 
  with an ink printer, and then pour a glass of water over them.
* Use good paper.
* If you print private keys, only print them encrypted. Do you trust my script?
  Even if you do, there is a lot of soft and hardware involved on the way 
  to having the paper in your hand. What about the pdf-viewer? What about the
  printer?
* Think where you print. You might want to skip the public wlan-printer in 
  your co-working place. Do printers keep copies of what they print? I don't 
  know...
* If you have longer files, print single sided. It makes finding mistakes
  a lot more convenient.
* Put the paper in a case that protects it (from viewing, even when put 
  towards light sources - but also from damage; dirt, water, etc). The case 
  should also seal it! You will want to know if anyone opened it and looked 
  at it. Sign the seal with your own handwriting or something - I'm no 
  expert for that...
* Put the paper somewhere that you will have access to in tenth of years, but 
  chose a place that is physically separated from your primary storage. I'm 
  talking kilometers here, natural desasters are a thing, and when your computers 
  all drown in a flood, you do not want your private key backup destroyed with them.
  Do your parents have a safe? How about that? Just hand them an envelope and tell 
  them to keep it really save and never touch it, until you say you need it back.
* Store multiple copies in different places. If it is for your company, keep in mind 
  that desaster might strike when one of you went on holidays - or might have passed 
  away. Those things happen. It is sad enough without your friends taking the 
  company to the grave with them.
* When your keys are encrypted, also store copies of your passphrases! Preferably in 
  places different from the printouts.
* A neat way to build passphrases is [Diceware][diceware].
* You can use a USB-Stick with [Tails Linux][tails] to have a dedicated 
  system for working with your keys. Only keep them there in the persistent 
  storage. `txt4print` was written to be used on a tails system that has no 
  network connections. That's why we needed the single binary version.
* If you want to spread responsibility for your secret keys over multiple 
  people, where e.g., 3 out of 5 people need to come together to use them, 
  take a look at [gfshare][gfshare]. I have not used it myself, but the 
  people making tails use it for their signing keys, see 
  [the tails doc][tailsdoc].
  
[diceware]: https://en.wikipedia.org/wiki/Diceware
[tails]: https://tails.boum.org/
[gfshare]: https://git.gitano.org.uk/libgfshare.git/
[tailsdoc]: https://tails.boum.org/doc/about/openpgp_keys/index.en.html#index2h1

## Limitations
The is no warranty for anything! 

The script was written for a printing small ASCII text files, and will not be very useful 
for other files. It supports long lines and many lines and binary, non-ASCII data, 
but you will not be happy typing those back in.

This script will not work on Windows, since the font inclusion trick will not work there.
