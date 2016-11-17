#!/usr/bin/make -f

DOCDIR = usr/share/co2monitor/lang

# all pofiles
POFILES = $(shell find $(DOCDIR) -type f -iname '*.po')
# the corresponding mofiles
MOFILES = $(POFILES:.po=.mo)
 
all: $(MOFILES)

# build the manpages
# manpages:

# compile the translations
%.mo: %.po
	msgfmt -o $@ $<


.PHONY: clean
clean:
	rm -f $(MOFILES)


	
