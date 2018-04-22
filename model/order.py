# -*- coding: utf-8 -*-

class Order:

    def __init__(self, user_email, product_id, assigns, date, price, state):
        self.user_email = user_email
        self.product_id = product_id
        self.assignments = assigns
        self.order_date = date
        self.price = price
        self.order_state = state