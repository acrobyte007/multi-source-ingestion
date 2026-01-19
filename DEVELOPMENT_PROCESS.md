## Thinking process
1.Making different components to handle different data sources
2.for csv data source, used csv reader to get the non null row to the columns
3.As the columns name can be diffent of each csv file, so I used the first row to get the column name and put the coulums to AI to get to mark the proper colums
4.After getting the proper columns, I used the column name to get the data from the csv file in the same order
5.for web scrapping data source, used the web scraping to get the data and put the data to the columns
6.Clean the HTML tags and get the proper data
7.To get the tittle, I used the header tag to get the tittle
8.To get the content, I used the body tag to get the content
9.For the news api data source, used the api to get the data and put the data to the columns
10.As the news api provides a clean json file, so I used the json file to get the full data
11.Finally in the main function, I used the different components to get the data from the different data sources and put the data to json file

## Prompt used
1. "create python function to get extract the first non null row from the csv file and put the data to the columns"
2. "create python funtion to get the columns as title and content from given columns names using langchai with strcuture output as {title: , content: } using mistral ai models"
3. "Write down the testing code using pytest to test the functions"
4. "use those marked columns to get the data from the csv file and put the data to the columns, out put should be list of dictionaries"
5. "create python function to get the data from the web scrapping data source, the first should be the tittle and body tags should be the content, output should be list of dictionaries"
6. "Write down the testing code using pytest to test the functions"
7. "create python function to get the data from the news api data source, the first should be the tittle and body tags should be the content, output should be list of dictionaries"
8. "Write down the testing code using pytest to test the functions"