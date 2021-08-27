# UsdEurRubPay
test task

This is a web app which can be integrated into an online store for customers to make payment through different payment platforms depending on the necessary currency. The app works in one of the 2 ways depending on the necessary currency:

1) either makes a direct request to the necessary payment platform's API
2) or uses the request data (provided by a customer) to fill out and validate an HTML form. If the form is validated, the customer is redirected to the payment platform's webpage.

Some customer's request data (currency, amount, request time and date, item description & shop order ID) is stored in an SQLite database.
