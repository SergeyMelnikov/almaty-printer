
ip_to_comp = {
  "127.0.0.1": "700A",
  "10.8.60.56": "700A",
}


name_team = [
('Мельников Сергей','700A'),
('Омашев Асылхан','700A'),
]


def get(ip):
    return ip_to_comp.get(ip, ip)


def get_names(team):
    names = []
    for n, t in name_team:
        if t == team:
            names.append(n)
    return ", ".join(names)
