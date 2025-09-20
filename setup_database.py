import sqlite3

# --- Data to be inserted into the database ---
# This is the complete, normalized data for the final application
symptoms_data = [
    ('s1', 'Headache (dull or severe)', 'Brain & Neurological'),
    ('s3', 'Nausea or Vomiting', 'Digestive & Stomach'),
    ('s4', 'Blurred or Double Vision', 'Brain & Neurological'),
    ('s5', 'Seizures', 'Brain & Neurological'),
    ('s6', 'Memory Loss or Confusion', 'Brain & Neurological'),
    ('s7', 'Dizziness or Vertigo', 'Brain & Neurological'),
    ('s9', 'Difficulty Speaking', 'Brain & Neurological'),
    ('s14', 'Fever (High or Low-grade)', 'General & Basic Health'),
    ('s15', 'Cough (Dry or Productive)', 'General & Basic Health'),
    ('s16', 'Sore Throat', 'General & Basic Health'),
    ('s17', 'Runny or Stuffy Nose', 'General & Basic Health'),
    ('s18', 'Body Aches', 'General & Basic Health'),
    ('s19', 'Diarrhea', 'Digestive & Stomach'),
    ('s20', 'Abdominal Cramps / Stomach Pain', 'Digestive & Stomach'),
    ('h1', 'Chest Pain or Discomfort', 'Heart & Circulation'),
    ('h2', 'Shortness of Breath', 'Heart & Circulation'),
    ('h3', 'Pain in Neck, Jaw, or Back', 'Heart & Circulation'),
    ('h4', 'Lightheadedness or Fainting', 'Heart & Circulation'),
]

keywords_data = [
    ('headache', 's1'), ('head hurt', 's1'),
    ('nausea', 's3'), ('vomiting', 's3'), ('sick to my stomach', 's3'),
    ('vision', 's4'), ('blurry', 's4'), ('double vision', 's4'),
    ('seizure', 's5'),
    ('confusion', 's6'), ('confused', 's6'),
    ('dizzy', 's7'), ('vertigo', 's7'),
    ('speaking', 's9'), ('slurred', 's9'),
    ('fever', 's14'), ('temperature', 's14'),
    ('cough', 's15'), ('coughing', 's15'),
    ('sore throat', 's16'), ('throat hurts', 's16'),
    ('runny nose', 's17'), ('stuffy', 's17'), ('congestion', 's17'),
    ('body ache', 's18'), ('muscles hurt', 's18'),
    ('diarrhea', 's19'), ('loose stool', 's19'),
    ('cramps', 's20'), ('stomach pain', 's20'),
    ('chest pain', 'h1'),
    ('shortness of breath', 'h2'), ('breathless', 'h2'),
    ('jaw pain', 'h3'), ('neck pain', 'h3'),
    ('lightheaded', 'h4'), ('fainting', 'h4'),
]

conditions_data = [
    ('c1', 'Probable Migraine', 'Medium', 'A migraine is not typically life-threatening, but you should see a doctor to confirm the diagnosis and explore prescription treatment options if they are frequent or severe.'),
    ('c6', 'Probable Influenza (Flu)', 'Medium', 'The flu can typically be managed at home, but consult a doctor if you are in a high-risk group (e.g., elderly, pregnant, chronic illness) or if you experience difficulty breathing.'),
    ('c7', 'Probable Gastroenteritis (Stomach Flu)', 'Medium', 'The main risk is dehydration. See a doctor if you cannot keep liquids down for more than 24 hours, have a very high fever, or see blood in your vomit or stool.'),
    ('c_emergency_brain', 'Symptoms Warrant URGENT Neurological Evaluation', 'Emergency', 'Based on symptoms like seizure, confusion, or difficulty speaking, you should seek immediate medical help. Go to the nearest emergency room or call for an ambulance now.'),
    ('c_emergency_heart', 'Symptoms Warrant URGENT Cardiac Evaluation', 'Emergency', 'Based on symptoms like chest pain or shortness of breath, you should seek immediate medical help. Go to the nearest emergency room or call for an ambulance now.'),
]

condition_symptoms_data = [
    ('c1', 's1', 3), ('c1', 's3', 2), ('c1', 's4', 1),
    ('c6', 's14', 4), ('c6', 's18', 4), ('c6', 's15', 3), ('c6', 's1', 2), ('c6', 's16', 1),
    ('c7', 's3', 4), ('c7', 's19', 4), ('c7', 's20', 3), ('c7', 's14', 2),
    ('c_emergency_brain', 's5', 5), ('c_emergency_brain', 's6', 5), ('c_emergency_brain', 's9', 5),
    ('c_emergency_heart', 'h1', 5), ('c_emergency_heart', 'h2', 5), ('c_emergency_heart', 'h3', 4), ('c_emergency_heart', 'h4', 4),
]

care_plan_data = [
    ('c1', '**Rest:** Lie down in a dark, quiet room. Light and sound can make the pain worse.'),
    ('c1', '**Temperature Therapy:** Apply a cold pack or cloth to your forehead or the back of your neck.'),
    ('c1', '**Hydration:** Sip water or an electrolyte drink. Dehydration can trigger or worsen migraines.'),
    ('c6', '**Rest and Isolate:** Stay home from work or school to rest and prevent spreading the virus.'),
    ('c6', '**Hydration:** Drink plenty of fluids like water, broth, and tea to prevent dehydration from fever.'),
    ('c6', '**Symptom Management:** Use a humidifier for cough and congestion.'),
    ('c7', '**Hydration is Key:** Sip small amounts of clear liquids (water, electrolyte drinks, clear broth) frequently.'),
    ('c7', '**Rest Your Stomach:** Avoid solid food for a few hours. When you\'re ready, ease back in with bland foods (bananas, rice, applesauce, toast - the BRAT diet).'),
    ('c7', '**Avoid Irritants:** Stay away from dairy, caffeine, alcohol, and spicy or fatty foods until you feel better.'),
    ('c_emergency_brain', '**Do not delay.** Time is critical in a potential neurological emergency.'),
    ('c_emergency_brain', '**Do not eat, drink, or take any medication** while waiting for medical professionals.'),
    ('c_emergency_heart', '**Do not delay.** Time is critical in a potential cardiac emergency.'),
    ('c_emergency_heart', '**Try to stay calm and rest in a comfortable position.**'),
    ('c_emergency_heart', '**If prescribed, take nitroglycerin as directed.** Do not take anyone else\'s medication.'),
]

medications_data = [
    ('c1', 'Ibuprofen (e.g., Advil, Motrin) or Naproxen (e.g., Aleve)', 'NSAID', 'Take as directed (e.g., 400mg Ibuprofen) at the very first sign of an attack. Do not take on an empty stomach.'),
    ('c6', 'Acetaminophen (e.g., Tylenol) or Ibuprofen (e.g., Advil)', 'Fever Reducer / Pain Reliever', 'Use to manage fever and body aches according to package directions. Do not give aspirin to children.'),
    ('c7', 'Oral Rehydration Solutions (e.g., Pedialyte)', 'Hydration Support', 'These are better than water for replacing lost electrolytes.'),
    ('c7', 'Anti-diarrheal (e.g., Loperamide)', 'Symptom Control', 'Use cautiously. It may not be recommended for certain types of infections. Avoid if you have a high fever.'),
]

# --- Database Creation Logic ---
def setup_database():
    """Creates and populates the SQLite database."""
    db_name = 'health_kb.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Drop existing tables to start fresh
    cursor.execute("DROP TABLE IF EXISTS keywords")
    cursor.execute("DROP TABLE IF EXISTS symptoms")
    cursor.execute("DROP TABLE IF EXISTS conditions")
    cursor.execute("DROP TABLE IF EXISTS condition_symptoms")
    cursor.execute("DROP TABLE IF EXISTS care_plans")
    cursor.execute("DROP TABLE IF EXISTS medications")

    # Create tables
    cursor.execute('''
    CREATE TABLE symptoms (
        symptom_id TEXT PRIMARY KEY,
        symptom_name TEXT NOT NULL,
        category TEXT NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE keywords (
        keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword_text TEXT NOT NULL UNIQUE,
        symptom_id TEXT,
        FOREIGN KEY (symptom_id) REFERENCES symptoms (symptom_id)
    )''')

    cursor.execute('''
    CREATE TABLE conditions (
        condition_id TEXT PRIMARY KEY,
        condition_name TEXT NOT NULL,
        urgency_level TEXT NOT NULL,
        urgency_text TEXT NOT NULL
    )''')

    cursor.execute('''
    CREATE TABLE condition_symptoms (
        condition_id TEXT,
        symptom_id TEXT,
        weight INTEGER NOT NULL,
        PRIMARY KEY (condition_id, symptom_id),
        FOREIGN KEY (condition_id) REFERENCES conditions (condition_id),
        FOREIGN KEY (symptom_id) REFERENCES symptoms (symptom_id)
    )''')
    
    cursor.execute('''
    CREATE TABLE care_plans (
        plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
        condition_id TEXT,
        plan_text TEXT NOT NULL,
        FOREIGN KEY (condition_id) REFERENCES conditions (condition_id)
    )''')

    cursor.execute('''
    CREATE TABLE medications (
        med_id INTEGER PRIMARY KEY AUTOINCREMENT,
        condition_id TEXT,
        med_name TEXT NOT NULL,
        med_type TEXT NOT NULL,
        advice TEXT NOT NULL,
        FOREIGN KEY (condition_id) REFERENCES conditions (condition_id)
    )''')

    # Insert data into tables
    cursor.executemany("INSERT INTO symptoms VALUES (?, ?, ?)", symptoms_data)
    cursor.executemany("INSERT INTO keywords (keyword_text, symptom_id) VALUES (?, ?)", keywords_data)
    cursor.executemany("INSERT INTO conditions VALUES (?, ?, ?, ?)", conditions_data)
    cursor.executemany("INSERT INTO condition_symptoms VALUES (?, ?, ?)", condition_symptoms_data)
    cursor.executemany("INSERT INTO care_plans (condition_id, plan_text) VALUES (?, ?)", care_plan_data)
    cursor.executemany("INSERT INTO medications (condition_id, med_name, med_type, advice) VALUES (?, ?, ?, ?)", medications_data)

    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created and populated successfully!")

if __name__ == "__main__":
    setup_database()

