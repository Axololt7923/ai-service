.PHONY: venv install run clean help clean-all

ifeq ($(OS),Windows_NT)
	GREEN=
	YELLOW=
	RED=
	RESET=
	BLUE=
    PYTHON_VENV=venv\Scripts\python
    UVICORN=venv\Scripts\uvicorn.exe
    PIP_VENV=venv\Scripts\pip
else
	GREEN=\033[1;32m
	YELLOW=\033[1;33m
	RED=\033[1;31m
	RESET=\033[0m
	BLUE=\033[34m

    PYTHON_VENV=venv/bin/python
    UVICORN=venv/bin/uvicorn.exe
    PIP_VENV=venv/bin/pip

endif

PYTHON_VERSION=3.14
VENV_DIR=$(CURDIR)/venv

venv:
	@echo "$(YELLOW)=== Checking and creating virtual environment (venv) ===$(RESET)"
	@if not exist venv (python3.14 -m venv venv && echo "$(GREEN)Created venv!$(RESET)") else (echo "$(YELLOW)venv directory already exists, skipping.$(RESET)")

install: venv
	@echo "$(YELLOW)=== Installing PyTorch (CUDA 12.6) ===$(RESET)"
ifeq ($(OS),Windows_NT)
	@$(PIP_VENV) install torch --index-url https://download.pytorch.org/whl/cu126
else
	
endif
	@echo "$(YELLOW)=== Installing libraries from requirements.txt ===$(RESET)"
	@if exist requirements.txt ( \
		$(PIP_VENV) install -r requirements.txt && echo "$(GREEN)Library installation complete!$(RESET)" \
	) else ( \
		echo "$(RED)Error: requirements.txt not found!$(RESET)" && exit 1 \
	)

run:
	@echo "$(GREEN)=== Starting FastAPI server ===$(RESET)"
	@if exist $(UVICORN) ( \
		$(UVICORN) app.main:app --reload --port 8000 \
	) else ( \
		echo "$(RED)Error: Uvicorn or venv not found. Run 'make install' first!$(RESET)" \
	)

clean:
	@echo "$(YELLOW)=== Cleaning project caches and data ===$(RESET)"
	@if exist chroma_data (rmdir /s /q chroma_data && echo "$(GREEN)Deleted chroma_data$(RESET)")
	@FOR /d /r . %%d in (__pycache__) DO @IF EXIST "%%d" (rmdir /s /q "%%d" && echo "$(GREEN)Deleted %%d$(RESET)")
	@echo "$(CYAN)Cleanup complete! Workspace is clean.$(RESET)"

clean-all: clean
	@echo "$(YELLOW)=== Deep cleaning (removing virtual environment) ===$(RESET)"
	@if exist venv (rmdir /s /q venv && echo "$(GREEN)Deleted venv$(RESET)")
	@echo "$(CYAN)Deep cleanup complete!$(RESET)"

help:
	@echo "$(BLUE)AI-SERVICE Project - Available Commands:$(RESET)"
	@echo ""
	@echo "$(GREEN)Setup & Build:$(RESET)"
	@echo "  	$(YELLOW)make venv$(RESET)        - Check and create virtual environment"
	@echo "  	$(YELLOW)make install$(RESET)     - make venv && install all needed package"
	@echo "=============================================="
	@echo "$(GREEN)Running:$(RESET)"
	@echo "	$(YELLOW)make run$(RESET)         - Start the service"
	@echo "=============================================="
	@echo "$(GREEN)Testing:$(RESET)"
	@echo "		$(RED)---Not available---$(RESET)"
	@echo "=============================================="
	@echo "$(GREEN)Cleaning:$(RESET)"
	@echo "  	$(YELLOW)make clean$(RESET)       - Clean project caches and data"
	@echo "  	$(YELLOW)make clean-all$(RESET)   - $(RED)Clean everything$(RESET)"
	@echo "=============================================="
	@echo "$(GREEN)Environment:$(RESET)"
	@echo "	Virtual environment: $(VENV_DIR)"
	@echo "	Python version required: $(PYTHON_VERSION)"
	@echo "=============================================="
	@echo "$(BLUE)Quick start: make install$(RESET)"