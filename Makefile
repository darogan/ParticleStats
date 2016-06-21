## Copyright 2015-2016 David Pinto
##
## Copying and distribution of this file, with or without modification,
## are permitted in any medium without royalty provided the copyright
## notice and this notice are preserved.  This file is offered as-is,
## without any warranty.

PACKAGE := $(shell grep -oP "(?<=^\tname = ')[a-zA-Z]+(?=',$$)" setup.py)
VERSION := $(shell grep -oP "(?<=^\tversion = ')[0-9\.]+(?=',$$)" setup.py)

TARGET_DIR      := target
RELEASE_DIR     := $(TARGET_DIR)/$(PACKAGE)-$(VERSION)
RELEASE_TARBALL := $(RELEASE_DIR).tar.gz

.PHONY: help python-package

help:
	@echo "Targets:"
	@echo "   python-package - Create $(RELEASE_TARBALL) for release"

python-package: $(RELEASE_TARBALL)

%.tar.gz: %
	tar -c -f - --posix -C "$(TARGET_DIR)" "$(notdir $<)" | gzip -9n > "$@"

$(RELEASE_DIR): .git/index
	@echo "Creating package version $(VERSION) release ..."
	-$(RM) -r "$@"
	git archive --format=tar --prefix="$@/" HEAD | tar -x
	$(RM) "$@/.gitignore"
	$(RM) "$@/Makefile"
	$(RM) -r "$@/web-interface"
	$(RM) -r "$@/doc"

clean:
	$(RM) -r $(TARGET_DIR)
