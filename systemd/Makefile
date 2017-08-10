SERVICEFILES := $(wildcard $(CURDIR)/*.service $(CURDIR)/*.timer)
NOTDIR_SERVICEFILES := $(notdir $(SERVICEFILES))

all: restart

install:
	@for file in $(SERVICEFILES) ; do \
		echo 'installing: ' $$file ; \
		sudo install -m 600 $$file /etc/systemd/system/ ; \
	done
	@sudo systemctl daemon-reload

enable: install
	@for file in $(NOTDIR_SERVICEFILES) ; do \
		echo 'enabling: ' $$file ; \
		sudo systemctl enable $$file ; \
	done

start restart: enable
	@for file in $(NOTDIR_SERVICEFILES) ; do \
		echo 'restarting: ' $$file ; \
		sudo systemctl restart $$file ; \
	done
