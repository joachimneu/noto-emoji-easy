.PHONY: noto-emoji-easy, clean, all

noto-emoji-easy:
	./src/noto-emoji-easy/generate.py
	./src/package.sh noto-emoji-easy

clean-noto-emoji-easy:
	rm -rf packages/pdf-noto-emoji-easy
	rm -f packages/noto-emoji-easy.*
	rm -rf dist/noto-emoji-easy
	rm -f dist/noto-emoji-easy.zip

clean:
	rm -rf packages
	rm -rf dist

all: clean noto-emoji-easy
