SHELL := /bin/bash

install:
	cp statusline.conf ~/.claude/statusline.conf
	cp settings.conf ~/.claude/settings.conf
	cp CLAUDE.md ~/.claude/CLAUDE.md

# ローカルの.claudeから設定を取得し、差分を表示→設定を取得するかどうかを選択する
import-settings:
	@diff_output=$$(diff ~/.claude/statusline.py ./statusline.py 2>/dev/null; \
	                diff ~/.claude/settings.json ./settings.json 2>/dev/null; \
	if [ -z "$$diff_output" ]; then \
	    echo "差分はありません。"; \
	    exit 0; \
	fi; \
	echo "=== statusline.py ===" && git diff --no-index --color=always ~/.claude/statusline.py ./statusline.py || true; \
	echo "=== settings.json ===" && git diff --no-index --color=always ~/.claude/settings.json ./settings.json || true; \
	echo "" && printf "上記の差分を取り込みますか？ (y/n): "; \
	read -n 1 -s answer && echo; \
	if [ "$$answer" = "y" ]; then \
	    cp ~/.claude/statusline.py ./statusline.py; \
	    cp ~/.claude/settings.json ./settings.json; \
	    echo "設定を取得しました。"; \
	else \
	    echo "設定の取得をキャンセルしました。"; \
	fi