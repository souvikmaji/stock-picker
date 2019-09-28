# Stock Picker

Install Dependencies

```sh
pip install -r requirements.txt
```

Run:

```sh
python main.py pathtocsv
```

## Assumptions

1. Dates appear in no particular order.
2. If a date appears twice for the same company, it is not an error scenario. The date appearing later overwrites the previous data.

## TODO

### Feature

- [x] Csv file input
- [x] File parsing
- [ ] Input Questionaire
- [ ] Mean and Std Deviation
- [x] Date, Price parsing
- [ ] Maximum Profit

### Error Handling

- [ ] File not found
- [ ] Csv parsing: date, price parsing error
- [x] Csv file ordering

### Decorations

- [ ] Closest Match for file input
- [ ] Pyfiglet for ascii welcome text

