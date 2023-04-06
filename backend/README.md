# dsa3101-2220-03-airline

```
.
├── backend
│   ├── database 
│   ├── model
│   └── unit_tests
└── README.md
```

### Database

All our data used are stored in the [folder](./database/data/). Instructions to set up and run are located [here](./database/README.md)

### Model

We tried a variety of models. Instruction to replicate their results are [here](./model/README.md)

### Unit-tests

We have set up a few simple unit test to ensure correctness of our functions on the backend side. <br>
To run them, navigate to the [folder](./unit_tests/) on command line. <br>
Run
```
pytest
```

### Data drift
To check if there are any data drifts in any of the columns used to train the model, follow the instructions located in this [file](./model/StatisticalTest/README.md)