import telebot
import sqlite3
from config import token


client = telebot.TeleBot(token)


class PhoneContact:
    def __init__(self):
        self.connection = sqlite3.connect("base.db")
        self.cursor = self.connection.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS PhoneList(
                            name TEXT,
                            contactNumber INT,
                            note TEXT
                       )""")

        self.connection.commit()

    @client.message_handler(commands=["view"])
    def view(self, message):
        outset = []
        for i in self.cursor.execute("select * from PhoneList"):
            outset.append({f"{i[0]}": [{"number": f"{str(i[1])}"}, {"note": f"{str(i[2])}"}]})
        print(outset)


class PhoneBook:
    def __init__(self):
        self.loc_connection = sqlite3.connect("base.db")
        self.loc_cursor = self.loc_connection.cursor()
        self.contactNumbers = []
        for i in self.loc_cursor.execute("SELECT contactNumber FROM PhoneList"):
            self.contactNumbers.append(str(i)[1:-2])

    @client.message_handler(commands=["getContactByName"])
    def getContactByName(self, name: str):
        numbers = []
        for i in self.loc_cursor.execute(f"SELECT contactNumber FROM PhoneList WHERE name = '{name}'"):
            numbers.append(str(i)[1:-2])
        print(numbers)

    @client.message_handler(commands=["add_contact"])
    def addContact(self, name: str, contactNumber: int, note: str):
        self.loc_cursor.execute(f"INSERT INTO PhoneList VALUES('{name}', {contactNumber}, '{note}')")
        self.loc_connection.commit()


PhoneContact = PhoneContact()
PhoneBook = PhoneBook()
client.polling(none_stop=True, interval=0)