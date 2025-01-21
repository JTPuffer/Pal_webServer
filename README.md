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

Command prompt 3:

    dnc client
    dana client.Cycle


Command prompt 3:

curl localhost:8008/meta/get_all_configs

choose one config

Command prompt 4:
curl -X POST -H "Content-Type: text/json" -d '{"config" :"replace me with the config switch testing"}' localhost:8008/meta/set_config


response time is significantly higher when running client.cycle