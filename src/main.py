import json
import random
from typing import List, Dict


def load_quotes(file_path: str = "data/quotes.json") -> List[str]:
    """Load motivational quotes from a JSON file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            quotes = json.load(f)
        if isinstance(quotes, list):
            return quotes
        return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def get_total_minutes() -> int:
    """Ask user for total available study time in minutes."""
    while True:
        raw = input("Enter total study time in minutes (e.g. 90): ").strip()
        try:
            minutes = int(raw)
            if minutes <= 0:
                print("Please enter a positive number.")
                continue
            return minutes
        except ValueError:
            print("Please enter a valid number (e.g. 60, 90, 120).")


def get_subjects() -> List[Dict]:
    """Collect subjects and priorities from the user."""
    print("\nAdd your subjects and their priority.")
    print("Priority: 1 (lowest) → 5 (highest).")
    print("Press Enter on subject name to finish.\n")

    subjects = []

    while True:
        name = input("Subject name (or press Enter to finish): ").strip()
        if not name:
            if subjects:
                break
            else:
                print("Add at least one subject.")
                continue

        while True:
            priority_raw = input(f"Priority for '{name}' [1–5]: ").strip()
            try:
                priority = int(priority_raw)
                if 1 <= priority <= 5:
                    break
                print("Priority must be between 1 and 5.")
            except ValueError:
                print("Please enter a number between 1 and 5.")

        subjects.append({"name": name, "priority": priority})

    return subjects


def build_study_plan(total_minutes: int, subjects: List[Dict]) -> List[Dict]:
    """
    Distribute total minutes across subjects.
    Base time is equal for all, extra minutes go to higher-priority subjects.
    """
    n = len(subjects)
    if n == 0:
        return []

    if total_minutes < n * 10:
        # Very little time: give everything to highest priority subject
        subjects_sorted = sorted(subjects, key=lambda s: s["priority"], reverse=True)
        top = subjects_sorted[0]
        return [{"name": top["name"], "minutes": total_minutes, "priority": top["priority"]}]

    base = total_minutes // n
    remaining = total_minutes - base * n

    allocations = [base] * n

    # Distribute remaining minutes to higher priority subjects first
    indices_by_priority = sorted(range(n), key=lambda i: subjects[i]["priority"], reverse=True)

    for idx in indices_by_priority:
        if remaining <= 0:
            break
        allocations[idx] += 1
        remaining -= 1

    plan = []
    for i, subject in enumerate(subjects):
        plan.append(
            {
                "name": subject["name"],
                "priority": subject["priority"],
                "minutes": allocations[i],
            }
        )

    return plan


def display_plan(plan: List[Dict]):
    """Print the generated study plan in a readable format."""
    if not plan:
        print("No plan generated.")
        return

    print("\n=== Your Study Plan ===\n")
    for i, block in enumerate(plan, start=1):
        name = block["name"]
        minutes = block["minutes"]
        priority = block["priority"]
        print(f"Block {i}: {name} — {minutes} minutes (priority {priority})")

    print("\nSuggestion: Take a 5-minute break between each block.\n")


def show_motivational_quote(quotes: List[str]):
    """Print one random motivational quote if available."""
    if not quotes:
        return
    quote = random.choice(quotes)
    print("⭐ Study Buddy says:")
    print(f"  \"{quote}\"\n")


def main():
    print("=== Study Buddy — Time Manager ===\n")

    total_minutes = get_total_minutes()
    subjects = get_subjects()
    plan = build_study_plan(total_minutes, subjects)
    display_plan(plan)

    quotes = load_quotes()
    show_motivational_quote(quotes)

    print("All the best with your session. 💻📚")


if __name__ == "__main__":
    main()
