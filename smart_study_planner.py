# Smart Study Planner
# Individual Project Coursework
#
# This program allows a student to:
# - Add study sessions
# - View all study sessions
# - Search sessions by subject
# - View study statistics
# - Save and reload study data using study_log.txt

FILE_NAME = "study_log.txt"


def classify_session(duration):
    """
    Classifies a study session based on its duration.

    Under 30 minutes  -> Short
    30 to 90 minutes  -> Medium
    Over 90 minutes   -> Long
    """
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def add_session(sessions):
    """Prompt the user for session details and add a session."""

    print("\n--- Add Study Session ---")

    subject = input("Enter subject name: ").strip()
    while not subject:
        print("Subject name cannot be empty.")
        subject = input("Enter subject name: ").strip()

    topic = input("Enter topic covered: ").strip()
    while not topic:
        print("Topic cannot be empty.")
        topic = input("Enter topic covered: ").strip()

    date = input("Enter date/day label: ").strip()
    while not date:
        print("Date/day label cannot be empty.")
        date = input("Enter date/day label: ").strip()

    # Keep asking until the user enters a positive number.
    while True:
        duration_input = input("Enter duration in minutes: ").strip()

        try:
            duration = float(duration_input)

            if duration <= 0:
                print("Duration must be a positive number.")
            else:
                break

        except ValueError:
            print("Please enter a valid number.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }

    sessions.append(session)

    print("\nStudy session added successfully!")


def print_session_table(sessions):
    """Display sessions in a formatted table."""

    if not sessions:
        return

    print("-" * 90)
    print(
        f"{'Subject':<20}"
        f"{'Topic':<30}"
        f"{'Date':<15}"
        f"{'Minutes':>10}"
        f"{'Class':>12}"
    )
    print("-" * 90)

    for session in sessions:
        classification = classify_session(session["duration"])

        print(
            f"{session['subject']:<20}"
            f"{session['topic']:<30}"
            f"{session['date']:<15}"
            f"{session['duration']:>10.1f}"
            f"{classification:>12}"
        )

    print("-" * 90)


def view_sessions(sessions):
    """Display every study session."""

    print("\n--- All Study Sessions ---")

    if not sessions:
        print("No study sessions have been recorded yet.")
        return

    print_session_table(sessions)


def search_by_subject(sessions, subject):
    """
    Search for sessions by subject.
    Matching is case-insensitive.
    """

    subject = subject.strip()

    matching_sessions = [
        session
        for session in sessions
        if session["subject"].lower() == subject.lower()
    ]

    if not matching_sessions:
        print(f"\nNo study sessions found for subject: {subject}")
        return

    print(f"\n--- Study Sessions for {subject} ---")

    print_session_table(matching_sessions)

    total_minutes = sum(
        session["duration"]
        for session in matching_sessions
    )

    print(f"Total time spent on {subject}: {total_minutes:.1f} minutes")
    print(f"Total time spent on {subject}: {total_minutes / 60:.2f} hours")


def search_menu(sessions):
    """Ask the user for a subject and perform a search."""

    print("\n--- Search Sessions by Subject ---")

    if not sessions:
        print("No study sessions have been recorded yet.")
        return

    subject = input("Enter subject to search for: ").strip()

    if not subject:
        print("Subject cannot be empty.")
        return

    search_by_subject(sessions, subject)


def study_statistics(sessions):
    """Calculate and display overall study statistics."""

    print("\n--- Study Statistics ---")

    if not sessions:
        print("No study sessions available for statistics.")
        return

    # Calculate total study time.
    total_minutes = sum(
        session["duration"]
        for session in sessions
    )

    total_hours = total_minutes / 60

    print(f"\nTotal hours studied overall: {total_hours:.2f} hours")

    # Calculate study time for each subject.
    subject_totals = {}

    for session in sessions:
        subject = session["subject"]

        if subject not in subject_totals:
            subject_totals[subject] = 0

        subject_totals[subject] += session["duration"]

    print("\nTotal study time per subject:")

    for subject, minutes in subject_totals.items():
        print(
            f"  {subject:<25} "
            f"{minutes:.1f} minutes "
            f"({minutes / 60:.2f} hours)"
        )

    # Find the subject with the least amount of study time.
    weakest_subject = min(
        subject_totals,
        key=subject_totals.get
    )

    weakest_time = subject_totals[weakest_subject]

    print(
        f"\nSubject with least study time "
        f"(weakest area): {weakest_subject}"
    )

    print(
        f"Time studied: {weakest_time:.1f} minutes "
        f"({weakest_time / 60:.2f} hours)"
    )

    # Find the longest individual study session.
    longest_session = max(
        sessions,
        key=lambda session: session["duration"]
    )

    print("\nLongest study session:")
    print(f"  Subject: {longest_session['subject']}")
    print(f"  Topic: {longest_session['topic']}")
    print(f"  Date: {longest_session['date']}")
    print(f"  Duration: {longest_session['duration']:.1f} minutes")
    print(
        f"  Classification: "
        f"{classify_session(longest_session['duration'])}"
    )


def save_sessions(sessions):
    """
    Save all sessions to study_log.txt.

    Each session is stored on one line using | as a separator.
    """

    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:

            for session in sessions:
                # Replace the separator character to avoid
                # breaking the file format.
                subject = session["subject"].replace("|", "/")
                topic = session["topic"].replace("|", "/")
                date = session["date"].replace("|", "/")

                file.write(
                    f"{subject}|"
                    f"{topic}|"
                    f"{date}|"
                    f"{session['duration']}\n"
                )

        print(f"\nSessions successfully saved to {FILE_NAME}")

    except OSError as error:
        print(f"\nError saving sessions: {error}")


def load_sessions():
    """
    Load existing sessions from study_log.txt.

    If the file does not exist, an empty list is returned.
    """

    sessions = []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:

            for line_number, line in enumerate(file, start=1):
                line = line.strip()

                if not line:
                    continue

                parts = line.split("|")

                if len(parts) != 4:
                    print(
                        f"Warning: Invalid data on line "
                        f"{line_number}. Skipping."
                    )
                    continue

                subject, topic, date, duration_text = parts

                try:
                    duration = float(duration_text)

                    if duration <= 0:
                        print(
                            f"Warning: Invalid duration on line "
                            f"{line_number}. Skipping."
                        )
                        continue

                    session = {
                        "subject": subject,
                        "topic": topic,
                        "date": date,
                        "duration": duration
                    }

                    sessions.append(session)

                except ValueError:
                    print(
                        f"Warning: Invalid duration on line "
                        f"{line_number}. Skipping."
                    )

    except FileNotFoundError:
        # This is normal during the first run.
        print("No previous study log found. Starting with an empty log.")

    except OSError as error:
        print(f"Error loading study sessions: {error}")

    return sessions


def display_menu():
    """Display the main program menu."""

    print("\n" + "=" * 55)
    print("             SMART STUDY PLANNER")
    print("=" * 55)
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")
    print("=" * 55)


def main():
    """Main program function."""

    # Load previously saved sessions when the program starts.
    sessions = load_sessions()

    print("\nWelcome to the Smart Study Planner!")

    if sessions:
        print(
            f"{len(sessions)} previously saved "
            f"study session(s) loaded."
        )

    while True:
        display_menu()

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)

        elif choice == "2":
            view_sessions(sessions)

        elif choice == "3":
            search_menu(sessions)

        elif choice == "4":
            study_statistics(sessions)

        elif choice == "5":
            save_sessions(sessions)

            print("Thank you for using Smart Study Planner!")
            print("Goodbye.")
            break

        else:
            print(
                "\nInvalid choice. "
                "Please select a number from 1 to 5."
            )


if __name__ == "__main__":
    main()