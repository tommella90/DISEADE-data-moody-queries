clear all
cd "Z:\dati_moody\zipped_files\all_data_gz\ownership_history\links_2016"

local country "CY"  // Change this for different countries
local first = 1      // Track first import

forvalues chunk = 0/100 {   // Loop from 0 to 100
    local file "`country'_chunk_`chunk'.csv.gz"
    display "Trying to import: `file'"

    capture gzimport delimited using "`file'", clear

    if _rc != 0 {   // If error occurs (file missing or other issue)
        display "No more files found at chunk `chunk'. Stopping loop."
        continue, break
    }

    if `first' == 1 {
        save temp_data, replace
        local first = 0
    }
    else {
        append using temp_data
        save temp_data, replace
    }
}

// Save final dataset
save "`country'_all_chunks.dta", replace
display "Appending completed!"
