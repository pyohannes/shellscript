find . -name "__pycache__" -exec rm -rv {} \;
find . -name "*.pyc" -exec rm -v {} \;
rm -rf doc/out
