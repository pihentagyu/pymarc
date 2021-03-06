# This file is part of pymarc. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution and at
# https://opensource.org/licenses/BSD-2-Clause. pymarc may be copied, modified,
# propagated, or distributed according to the terms contained in the LICENSE
# file.

import os
import unittest

import pymarc


class MARCUnicodeTest(unittest.TestCase):
    def test_read_utf8(self):
        self.field_count = 0

        def process_xml(record):
            for field in record.get_fields():
                self.field_count += 1

        pymarc.map_xml(process_xml, "test/utf8.xml")
        self.assertEqual(self.field_count, 8)

    def test_copy_utf8(self):
        writer = pymarc.MARCWriter(open("test/write-utf8-test.dat", "wb"))
        new_record = pymarc.Record(to_unicode=True, force_utf8=True)

        def process_xml(record):
            new_record.leader = record.leader

            for field in record.get_fields():
                new_record.add_field(field)

        pymarc.map_xml(process_xml, "test/utf8.xml")

        try:
            writer.write(new_record)
            writer.close()

        finally:
            # remove it
            os.remove("test/write-utf8-test.dat")

    def test_combining_diacritic(self):
        """Issue 74: raises UnicodeEncodeError on Python 2."""
        reader = pymarc.MARCReader(open("test/diacritic.dat", "rb"))
        record = next(reader)
        str(record)


def suite():
    test_suite = unittest.makeSuite(MARCUnicodeTest, "test")
    return test_suite


if __name__ == "__main__":
    unittest.main()
