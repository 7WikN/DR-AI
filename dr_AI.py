import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.spinner import Spinner

# Initialize Rich Console
console = Console()

# --- UNIFIED KNOWLEDGE BASE (Final Version with Categories) ---
# Contains all data for both checklist and NLP modes.
UNIFIED_KB = {
    "symptom_categories": {
        "General & Basic Health": {
            "s14": "Fever (High or Low-grade)",
            "s18": "Body Aches",
            "s15": "Cough (Dry or Productive)",
            "s16": "Sore Throat",
            "s17": "Runny or Stuffy Nose",
        },
        "Brain & Neurological": {
            "s1": "Headache (dull or severe)",
            "s7": "Dizziness or Vertigo",
            "s6": "Memory Loss or Confusion",
            "s9": "Difficulty Speaking",
            "s4": "Blurred or Double Vision",
            "s5": "Seizures",
        },
        "Heart & Circulation": {
            "h1": "Chest Pain or Discomfort",
            "h2": "Shortness of Breath",
            "h3": "Pain in Neck, Jaw, or Back",
            "h4": "Lightheadedness or Fainting",
        },
        "Digestive & Stomach": {
            "s3": "Nausea or Vomiting",
            "s19": "Diarrhea",
            "s20": "Abdominal Cramps / Stomach Pain",
        }
    },
    "keywords_to_symptoms": {
        # This is for the NLP mode
        "headache": "s1", "head hurt": "s1", "migraine": "c1",
        "nausea": "s3", "vomiting": "s3", "sick to my stomach": "s3",
        "vision": "s4", "blurry": "s4", "double vision": "s4",
        "fever": "s14", "temperature": "s14",
        "cough": "s15", "coughing": "s15",
        "sore throat": "s16", "throat hurts": "s16",
        "runny nose": "s17", "stuffy": "s17", "congestion": "s17",
        "body ache": "s18", "muscles hurt": "s18",
        "diarrhea": "s19", "loose stool": "s19",
        "cramps": "s20", "stomach pain": "s20",
        "seizure": "s5", "confusion": "s6", "speaking": "s9", "dizzy": "s7",
        "chest pain": "h1", "shortness of breath": "h2", "breathless": "h2", "fainting": "h4"
    },
    "conditions": {
        "c1": {
            "name": "Probable Migraine",
            "urgency": {"level": "Medium", "text": "A migraine is not typically life-threatening, but you should see a doctor to confirm the diagnosis and explore prescription treatment options if they are frequent or severe."},
            "symptoms": {"s1": 3, "s3": 2, "s4": 1},
            "care_plan": [
                "**Rest:** Lie down in a dark, quiet room. Light and sound can make the pain worse.",
                "**Temperature Therapy:** Apply a cold pack or cloth to your forehead or the back of your neck.",
                "**Hydration:** Sip water or an electrolyte drink. Dehydration can trigger or worsen migraines."
            ],
            "medications": [
                {"name": "Ibuprofen (e.g., Advil, Motrin) or Naproxen (e.g., Aleve)", "type": "NSAID", "advice": "Take as directed (e.g., 400mg Ibuprofen) at the very first sign of an attack. Do not take on an empty stomach."}
            ]
        },
        "c6": {
            "name": "Probable Influenza (Flu)",
            "urgency": {"level": "Medium", "text": "The flu can typically be managed at home, but consult a doctor if you are in a high-risk group (e.g., elderly, pregnant, chronic illness) or if you experience difficulty breathing."},
            "symptoms": {"s14": 4, "s18": 4, "s15": 3, "s1": 2, "s16": 1},
            "care_plan": [
                "**Rest and Isolate:** Stay home from work or school to rest and prevent spreading the virus.",
                "**Hydration:** Drink plenty of fluids like water, broth, and tea to prevent dehydration from fever.",
                "**Symptom Management:** Use a humidifier for cough and congestion."
            ],
            "medications": [
                {"name": "Acetaminophen (e.g., Tylenol) or Ibuprofen (e.g., Advil)", "type": "Fever Reducer / Pain Reliever", "advice": "Use to manage fever and body aches according to package directions. Do not give aspirin to children."}
            ]
        },
        "c7": {
            "name": "Probable Gastroenteritis (Stomach Flu)",
            "urgency": {"level": "Medium", "text": "The main risk is dehydration. See a doctor if you cannot keep liquids down for more than 24 hours, have a very high fever, or see blood in your vomit or stool."},
            "symptoms": {"s3": 4, "s19": 4, "s20": 3, "s14": 2},
            "care_plan": [
                "**Hydration is Key:** Sip small amounts of clear liquids (water, electrolyte drinks, clear broth) frequently.",
                "**Rest Your Stomach:** Avoid solid food for a few hours. When you're ready, ease back in with bland foods (bananas, rice, applesauce, toast - the BRAT diet).",
                "**Avoid Irritants:** Stay away from dairy, caffeine, alcohol, and spicy or fatty foods until you feel better."
            ],
            "medications": [
                {"name": "Oral Rehydration Solutions (e.g., Pedialyte)", "type": "Hydration Support", "advice": "These are better than water for replacing lost electrolytes."},
                {"name": "Anti-diarrheal (e.g., Loperamide)", "type": "Symptom Control", "advice": "Use cautiously. It may not be recommended for certain types of infections. Avoid if you have a high fever."}
            ]
        },
        "c_emergency_brain": {
             "name": "Symptoms Warrant URGENT Neurological Evaluation",
            "urgency": {"level": "Emergency", "text": "Based on symptoms like seizure, confusion, or difficulty speaking, you should seek immediate medical help. Go to the nearest emergency room or call for an ambulance now."},
            "symptoms": {"s5": 5, "s6": 5, "s9": 5, "s2": 4},
            "care_plan": [
                "**Do not delay.** Time is critical in a potential neurological emergency.",
                "**Do not eat, drink, or take any medication** while waiting for medical professionals."
            ],
            "medications": []
        },
        "c_emergency_heart": {
             "name": "Symptoms Warrant URGENT Cardiac Evaluation",
            "urgency": {"level": "Emergency", "text": "Based on symptoms like chest pain or shortness of breath, you should seek immediate medical help. Go to the nearest emergency room or call for an ambulance now."},
            "symptoms": {"h1": 5, "h2": 5, "h3": 4, "h4": 4},
            "care_plan": [
                "**Do not delay.** Time is critical in a potential cardiac emergency.",
                "**Try to stay calm and rest in a comfortable position.**",
                "**If prescribed, take nitroglycerin as directed.** Do not take anyone else's medication."
            ],
            "medications": []
        }
    }
}

class DrAI_Core:
    """ Unified core logic for the AI doctor. """

    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.emergency_conditions = ["c_emergency_brain", "c_emergency_heart"]


    def analyze_from_text(self, user_input):
        """ Analyzes natural language input (v3 logic). """
        detected_symptoms = set()
        text_lower = user_input.lower()
        for keyword, symptom_id in self.kb["keywords_to_symptoms"].items():
            if keyword in text_lower:
                detected_symptoms.add(symptom_id)
        return self.analyze_from_symptom_ids(list(detected_symptoms))

    def analyze_from_symptom_ids(self, symptom_ids):
        """ Analyzes a list of symptom IDs (v2 logic). """
        if not symptom_ids:
            return None, None

        # Check for immediate emergency flags
        for emergency_id in self.emergency_conditions:
            for symptom_id in symptom_ids:
                if symptom_id in self.kb["conditions"][emergency_id]["symptoms"]:
                    return self.kb["conditions"][emergency_id], symptom_ids

        condition_scores = []
        for cond_id, condition_data in self.kb["conditions"].items():
            if cond_id in self.emergency_conditions: continue
            
            score = 0
            if "symptoms" in condition_data:
                for symptom_id in symptom_ids:
                    if symptom_id in condition_data["symptoms"]:
                        score += condition_data["symptoms"][symptom_id]
            
            if score > 0:
                condition_scores.append({"score": score, "condition": condition_data})

        if not condition_scores:
            return None, symptom_ids

        best_match = max(condition_scores, key=lambda x: x["score"])["condition"]
        return best_match, symptom_ids

def apply_safety_guardrails(report_panel):
    """ Ensures the final output contains the necessary disclaimers. """
    disclaimer = Panel(
        "This AI-generated report is for informational purposes only and is **NOT** a substitute for a diagnosis from a qualified medical professional. Always consult a doctor for any health concerns.",
        title="[bold red]CRITICAL MEDICAL DISCLAIMER[/bold red]",
        border_style="bold red"
    )
    console.print(report_panel)
    console.print(disclaimer)

def create_report_panel(result):
    """ Formats and displays the final, detailed report for both modes. """
    if not result:
        return Panel("I couldn't identify a clear pattern from your symptoms. For any health concerns, it's always best to speak with a doctor.", title="[yellow]Analysis Inconclusive[/yellow]")

    urgency_level = result['urgency']['level']
    urgency_color = {"Low": "green", "Medium": "yellow", "Emergency": "red"}.get(urgency_level, "white")
    urgency_panel = Panel(f"[bold]Recommended Action:[/bold]\n{result['urgency']['text']}", title="[bold]Urgency Assessment[/bold]", style=f"bold {urgency_color}", border_style=f"bold {urgency_color}")
    
    assessment_panel = Panel(f"[bold blue]{result['name']}[/bold blue]", title="[bold]Preliminary Assessment[/bold]")
    
    care_plan_text = "\n".join(f"- {item}" for item in result['care_plan'])
    care_plan_panel = Panel(care_plan_text, title="[bold]At-Home Care Plan[/bold]")

    med_text = ""
    if result['medications']:
        for med in result['medications']:
            med_text += f"[bold]{med['name']}[/bold] ({med['type']})\n[italic]Advice: {med['advice']}[/italic]\n\n"
    else:
        med_text = "No over-the-counter medication is recommended. Please follow medical advice."
    medication_panel = Panel(med_text.strip(), title="[bold]Suggested OTC Medication[/bold]")

    main_content = f"{urgency_panel}\n{assessment_panel}\n{care_plan_panel}\n{medication_panel}"
    return Panel(main_content, title="[bold green]-- Clinical Analysis Report --[/bold green]")

def run_checklist_mode(dr_ai):
    """ Handles the guided symptom selection with categories. """
    # Stage 1: Select Category
    clear_screen()
    console.print(Panel(Text("Please select a symptom category.", justify="center"), title="[bold green]Guided Symptom Checklist - Step 1 of 2[/bold green]"))
    
    categories = list(UNIFIED_KB["symptom_categories"].keys())
    for i, name in enumerate(categories):
        console.print(f"[cyan]{i+1}[/cyan]. {name}")

    while True:
        try:
            selection = Prompt.ask("\n[bold]Enter your category choice[/bold]")
            selected_index = int(selection) - 1
            if 0 <= selected_index < len(categories):
                selected_category_name = categories[selected_index]
                break
            else:
                console.print("[bold red]Invalid selection. Please enter a number from the list.[/bold red]")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter a single number.[/bold red]")

    # Stage 2: Select Symptoms from the chosen category
    clear_screen()
    console.print(Panel(Text(f"Category: {selected_category_name}\nPlease select your symptoms by entering the numbers, separated by spaces (e.g., 1 3).", justify="center"), title="[bold green]Guided Symptom Checklist - Step 2 of 2[/bold green]"))

    symptom_map = UNIFIED_KB["symptom_categories"][selected_category_name]
    symptom_list = list(symptom_map.items())

    for i, (s_id, s_name) in enumerate(symptom_list):
        console.print(f"[cyan]{i+1}[/cyan]. {s_name}")

    while True:
        try:
            selection = Prompt.ask("\n[bold]Enter your symptom selection(s)[/bold]")
            selected_indices = [int(i) - 1 for i in selection.split()]
            
            if all(0 <= i < len(symptom_list) for i in selected_indices):
                symptom_ids = [symptom_list[i][0] for i in selected_indices]
                return dr_ai.analyze_from_symptom_ids(symptom_ids)
            else:
                console.print("[bold red]Invalid selection. Please enter numbers from the list.[/bold red]")
        except ValueError:
            console.print("[bold red]Invalid input. Please enter numbers only, separated by spaces.[/bold red]")

def run_conversation_mode(dr_ai):
    """ Handles the v3 style natural language input. """
    clear_screen()
    console.print(Panel(Text("Please describe your symptoms in a single sentence.", justify="center"), title="[bold green]Advanced Conversation Mode[/bold green]"))
    console.print("\n[italic]Example: 'I have a terrible headache and feel sick to my stomach.'[/italic]\n")
    user_input = Prompt.ask("[bold]How are you feeling today?[/bold]")
    return dr_ai.analyze_from_text(user_input)

def main():
    """ Main function to run the application and show the menu. """
    dr_ai = DrAI_Core(UNIFIED_KB)
    
    while True:
        clear_screen()
        console.print(Panel(Text("Welcome to Dr. AI\nYour Unified Clinical Assistant", justify="center", style="bold magenta"), subtitle="[cyan]Final Version[/cyan]"))
        console.print(Panel(
            "How would you like to describe your symptoms?\n\n"
            "[bold]1.[/bold] Use a Guided Checklist\n"
            "[bold]2.[/bold] Describe in a Sentence (Advanced)\n\n"
            "[bold]3.[/bold] Exit",
            title="[bold green]Main Menu[/bold green]"
        ))
        choice = Prompt.ask("[bold]Enter your choice[/bold]", choices=["1", "2", "3"])

        result = None
        if choice == "1":
            result, _ = run_checklist_mode(dr_ai)
        elif choice == "2":
            with console.status("[bold green]Analyzing...[/bold]", spinner="dots"):
                time.sleep(1.5) # Simulate processing
                result, _ = run_conversation_mode(dr_ai)
        elif choice == "3":
            console.print("\nStay healthy! Exiting Dr. AI.", style="bold green")
            break
        
        if result:
            clear_screen()
            report_panel = create_report_panel(result)
            apply_safety_guardrails(report_panel)
            Prompt.ask("\n[bold]Press Enter to return to the Main Menu...[/bold]")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()

