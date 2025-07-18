class Employee:
 def __init__(self):
 
   self._project = "project_encapsulate"

class Company(Employee):
 def __init__(self, name, salary ):
  self.name = name
  self.__salary = salary
  Employee.__init__(self)
 def show_sal(self):
  print(f"{self.name} earns {self.__salary}")
 
 def show_proj(self):
  print(f"{self.name} is working on {self._project}")

emp = Company('jojo',20000)
emp.show_proj()
emp.show_sal()