import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("C:/Users/hp/PycharmProjects/pythonProject/serviceAccountKey.json")




firebase_admin.initialize_app (cred,{
    'databaseURL':"https://face-recognition-5bd76-default-rtdb.firebaseio.com/"
})
ref=db.reference('Students')

data={
    "1":
        {
            "Name":"NEERAJ N",
            "REG NO":22011102062,
            "DEPARTMENT":"CSE",
            "BRANCH":"IOT",
            "AGE":21
        }
}
for key,value in data.items():
 ref.child(key).set(value)