export NEWDRAWS_PG_PASSWORD:=<YOUR_POSTGRES_PASSWORD_HERE>

.PHONY: all
all :
	python3.6 artspambot.py

.PHONY: i
i :
	python3.6 -i artspambot.py
