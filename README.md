**_DESCRIPTION_**
This a basic gmail auth app, which authenticates with gmail api using gmail acoount and process the emails using python script

**Pulling code to local**
git clone https://github.com/Krishna-05012000/GMAIL_API_processing.git

**Installing the requirements**
pip install -r requirements.txt

**Authentication, connecting to gmail and storing the mails in DATABASE**
python main.py
step 1 : Authentication 
* run python main.py ,if yourn't authenticated a desktop app opens up and u can authenticate with ur google mail API. Then go back to terminal. (if already authenticated nothing will take place u will have the next part of code)
step 2 : email storing in DB
* Now in terminal it will ask for date (YYYY-MM-DD) for fetching emails after this date , to reduce longer process for reviewer to handle it with ease.
* after giving date ,all the mails will be loaded to DB

**Processing email and applying rules**
python rules_processor.py
* run python rules_processor.py . Now u will get the list of rules tht u can use for processing email.
* choose any rule number and it will ask to give any value. (u can use the example for giving values to a particular rule)
* Then u can see the processing bar , along with the mails with mail ID that the action took place.
* If u want to run for anyother rule u can run the command line again

**Testing**
python -m unittest discover -s test
* If u run the command line it will test certain functions with the mock test cases and will show the results of the test. Havent handelled all the possibilities just handled for certain scenarios
