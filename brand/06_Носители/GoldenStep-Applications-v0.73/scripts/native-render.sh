#!/bin/bash
set -euo pipefail
root="$(git rev-parse --show-toplevel)"
p="$root/brand/06_Носители/GoldenStep-Applications-v0.73"
log="$(mktemp /tmp/arvectum-v073-fonts.XXXXXX)"
cleanup(){
 if [ -f "$log" ]; then while IFS= read -r file; do [ ! -e "$file" ] || rm -f -- "$file";done < "$log";rm -f "$log";fi
 /usr/bin/osascript -e 'tell application "Pages" to if (count of documents) is 0 then quit' >/dev/null 2>&1 || true
 echo 'TEST_FONT_COPIES_CLEANED'
}
trap cleanup EXIT
for app in Pages; do
 if pgrep -x "$app" >/dev/null;then
  n=$(/usr/bin/osascript -e "tell application \"$app\" to count of documents")
  [ "$n" = 0 ] || { echo "ABORT_USER_DOCUMENTS_OPEN_$app=$n"; exit 10; }
 fi
done
for st in Display Text; do
 typ=Regular;[ "$st" != Display ] || typ=Medium
 name="Arvectum${st}GoldenStepDraft064-${typ}.otf"
 source="$p/fonts/$name";target="$HOME/Library/Fonts/$name"
 [ -s "$source" ] && [ ! -e "$target" ] || { echo "PREEXISTING_TEST_FONT_OR_MISSING_SOURCE $name";exit 11; }
 cp -- "$source" "$target"
 printf '%s\n' "$target" >> "$log"
done
/usr/bin/open -a /Applications/Pages.app
sleep 2
for base in letterhead proposal; do
 /usr/bin/osascript "$p/scripts/export-pages.applescript" "$p/office/$base-editable.docx" "$p/proofs/$base-native-pages.pdf"
 test -s "$p/proofs/$base-native-pages.pdf" || exit 12
done
# Keynote GUI export was not reliable on this Mac mini.
# It is deliberately excluded from unattended reproduction; HTML slides PDF
# and PPTX OOXML remain separate and are explicitly not claimed pixel-equivalent.
echo "KEYNOTE_EXPORT_NOT_ATTEMPTED_IN_SAFE_REPRODUCTION"
for pdf in "$p/proofs"/*native*.pdf;do echo "NATIVE_PDF $(basename "$pdf")";pdfinfo "$pdf" | grep -E '^Pages:|^Page size:';pdffonts "$pdf" | grep -E 'Arvectum' | head -5;done
