on run argv
  set inputFile to POSIX file (item 1 of argv)
  set outputFile to POSIX file (item 2 of argv)
  tell application "Keynote"
    activate
    open inputFile
    if (count of documents) is 0 then error "Keynote returned no open document"
    set targetDoc to front document
    set nameOfDoc to name of targetDoc
    export targetDoc to outputFile as PDF
    close targetDoc saving no
  end tell
  return "KEYNOTE_EXPORT_PASS " & nameOfDoc
end run
