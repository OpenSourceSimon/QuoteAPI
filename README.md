# Quote API
Quote API for my project [QuoteTab](https://github.com/OpenSourceSimon/QuoteTab)

## Usage
You can self host this API or use the one I host at [https://simonrijntjes.nl/quote.php](https://simonrijntjes.nl/quote.php)
### Get a random quote with author
```http
GET https://simonrijntjes.nl/quote.php
```
### Get a random quote translated
```http
GET https://simonrijntjes.nl/quote.php?lang=nl
```

## Contributing
If you want to add a quote, please create a pull request with the quote in the `main.json` file. Thanks in advance! <br>
Please don't edit the translations, they are automatically generated. The translation library this project currently uses is Argos Translate.
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.