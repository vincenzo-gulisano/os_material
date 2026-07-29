PANDOC ?= pandoc

SOURCES := organization.md lab1.md lab2.md lab3.md group_allocation_schedule.md
OUTPUT_DIR := compiled
OUTPUTS := $(SOURCES:%.md=$(OUTPUT_DIR)/%.html)

.PHONY: all

all: $(OUTPUTS)

$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

$(OUTPUT_DIR)/%.html: %.md | $(OUTPUT_DIR)
	$(PANDOC) --from=gfm --to=html5 --wrap=none --output=$@ $<
