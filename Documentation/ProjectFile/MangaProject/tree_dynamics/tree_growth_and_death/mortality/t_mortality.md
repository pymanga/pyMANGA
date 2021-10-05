

Mortality concepts define why trees die.  
The following concepts are available for `SimpleBettina` and `NetworkBettina`

- `NoGrowth`: trees die if growth is <= 0
- `Random`: trees die randomly with a defined probability
- `Memory`: trees die if relative growth falls below a given threshold

Mortality concepts are defined using the tag `<mortality>`. 
The default concept is `NoGrowth` (no specification in the input xml file required).
Concepts can be combined by listing them in `<mortality>`, separated by a whitespace, e.g. `<mortality> Random Memory </mortality>`.
