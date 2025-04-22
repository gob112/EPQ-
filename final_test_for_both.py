
from stable_baselines3 import PPO
from final_test_no_RL import Run
from final_test_simulation import TrafficLighAi
import threading
import csv
import multiprocessing
import random


class Env:
    def __init__(self):
        self.env = TrafficLighAi()
        self.obs = self.env.reset()
    def run(self):
        model = PPO.load("ppo_traffic_model")
        
        

        for _ in range(500000):  # Run for a few episodes
            action, _ = model.predict(self.obs)
            self.obs, reward, done, info = self.env.step(action)
            self.env.render()

            if self.env.total_cars_passed==100:
                with open("RL.csv", mode='a', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        self.env.total_reward,
                        self.env.total_cars_stoped,
                        self.env.negetive_reward
                    ])
                self.obs = self.env.reset()

def run_without_rl():
    without = Run()
    without.run()

def run_with_rl():
    with_rl = Env()
    with_rl.run()

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")  # Required on some systems
   
    p1 = multiprocessing.Process(target=run_without_rl)
    p2 = multiprocessing.Process(target=run_with_rl)

    p2.start()
    p1.start()
   
    p2.join()
    p1.join()
    

    print("Both processes finished execution!")