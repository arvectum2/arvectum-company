#!/bin/bash
set -euo pipefail
root="$(git rev-parse --show-toplevel)"
p="$root/brand/04_Цвет и типографика/Arvectum-Typeface-v0.65"
logfile="$(mktemp /tmp/arvectum-v065-fonts.XXXXXX)"
cleanup() {
  if [ -f "$logfile" ]; then
    while IFS= read -r path; do
      if [ -f "$path" ]; then rm -f -- "$path"; fi
    done < "$logfile"
    rm -f "$logfile"
  fi
  /usr/bin/osascript -e 'tell application "Pages" to if (count of documents) is 0 then quit' >/dev/null 2>&1 || true
  echo "TEMP_FONTS_REMOVED"
}
trap cleanup EXIT
if pgrep -x Pages >/dev/null; then
  n=$(/usr/bin/osascript -e 'tell application "Pages" to return count of documents')
  if [ "$n" != "0" ]; then echo "ABORT_OPEN_PAGES_DOCUMENTS";exit 4;fi
  /usr/bin/osascript -e 'tell application "Pages" to quit'
fi
for ver in 061 064; do
  for st in Display Text; do
    typ=Regular
    [ "$st" = Display ] && typ=Medium
    name="$(printf 'Arvectum%sGoldenStepDraft%s-%s.otf' "$st" "$ver" "$typ")"
    rev="$(echo "$ver" | sed 's/^0//')"
    src="$root/brand/04_Цвет и типографика/Arvectum-Typeface-v0.$rev/experimental/$name"
    dst="$HOME/Library/Fonts/$name"
    test -s "$src"
    if [ -e "$dst" ]; then echo "ABORT_EXISTING_FONT $name";exit 5;fi
    cp "$src" "$dst"
    printf '%s\n' "$dst" >> "$logfile"
  done
done
/usr/bin/open -a /Applications/Pages.app
sleep 2
for ver in 061 064; do
  /usr/bin/osascript "$p/native-pages/office-pages.applescript" "$p/documents/golden-step-$ver-mac-office.docx" "$p/native-pages/golden-step-$ver-pages.pdf"
  test -s "$p/native-pages/golden-step-$ver-pages.pdf"
  echo "PAGES_EXPORT_$ver"
done
