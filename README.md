# Library
`library` is a tool written in [Python](https://www.python.org/) that streamlines management of book metadata.

Running the program in a terminal offers a prompt to enter book [ISBNs](https://en.wikipedia.org/wiki/ISBN). Originally when I wrote this tool I used a USB plug-and-play barcode scanner ([Here's an example from Amazon](https://www.amazon.com/Officelab-Barcode-Scanner-Handheld-Scanning/dp/B0BBFL61CY)).

### Usage
After an ISBN has been entered, metadata will be retrieved from [openlibrary.org](https://openlibrary.org/developers/api), which is a free to use service for getting book information made by the [InternetArchive](https://github.com/internetarchive/openlibrary). For now only the author and title are retrieved, but in the future this tool could easily be extended to include additional information about each book. 

After quitting the prompt all data will be written to an inventory spread sheet that can act as a running inventory for future usage.
