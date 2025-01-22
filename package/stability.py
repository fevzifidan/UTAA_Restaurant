class Stability:
    """
    We want to get the most stable value to both facilitate the operation of
    the program and showing a stable value to the customer when color and shape
    detection functions produce frequent and unstable results.
    """

    def __init__(self, menu):
        self.menu = menu
        self.color_stability_list = list()
        self.shape_stability_list = list()
        self.order_stability_list = list()

    def get_stable_order(self, shape, color):

        def get_stable_property(lst, active_value):

            if active_value != None: return active_value
            value_dict = dict()
            for item in lst:
                if item != None: value_dict[item] = value_dict.get(item, 0) + 1
            
            try:
                max_value = max(value_dict, key=value_dict.get)
            except ValueError:
                # The list is most likely empty
                max_value = None
            return max_value
        
        stable_shape = get_stable_property(self.shape_stability_list, shape)
        stable_color = get_stable_property(self.color_stability_list, color)

        order = self.menu.get_name(stable_color, stable_shape)
        self.order_stability_list.append(order)
        return get_stable_property(self.order_stability_list, order)
    
    def reset(self):
        self.color_stability_list.clear()
        self.shape_stability_list.clear()
        self.order_stability_list.clear()


# END