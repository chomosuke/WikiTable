It would be difficult to start without a exact specification of the behaviour of program.<br>
Hence:<br>
Exact requirement for the program:<br>
This will be a python command line program that has a command line interface.<br>
1. Once started, it will prompt user to enter a Wikipedia URL.<br>
2. Upon recieving its input, it would then check if it actually is a valid URL. If no, it will tell the user then prompt them to enter another URL.<br>
3. It would then attempt to scan the page for a table.<br>
4. If it found a table that contains a numeric column, it'll tell the user some information about the table and the column, and ask if the user wants to go ahead with this numeric column.<br>
5. If the user type yes, then it'll prompt user to enter a location for the image file to go. The location can be absolute or relative. There will be a default localtion to be used if no location is entered. Then it'll go back to step 3.<br>
6. if the user type no, then it'll go back to step 3.
7. if after step 3, it can not find a Table with a numeric column. It'll tell the user and prompt then to enter another URL.