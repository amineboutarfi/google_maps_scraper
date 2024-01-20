# Google Maps Scraper

This is simple scraper that uses Playwright to extract data from Google Maps. 

This example is made for educational purposese.

This scrapit is easy to customize.

check both Excel & CSV files (google_maps_data) to see how final data will look like. 

## To Install:
- (Optional: create & activate a virtual environment) `virtualenv venv`, then `source venv/bin/activate`

- `pip install -r requirements.txt`
- `playwright install chromium`

## to Run:
### A single search:
- `python3 main.py -s=<what & where to search for> -t=<how many>`

### Multiple searches at once
1. Add searches in `input.txt`, each search should be in a new line as shown in the example (check `input.txt`)
2. Then run: `python3 main.py` 
3. If you pass `-t=<how many>` it will be applied to all the searches. 

## Tips:
If you want to search more than the limited 120 results, detail you search more and as granular as you need it to be in the `input.txt`, for example:

- Instead of using:

`United states dentist`

- Use:

`Unites States Boston dentist`

`Unites States New York dentist`

`Unites States Texas dentist`

And so on... 



