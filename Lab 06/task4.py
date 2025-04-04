from ortools.sat.python import cp_model
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import random
import time


class WarehouseRobotPlanning:
    def __init__(self, grid_size, num_robots, num_packages):
        self.grid_size = grid_size
        self.num_robots = num_robots
        self.num_packages = num_packages
        self.time_horizon = grid_size[0] * grid_size[1] * 2

        self.model = cp_model.CpModel()

        self.generate_warehouse_setup()

        self.define_variables()

        self.add_constraints()

        self.define_objective()

    def generate_warehouse_setup(self):
        rows, cols = self.grid_size

        self.robot_start_positions = []
        self.robot_capacities = []
        self.robot_battery_levels = []

        positions = set()
        for i in range(self.num_robots):
            while True:
                pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))
                if pos not in positions:
                    positions.add(pos)
                    self.robot_start_positions.append(pos)
                    break

            self.robot_capacities.append(random.randint(1, 3))

            self.robot_battery_levels.append(random.randint(20, 40))

        self.package_locations = []
        self.package_destinations = []
        self.package_weights = []

        for i in range(self.num_packages):

            while True:
                pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))
                if pos not in positions:
                    positions.add(pos)
                    self.package_locations.append(pos)
                    break

            while True:
                pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))
                if pos not in positions:
                    positions.add(pos)
                    self.package_destinations.append(pos)
                    break

            self.package_weights.append(random.randint(1, 3))

        self.charging_stations = []
        num_charging_stations = min(3, rows * cols - len(positions))

        for i in range(num_charging_stations):
            while True:
                pos = (random.randint(0, rows - 1), random.randint(0, cols - 1))
                if pos not in positions:
                    positions.add(pos)
                    self.charging_stations.append(pos)
                    break

    def define_variables(self):
        """Define all variables for the CSP model"""

        self.robot_positions_x = {}
        self.robot_positions_y = {}

        for r in range(self.num_robots):
            for t in range(self.time_horizon):
                self.robot_positions_x[r, t] = self.model.NewIntVar(
                    0, self.grid_size[0] - 1, f"robot_{r}_pos_x_{t}"
                )
                self.robot_positions_y[r, t] = self.model.NewIntVar(
                    0, self.grid_size[1] - 1, f"robot_{r}_pos_y_{t}"
                )

        self.package_pickup_time = {}
        for p in range(self.num_packages):
            self.package_pickup_time[p] = self.model.NewIntVar(
                0, self.time_horizon - 1, f"pickup_time_{p}"
            )

        self.package_delivery_time = {}
        for p in range(self.num_packages):
            self.package_delivery_time[p] = self.model.NewIntVar(
                0, self.time_horizon - 1, f"delivery_time_{p}"
            )

        self.robot_assigned = {}
        for p in range(self.num_packages):
            self.robot_assigned[p] = self.model.NewIntVar(
                0, self.num_robots - 1, f"robot_assigned_{p}"
            )

        self.robot_battery = {}
        for r in range(self.num_robots):
            for t in range(self.time_horizon):
                self.robot_battery[r, t] = self.model.NewIntVar(
                    0, 100, f"robot_{r}_battery_{t}"
                )

        self.robot_load = {}
        for r in range(self.num_robots):
            for t in range(self.time_horizon):
                self.robot_load[r, t] = self.model.NewIntVar(
                    0, self.robot_capacities[r], f"robot_{r}_load_{t}"
                )

        self.robot_charging = {}
        for r in range(self.num_robots):
            for t in range(self.time_horizon):
                self.robot_charging[r, t] = self.model.NewBoolVar(
                    f"robot_{r}_charging_{t}"
                )

        self.package_carried = {}
        for p in range(self.num_packages):
            for t in range(self.time_horizon):
                self.package_carried[p, t] = self.model.NewBoolVar(
                    f"package_{p}_carried_{t}"
                )

        self.package_carrier = {}
        for p in range(self.num_packages):
            for t in range(self.time_horizon):
                self.package_carrier[p, t] = self.model.NewIntVar(
                    -1, self.num_robots - 1, f"package_{p}_carrier_{t}"
                )

    def add_constraints(self):
        """Add all constraints to the model"""

        for r in range(self.num_robots):
            self.model.Add(
                self.robot_positions_x[r, 0] == self.robot_start_positions[r][0]
            )
            self.model.Add(
                self.robot_positions_y[r, 0] == self.robot_start_positions[r][1]
            )
            self.model.Add(self.robot_battery[r, 0] == self.robot_battery_levels[r])
            self.model.Add(self.robot_load[r, 0] == 0)

        for p in range(self.num_packages):
            self.model.Add(self.package_carried[p, 0] == False)
            self.model.Add(self.package_carrier[p, 0] == -1)

        for r in range(self.num_robots):
            for t in range(self.time_horizon - 1):

                x_diff = self.model.NewIntVar(
                    -self.grid_size[0], self.grid_size[0], f"x_diff_{r}_{t}"
                )
                y_diff = self.model.NewIntVar(
                    -self.grid_size[1], self.grid_size[1], f"y_diff_{r}_{t}"
                )

                self.model.Add(
                    x_diff
                    == self.robot_positions_x[r, t + 1] - self.robot_positions_x[r, t]
                )
                self.model.Add(
                    y_diff
                    == self.robot_positions_y[r, t + 1] - self.robot_positions_y[r, t]
                )

                x_diff_abs = self.model.NewIntVar(
                    0, self.grid_size[0], f"x_diff_abs_{r}_{t}"
                )
                y_diff_abs = self.model.NewIntVar(
                    0, self.grid_size[1], f"y_diff_abs_{r}_{t}"
                )

                self.model.AddAbsEquality(x_diff_abs, x_diff)
                self.model.AddAbsEquality(y_diff_abs, y_diff)

                self.model.Add(x_diff_abs + y_diff_abs <= 1)

        for r1 in range(self.num_robots):
            for r2 in range(r1 + 1, self.num_robots):
                for t in range(self.time_horizon):

                    same_pos = self.model.NewBoolVar(f"same_pos_{r1}_{r2}_{t}")

                    self.model.Add(
                        self.robot_positions_x[r1, t] == self.robot_positions_x[r2, t]
                    ).OnlyEnforceIf(same_pos)
                    self.model.Add(
                        self.robot_positions_y[r1, t] == self.robot_positions_y[r2, t]
                    ).OnlyEnforceIf(same_pos)

                    self.model.Add(same_pos == 0)

        for r in range(self.num_robots):
            for t in range(self.time_horizon - 1):

                is_charging = self.robot_charging[r, t]

                self.model.Add(is_charging == 0)

                for cs in range(len(self.charging_stations)):
                    at_station = self.model.NewBoolVar(f"robot_{r}_at_station_{cs}_{t}")

                    self.model.Add(
                        self.robot_positions_x[r, t] == self.charging_stations[cs][0]
                    ).OnlyEnforceIf(at_station)
                    self.model.Add(
                        self.robot_positions_y[r, t] == self.charging_stations[cs][1]
                    ).OnlyEnforceIf(at_station)

                    self.model.Add(is_charging == 1).OnlyEnforceIf(at_station)

                charging_amount = self.model.NewIntVar(
                    0, 10, f"charging_amount_{r}_{t}"
                )
                self.model.Add(charging_amount == 10).OnlyEnforceIf(is_charging)
                self.model.Add(charging_amount == -1).OnlyEnforceIf(is_charging.Not())

                next_battery = self.model.NewIntVar(0, 100, f"next_battery_{r}_{t}")
                self.model.Add(
                    next_battery == self.robot_battery[r, t] + charging_amount
                )

                battery_limited = self.model.NewIntVar(
                    0, 100, f"battery_limited_{r}_{t}"
                )
                self.model.Add(battery_limited <= next_battery)
                self.model.Add(battery_limited <= 100)
                self.model.AddMaxEquality(battery_limited, [next_battery, 100])
                self.model.Add(self.robot_battery[r, t + 1] == battery_limited)

                self.model.Add(self.robot_battery[r, t] > 0)

        for p in range(self.num_packages):
            for t in range(self.time_horizon - 1):

                self.model.Add(
                    self.package_carried[p, t + 1] == self.package_carried[p, t]
                )
                self.model.Add(
                    self.package_carrier[p, t + 1] == self.package_carrier[p, t]
                )

        for p in range(self.num_packages):
            r_var = self.robot_assigned[p]
            t_var = self.package_pickup_time[p]

            for t in range(self.time_horizon):
                before_pickup = self.model.NewBoolVar(f"before_pickup_{p}_{t}")
                self.model.Add(t < t_var).OnlyEnforceIf(before_pickup)
                self.model.Add(t >= t_var).OnlyEnforceIf(before_pickup.Not())

                self.model.Add(self.package_carried[p, t] == False).OnlyEnforceIf(
                    before_pickup
                )
                self.model.Add(self.package_carrier[p, t] == -1).OnlyEnforceIf(
                    before_pickup
                )

            for r in range(self.num_robots):

                robot_assigned_p = self.model.NewBoolVar(f"robot_{r}_assigned_p_{p}")
                self.model.Add(r_var == r).OnlyEnforceIf(robot_assigned_p)
                self.model.Add(r_var != r).OnlyEnforceIf(robot_assigned_p.Not())

                for t in range(self.time_horizon - 1):

                    pickup_at_t = self.model.NewBoolVar(f"pickup_{p}_at_t_{t}")
                    self.model.Add(t_var == t).OnlyEnforceIf(pickup_at_t)
                    self.model.Add(t_var != t).OnlyEnforceIf(pickup_at_t.Not())

                    pickup_by_robot_at_t = self.model.NewBoolVar(
                        f"pickup_by_robot_{r}_at_t_{p}_{t}"
                    )
                    self.model.AddBoolAnd(
                        [robot_assigned_p, pickup_at_t]
                    ).OnlyEnforceIf(pickup_by_robot_at_t)

                    self.model.Add(
                        self.robot_positions_x[r, t] == self.package_locations[p][0]
                    ).OnlyEnforceIf(pickup_by_robot_at_t)
                    self.model.Add(
                        self.robot_positions_y[r, t] == self.package_locations[p][1]
                    ).OnlyEnforceIf(pickup_by_robot_at_t)

                    self.model.Add(
                        self.robot_load[r, t] + self.package_weights[p]
                        <= self.robot_capacities[r]
                    ).OnlyEnforceIf(pickup_by_robot_at_t)

                    self.model.Add(
                        self.robot_load[r, t + 1]
                        == self.robot_load[r, t] + self.package_weights[p]
                    ).OnlyEnforceIf(pickup_by_robot_at_t)

                    self.model.Add(
                        self.package_carried[p, t + 1] == True
                    ).OnlyEnforceIf(pickup_by_robot_at_t)
                    self.model.Add(self.package_carrier[p, t + 1] == r).OnlyEnforceIf(
                        pickup_by_robot_at_t
                    )

        for p in range(self.num_packages):
            r_var = self.robot_assigned[p]
            t_var = self.package_delivery_time[p]

            for t in range(self.time_horizon):
                after_delivery = self.model.NewBoolVar(f"after_delivery_{p}_{t}")
                self.model.Add(t > t_var).OnlyEnforceIf(after_delivery)
                self.model.Add(t <= t_var).OnlyEnforceIf(after_delivery.Not())

                self.model.Add(self.package_carried[p, t] == False).OnlyEnforceIf(
                    after_delivery
                )
                self.model.Add(self.package_carrier[p, t] == -1).OnlyEnforceIf(
                    after_delivery
                )

            for r in range(self.num_robots):

                robot_assigned_p = self.model.NewBoolVar(
                    f"robot_{r}_assigned_del_p_{p}"
                )
                self.model.Add(r_var == r).OnlyEnforceIf(robot_assigned_p)
                self.model.Add(r_var != r).OnlyEnforceIf(robot_assigned_p.Not())

                for t in range(self.time_horizon - 1):

                    delivery_at_t = self.model.NewBoolVar(f"delivery_{p}_at_t_{t}")
                    self.model.Add(t_var == t).OnlyEnforceIf(delivery_at_t)
                    self.model.Add(t_var != t).OnlyEnforceIf(delivery_at_t.Not())

                    delivery_by_robot_at_t = self.model.NewBoolVar(
                        f"delivery_by_robot_{r}_at_t_{p}_{t}"
                    )
                    self.model.AddBoolAnd(
                        [robot_assigned_p, delivery_at_t]
                    ).OnlyEnforceIf(delivery_by_robot_at_t)

                    self.model.Add(
                        self.robot_positions_x[r, t] == self.package_destinations[p][0]
                    ).OnlyEnforceIf(delivery_by_robot_at_t)
                    self.model.Add(
                        self.robot_positions_y[r, t] == self.package_destinations[p][1]
                    ).OnlyEnforceIf(delivery_by_robot_at_t)

                    self.model.Add(self.package_carried[p, t] == True).OnlyEnforceIf(
                        delivery_by_robot_at_t
                    )
                    self.model.Add(self.package_carrier[p, t] == r).OnlyEnforceIf(
                        delivery_by_robot_at_t
                    )

                    self.model.Add(
                        self.robot_load[r, t + 1]
                        == self.robot_load[r, t] - self.package_weights[p]
                    ).OnlyEnforceIf(delivery_by_robot_at_t)

            self.model.Add(self.package_pickup_time[p] < self.package_delivery_time[p])

            min_travel_time = self.model.NewIntVar(
                1, self.time_horizon, f"min_travel_time_{p}"
            )

            px, py = self.package_locations[p]
            dx, dy = self.package_destinations[p]
            manhattan_dist = abs(px - dx) + abs(py - dy)

            self.model.Add(min_travel_time >= manhattan_dist)

            self.model.Add(
                self.package_delivery_time[p]
                >= self.package_pickup_time[p] + min_travel_time
            )

    def define_objective(self):
        """Define the objective function to minimize total delivery time"""
        max_delivery_time = self.model.NewIntVar(
            0, self.time_horizon, "max_delivery_time"
        )

        for p in range(self.num_packages):
            self.model.Add(max_delivery_time >= self.package_delivery_time[p])

        self.model.Minimize(max_delivery_time)

    def solve(self):
        """Solve the model and return the solution"""
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 120
        solver.parameters.log_search_progress = True

        print("Solving the warehouse robot planning problem...")
        start_time = time.time()
        status = solver.Solve(self.model)
        end_time = time.time()

        print(f"Solving completed in {end_time - start_time:.2f} seconds.")

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            print(
                f"Found {'optimal' if status == cp_model.OPTIMAL else 'feasible'} solution:"
            )

            solution = {
                "robot_paths": {},
                "package_assignments": {},
                "package_pickup_times": {},
                "package_delivery_times": {},
                "robot_capacities": self.robot_capacities,
                "package_weights": self.package_weights,
                "package_locations": self.package_locations,
                "package_destinations": self.package_destinations,
                "charging_stations": self.charging_stations,
            }

            for r in range(self.num_robots):
                solution["robot_paths"][r] = []
                for t in range(self.time_horizon):
                    x = solver.Value(self.robot_positions_x[r, t])
                    y = solver.Value(self.robot_positions_y[r, t])
                    solution["robot_paths"][r].append((x, y))

                    if (
                        t > 0
                        and solution["robot_paths"][r][t]
                        == solution["robot_paths"][r][t - 1]
                    ):

                        all_delivered = True
                        for p in range(self.num_packages):
                            if (
                                solver.Value(self.robot_assigned[p]) == r
                                and solver.Value(self.package_delivery_time[p]) >= t
                            ):
                                all_delivered = False
                                break

                        if all_delivered:
                            solution["robot_paths"][r] = solution["robot_paths"][r][
                                : t + 1
                            ]
                            break

            for p in range(self.num_packages):
                robot_id = solver.Value(self.robot_assigned[p])
                pickup_time = solver.Value(self.package_pickup_time[p])
                delivery_time = solver.Value(self.package_delivery_time[p])

                solution["package_assignments"][p] = robot_id
                solution["package_pickup_times"][p] = pickup_time
                solution["package_delivery_times"][p] = delivery_time

                print(
                    f"Package {p+1}: Robot {robot_id+1} picks up at time {pickup_time}, delivers at time {delivery_time}"
                )

                print(f"Pickup location: {self.package_locations[p]}")
                print(f"Delivery location: {self.package_destinations[p]}")
                print(f"Robot start position: {self.robot_start_positions[robot_id]}")
                print(f"Robot capacity: {self.robot_capacities[robot_id]}")
                print(f"Package weight: {self.package_weights[p]}")
                print()

            max_delivery_time = max(solution["package_delivery_times"].values())
            print(f"Total completion time: {max_delivery_time}")

            return solution
        else:
            print("No solution found.")
            return None


if __name__ == "__main__":
    random.seed(42)

    warehouse = WarehouseRobotPlanning((6, 6), 5, 10)
    solution = warehouse.solve()
