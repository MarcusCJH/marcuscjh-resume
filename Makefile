# Local build targets matching IntelliJ / PyCharm run configs:
#   Python.sync_resume -> sync_resume.py
#   LaTeX.resume       -> pdflatex, out/, auxil/, cwd=src

PYTHON ?= python
PDF := out/resume.pdf

.PHONY: help sync pdf build open clean

help:
	@echo.
	@echo   sync    sync sections from data.json
	@echo   pdf     compile out/resume.pdf
	@echo   build   sync + pdf
	@echo   open    open out/resume.pdf
	@echo   clean   remove out/ and auxil/
	@echo.

sync:
	@echo [sync] Updating sections from data.json...
	@$(PYTHON) sync_resume.py
	@echo [sync] Done.

pdf:
	@echo [pdf] Compiling $(PDF)...
	@$(PYTHON) -c "from pathlib import Path; Path('out').mkdir(exist_ok=True); Path('auxil').mkdir(exist_ok=True)"
	@cd src && pdflatex -interaction=nonstopmode -output-directory=../out -aux-directory=../auxil resume.tex >nul
	@echo [pdf] Done: $(PDF)

build: sync pdf
	@echo [build] Done.

open:
	@$(PYTHON) -c "import os, sys; from pathlib import Path; p = Path(r'$(PDF)'); \
	sys.exit('[open] $(PDF) not found. Run: make pdf') if not p.exists() else (os.startfile(str(p.resolve())), print('[open] $(PDF)'))"

clean:
	@echo [clean] Removing out/ and auxil/...
	@$(PYTHON) -c "import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ('out', 'auxil')]"
	@echo [clean] Done.
