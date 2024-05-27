class MenuStructure:
    def __init__(self, restaurant_name):
        self.restaurant_name = restaurant_name
        self._next_id = 1
        self._dishes = []

    
    def _generateId(self):
        generated_id = self._next_id
        self._next_id += 1
        return generated_id

    def add_dish(self, dish):
       
        dish["restaurant_name"] = self.restaurant_name
        dish["id"] = self._generateId()
        
        self._dishes.append(dish)

        return dish
    
    def update_dish(self, id, updated_dish):
        for dish in self._dishes:
            if dish["id"] == id:
                dish.update(updated_dish)
                return dish
        return None

    def delete_dish(self, id):
        for position in range(len(self._dishes)):
            if self._dishes[position]["id"] == id:
                self._dishes.pop(position)
                
                return None

    def get_dish(self, id):
        for dish in self._dishes:
            if dish["id"] == int(id):
                return dish
            
        return None

    
    def get_all_dishes(self):
        return self._dishes