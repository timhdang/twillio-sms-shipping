
import config
from twilio.rest import Client
# Download the helper library from https://www.twilio.com/docs/python/install
import pandas as pd
from twilio.base.exceptions import TwilioRestException

#Read and fetch csv data into dataframes, lists
col_list = ['Print Date', 'Amount Paid','ORDER #','SELLER','Recipient', 'Phone', 'Status' , 'Tracking #', 'Class Service', 'Weight']
df = pd.read_csv("data.csv", usecols=col_list)
pn = df["Phone"]
status = df["Status"]
tracking_codes = df["Tracking #"]
customers = df["Recipient"]

#prep data, only "Printed" goes through, "pending" is for orders that is on hold, or customer cancelled.
customers_list_to_be_sent = []
pn_list_to_be_sent = [] 
tracking_code_to_be_sent = []
for i in range(len(pn)): 
        #For Debug
        print(str(tracking_codes[i]))       
        if(status[i] == 'Printed'):
            pn_list_to_be_sent.append(pn[i])
            customers_list_to_be_sent.append(customers[i])
            tracking_code_to_be_sent.append(tracking_codes[i].replace(" ",""))
for j in range(len(pn_list_to_be_sent)):
    #For Debug
    print(pn_list_to_be_sent[j])      
    print(customers_list_to_be_sent[j])  
    print(tracking_code_to_be_sent[j])  
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

#---------------------------------------------#
#-------Create a file name config.py (in the same directory)-------
#api_key = "change-me"
#api_secret = "change-me"
#twilio_active_number = "change-me"
#---------------------------------------------#

account_sid = config.api_key
auth_token = config.api_secret
from_phone = config.twilio_active_number
client = Client(account_sid, auth_token)


for i in range(len(pn_list_to_be_sent)):
    try:
        message = client.messages \
                    .create(
                        body="From <COMPANY NAME>,\n Dear " + customers_list_to_be_sent[i] + "\n" +
                        "Great news! Your order is shipped and can be track with USPS, Track at " +
                        "https://tools.usps.com/go/TrackConfirmAction?tRef=fullpage&tLc=2&text28777=&tLabels=" + str(tracking_code_to_be_sent[i]),
                        from_= from_phone,
                        to= pn_list_to_be_sent[i],
                    )
        print("sending to" + customers_list_to_be_sent[i] + " " + message.sid)
    except TwilioRestException as err:
        print(err)
