on run argv
    set inputPath to item 1 of argv
    set outputPath to item 2 of argv
    tell application "Microsoft Word"
        activate
        open (POSIX file inputPath) read only true add to recent files false
        set q to active document
        set docname to name of q
        save as q file name outputPath file format format PDF
        close q saving no
    end tell
    return "WORD_PDF_EXPORT_PASS " & docname
end run
