on run argv
    set inputFile to POSIX file (item 1 of argv)
    set outputFile to POSIX file (item 2 of argv)
    tell application "Pages"
        activate
        open inputFile
        set n to count of documents
        if n is 0 then error "Pages returned no open document"
        set q to front document
        set docname to name of q
        export q to outputFile as PDF
        close q saving no
    end tell
    return "PAGES_EXPORT_PASS " & docname
end run
