PYTHON = python
POETRY ?= poetry

.PHONY: init
init:
	$(POETRY) install

.PHONY: update
update:
	$(POETRY) lock
	$(POETRY) install

.PHONY: run
run:
	@$(POETRY) run main

.PHONY: loop
loop:
	@$(POETRY) run loop
