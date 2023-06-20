"""
Check style attributes, including cascading.

The rest of the checks will run lots of testing.  Adding this here as a simple check to make sure Styles are working
"""

import random as rnd
from shapely_plotly.tests.utils.utils import rnd_style
from shapely_plotly.tests.utils.run_main import run_main, TDef, start_end_id


def test_styles(test_num=None):
    s, e = start_end_id(test_num, 100, 200)

    for i in range(s, e):
        rnd.seed(i)
        s = rnd_style(rnd.choice((True, False)))  # Create and tests a random style.


test_list = [
    TDef(test_styles, has_id=True)
]

if __name__ == "__main__":
    run_main(test_list)
