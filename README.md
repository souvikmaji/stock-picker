# Stock Picker

Install Dependencies

```sh
make init
```

Run:

```sh
python main.py pathtocsv
```

Run unit tests:

```sh
make test
```

Code is developed and tested in python3 environment.

## Sample Output

```txt
     _______.___________.  ______     ______  __  ___
    /       |           | /  __  \   /      ||  |/  /
   |   (----`---|  |----`|  |  |  | |  ,----'|  '  /
    \   \       |  |     |  |  |  | |  |     |    <
.----)   |      |  |     |  `--'  | |  `----.|  .  \
|_______/       |__|      \______/   \______||__|\__\

.______    __    ______  __  ___  _______ .______
|   _  \  |  |  /      ||  |/  / |   ____||   _  \
|  |_)  | |  | |  ,----'|  '  /  |  |__   |  |_)  |
|   ___/  |  | |  |     |    <   |   __|  |      /
|  |      |  | |  `----.|  .  \  |  |____ |  |\  \----.
| _|      |__|  \______||__|\__\ |_______|| _| `._____|


Welcome Agent!

Which Stock You Need to Process? :- aicic
Do You Mean AICIXE? (y):- y
From which date you want to start? :- 20/01/2019
Till which date you want to analyze? :- 30-feb-2019
Error in Parsing Query. Cause: day is out of range for month. Please try again.
Do You Want to Continue? (y or n) :- y

Which Stock You Need to Process? :- AMBKP
From which date you want to start? :- 20th jan 2019
Till which date you want to analyze? :- 31st jan 2019
Here is your result :-
Mean: 31.758000000000003	Std: 3.253809920692972	Buy Date: 22-Jan-2019	Sell date: 24-Jan-2019	Profit: 6.1320000000000014
Thanks For Using. Goodbye!
```

## TODO

- Round floats up to 3 decimal places for output.
- Refactor unit test structures.
- Increase code coverage.
