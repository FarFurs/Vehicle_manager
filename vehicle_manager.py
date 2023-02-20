import requests
from math import radians, cos, sin, asin, sqrt

class VehicleManager:
    """Класс для работы с API и объектами класса Vehicle""" 
    cars = [] #Объявление списка с объектами класса Vehicle





    def __init__(self, url):
        """Инициализация экземпляра класса VehicleManager и объектов класса Vehicle"""
        self.url = url
        response = requests.get(self.url + '/vehicles')
        for data in response.json():
            VehicleManager.cars.append(Vehicle(data))





    def get_vehicles(self):
        """Вывод всех авто(выводятся объекты класса Vehicle, так как БД не обновляется и новые/изменненые она не выведет"""
        response = requests.get(self.url + '/vehicles') 
        for item in VehicleManager.cars:
            item.display_vehicle()





    def filter_vehicles(self, params):
        """Выводит авто по заданным параметрам"""
        # Таким должен быть запрос к БД, если бы она работала на запись(не выведет новые и измененные авто)
        
        # response = requests.get(self.url + '/vehicles') 
        # for item in response.json():
        #     compare_keys = item.keys() - (item.keys() - params.keys())
        #     if compare_keys == 0:
        #         compare_keys == params.keys()
        #     flag = 0
        #     for key in compare_keys:
        #         if item[key] != params[key]:
        #             flag = 1
        #     if flag == 0:
        #         VehicleManager.cars[item['id'] - 1].display_vehicle()


        compare_keys = VehicleManager.cars[1].__dict__.keys() - (VehicleManager.cars[1].__dict__.keys() - params.keys()) # список ключей для сравнения
        if compare_keys == 0:
            compare_keys = params.keys()
        for item in VehicleManager.cars: # Поиск авто удовлетворяющего заданным параметрам
            flag = 0
            for key in compare_keys:
                if getattr(item, key) != params[key]:
                    flag = 1
            if flag == 0:
                item.display_vehicle()





    def get_vehicle(self, vehicle_id):
        """Вывод авто по id"""
        response = requests.get(self.url + '/vehicles/' + str(vehicle_id)) # Запрос к БД 
        
        for item in VehicleManager.cars:
            if item.id == vehicle_id:
                item.display_vehicle()
                break





    def add_vehicle(self, data):
        """Добавление нового авто"""
        vehicle_id = VehicleManager.cars[-1].id + 1
        data.update({'id': vehicle_id})
        VehicleManager.cars.append(Vehicle(data))
        VehicleManager.cars[vehicle_id - 1].display_vehicle()
        requests.post(self.url + '/vehicles', data = data)





    def update_vehicle(self, id, data):
        """Изменение атрибутов авто"""
        if len(data) > 1:
            for item in data:
                for key in item.keys():
                    setattr(VehicleManager.cars[id - 1], key, data[key]) # Обновляет экземпляр класса Vehicle
        else:
            for key in data.keys():
                setattr(VehicleManager.cars[id - 1], key, data[key]) # Обновляет экземпляр класса Vehicle

        requests.put(self.url + 'vehicles/' + str(id), data = data) # Обновляет БД





    def delete_vehicle(self, id):
        """Удаление авто"""
        requests.delete(self.url + 'vehicles/'+ str(id)) #Удаление из БД
        del VehicleManager.cars[id - 1] #Удаление объекта класса Vehicle




    def get_distance(self, id1, id2):
        """Находит расстояние между двумя заданными авто"""

        vehicle_1 = requests.get(self.url + '/vehicles/' + str(id1))
        vehicle_2 = requests.get(self.url + '/vehicles/' + str(id2))

        la_1 = radians(VehicleManager.cars[id1 - 1].latitude)
        la_2 = radians(VehicleManager.cars[id2 - 1].latitude)
        lo_1 = radians(VehicleManager.cars[id1 - 1].longitude)
        lo_2 = radians(VehicleManager.cars[id2 - 1].longitude)
        d_la = la_2 - la_1
        d_lo = lo_2 - lo_1
        p = sin(d_la / 2)**2 + cos(la_1) * cos(la_2) * sin(d_lo / 2)**2
        q = 2 * asin(sqrt(p))
        distance = q * 6371
        print('Растояние в км = ', distance)
    



    def get_nearest_vehicle(self, id):
        """Находить ближайщий авто к заданному"""

        vehicle_1 = requests.get(self.url + '/vehicles/' + str(id))
        vehicle_all = requests.get(self.url + '/vehicles')

        distance = 0
        for item in VehicleManager.cars:
            if item.id != id:
                la_1 = radians(VehicleManager.cars[id - 1].latitude)
                la_2 = radians(item.latitude)
                lo_1 = radians(VehicleManager.cars[id - 1].longitude)
                lo_2 = radians(item.longitude)
                d_la = la_2 - la_1
                d_lo = lo_2 - lo_1
                p = sin(d_la / 2)**2 + cos(la_1) * cos(la_2) * sin(d_lo / 2)**2
                q = 2 * asin(sqrt(p))
                if distance == 0 or distance > q * 6371:
                    distance = q * 6371
                    nearest_vehicle = item
        nearest_vehicle.display_vehicle()




class Vehicle:
    """Хранит инфо по авто"""
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.model = data['model']
        self.year = data['year']
        self.color = data['color']
        self.price = data['price']
        self.latitude = data['latitude']
        self.longitude = data['longitude']




    def display_vehicle(self):
        """Отображает авто"""
        print(self.name, self.model, self.year, self.color, self.price, '\n')




    def display_vehicle_info(self):
        """Отображает всю инфо по авто"""
        print(self.id, self.name, self.model, self.year, self.color, self.price, self.latitude, self.longitude, '\n')




def exeption(filter): #Проверяет корректность введенных данных
    if filter.split(',') != 0:
        for item in filter.split(','):
            x = item.split(':')[0].lstrip()
            if x != 'name' and x != 'model' and x != 'year' and x != 'color' and x != 'price' and x != 'latitude' and x != 'longitude':
                return 1
    else:
        x = item.split(':')[0].lstrip()
        if x != 'name' and x != 'model' and x != 'year' and x != 'color' and x != 'price' and x != 'latitude' and x != 'longitude':
            return 1
    return 0




def control(manager): #Функция для управление из консоли
    while True:
        print('Получить спискок автомобилей - 1\nПолучить список по заданным параметрам - 2')
        print('Получить инфо об авто по id - 3\nДобавить новое авто - 4')
        print('Изменить инфо об авто - 5\nУдалить авто - 6')
        print('Расстояние между двумя авто - 7\nНайти ближайщее авто к заданному - 8')
        print('Выйти - 9\nВведите число')
        x = int(input())
        
        
        if x == 1:
            manager.get_vehicles()
        
        
        if x == 2:
            while True:
                print('Введите параметры в формате - name: Toyota, price: 20000')
                filter = input()
                flag = exeption(filter)
                if flag == 1:
                    print('Некорректный ввод данных')
                    break
                else:
                    params = {}
                    for item in filter.split(','):
                        param = item.split(':')
                        params.update({param[0].lstrip(): param[-1].lstrip()})
                    manager.filter_vehicles(params = params)
                    break
        

        if x == 3:
            print('Введите id')
            id = int(input())
            manager.get_vehicle(vehicle_id = id)


        if x == 4:
            while True:
                print('Введите параметры авто в формате - name: Toyota, model: Land Cruser...(name,model,year,color,price,latitude,longitude)')
                filter = input()
                flag = exeption(filter)
                if flag == 1:
                    print('Некорректный ввод данных')
                    break
                else:
                    if len(filter.split(',')) < 6:
                        print('Некорректный ввод данных')
                        break
                    data={}
                    for item in filter.split(','):
                        param = item.split(':')
                        data.update({param[0].lstrip(): param[-1].lstrip()})
                    manager.add_vehicle(data)
                    break


        if x == 5:
            while True:
                for item in VehicleManager.cars:
                    item.display_vehicle_info()
                print('Введите id авто, которое хотите изменить')
                id = int(input())
                print('Введите параметры в формате - name: Toyota, price: 20000')
                filter = input()
                flag = exeption(filter)
                if flag == 1:
                    print('Некорректный ввод данных')
                    break
                else:
                    data = {}
                    for item in filter.split(','):
                        param = item.split(':')
                        data.update({param[0].lstrip(): param[-1].lstrip()})
                    manager.update_vehicle(id, data)
                    break


        if x == 6:
            print('Введите id авто, которое хотите удалить')
            id = int(input())
            manager.delete_vehicle(id)


        if x == 7:
            print('Введите id авто, для которых нужно рассчитать расстояние в формате id, id')
            ids = input()
            manager.get_distance(int(ids.split(',')[0]), int(ids.split(',')[-1].lstrip()))


        if x == 8:
            print('Введите id авто')
            id = int(input())
            manager.get_nearest_vehicle(id)


        if x == 9:
            break

    


def main():
    manager = VehicleManager('https://test.tspb.su/test-task')
    control(manager)




if __name__ == '__main__':
    main()