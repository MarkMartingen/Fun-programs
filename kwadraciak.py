'''
GUI in Polish. User inputs two quadratic equations and the program
solves the set of equations and graphs solution using matplotlib.
'''

import matplotlib.pyplot as plt
import numpy as np

def pobierz_wspolczynniki(tekst):
    wpowadzono = False
    while not wpowadzono:
        wsp = input("Podaj 3 współczynniki " + tekst + " równania kwadratowego rozdzielone spacją\n>" )
        try:
            a, b, c = [float(x) for x in wsp.split(sep=' ')]
            wpowadzono = True
        except:
            print("niepoprawnie wprowadzono współczynniki\n")
    return a,b,c

class Equation:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    def __str__(self):
        return 'y = {:.2f}x^2+{:.2f}x+{:.2f}'.format(self.a, self.b, self.c)

    def solve(self):
        if self.a == 0 and self.b == 0 and self.c == 0:
            return 'R'
        if self.a == 0 and self.b == 0 and self.c != 0:
            return None
        if self.a == 0 and self.b != 0:
            return (-self.c/self.b,)
        if self.a != 0:
            delta = self.b**2 - 4*self.a*self.c
            if delta<0:
                return None
            else:
                return ((-self.b + delta**0.5)/(2*self.a), (-self.b - delta**0.5)/(2*self.a))

    def merge(self, other):
        new_a = self.a - other.a
        new_b = self.b - other.b
        new_c = self.c - other.c
        return Equation(new_a, new_b, new_c)

    def make_plot(self, color='r'):
        x_values = np.arange(-100,100,0.1)
        y_values = self.a * x_values**2 + self.b * x_values + self.c
        return plt.plot(x_values,y_values, color)

    def yvalue(self, x):
        x = np.array(x)
        return tuple(self.a * x**2 + self.b * x + self.c)

if __name__ =='__main__':
    a,b,c = pobierz_wspolczynniki("pierwszego")
    Rownanie1 = Equation(a,b,c)

    a, b, c = pobierz_wspolczynniki("drugiego")
    Rownanie2 = Equation(a,b,c)

    Rownanie = Rownanie1.merge(Rownanie2)
    rozwiazanie = Rownanie.solve()

    if rozwiazanie is None:
        print('Podany układ równan kwadratowych nie ma rozwiązań')
        Rownanie1.make_plot(color = 'r')
        Rownanie2.make_plot(color='b')
        plt.title('Rozwiązanie układu równań kwadratowych')
        plt.show()

    elif rozwiazanie == 'R':
        print('Wszystkie liczby rzeczywiste są rozwiązaniem układu. Równania tożsamościowe.')
        Rownanie1.make_plot(color='r')
        Rownanie2.make_plot(color='b')
        plt.title('Rozwiązanie układu równań kwadratowych')
        plt.show()
    else:
        xmin = min(rozwiazanie) - 20
        xmax = max(rozwiazanie) + 20
        ymin = min(Rownanie1.yvalue(rozwiazanie)) - 20
        ymax = max(Rownanie1.yvalue(rozwiazanie)) + 20
        Rownanie1.make_plot(color='r')
        Rownanie2.make_plot(color='b')
        plt.xlim((xmin, xmax))
        plt.ylim((ymin, ymax))
        for i in range(len(rozwiazanie)):
            plt.annotate('({:.2f}, {:.2f})'.format(rozwiazanie[i], Rownanie1.yvalue(rozwiazanie)[i]),
                         xy=(rozwiazanie[i], Rownanie1.yvalue(rozwiazanie)[i]))
        plt.plot(rozwiazanie, Rownanie1.yvalue(rozwiazanie), ls="",  marker='^')
        plt.legend([Rownanie1.__str__(), Rownanie2.__str__()], loc='best')
        plt.title('Rozwiązanie układu równań kwadratowych')
        plt.show()