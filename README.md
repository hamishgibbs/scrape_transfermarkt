# scrape_transfermarkt

## Workflow Diagram
![](./rulegraph.svg)

## Tests

Download test data with:

```{}
snakemake -j1 update_test_data
```

Run unit tests with:

```{}
python -m pytest tests/unit
```