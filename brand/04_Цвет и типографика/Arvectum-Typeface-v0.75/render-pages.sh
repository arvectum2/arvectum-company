#!/bin/bash
set -euo pipefail
repo="$(git rev-parse --show-toplevel)"
p="$repo/brand/04_Цвет и типографика/Arvectum-Typeface-v0.75"
list="$(mktemp /tmp/arvectum-v075-fonts.XXXXXX)"
cleanup(){
 while IFS= read -r f; do [ ! -f "$f" ] || rm -f -- "$f";done < "$list"
 rm -f "$list"
 /usr/bin/osascript -e 'tell application "Pages" to if (count of documents) is 0 then quit' >/dev/null 2>&1 || true
 echo 'FONT_TEST_COPIES_CLEANED'
}
trap cleanup EXIT
if pgrep -x Pages >/dev/null;then n=$(/usr/bin/osascript -e 'tell application "Pages" to count documents');[ "$n" = 0 ] || { echo "USER_PAGES_DOCUMENTS_OPEN_$n";exit 4; };fi
for st in Display Text;do
  typ=Regular;[ "$st" != Display ] || typ=Medium
  name="Arvectum${st}GoldenStepDraft064-${typ}.otf"
  src="$repo/brand/04_Цвет и типографика/Arvectum-Typeface-v0.64/experimental/$name"
  dst="$HOME/Library/Fonts/$name"
  [ -s "$src" ] && [ ! -e "$dst" ] || { echo "SOURCE_MISSING_OR_ALREADY_INSTALLED_$name";exit 5; }
  cp -- "$src" "$dst";printf '%s\n' "$dst" >> "$list"
done
/usr/bin/open -a /Applications/Pages.app
sleep 2
/usr/bin/osascript "$p/export-pages.applescript" "$p/Arvectum-Brandbook-Typography-DRAFT-v075.docx" "$p/proofs/Brandbook-Typeface-v075-Pages.pdf"
test -s "$p/proofs/Brandbook-Typeface-v075-Pages.pdf"
pdfinfo "$p/proofs/Brandbook-Typeface-v075-Pages.pdf" | grep -E '^Pages:|^Page size:'
pdffonts "$p/proofs/Brandbook-Typeface-v075-Pages.pdf" | grep 'Arvectum' | head -5
