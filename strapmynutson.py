import csv
from collections import defaultdict


class Card:
    def __init__(self, card_name, card_grade, cost):
        self.card_name = card_name
        try:
            self.card_grade = int(card_grade)
        except ValueError:
            raise TypeError("card_grade must be an integer or a string representation of an integer")
        self.cost = float(cost)


class CardReport:
    def __init__(self, card_name, filename='graded_card_data.csv'):
        self.card_name = card_name
        self.filename = filename
        self.total_graded = 0
        self.num_10s = 0
        self.num_9s = 0
        self.num8_lower = 0
        self.data = []
        self.tally = defaultdict(lambda: {'Total': 0, '10s': 0, '9s': 0, '8s or lower': 0})
        self.revenues = defaultdict(lambda: 0)

    def get_counts(self, card_name):
        return self.tally[card_name]

    def add_card(self, card):
        self.total_graded += 1
        if card.card_grade == 10:
            self.num_10s += 1
        elif card.card_grade == 9:
            self.num_9s += 1
        else:
            self.num8_lower += 1
        self.data.append({'Card Name': card.card_name, 'Card Grade': card.card_grade})
        counts = self.get_counts(card.card_name)
        counts['Total'] += 1
        if card.card_grade == 10:
            counts['10s'] += 1
        elif card.card_grade == 9:
            counts['9s'] += 1
        else:
            counts['8s or lower'] += 1
        self.revenues[card.card_name] = 0

    def remove_card(self, card):
        self.total_graded -= 1
        if card.card_grade == 10:
            self.num_10s -= 1
        elif card.card_grade == 9:
            self.num_9s -= 1
        else:
            self.num8_lower -= 1
        self.data.remove({'Card Name': card.card_name, 'Card Grade': card.card_grade})
        counts = self.get_counts(card.card_name)
        counts['Total'] -= 1
        if card.card_grade == 10:
            counts['10s'] -= 1
        elif card.card_grade == 9:
            counts['9s'] -= 1
        else:
            counts['8s or lower'] -= 1
        if counts['Total'] == 0:
            del self.tally[card.card_name]
            del self.revenues[card.card_name]

    def update_revenue(self, card_name, revenue):
        if card_name not in self.revenues:
            print(f"Card {card_name} not found.")
        else:
            self.revenues[card_name] = revenue

    def get_profit(self, card_name):
        if card_name not in self.revenues:
            return 0
        return self.revenues[card_name] - self.get_cost(card_name)

    def get_cost(self, card_name):
        card_costs = {'Card A': 10.0, 'Card B': 5.0, 'Card C': 2.0}  # example card costs
        if card_name in card_costs:
            return card_costs[card_name]
        else:
            return 0

    def write_to_file(self):
        try:
            with open(self.filename, mode='w', newline='') as csvfile:
                fieldnames = ['Card Name', 'Card Grade', 'Quantity', '10s', '9s', '8s or lower', 'Cost', 'Revenue',
                              'Profit']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                for card in self.data:
                    card_name = card['Card Name']
                    counts = self.get_counts(card_name)
                    quantity = counts['Total']
                    if quantity == 0:
                        continue

                    cost = self.get_cost(card_name)
                    revenue = self.revenues[card_name]
                    profit = self.get_profit(card_name)

                    row = {
                        'Card Name': card_name,
                        'Card Grade': card['Card Grade'],
                        'Quantity': quantity,
                        '10s': counts['10s'],
                        '9s': counts['9s'],
                        '8s or lower': counts['8s or lower'],
                        'Cost': cost,
                        'Revenue': revenue,
                        'Profit': profit,
                    }
                    writer.writerow(row)
        except FileNotFoundError:
            print(f"File {self.filename} not found.")


if __name__ == '__main__':
    def main():
        card_report = CardReport('My Card Report')
        while True:
            print('1. Add card')
            print('2. Remove card')
            print('3. Update revenue')
            print('4. Print report')
            print('5. Quit')

            choice = input('Enter your choice: ')
            if choice == '1':
                card_name = input('Enter card name: ')
                card_grade = input('Enter card grade: ')
                cost = input('Enter card cost: ')
                card = Card(card_name, card_grade, cost)
                card_report.add_card(card)
            elif choice == '2':
                card_name = input('Enter card name: ')
                card_grade = input('Enter card grade: ')
                cost = input('Enter card cost: ')
                card = Card(card_name, card_grade, cost)
                card_report.remove_card(card)
            elif choice == '3':
                card_name = input('Enter card name: ')
                revenue = input('Enter card revenue: ')
                card_report.update_revenue(card_name, revenue)
            elif choice == '4':
                card_report.write_to_file()
            elif choice == '5':
                break
            else:
                print('Invalid choice. Please enter a number between 1 and 5.')






