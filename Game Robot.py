import random #pustaka yg mengahilkan angka acak
import time

class Robot:# ini adalah sebuah kelas 
    def __init__(self, name, hp, attack_power):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack_power = attack_power
        self.accuracy = 0.7  
        self.is_stunned = False
        self.is_silenced = False
        self.defense_bonus = 0 
    
    def attack_enemy(self, enemy):
        if self.is_stunned:
            print(f"----------- {self.name} tidak bisa menyerang (stunned) -----------")
            self.is_stunned = False
            return False
            
        if random.random() <= self.accuracy:
            damage = self.attack_power
            
            # Apply defense bonus if enemy has it
            if enemy.defense_bonus > 0:
                reduced_damage = int(damage * (1 - enemy.defense_bonus/100))
                damage_reduced = damage - reduced_damage
                print(f"{enemy.name} mengurangi {damage_reduced} damage karena pertahanan")
                damage = reduced_damage
                enemy.defense_bonus = 0  # Use up the defense bonus
                
            enemy.hp -= damage
            print(f"{self.name} menyerang {enemy.name} dan mengurangi {damage} HP")
            
            if enemy.hp < 0:
                enemy.hp = 0
            return True
        else:
            return False
    
    def regen_health(self, amount=None): # Memulihkan HP dan mendapatkan bonus pertahanan.
        if amount is None:
            amount = int(self.max_hp * 0.1)  # Regenerate 10% of max HP by default
        
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
            
        # Add defense bonus for next round
        self.defense_bonus = 30  # Reduce incoming damage by 30%
        print(f"{self.name} memulihkan {amount} HP dan mendapatkan bonus pertahanan")
    
    def stun(self, enemy): # Mencoba men-stun musuh (50% berhasil).
        if random.random() <= 0.5:  # 50% chance to stun
            enemy.is_stunned = True
            print(f"{self.name} berhasil menstun {enemy.name}!")
            return True
        return False
    
    def silence(self, enemy): #Mencoba men-silence musuh (40% berhasil).
        if random.random() <= 0.4:  # 40% chance to silence
            enemy.is_silenced = True
            print(f"{self.name} berhasil menyilence {enemy.name}!")
            return True
        return False
    
    def __str__(self):
        return f"{self.name} [{self.hp}|{self.attack_power}]"


class Game:# kelas game 
    def __init__(self, robot1, robot2):
        self.robot1 = robot1
        self.robot2 = robot2
        self.round = 0
    
    def display_status(self): # Menampilkan status kedua robot.
        print(f"Round-{self.round} {'=' * 50}")
        print(self.robot1)
        print(self.robot2)
        print()
    
    def display_options(self, robot): #  Menampilkan opsi aksi yang bisa diambil oleh robot.
        basic_options = "1. Attack    2. Defense    3. Giveup"
        if not robot.is_silenced:
            return basic_options + "    4. Stun    5. Silence"
        else:
            print(f"{robot.name} sedang dalam kondisi silence, tidak bisa menggunakan skill!")
            robot.is_silenced = False  # Remove silence after this round
            return basic_options
    
    def get_action(self, robot): # Meminta input pemain untuk memilih aksi robot.
        options = self.display_options(robot)
        print(options)
        action = input(f"{robot.name}, pilih aksi: ")
        return action
    
    def execute_action(self, attacker, defender, action): #  Menjalankan aksi berdasarkan input pemain.
        if action == '1':  # Attack
            if attacker.attack_enemy(defender):
                pass  # Successful attack
            else:
                print(f"----------- {attacker.name} gagal menyerang -----------")
        elif action == '2':  # Defense
            attacker.regen_health()
        elif action == '3':  # Give up
            attacker.hp = 0
            print(f"{attacker.name} menyerah!")
            return True
        elif action == '4' and not attacker.is_silenced:  # Stun
            attacker.stun(defender)
        elif action == '5' and not attacker.is_silenced:  # Silence
            attacker.silence(defender)
        
        # Check if the game is over after this action
        return self.check_game_over()
    
    def play_round(self): #Mengatur jalannya satu ronde permainan (giliran Robot 1, lalu Robot 2).
        self.round += 1
        self.display_status()
        
        # Robot 1's turn
        action1 = self.get_action(self.robot1)
        print()
        
        game_over = self.execute_action(self.robot1, self.robot2, action1)
        if game_over:
            return True
            
        # Robot 2's turn
        print()
        action2 = self.get_action(self.robot2)
        print()
        
        game_over = self.execute_action(self.robot2, self.robot1, action2)
        return game_over
    
    def check_game_over(self): ##Mengecek apakah ada robot yang HP-nya sudah habis.
        if self.robot1.hp <= 0:
            print(f"{self.robot2.name} menang!")
            return True
        elif self.robot2.hp <= 0:
            print(f"{self.robot1.name} menang!")
            return True
        return False
    
    def play_game(self): #Menjalankan permainan sampai ada pemenang.
        game_over = False
        while not game_over:
            game_over = self.play_round()
            if not game_over:
                print("\n")
                time.sleep(1)  # Add a short pause between rounds


def main():
    print("=== ROBOT BATTLE GAME ===")
    print("Dua robot akan bertarung sampai salah satu memiliki HP = 0")
    print("Setiap robot memiliki kemampuan attack, defense, dan special skills\n")
    
    name1 = input("Masukkan nama Robot 1: ") 
    name2 = input("Masukkan nama Robot 2: ") 
    
    print("\nPilih preset robot atau custom stats:")
    print("1. Balanced (HP: 500, Attack: 50)")
    print("2. Tank (HP: 800, Attack: 30)")
    print("3. Attacker (HP: 300, Attack: 80)")
    print("4. Custom")
    
    choice1 = input(f"Pilih preset untuk {name1}: ")
    choice2 = input(f"Pilih preset untuk {name2}: ")
    
    if choice1 == '1':
        robot1 = Robot(name1, 500, 50)
    elif choice1 == '2':
        robot1 = Robot(name1, 800, 30)
    elif choice1 == '3':
        robot1 = Robot(name1, 300, 80)
    elif choice1 == '4':
        hp1 = int(input(f"Masukkan HP untuk {name1}: "))
        attack1 = int(input(f"Masukkan Attack untuk {name1}: "))
        robot1 = Robot(name1, hp1, attack1)
    else:
        robot1 = Robot(name1, 500, 50)  # Default to balanced
    
    if choice2 == '1':
        robot2 = Robot(name2, 500, 50)
    elif choice2 == '2':
        robot2 = Robot(name2, 800, 30)
    elif choice2 == '3':
        robot2 = Robot(name2, 300, 80)
    elif choice2 == '4':
        hp2 = int(input(f"Masukkan HP untuk {name2}: "))
        attack2 = int(input(f"Masukkan Attack untuk {name2}: "))
        robot2 = Robot(name2, hp2, attack2)
    else:
        robot2 = Robot(name2, 500, 50)  # Default to balanced
    
    print(f"\n{name1} vs {name2}! Pertarungan dimulai!\n")
    
    # Create and start the game
    game = Game(robot1, robot2)
    game.play_game()
    
    print("\nGame Over!")
    
    play_again = input("\nMain lagi? (y/n): ")
    if play_again.lower() == 'y':
        main()


if __name__ == "__main__":
    main()
    
    
    #Deskripsi Permainan Game ini 
# Setiap robot memiliki giliran secara bergantian dan juga pemain akan Pemain memilih aksi untuk robotnya misalngya gini;
# 1. Attack → Menyerang musuh.
# 2. Defense → Memulihkan HP dan mendapatkan pertahanan.
# 3. Giveup → Menyerah dan langsung kalah.
# 4. Stun → Mencoba men-stun lawan (hanya bisa jika tidak silence).
# 5. Silence → Mencoba men-silence lawan (hanya bisa jika tidak silence).
# Pertarungan berlanjut sampai salah satu robot kehabisan HP.
# Pemenang diumumkan dan ada pilihan untuk bermain lagi.