# -- Imports --------------------------------------------------------------------------

from benchmarker import Benchmarker

# -------------------------------------------------------------------------- Imports --


# -- PublicFunctions --------------------------------------------------------------------------


def string_bench():
    """
    Run a benchmark and print the results.
    https://pythonhosted.org/Benchmarker/
    """
    with Benchmarker(1000 * 1000, width=20) as bench:
        s1, s2, s3, s4, s5 = "Haruhi", "Mikuru", "Yuki", "Itsuki", "Kyon"

        @bench('empty-loop')
        def _(bm):
            for i in bm:
                pass

        @bench("string-join")
        def _(bm):
            for i in bm:
                sos = ''.join((s1, s2, s3, s4, s5))

        @bench("string-concat")
        def _(bm):
            for i in bm:
                sos = s1 + s2 + s3 + s4 + s5

        @bench("string-format")
        def _(bm):
            for i in bm:
                sos = '%s%s%s%s%s' % (s1, s2, s3, s4, s5)

# -------------------------------------------------------------------------- PublicFunctions --
