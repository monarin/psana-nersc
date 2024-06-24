## Mannage build with psrel
User psrel is responsible for creating new build releases. To become psrel on a machine, **make sure** that your k-ticket is valid (do `kinit` if needed then
```
ssh `hostname` -l psrel
```
Note that the list of permitted user is in
```
cat .k5login
```
