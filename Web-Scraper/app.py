from flask import Flask, request
import africastalking
from decouple import config
from pymongo import MongoClient
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from send_sms import send_sms

app = Flask(__name__)
username = config('AFRICAS_TALKING_USERNAME')
api_key = config('AFRICAS_TALKING_API_KEY')
africastalking.initialize(username, api_key)

mongo_uri = config('MONGODB_URI')
client = MongoClient(mongo_uri)
database = client['priceTracker']
users_collection = database['users']

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response
    session_id = request.values.get("sessionId",None)
    phone_number = request.values.get("phoneNumber",None)
    text = request.values.get("text","")

    
    user = users_collection.find_one({
        "phone_number": phone_number
    })

    user_response = text.split("*")
    print(user_response)


    if not user:
        # Sign Up new User Name
        if len(user_response) == 1 and user_response[0] == '':
            response = "CON Kindly Enter your Full Name?\n"

        elif len(user_response) == 1:
            response = "CON Kindly Enter your PIN (Its your secret 🤐)?\n"

        elif len(user_response) == 2:
            name =  user_response[0]
            password = user_response[1]

            user_data = {
            "name": name,
            "password": generate_password_hash(password),
            "phone_number": phone_number,
            "sms tokens": 10,
            "created_at": datetime.datetime.now()
            }

            users_collection.insert_one(user_data)
            response = "END Thank you {}, you have successfully signed up! 🎉 You have 10 free tokens" .format(name)
            
            user_response = ""

        else:
            response = "END invalid input.please start again"
            user_response = ""

    else:
        if len(user_response) and user_response[0] == '':
            response = "CON Enter your Password (🔒):"
        
        elif len(user_response) == 1:
            stored_password = user["password"]
            entered_password = user_response[0].strip()

            if check_password_hash(stored_password, entered_password):
                name = user['name']
                response = "CON You have successfully signed up, {} 🎉.\n What do you want to do continue \n".format(user['name'])
                response += "1. Make a payment for services.\n"
                response += "2. Compare the prices of a product.\n"
                response += "3. About us."
            else:
                response = "END Login failed. Incorrect PIN. Please try again."
                user_response = ""

        elif len(user_response) == 2:
            entered_password = user_response[0]
            menu_option = user_response[1]

            if  menu_option == "1":
                response = "CON Enter the amount (1 Kshs is equal to 15 SMS):"

            elif menu_option == '2':
                response = "CON Enter the name of the product you want to compare:"
            
            elif menu_option == '3':
                response = "END Hustler Tracker is a convenient place to track the prices of your favorite products in the supermarkets.\n \n"
                response += "Currently we have access to several databases of products at our disposal\n \n"
                response += "We charge 1 Ksh for 15 SMS\n"
                response += "Thank you for choosing us 😉! \n"
            else:
                response = "END Invalid input. Please try again."
        
        elif len(user_response) == 3:
            entered_password = user_response[0]
            menu_option = user_response[1]
            choices_option = user_response[2]

            if menu_option == "1":
                try:
                    amount = int(choices_option)
                    if amount > 0:
                        tokens = amount * 15
                        response = f"END Payment of KES {amount} received successfully! 🎉\n"
                        response += f"You have been credited with {tokens} SMS tokens. 📩"
                        # (Optional: Update user's tokens in MongoDB here)
                    else:
                        response = "END Invalid amount entered. Please try again."

                except ValueError:
                    response = "END Invalid amount. Please enter a number."
            
            elif menu_option == "2":
                product_name = choices_option.strip()

                try:
                    send_sms(product_name, phone_number)
                    response = "END. The prices will be sent to your phone number, {}, via sms.\n Kindly Check your messages.\n Thank you for choosing us.".format(phone_number)
                except Exception as e:
                    response = "END Failed to fetch the product prices. Kindly contact the service provider"

        else:
            response = "END Invalid input. Please try again."
            user_response = ""

                
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config("PORT"))                                        