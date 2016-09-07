# Run a local mod_wsgi server
export PYTHONPATH=${PYTHONPATH}:..
python3.4 -m dashlivesim.mod_wsgi.mod_dashlivesim $*
