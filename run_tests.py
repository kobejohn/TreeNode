import nose
import sys

argv = sys.argv[:]
argv.insert(1, "-m unittest discover -s test -p *.py")
nose.main(argv=argv)