rm -fr build ~/fe_work; ./tools/build_ttrpg.py -j0 -g -m "$1"; find . -name "*_*.pdf" -delete; echo "Done"
