# Three-Phase Commit Protocol Implementation in Python
import time
import random

class Coordinator:
    def __init__(self, participants, k):
        self.participants = participants
        self.logs = []
        self.k = k  # Minimum number of participants needed to commit

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

        # Phase 2: Pre-Commit Phase
        if all(vote == "ready" for vote in votes):
            print("Coordinator: All participants are ready. Entering Pre-Commit phase...")
            self.logs.append("<Pre-Commit T>")
            acknowledgements = 0
            for participant in self.participants:
                if participant.pre_commit():
                    acknowledgements += 1
            
            # Phase 3: Commit or Abort Phase
            if acknowledgements >= self.k:
                print("Coordinator: Minimum acknowledgements received. Committing transaction...")
                self.logs.append("<Commit T>")
                for participant in self.participants:
                    participant.commit()
            else:
                print("Coordinator: Not enough acknowledgements. Aborting transaction...")
                self.logs.append("<Abort T>")
                for participant in self.participants:
                    participant.abort()
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

    def pre_commit(self):
        # Simulate possible failure before pre-commit
        if random.random() > 0.2:  # 80% chance of acknowledgement
            self.logs.append("<Pre-Commit T>")
            print(f"Participant {self.name}: Acknowledges pre-commit.")
            return True
        else:
            print(f"Participant {self.name}: Failed to acknowledge pre-commit.")
            return False

    def commit(self):
        self.logs.append("<Commit T>")
        print(f"Participant {self.name}: Committing transaction.")

    def abort(self):
        self.logs.append("<Abort T>")
        print(f"Participant {self.name}: Aborting transaction.")

# Example Usage
k = 2  # Minimum number of acknowledgements required
participants = [Participant("Store 1"), Participant("Store 2"), Participant("Store 3")]
coordinator = Coordinator(participants, k)
coordinator.start_transaction()