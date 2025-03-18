.PHONY: pdf epub html all clean

all: pdf epub html

pdf:
	pandoc --toc \
	  --template=templates/book.tex \
	  --pdf-engine=lualatex \
	  --filter pandoc-crossref \
	  -o book.pdf \
	  metadata.yaml \
	  chapters/*.md

epub:
	pandoc --toc \
	  --epub-cover-image=images/generated/book_cover.png \
	  --filter pandoc-crossref \
	  -o book.epub \
	  metadata.yaml \
	  chapters/*.md

html:
	pandoc --toc \
	  --template=templates/book.html \
	  --filter pandoc-crossref \
	  --self-contained \
	  -o book.html \
	  metadata.yaml \
	  chapters/*.md

clean:
	rm -f book.pdf book.epub book.html