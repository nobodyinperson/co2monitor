#!/usr/bin/make -f

# directories
LANGDIR = usr/share/co2monitor/lang
DOCDIR  = usr/share/doc/co2monitor/manpages

# the changelog
CHANGELOG = debian/changelog

# all pofiles
POFILES = $(shell find $(LANGDIR) -type f -iname '*.po')
# the corresponding mofiles
MOFILES = $(POFILES:.po=.mo)

# all markdown manpages
MDMANPAGES = $(shell find $(DOCDIR) -type f -iname '*.1.md')
# corresponding groff manpages
GFMANPAGES = $(MDMANPAGES:.1.md=.1)

# source files that contain translatable text - the _(...) function
# that is, all python files
PYTHONFILES = $(shell find usr -type f -exec file {} \; | perl -ne 'print if s/^([^:]+):.*python.*$$/$$1/ig')

# temporary pot-file template
POTFILE = usr/share/co2monitor/lang/co2monitor.pot

# get information from changelog
CO2MONITORVERSION = $(shell perl -ne 'if(s/^co2monitor\s*\((.*?)\).*$$/$$1/g){print;exit}' $(CHANGELOG))
CO2MONITORDATE    = $(shell perl -ne 'if(s/^\s*--.*@.*,\s*(.*)$$/$$1/g){print;exit}' $(CHANGELOG))

# pandoc options for manpage creation
PANDOCOPTS = -f markdown -t man --standalone -Vfooter='Version $(CO2MONITORVERSION)' -Vdate='$(CO2MONITORDATE)'
 
all: $(MOFILES) $(GFMANPAGES)

# build the manpages
# manpages:
%.1: %.1.md
	pandoc $(PANDOCOPTS) -o $@ $<

# create the pot-file with all translatable strings from the srcfiles
$(POTFILE): $(PYTHONFILES)
	xgettext -L Python -o $(POTFILE) $(PYTHONFILES)

# update the translated catalog
%.po: $(POTFILE)
	VERSION_CONTROL=off msgmerge -U --backup=off $@ $<

# compile the translations
%.mo: %.po
	msgfmt -o $@ $<


.PHONY: clean
clean:
	rm -f $(MOFILES)
	rm -f $(POTFILE)
	rm -f $(GFMANPAGES)


	
