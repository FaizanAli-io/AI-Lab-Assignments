import random


class Environment:
    def __init__(self):
        self.grid = [["C" for _ in range(10)] for _ in range(10)]
        elements = [("P", 5), ("M", 5), ("N", 5)]

        for label, count in elements:
            for _ in range(count):
                while True:
                    x, y = random.randint(0, 9), random.randint(0, 9)
                    if self.grid[x][y] == "C":
                        self.grid[x][y] = label
                        break

        self.show_state()
        self.show_legend()
        self.get_locations()

    def show_legend(self):
        self.legend = {
            "P": "Patient Room",
            "M": "Medicine Storage",
            "N": "Nurse Station",
            "C": "Corridor",
        }

        print("Legend:")
        for key, desc in self.legend.items():
            print(f"{key}: {desc}")
        print()

    def show_state(self):
        print("   " + " ".join(f"{i:2}" for i in range(len(self.grid[0]))))
        print("  " + "-" * (len(self.grid[0]) * 3))

        for i, row in enumerate(self.grid):
            print(f"{i:2}| " + "  ".join(row))
        print()

    def get_locations(self):
        self.locations = {"N": [], "M": [], "P": []}

        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if cell in self.locations:
                    self.locations[cell].append((i, j))

        for key in self.locations:
            self.locations[key].sort()
            print(f"{key}: {self.locations[key]}")
        print()

    def get_nearest_room(self, start, room_type):
        nearest_room = min(
            self.locations[room_type],
            key=lambda pos: abs(pos[0] - start[0]) + abs(pos[1] - start[1]),
        )

        distance = abs(nearest_room[0] - start[0]) + abs(nearest_room[1] - start[1])
        return nearest_room, distance


class Agent:
    def __init__(self, env):
        self.env = env
        self.position = (0, 0)
        self.visited_patients = set()

    def move_to(self, dest_type, destination):
        dest_name = self.env.legend[dest_type]
        print(f"🤖: Moving to {dest_name} at {destination}...")
        self.position = destination

    def scan_patient_id(self, patient_pos):
        patient_id = f"P-{patient_pos[0]}{patient_pos[1]}"
        print(f"🤖: Scanning patient {patient_id}...")
        return patient_id

    def alert_nurse(self, patient_id, patient_pos):
        nurse_pos, _ = self.env.get_nearest_room(patient_pos, "N")

        self.move_to("N", nurse_pos)
        print(f"🤖: Alerted Nurse at {nurse_pos} about patient {patient_id}.")

    def get_medicine(self, patient_id, patient_pos):
        med_pos, _ = self.env.get_nearest_room(patient_pos, "M")

        self.move_to("M", med_pos)
        print(f"🤖: Collecting 💊 medicine from {med_pos} for patient {patient_id}...")

        self.move_to("P", patient_pos)
        print(f"🤖: Delivered 💊 medicine to patient {patient_id}.")

    def run(self):
        for patient_pos in self.env.locations.get("P", []):
            self.move_to("P", patient_pos)
            patient_id = self.scan_patient_id(patient_pos)

            if random.random() < 0.4:
                print(f"🤖: Patient {patient_id} is in critical condition 🚨")
                self.alert_nurse(patient_id, patient_pos)
            elif random.random() < 0.6:
                print(f"🤖: Patient {patient_id} needs medicine 💊")
                self.get_medicine(patient_id, patient_pos)
            else:
                print(f"🤖: Patient {patient_id} is stable ✅")
            print()

        print("🤖: All patient rooms have been visited. Task complete! ✅")


env = Environment()
Agent(env).run()
