default: static-files

static-files:
	python -c "from generate_static_files import GenerateStaticFiles; GenerateStaticFiles().main()" generate_static_files.py
run:
	python stremio-addon.py
