# BackEnd Challenge T1-BD-UFES
First pratical project of the database course.

The task was to select a challenge from [BackEnd Challenges](https://github.com/CollabCodeTech/backend-challenges) and implement it.
The challenge selected to implement was the [PETLOVE](https://github.com/petlove/vagas/tree/master/backend-ruby) challenge, but using Python instead of Ruby.

To develop this API, were used:

|     Tool      |                   Used                   |
|:-------------:|:----------------------------------------:|
| Web Framework | [FastApi](https://fastapi.tiangolo.com/) |
|   Database    |     [MySQL](https://www.mysql.com/)      |
|     Tests     |    [Pytest](https://docs.pytest.org)     |

To see the documentation about the available methods access: `localhost:8000/docs`
while the application is running.

---

## Summary

1. [The project](#project)
2. [Prerequisites](#prerequisites)
3. [QuickStart](#quickstart)
4. [Automated Tests](#automated-tests)

---

## The project <a name="abstract"></a>

This project creates an api for a database server of a petshop called Petlove. Both api and database
server were containerized with docker client. The database server were modeled based on the follow 
entity-relationship diagram:
<p align="center">
  <img src="https://github.com/ivarejao/T1-BD/blob/main/images/ERDiagram-Petlove.png" />
</p>



---

## Prerequisites <a name="prerequisites"></a>

Having Docker installed in your machine.

If that's not the case follow the steps in this [Docker installation tutorial](https://docs.docker.com/engine/install/ubuntu/).

---

## QuickStart <a name="quickstart"></a>

1. Clone the repository:

```bash
git clone https://github.com/ivarejao/T1-BD.git
```

2. Enter the folder:

```bash
cd T1-BD
```

3. Create and run the Docker Containers (if the containers already exists, it just start the container):

```bash
docker-compose up
```

4. Access the web page:
```
localhost:8000
```

**Additional commands**:

|          Task         |            Step            |
|:---------------------:|:--------------------------:|
|    Stop Application   | `CTRL + C` in the terminal |
|   Resume Application  |     `docker-compose up`    |
| Delete the Containers |    `docker-compose down`   |

---

## Automated Tests <a name="automated-tests"></a>

The tests are divided by methods in files in the following format:

| Method 	|      File      	| Number of Tests 	|
|:------:	|:--------------:	|:---------------:	|
|   GET  	|   test_get.py  	|        8        	|
|  POST  	|  test_post.py  	|        3        	|
|   PUT  	|   test_put.py  	|        2        	|
| DELETE 	| test_delete.py 	|        3        	|

There is a bash script in the src folder that will run the tests using the following command:
```bash
docker exec api /usr/src/server/RunTests.sh
```
The command above can be used anywhere inside the T1-BD folder.
