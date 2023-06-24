import sys
import re
import argparse


# FIXME: Add regression test documentation.

class TDef:
    def __init__(self, f, has_id=False, has_show=False):
        self.f = f
        self.has_id = has_id
        self.has_show = has_show
        return

    @property
    def name(self):
        return self.f.__name__

    def run(self, args):
        kwargs = {}
        if self.has_id:
            kwargs["test_num"] = args.test_num

        if self.has_show:
            kwargs["show"] = args.show

        self.f(**kwargs)


def run_main(test_list):
    usage = """Usage: %(prog)s [options] tests...

Tests can be regular expressions.  All matching test names will be matched.

Defined tests are:"""

    for t in test_list:
        usage += "\n   " + t.name

    parser = argparse.ArgumentParser(usage=usage)

    parser.add_argument("-s", "--show", default=False, action="store_true",
                        help="Show the results of any geometries built during the test.")

    parser.add_argument("-n", "--test_num", type=int, default=[], action="append",
                        help="For random tests, which random seeds to run. "
                             "Can be given twice to define a beginning and (exclusive) end.")

    parser.add_argument("test_list", nargs="+",
                        help="List tests to execute at the end. These are regular expressions. "
                             "All matching tests will executed.")

    args = parser.parse_args()

    tail_args = args.test_list
    if len(tail_args) == 0:
        parser.print_usage()
        print("\nList test(s) to execute.")
        return

    test_res = [re.compile(tail_arg) for tail_arg in tail_args]

    for test_re in test_res:
        num_found = 0
        for test in test_list:
            if test_re.fullmatch(test.name) is not None:
                print("Running Test " + test.name + "\n")
                # Run test!
                test.run(args)
                print()
                num_found += 1
                break
        if num_found == 0:
            print("\nTest {repr(test_re)} not found.")

    return


def start_end_id(t, def_s, def_e):
    if t is None:
        return def_s, def_e

    if isinstance(t, int):
        return t, t + 1

    if len(t) == 0:
        return def_s, def_e

    if len(t) == 1:
        return t[0], t[0] + 1

    assert len(t) == 2

    return t[0], t[1]
