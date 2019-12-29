default: static-files

static-files:
	python generate_static_files.py	

run:
	python stremio-addon.py
