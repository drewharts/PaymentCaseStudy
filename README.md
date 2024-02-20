# PaymentCaseStudy
## Directions (as given by recruiter)
- Imports the most recent year's data
- Checks regularly to get the most recent updates
- Build a search tool with a typeahead that returns all relevant data
- When search results are returned in your tool, build an "Export to Excel" feature that this outputs to an XLS file

- https://openpaymentsdata.cms.gov/about/api

## Directions to test

- Run using docker so make sure you have Docker and Docker Compose

- Once you have docker and project open run *docker-compose up -d --build*

- Navigate to http://localhost:3000

- You can shutdown containers afterwards with *docker compose down*

## What I'd do without a 2.5 day time constraint:

- Add many more tests for PostgreSQL entries, elasticsearch document sending and batch sizes, and for each of the endpoints

- Write a robust way to periodically check if there have been changes, I read they only happen twice a year so I didn't prioritize this

- Add much more functionality to elastic search and returning groups of data based on certain criteria. There are endless possibilites with this

- Overall, try to seperate functions better and improve readibility 

- Add something to import data immediately so there *appears* to be no bootup time


