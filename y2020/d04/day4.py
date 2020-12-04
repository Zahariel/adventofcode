import re

def parse(line):
    result = dict()
    for entry in line.split(' '):
        key, value = re.fullmatch(r"(.+):(.+)", entry).groups()
        result[key] = value
    return result


passports = []
with open("input.txt") as f:
    passport = []
    for line in f:
        line = line.strip()
        if line == "":
            passports.append(parse(" ".join(passport)))
            passport = []
        else:
            passport.append(line)


required_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

valid = sum(1 for passport in passports if all(field in passport for field in required_fields))
print(valid)

def byr(val):
    try:
        val = int(val)
        return 1920 <= val <= 2002
    except:
        return False

def iyr(val):
    try:
        val = int(val)
        return 2010 <= val <= 2020
    except:
        return False

def eyr(val):
    try:
        val = int(val)
        return 2020 <= val <= 2030
    except:
        return False

def hgt(val):
    try:
        amt, unit = re.fullmatch(r"(\d+)(in|cm)", val).groups()
        if unit == "cm":
            return 150 <= int(amt) <= 193
        elif unit == "in":
            return 59 <= int(amt) <= 76
        else:
            return False
    except:
        return False

def hcl(val):
    match = re.fullmatch(r"#[0-9a-f]{6}", val)
    return match is not None

eye_colors = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
def ecl(val):
    return val in eye_colors

def pid(val):
    match = re.fullmatch(r"\d{9}", val)
    return match is not None

validation = {
    "byr": byr,
    "iyr": iyr,
    "eyr": eyr,
    "hgt": hgt,
    "hcl": hcl,
    "ecl": ecl,
    "pid": pid,
}

print(sum(1 for passport in passports if all(key in passport and validation[key](passport[key]) for key in validation)))


def test(input):
    passport = parse(input)
    for key in validation:
        print(key, passport[key], validation[key](passport[key]))
    print()

test("iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719")

test("pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980 hcl:#623a2f")

test("eyr:2029 ecl:blu cid:129 byr:1989 iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm")

test("hcl:#888785 hgt:164cm byr:2001 iyr:2015 cid:88 pid:545766238 ecl:hzl eyr:2022")

test("eyr:1972 cid:100 hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926")

test("iyr:2019 hcl:#602927 eyr:1967 hgt:170cm ecl:grn pid:012533040 byr:1946")

test("hcl:dab227 iyr:2012 ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277")

test("hgt:59cm ecl:zzz eyr:2038 hcl:74454a iyr:2023 pid:3556412378 byr:2007")