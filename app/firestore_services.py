import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

credential_app = credentials.ApplicationDefault()
firebase_admin.initialize_app(credential_app, {
    'projectId': 'todo-list-flask',
})

db = firestore.client()


def get_users():
    return db.collection('users').get()


def get_user_by_id(user_id):
    return db.collection('users')\
        .document(user_id).get()


def get_tasks(user_id):
    return db.collection('users')\
        .document(user_id)\
        .collection('tasks').get()
