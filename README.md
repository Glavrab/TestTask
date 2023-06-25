Test task project

To run project execute:
```shell
docker compose up --build
```

Interactive docs are available on http://localhost:8080/docs

To run api tests set RUN_TEST environment variable to "True" in docker-compose.yaml. 
After that start project with command described in previous step:
```yaml
    environment:
      RUN_TESTS: "True"
```
