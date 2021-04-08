#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
class Building(object):
    def __init__(self):
        self.num_of_floors = input("input num_of_floors:")
        while(self.num_of_floors.isdigit()==False):
            print("Wrong Input!!!")
            self.num_of_floors = input("input num_of_floors:")
            if(self.num_of_floors.isdigit()):
                break
                
        self.nc = input("input num_of_customers:")
        while(self.nc.isdigit()==False):
            print("Wrong Input!!!")
            self.nc = input("input num_of_customers:")
            if(self.nc.isdigit()):
                break
        self.e = Elevator(int(self.num_of_floors))
        self.customer_list = []
        for i in range(int(self.nc)):
            c = Customer(i+1, int(self.num_of_floors))
            self.customer_list.append(c)
        print("\r")
        print("\r")
    def check(self):
        for c in self.customer_list:
            if c.finished == False:
                return False
            else:
                continue
        return True

    def run(self):
        while(True):
            if(self.check()==False):
                for c in self.customer_list:
                    if c.in_elevator == False and c.finished == False and c.cur_floor == self.e.cur_floor:
                        self.e.register_customer(c)
                for c in self.e.register_list[:]:
                    if c.in_elevator == True and c.finished == False and c.dst_floor == self.e.cur_floor:
                        self.e.cancel_customer(c)  
                self.output()
                print("->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->")
                print("\r")  
                if(self.check()==False):
                    self.e.move()
            elif(self.check()==True):
                print("\r")
                print("All Customers Arrived at Destination")
                break
            

    def output(self):
        print('\r')
        print("Elevator's Current Floor :", self.e.cur_floor, "Elevator's direction:", self.e.direction)
        print("Customers: ")
        for c in self.customer_list:
            print("            Customer %s  current floor: %s" % (c.ID, c.cur_floor), "       destination floor : %s " % (c.dst_floor),'\n',"                       in Elevator : %s"%(c.in_elevator), "     is Finished : %s" %(c.finished))
        print("\r")
        
class Elevator(object):
    
    def __init__(self, num_of_floors):
        self.num_of_floors = num_of_floors
        self.cur_floor = random.randint(1,int(self.num_of_floors))
        self.direction = "up"
        if(self.cur_floor==self.num_of_floors):
            self.direction = "down"
        self.register_list = []
        

    def move(self):
        if self.cur_floor == self.num_of_floors:
            self.direction = 'down'
            print("The Elevator is on the Top Floor Now")
        if self.cur_floor == 1:
            self.direction = 'up'
            print("The Elevator is on the Bottom Floor Now")
        if self.direction == 'up':
            self.cur_floor += 1
            print("Elevator : %s => %s" %(self.cur_floor-1, self.cur_floor))
        elif self.direction == 'down':
            self.cur_floor -= 1
            print("Elevator : %s => %s" %(self.cur_floor+1, self.cur_floor))

    def register_customer(self, customer):
        if self.cur_floor == customer.cur_floor:
            print("Customer %s"%(customer.ID),"->Elevator")
            customer.in_elevator = True
            self.register_list.append(customer)
    

    def cancel_customer(self, customer):
        if self.cur_floor == customer.dst_floor:
            print("Customer %s"%(customer.ID),"->Destination Floor")
            self.register_list.remove(customer)
            customer.in_elevator = False
            customer.finished = True

class Customer(object):
    def __init__(self, ID, num_of_floors):
        self.ID = ID
        self.cur_floor = random.randint(1,num_of_floors)
        self.dst_floor = random.randint(1,num_of_floors)
        while self.cur_floor==self.dst_floor:
            self.cur_floor = random.randint(1,num_of_floors)
            self.dst_floor = random.randint(1,num_of_floors)
        self.in_elevator = False
        self.finished = False

    def __str__(self):
        return "Customer " + str(self.ID)

test = Building()
test.run()


# In[ ]:




