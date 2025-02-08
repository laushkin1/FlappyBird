default:
	@make run

run:
	python3 game/set_settings.py 2
	python3 main.py

small:
	python3 game/set_settings.py 1
	python3 main.py

init:
	pip3 install pygame

