# img-count-tests
Tests around img-count.py python script

REQUIREMENTS
python 2.7.6

img_count_test.py will import the following:
(These should be included with python 2.7.6)
import unittest
import json
import sys
import subprocess
import time

TO RUN
python img_count_test.py <path>
<path> is the path to img_count.py
If <path> is not specified, we assume that we are running "img_count.py" in the current working directory
