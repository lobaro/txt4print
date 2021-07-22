#!/usr/bin/env python3
import base64
import datetime
import hashlib
import os.path
import random
import string
import sys
import tempfile

from fpdf import FPDF
from font import FONT_REGULAR, FONT_BOLD

printable = string.ascii_letters + string.digits + string.punctuation
printable_byte = printable.encode()

__version__ = "0.1"

def calc_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for i in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.regular = None
        self.bold = None
        self.alias_nb_pages("ä")
        self.load_font()

        self.font_regular()
        self.ln_width = self.get_string_width("0000 ")
        self.content_width = self.get_string_width("x"*80 + " ")
        self.crc_width = self.get_string_width("0000")
        self.total_width = self.get_string_width("a"*(5+80+5))
        m = (self.w - self.total_width) / 2
        self.set_margins(m, 10, m)

    def load_font(self):
        self.regular = tempfile.NamedTemporaryFile()
        self.regular.write(base64.b64decode(FONT_REGULAR))
        self.add_font('Font', '', self.regular.name, uni=True)
        self.bold = tempfile.NamedTemporaryFile()
        self.bold.write(base64.b64decode(FONT_BOLD))
        self.add_font('Font', 'B', self.bold.name, uni=True)

    def font_regular(self, size=10):
        self.set_font("Font", "", size)

    def font_bold(self, size=10):
        self.set_font("Font", "B", size)

    def footer(self):
        self.font_regular()
        self.set_y(-15)
        self.set_x(self.l_margin)
        self.cell(0, 4, self.fname)
        self.set_y(-15)
        self.set_x(self.l_margin)
        self.cell(self.total_width, 4, self.ident + " - " + str(self.page_no()) + "/ä", 0, 0, "R")

    def text_line(self, s, bold=False):
        if bold:
            self.font_bold()
        else:
            self.font_regular()
        self.cell(0, 4, "     " + s, 0, 1)

    def to_line(self, raw):
        cs = []
        for b in raw:
            if b == ord(" "):
                cs.append('·')
            elif b == ord("\n"):
                cs.append('¶')
            elif b in printable_byte:
                cs.append(chr(b))
            else:
                cs.append(r'¿{0:02x}'.format(b))
        return "".join(cs)

    def do(self, fpath):
        self.ident = "".join(["%02x" % random.randint(0, 0xff) for _ in range(4)])
        self.date = datetime.datetime.now().replace(microsecond=0).isoformat()
        fname = os.path.basename(fpath)
        self.fname = fname
        with open(fpath, "rb") as f:
            raw = f.read()
            l = len(raw)
            sha = hashlib.sha256(raw).hexdigest()

        self.add_page()
        self.font_bold()
        self.text_line("=== File printout ===", True)
        self.text_line("File name:    %s" % fname)
        self.text_line("File size:    %d bytes" % l)
        self.text_line("File sha256:  %s" % sha)
        self.text_line("Printed:      %s         Pages: ä         Random ID: %s" % (self.date, self.ident))
        self.ln()
        self.text_line('Bytes are printed as ASCII chars if possible. Spaces (0x20) are printed as "·",')
        self.text_line('newlines (0x0a) are printed as "¶". All other bytes are printed as "¿xx", with ')
        self.text_line('"xx" being the value of the byte as hex number, e.g., "¿09" for a tab, "¿0d" for')
        self.text_line('a carriage return.')
        self.text_line("Text printed in bold is not part of the file. On the left is the line number, on")
        self.text_line("right a per line checksum (CRC-16-IBM). Lines longer than 80 chars are wrapped.")
        self.ln()
        self.text_line("Created with txt4print version " + __version__ + " - for additional information see")
        self.text_line("https://github.com/lobaro/txt4print")
        self.ln()
        self.text_line("================ BEGIN OF FILE =================================================", True)
        raw_lines = raw.splitlines(True)
        if raw_lines[-1][-1] == ord(b'\n'):
            raw_lines.append(b"")
        for n, raw_line in enumerate(raw_lines):
            crc = calc_crc(raw_line)
            line = self.to_line(raw_line)
            self.font_bold()
            self.cell(self.ln_width, 4, "%04d" % (n+1), 0, 0)
            self.font_regular()
            while len(line) > 80:
                self.cell(self.content_width, 4, line[:80], 0, 1)
                self.cell(self.ln_width, 4, "     ", 0, 0)
                line = line[80:]
            self.cell(self.content_width, 4, line, 0, 0)
            self.font_bold()
            self.cell(self.crc_width, 4, "%04x" % crc, 0, 1)
        self.text_line("================  END OF FILE  =================================================", True)

        self.output(fname + ".pdf")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        pdf = PDF()
        pdf.do(sys.argv[1])
    else:
        print("txt4print v"+__version__+" - Basic text file printing tool")
        print("Create a pdf for printing out files so that they can be recovered.")
        print("See https://github.com/lobaro/txt4print for more information.")
        print("This will only work well with small text files with short lines.")
        print("Usage: %s <filename>" % sys.argv[0])
