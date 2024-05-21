from datetime import date
from PIL import Image, ImageTk
import re
import requests
import roman
import tkinter as tk


def get_wordle():
    r = requests.get(
        "https://www.nytimes.com/svc/wordle/v2/{0}.json".format(date.today())
    )
    return r.json().get("solution")


wordle = get_wordle()


class PasswordGame:
    def __init__(self):
        window = tk.Tk()
        window.title("The Password Game")
        window.iconphoto(False, tk.PhotoImage(file="images/icon.png"))
        window.geometry("600x600")

        self.rules = [
            rule_1,
            rule_2,
            rule_3,
            rule_4,
            rule_5,
            rule_6,
            rule_7,
            rule_8,
            rule_9,
            rule_10,
        ]
        self.active_rules = []
        self.previous_state = None
        self.rules_frame = tk.Frame()
        self.render()
        window.mainloop()

    def render(self):
        greeting = tk.Label(text="The Password Game", font=("", 16))
        greeting.pack(pady=48)
        text_box = tk.Entry()
        text_box.pack()
        text_box.focus()
        text_box.bind("<KeyRelease>", lambda e: self.update(text_box.get()))
        self.rules_frame.pack(pady=24)

    def label(self, text):
        label = tk.Label(master=self.rules_frame, text=text, wraplength=500)
        label.pack()

    def update(self, password):
        valid_rules = []

        for i in range(self.active_rules.__len__()):
            valid_rules.append(self.active_rules[i](password))

        # skip unnecessary update
        if not all(valid_rules) and self.previous_state == valid_rules:
            return

        for child in self.rules_frame.winfo_children():
            child.pack_forget()

        for i in range(self.active_rules.__len__()):
            if valid_rules[i]:
                continue
            match i + 1:
                case 1:
                    self.label("Rule 1: Your password must be at least 5 characters.")
                case 2:
                    self.label("Rule 2: Your password must include a number.")
                case 3:
                    self.label(
                        "Rule 3: Your password must include an uppercase letter."
                    )
                case 4:
                    self.label(
                        "Rule 4: Your password must include a special character."
                    )
                case 5:
                    self.label("Rule 5: The digits in your password must add up to 25.")
                case 6:
                    self.label(
                        "Rule 6: Your password must include a month of the year."
                    )
                case 7:
                    self.label("Rule 7: Your password must include a roman numeral.")
                case 8:
                    self.label(
                        "Rule 8: Your password must include one of our sponsors:"
                    )
                    sponsors_frame = tk.Frame(master=self.rules_frame)
                    for sponsor in ["pepsi", "starbucks", "shell"]:
                        image = Image.open(f"images/{sponsor}.png")
                        image = image.resize((85, 85))
                        photo = ImageTk.PhotoImage(image)
                        label = tk.Label(master=sponsors_frame, image=photo)
                        label.image = photo
                        label.pack(side=tk.LEFT)
                        sponsors_frame.pack()
                case 9:
                    self.label(
                        "Rule 9: The roman numerals in your password should multiply to 35."
                    )
                case 10:
                    self.label(
                        "Rule 10: Your password must include today's Wordle answer."
                    )

        if all(valid_rules):
            if self.active_rules.__len__() == self.rules.__len__():
                self.label(
                    "Congratulations! You have successfully chosen a password in "
                    + str(password.__len__())
                    + " characters."
                )
            else:
                self.active_rules.append(self.rules[self.active_rules.__len__()])
                self.update(password)

        self.previous_state = valid_rules


def rule_1(password):
    return len(password) >= 5


def rule_2(password):
    return bool(re.search(r"\d", password))


def rule_3(password):
    return bool(re.search(r"[A-Z]", password))


def rule_4(password):
    return bool(re.search(r"[ `!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?~]", password))


def rule_5(password):
    digits = [int(x) for x in password if x.isdigit()]
    return sum(digits) == 25


def rule_6(password):
    months = [
        "january",
        "february",
        "march",
        "april",
        "may",
        "june",
        "july",
        "august",
        "september",
        "november",
        "december",
    ]
    return any(month in password.lower() for month in months)


def rule_7(password):
    return bool(re.search(r"[IVXLCDM]", password))


def rule_8(password):
    sponsors = ["pepsi", "starbucks", "shell"]
    return any(sponsor in password.lower() for sponsor in sponsors)


def rule_9(password):
    numerals = re.findall(
        r"(?=.)M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})",
        password,
    )
    product = 1
    for numeral in numerals:
        for i in range(numeral.__len__()):
            value = numeral[i]
            if len(value) == 0:
                continue
            product *= roman.fromRoman(value)
    return product == 35


def rule_10(password):
    return password.lower().find(wordle) != -1


def main():
    PasswordGame()


if __name__ == "__main__":
    main()
