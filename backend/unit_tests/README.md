Currently, there are 3 unit test set up. <br>

1. database_test
    - checks csv file is converted to sql file correctly
2. test_lime_simple
    - checks prediction is between 0 and 1
    - checks correct length of return list
3. test_lime_weather
    - checks prediction is between 0 and 1
    - checks correct length of return list

To run all test:
```
pytest
```