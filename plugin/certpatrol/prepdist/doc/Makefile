# typical usage: just edit the pht file, then make

PREP = ../bin/prep

.SUFFIXES:	.pht .html

.pht.html:
	# $(PREP) D $*.pht >$*.de.html
	# $(PREP) E $*.pht >$*.en.html
	$(PREP) $*.pht >$*.html

all:	*.html

