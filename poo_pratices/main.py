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

