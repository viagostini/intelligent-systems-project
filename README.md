![tests](https://github.com/viagostini/intelligent-systems-project/actions/workflows/tests.yml/badge.svg)

# :sparkles: Product Categorization :sparkles:

### :rocket: Overview

The data used in this project is from an [open source dataset][1] made by [Elo7][2],
the largest online handcrafts marketplace in Brazil. More info about it can be found
[here][3].

The goal of this project is to first develop a categorization model using the available
data and then serve this model through a REST API, to categorize new products.

The stack used was:

- **Model**: scikit-learn
- **API**: FastAPI
- **(Extra) Metrics Dashboard**: Prometheus + Grafana

### :zap: Why FastAPI?
FastAPI is, as its own docs say, "high performance, easy to learn, fast to code,
ready for production" framework. We are not really concerned with our API performance
in this project, however, FastAPI gives us many awesome functionality for free, taking
advantage of its great integration with Pydantic for schema validation, object
(de)serialization and FastAPI also auto generates API documentation for us, which
is pretty cool.

### :memo: How to run the training notebook
First, I will assume that [Docker][4] and [docker-compose][5] are installed, so make
sure you have it or install it if you don't.

To bring up Jupyter with access to the training notebook, run
`docker-compose up -f training/docker-compose.yml --build`.

### :memo: How to start the serving API
Again, I will assume that [Docker][4] and [docker-compose][5] are already installed.

In order to bring up the serving stack, you can run 
`docker-compose up -f server/docker-compose.yml --build`. This will start three services
that can be accessed in localhost: a **FastAPI** application on port `5000`,
**Prometheus** on port `9090` and finally **Grafana** on port `3000`.

You can now proceed to make POST requests on `localhost:5000/v1/categorize` to receive
predictions. If you have `curl` installed, you can do
`curl -XPOST localhost:5000/v1/categorize -d @data/test_products.json`.

Alternatively, you can also test the endpoint through FastAPI's auto generated docs

### :memo: Monitor the serving API
First, start the serving stack with the command on the last section if you haven't. Then
you can access the Grafana dashboard at `localhost:3000`.

For now, as this was an extra feature, the Prometheus datasource needs to be manually
added to Grafana (use `http://prometheus:9090` as the host) and the dashboard must be
imported from the file `dashboard.json` located in the root folder of the project.

Note: There is a bug sometimes in the requests/sec gauge that ends up displaying two
of them for the same route or sometimes it doesn't display the route name.

Some screenshots:

<img src="images/dash2.png" width="1000">

<img src="images/dash3.png" width="1000">

<img src="images/dash5.png" width="1000">

<img src="images/dash4.png" width="1000">



[1]: https://github.com/elo7/data7_oss/tree/master/elo7-search
[2]: https://elo7.com.br/sobre
[3]: data/README.md
[4]: https://docs.docker.com/get-docker/
[5]: https://docs.docker.com/compose/install/