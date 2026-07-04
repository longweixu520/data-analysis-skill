.PHONY: doctor demo init analyze plot report export validate all

PYTHON ?= python3
PROJECT ?= examples/demo

doctor:
	$(PYTHON) scripts/doctor.py

demo:
	bash scripts/run_demo.sh

init:
	$(PYTHON) scripts/init_project.py $(NAME) --with-sample

analyze:
	$(PYTHON) scripts/check_long_table.py $(PROJECT)/output/02_清洗后长表.csv
	$(PYTHON) scripts/analyze_long_table.py $(PROJECT)/output/02_清洗后长表.csv -o $(PROJECT)/output/

plot:
	$(PYTHON) scripts/plot_delivery.py $(PROJECT)/output/

report:
	$(PYTHON) scripts/generate_report.py $(PROJECT)

export:
	$(PYTHON) scripts/export_workbook.py $(PROJECT)/output/

validate:
	$(PYTHON) scripts/validate_delivery.py $(PROJECT)/output/ --strict --project $(PROJECT)

all: analyze plot report export validate
