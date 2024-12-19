# Two-Phase Commit Protocol Implementation in Python
import time
import random

class Coordinator:
    def __init__(self, participants):
        self.participants = participants
        self.logs = []

    def start_transaction(self):
        print("Coordinator: Starting transaction...")
        self.logs.append("<Prepare T>")
        # Phase 1: Prepare Phase
        votes = []
        for participant in self.participants:
            vote = participant.prepare()
            votes.append(vote)
            if vote == "abort":
                break

        # Phase 2: Commit or Abort
        if all(vote == "ready" for vote in votes):
            print("Coordinator: All participants are ready. Committing transaction...")
            self.logs.append("<Commit T>")
            for participant in self.participants:
                participant.commit()
        else:
            print("Coordinator: Abort received. Aborting transaction...")
            self.logs.append("<Abort T>")
            for participant in self.participants:
                participant.abort()

class Participant:
    def __init__(self, name):
        self.name = name
        self.logs = []

    def prepare(self):
        decision = random.choice(["ready", "abort"])
        if decision == "abort":
            self.logs.append(f"<no T>")
            print(f"Participant {self.name}: Vote to abort.")
            return "abort"
        else:
            self.logs.append(f"<ready T>")
            print(f"Participant {self.name}: Vote to commit.")
            return "ready"

    def commit(self):
        self.logs.append("<Commit T>")
        print(f"Participant {self.name}: Committing transaction.")

    def abort(self):
        self.logs.append("<Abort T>")
        print(f"Participant {self.name}: Aborting transaction.")

# Example Usage
participants = [Participant("Store 1"), Participant("Store 2"), Participant("Store 3")]
coordinator = Coordinator(participants)
coordinator.start_transaction()