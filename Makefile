# Find all .tex files in subdirectories (excluding hidden directories)
TEX_FILES := $(shell find . -name "*.tex" -not -path "./.*/*" -not -path "./tools/*")

# Generate corresponding PDF targets
PDF_FILES := $(TEX_FILES:.tex=.pdf)

# Extract directory names for directory-specific targets
DIRS := $(sort $(dir $(TEX_FILES)))
DIRS := $(DIRS:/=)

# Default target - compile all PDFs
all: $(PDF_FILES)

# Compile all PDFs in a specific directory
$(DIRS):
	@$(MAKE) $(addsuffix .pdf,$(basename $(wildcard $@/*.tex)))

# Pattern rule to compile PDFs from .tex files
%.pdf: %.tex
	@mkdir -p "$(dir $@)"
	@echo "Compiling $<..."
	@$(GIT_REPO)/tools/compile_latex.sh -f "$<" -n "$(notdir $@)"
	@echo "Generated: $@"

# Compile specific PDF
%: %.tex
	@$(MAKE) "$@.pdf"

# Clean generated PDFs
clean:
	@find . -name "*.pdf" -not -path "./.*/*" -not -path "./tools/*" -delete
	@echo "Cleaned all PDF files"

# Clean specific directory
clean-%:
	@find $* -name "*.pdf" -delete 2>/dev/null || true
	@echo "Cleaned PDF files in $*"

# List all available targets
list:
	@echo "All .tex files found:"
	@$(foreach file,$(TEX_FILES),echo "  $(file:.tex=)";)

# Help target
help:
	@echo "Available targets:"
	@echo "  all          - Compile all PDFs (default)"
	@echo "  clean        - Remove all generated PDFs"
	@echo "  clean-<dir>  - Clean PDFs in specific directory"
	@echo "  rebuild      - Clean and rebuild all PDFs"
	@echo "  list         - List all available .tex files"
	@echo "  help         - Show this help"
	@echo ""
	@echo "You can also compile individual files:"
	@echo "  make path/to/file       - Compile path/to/file.tex"
	@echo "  make path/to/directory  - Compile all .tex files in directory"

# Rebuild all
rebuild: clean all

# Phony targets
.PHONY: all clean rebuild help list $(DIRS) clean-%

# Prevent make from deleting intermediate files
.SECONDARY:

