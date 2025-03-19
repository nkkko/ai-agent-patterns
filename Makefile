.PHONY: pdf epub html all clean simple-pdf clean-pdf clean-epub clean-html clean-all very-simple-pdf debug-pdf check-pdf-engine

# Define common variables
PANDOC = pandoc
TOC = --toc
SYNTAX = --syntax-definition=templates/python.xml
HIGHLIGHT = --highlight-style=templates/python-highlight.theme
CROSSREF = --filter pandoc-crossref
MERMAID = --filter mermaid-filter
METADATA = metadata.yaml
CHAPTERS = $(shell find chapters -name "*.md" | sort)
ALL_CHAPTERS = $(shell find chapters -name "*.md" -not -name "README.md" | sort)

# Detect available PDF engines
HAS_XELATEX := $(shell which xelatex > /dev/null 2>&1 && echo yes || echo no)
HAS_LUALATEX := $(shell which lualatex > /dev/null 2>&1 && echo yes || echo no)
HAS_PDFLATEX := $(shell which pdflatex > /dev/null 2>&1 && echo yes || echo no)

# Set PDF engine based on availability
ifeq ($(HAS_XELATEX),yes)
  PDF_ENGINE = --pdf-engine=xelatex
else ifeq ($(HAS_LUALATEX),yes)
  PDF_ENGINE = --pdf-engine=lualatex
else ifeq ($(HAS_PDFLATEX),yes)
  PDF_ENGINE = --pdf-engine=pdflatex
else
  PDF_ENGINE = --pdf-engine=xelatex
endif

# Common pandoc options
SIMPLE_PDF_OPTS = $(TOC) $(PDF_ENGINE) --no-highlight --top-level-division=chapter --number-sections --shift-heading-level-by=-1
PDF_OPTS = $(TOC) --template=templates/book.tex $(PDF_ENGINE) $(SYNTAX) $(HIGHLIGHT) $(CROSSREF) --number-sections
EPUB_OPTS = $(TOC) $(SYNTAX) $(HIGHLIGHT) $(CROSSREF)
HTML_OPTS = $(TOC) --template=templates/book.html $(SYNTAX) $(HIGHLIGHT) $(CROSSREF) --self-contained

# Main targets
all: pdf epub html

# Check that at least one PDF engine is available
check-pdf-engine:
	@if [ "$(HAS_XELATEX)" = "no" ] && [ "$(HAS_LUALATEX)" = "no" ] && [ "$(HAS_PDFLATEX)" = "no" ]; then \
		echo "Error: No PDF engine (xelatex, lualatex, or pdflatex) found in PATH"; \
		echo "Please install TeX Live, MacTeX, or another TeX distribution"; \
		echo "For macOS: brew install --cask mactex"; \
		echo "For Ubuntu: apt-get install texlive-xetex texlive-latex-extra"; \
		exit 1; \
	else \
		echo "Using PDF engine: $(PDF_ENGINE)"; \
	fi

pdf: check-pdf-engine
	$(PANDOC) $(PDF_OPTS) -o book.pdf $(METADATA) $(CHAPTERS)

epub:
	$(PANDOC) $(EPUB_OPTS) $(MERMAID) -o book.epub $(METADATA) $(ALL_CHAPTERS)

html:
	$(PANDOC) $(HTML_OPTS) $(MERMAID) -o book.html $(METADATA) $(ALL_CHAPTERS)

# Clean targets
clean:
	rm -f book.pdf book.epub book.html book_simple.pdf book_clean.pdf book_clean.epub book_clean.html very_simple.pdf *.bak

# Alternative PDF formats
simple-pdf: check-pdf-engine
	$(PANDOC) $(TOC) --template=templates/simple_book.tex $(PDF_ENGINE) -o book_simple.pdf $(METADATA) $(ALL_CHAPTERS)

very-simple-pdf: check-pdf-engine
	$(PANDOC) $(SIMPLE_PDF_OPTS) -o very_simple.pdf $(METADATA) $(CHAPTERS)

# Clean format targets
clean-pdf: check-pdf-engine
	$(PANDOC) $(PDF_OPTS) -o book_clean.pdf $(METADATA) $(CHAPTERS)

clean-epub:
	$(PANDOC) $(EPUB_OPTS) -o book_clean.epub $(METADATA) $(CHAPTERS)

clean-html:
	$(PANDOC) $(HTML_OPTS) -o book_clean.html $(METADATA) $(CHAPTERS)

clean-all: clean-pdf clean-epub clean-html
	@echo "All clean formats have been generated."

# Debug target
debug-pdf: check-pdf-engine
	$(PANDOC) $(TOC) --template=templates/book.tex $(PDF_ENGINE) $(SYNTAX) $(HIGHLIGHT) $(CROSSREF) --top-level-division=chapter -o book.tex $(METADATA) $(CHAPTERS)
	sed -i.bak 's/\\section{/\\chapter{/g' book.tex
	sed -i.bak 's/\\subsection{/\\section{/g' book.tex
	sed -i.bak 's/\\subsubsection{/\\subsection{/g' book.tex
	sed -i.bak 's/\\numberline {0\./\\numberline {/g' book.tex