import pickle

def load_user_session(user_raw_data):
    # Zafiyetli kod: Güvenilmeyen baytlar pickle ile açılıyor
    session_data = pickle.loads(user_raw_data)
    return session_data