# CSCI_112
To create a virtual environment run

python3 -m venv ./.env

Activate it with

source ./.env/bin/activate

Install dependencies with

pip install -r requirements.txt

To close the environment when you're done, run 

deactivate

Steps: 
1. Run create_table.py to create the table 
2. Run user_profile.py for the functions related to user 
3. Run order_profile.py for the functions related to order
4. Run populate_date.py to add data to the created table 
5. Run read_order_bystatusdate4.py to query the orders of a user given the status and date [ACCESS PATTERN 4]
6. Run read_pending_orders5.py to query all pending orders [ACCESS PATTERN 5]
