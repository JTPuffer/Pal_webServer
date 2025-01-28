# generating content

The workloads in this repository are designed to operate with a set of included content. You may wish to provide your own workloads and content beyond this. To use this included workloads, the repository contains a bast list of "htdocs" content which must be expanded into a full set by using a generator program.

Command prompt 1:

    cd web_server/htdocs/
    dnc .
    dana GenerateContent.o




# testing
To run a machine learning experiment, you'll need three command prompts, as follows:

Command prompt 1:

    cd web_server
    dnc .
    dana pal.rest WebServer.o



Command prompt 2:

    python3 measureVariance.py

a Graph should pop up allow it to complete, the variance will be printed at the end, close the graph to kill the program once completed


Command prompt 3:

    git switch --detach  cba25b86e803da6a7bc898b475cb6501acb05c9f

changes you to the branch with the old code 



Command prompt 4:

    python3 measureVariance.py

compare the 2 results


to change back to the new code use

Command prompt 5:
    git switch old-code


old-code branch is the branch with the new code on, i know its confusing


