class Canal:
    def __init__(self, name, description, subscribers):
        self.name = name
        self.description = description
        self.subscribers = subscribers
    def subscribe(self, act=1):
        self.subscribers += act

class CanalEmpresarial(Canal):
    def __init__(self, name, description, subscribers):
        super().__init__(name, description, subscribers)
        self._team = []

    @property
    def team(self):
            return self._team

    def add_team_member(self, member):
         if member not in self._team:
              self._team.append(member)
         else:
              print("esse memnbro já tá no time")

class Video:
     def __init__(self, title, desc):
          self.title = title
          self.desc = desc

canal_crab_master_duel = Canal("Crab master duel", "Videos of master duel ranked", 27350)

print(canal_crab_master_duel.name)
print(canal_crab_master_duel.subscribers)
canal_crab_master_duel.subscribe()
print(canal_crab_master_duel.subscribers)

canal_riot = CanalEmpresarial("Riot games", "lol", 1200000)
print(canal_riot._team)

canal_riot.add_team_member("Ana")

print(canal_riot._team)

canal_riot.add_team_member("Ana")

print(canal_riot._team)


class Card:
     def __init__(self, atk, defense, effect, ):
          self.atk = atk
          self.defense = defense
          self.effect = effect
          
Dark_Old_Fairy = Card(1000, 1200, "Passa o turno se destruída no seu turno.")

print(Dark_Old_Fairy.atk)

with open("cards.json", "w", encoding="utf-8" ) as q:
     q.write("{")
     q.write("=" * 50 )
     q.write("\nDark Old Fairy\n")
     q.write(f"\natk:{Dark_Old_Fairy.atk}\n")
     q.write(f"\ndef:{Dark_Old_Fairy.defense}\n")
     q.write(f"\neffect:{Dark_Old_Fairy.effect}\n")
     q.write("=" * 50)
     q.write("}")

