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


def insert_user(user_data):
    data = {
        'password': user_data.password,
    }
    db.collection('users').document(user_data.username).set(data)


def get_tasks(user_id):
    return db.collection('users')\
        .document(user_id)\
        .collection('tasks').get()


def post_task(user_id, task):
    data = {
        'description': task,
        'done': False
    }
    db.collection('users')\
        .document(user_id)\
        .collection('tasks').add(data)


def delete_task(user_id, task_id):
    db.document('users/{}/tasks/{}'.format(user_id, task_id)).delete()


def update_task(user_id, task_id, done):
    task_done = not bool(done)
    task_ref = db.document('users/{}/tasks/{}'.format(user_id, task_id))

    #task_done = not bool(done)
    #task_ref = _get_task_ref(user_id, task_id)
    task_ref.update({'done': task_done})


# def _get_task_ref(user_id, task_id):
#    return db.document('users/{}/tasks/{}'.format(user_id, task_id))
