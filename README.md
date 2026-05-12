# 💲 Exchange Rate Alerts API

This is a **simple Rest API** developed in **Flask** and built on top of [Frankfurter v1 API](https://frankfurter.dev/v1/).
<br>
All of the data is stored on a MongoDB instance.
<br><br>
Authenticated user can set a currency exchange rate target and get a list of currencies where the rate has fallen below this threshold.
> [!NOTE]
> API was developed as part of the university group project for the "Testing of IT Applications" course and as such it is **mainly focused on unit tests and the CI/CD pipeline**.

## API Endpoints

| Endpoint & HTTP method | Description |
| :--- | :--- |
| **POST**<br>`/register` | Creates a new user account.<br><br>Requires `username` (3-20 characters) and `password` (min 8 characters, 1 letter, 1 number) in the request body. |
| **POST**<br>`/login` | Verifies user credentials and returns a JWT token.<br><br>Requires `username` and `password` in the request body. |
| **GET**<br>`/targets` | Retrieves all currency targets set by the authenticated user. |
| **POST**<br>`/targets` | Creates a new target or updates an existing one for a specific currency pair.<br><br>Requires `base_currency`, `quote_currency`, and `target_value` (float) in the request body. |
| **DELETE**<br>`/targets` | Deletes a specific currency target from the user's list<br><br>Requires `base_currency` and `quote_currency` in the request body. |
| **GET**<br>`/alerts` | Compares the user's targets against current market rates.<br><br>Returns a list of currency pairs where the market rate is less than or equal to the `target_value`. |

## Getting started

1. **Create a virtual python environment**

2. **Install required packages**
   <br>Run the command listed below to install all of the required packages.
   ```bash
   pip install -r requirements.txt
   ```
3. **Run tests**
   ```bash
   pytest -v
   ```
4. **Create a .env file next to the app.py file**  
   Below is a template .env file:
   ```bash
   MONGO_STR="mongodb+srv://USERNAME:PASSWORD@cluster.mongodb.net/?appName=CLUSTER_NAME"
   ```
5. **Run the API**  
   API will be available at `https://localhost:5000`.
   ```bash
   python app.py
   ```
