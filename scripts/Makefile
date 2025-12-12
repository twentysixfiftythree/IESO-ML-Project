# runs all py files
PY_FILES := $(wildcard *.py)


.PHONY: all
all: $(PY_FILES)
	@for file in $(PY_FILES); do \
		echo "Running $$file..."; \
		python3 $$file; \
	done


%.py:
	python3 $@

# clean target
.PHONY: clean
clean:
	rm -rf __pycache__ *.pyc