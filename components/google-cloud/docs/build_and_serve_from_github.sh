# run from components/google-cloud
pip3 install -e "..[docs]"
sphinx-build -M html "source" $builddir
pushd $builddir/html
python3 -m http.server
popd