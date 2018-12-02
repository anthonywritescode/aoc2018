EPISODES = $(wildcard day*)
EPISODES_MAKE = $(patsubst %,make-%,$(EPISODES))

all: index.htm $(EPISODES_MAKE)

venv: requirements.txt
	rm -rf venv
	virtualenv venv -ppython3
	venv/bin/pip install -rrequirements.txt
	venv/bin/pre-commit install -f --install-hooks

index.htm: README.md venv
	venv/bin/markdown-code-blocks-highlight $< > $@

%/assets:
	cd $* && ln -s ../assets .

.PHONY: make-%
make-%: %/assets venv
	cd $* && ../venv/bin/markdown-to-presentation run-build

push: venv
	venv/bin/markdown-to-presentation push index.htm */index.htm */build

clean:
	rm -rf index.htm venv */.mtp */assets */build */index.htm

.SECONDARY:
