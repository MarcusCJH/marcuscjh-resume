# Local build targets:
#   CV     = full dossier (pdfLaTeX)  -> out/cv.pdf
#   Resume = curated one-pager (XeLaTeX) -> out/resume.pdf

PYTHON ?= python
CV_PDF := out/cv.pdf
RESUME_PDF := out/resume.pdf

.PHONY: help sync cv resume pdf build open open-cv open-resume clean

help:
	@echo.
	@echo   sync         sync CV + Resume sections from www.marcuscjh.com/data.json
	@echo   cv           compile out/cv.pdf          (full dossier, pdfLaTeX)
	@echo   resume       compile out/resume.pdf      (curated one-pager, XeLaTeX)
	@echo   pdf          alias for resume
	@echo   build        sync + cv + resume
	@echo   open-cv      open out/cv.pdf
	@echo   open-resume  open out/resume.pdf
	@echo   open         alias for open-resume
	@echo   clean        remove out/ and auxil/
	@echo.

sync:
	@echo [sync] Updating sections (local data.json if present, else remote)...
	@$(PYTHON) sync_resume.py --source auto --target all
	@echo [sync] Done.

cv:
	@echo [cv] Compiling $(CV_PDF)...
	@$(PYTHON) -c "from pathlib import Path; import subprocess, sys; \
	Path('out').mkdir(exist_ok=True); out=str(Path('out').resolve()); \
	r=subprocess.run(['pdflatex','-interaction=nonstopmode',f'-output-directory={out}','cv.tex'], cwd='src'); \
	sys.exit(r.returncode)"
	@echo [cv] Done: $(CV_PDF)

resume:
	@echo [resume] Compiling $(RESUME_PDF)...
	@$(PYTHON) -c "from pathlib import Path; import subprocess, sys; \
	Path('out').mkdir(exist_ok=True); out=str(Path('out').resolve()); \
	r=subprocess.run(['xelatex','-interaction=nonstopmode',f'-output-directory={out}','resume.tex'], cwd='src'); \
	sys.exit(r.returncode)"
	@echo [resume] Done: $(RESUME_PDF)

pdf: resume

build: sync cv resume
	@echo [build] Done.

open-cv:
	@$(PYTHON) -c "import os, sys; from pathlib import Path; p = Path(r'$(CV_PDF)'); \
	sys.exit('[open-cv] missing') if not p.exists() else (os.startfile(str(p.resolve())), print('[open-cv] $(CV_PDF)'))"

open-resume:
	@$(PYTHON) -c "import os, sys; from pathlib import Path; p = Path(r'$(RESUME_PDF)'); \
	sys.exit('[open-resume] missing') if not p.exists() else (os.startfile(str(p.resolve())), print('[open-resume] $(RESUME_PDF)'))"

open: open-resume

clean:
	@echo [clean] Removing out/ and auxil/...
	@$(PYTHON) -c "from pathlib import Path; import shutil; [shutil.rmtree(p, ignore_errors=True) for p in ('out', 'auxil')]"
	@echo [clean] Done.
