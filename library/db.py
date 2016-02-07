import yaml
from numpy import linspace, sqrt
from django.conf import settings
import os


class L:

    url = os.path.join(settings.STATIC_PATH, 'library/database/')
    library = os.path.join(url, 'library.yml')
   

    def __init__(self):
        self.N = 100
        self.x_data = None
        self.lib = self.read_data()

    def read_data(self, key=library):
        with open(key, 'r') as f:
            doc = yaml.load(f)
        return doc

    def shelves(self):

        table=[]
        doc = self.lib
        for item in doc:
            table.append([item['SHELF'], item['name']])

        return table

    def shelf(self, key):
        
        count_shelf = 0
        count_book = 0
        table=[]
        a = self.lib
        for item in a:
            count_shelf += 1
            if item['SHELF']==key:
                for book in item['content']:
                    if 'BOOK' in book:
                        count_book += 1
                        table.append(['%d%03d' % (count_shelf, count_book), book['BOOK'], book['name'][:50]])
                    else:
                        continue
                break
        
        if len(table)==0:
            return None
        else:
            return table

    def book(self, key):
        count_shelf = 0
        count_book = 0
        count_page = 0
        table=[]
        a = self.lib
        for shelf in a:
            count_shelf += 1
            count_book=0
            for book in shelf['content']:
                if 'BOOK' in book:
                    count_book += 1
                    if book['BOOK']==key:
                        for page in book['content']:
                            count_page += 1
                            table.append(['%d%03d%02d' % (count_shelf, count_book, count_page) , page['PAGE'], page['name'][:50]])
                            
        if len(table)==0:
            return None
        else:
            return table

    def page(self, key, url=url):
        try:
            key = int(key)
        except ValueError:
            return 'Please enter a valid ID'

        key = map(int, str(key))
        shelf_id = key[0]
        book_id = int(''.join(map(str, key[1:4])))
        page_id = int(''.join(map(str, key[4:])))
        count_shelf = 0
        count_book = 0
        count_page = 0
        table = []
        a = self.lib
        for shelf in a:
            count_shelf += 1
            if count_shelf == shelf_id:
                for book in shelf['content']:
                    if 'BOOK' in book:
                        count_book += 1
                        if count_book == book_id:
                            for page in book['content']:
                                count_page += 1
                                if count_page == page_id:
                                    return  self.read_data('%s%s' % (url,page['path']))

    def search(self, keyword, deep=False):
        a = self.lib
        count_shelf = 0
        count_book = 0
        count_page = 0
        table = []
        for shelf in a:
            count_shelf += 1
            count_book = 0
            for book in shelf['content']:
                if 'BOOK' in book:
                    count_book += 1
                    count_page = 0
                    for page in book['content']:
                        if 'PAGE' in page:
                            count_page += 1
                            deep_check = ''
                            if deep:
                                try:
                                    deep_check = str(self.read_data('../refractiveindex/database/%s' % (page['path'])))
                                except:
                                    pass
                            check = '%s, %s, %s' % (page['PAGE'], page['path'], deep_check)
                            if keyword.lower() in check.lower():
                                table.append(['%d%03d%02d' % (count_shelf, count_book, count_page) , shelf['SHELF'], book['BOOK'], page['PAGE'], page['name'][:30]])
                            
        if len(table)==0 and deep:
            print '-----------'
            print 'No Results'
            print '-----------'
        elif len(table) == 0:
            self.search(keyword, deep=True)
        else:
            print tabulate(table,
                           headers=['ID', 'SHELF', 'BOOK', 'PAGE', 'DESCRIPTION'],
                           tablefmt='orgtbl')
        
    def data(self, key, flag=True):
        count = 0
        page = self.page(key)
        if flag:
            for item in page['DATA']:
                if item['type']=='tabulated k':
                    data = list(self.tbk(item['data']))
                    N = self.N
                    self.x_data = data[0]
                    self.N = len(data[0])
                    new_data = self.data(key,flag=False)
                    data.insert(1, list(new_data[1]))
                    self.N = N
                    self.x_data = None
                    return data

        for item in page['DATA']:
             if item['type'] == 'formula 1':
                 data = []
                 data = self.f1(item['coefficients'], item['range'])
             elif item['type'] == 'formula 2':
                 data = []
                 data = self.f2(item['coefficients'], item['range'])
             elif item['type'] == 'formula 3':
                 data = []
                 data = self.f3(item['coefficients'], item['range'])
             elif item['type'] == 'formula 4':
                 data = []
                 data = self.f4(item['coefficients'], item['range'])
             elif item['type'] == 'formula 5':
                 data = []
                 data = self.f5(item['coefficients'], item['range'])
             elif item['type'] == 'tabulated nk':
                 data = []
                 data = self.tbnk(item['data'])
             else:
                 return "Can't do this yet"
             return data

    def plot(self, key):
        data = self.data(key)
        fig = plt.figure(figsize=(8,6))
        ax = fig.add_subplot(111)
        ax.plot(data[0], data[1], 'o-', color='red')
        ax.set_ylabel(r"$n$")
        ax.set_xlabel(r"Wavelength, $\lambda$ ($\mu$m)")
        if len(data)>2:
            ax2 = ax.twinx()
            ax2.plot(data[0], data[2], 'o-', color='blue')
            ax2.set_ylabel(r"$\kappa$")
        plt.show()
        
                 

    def f1(self, coeffs, wlrange):
        coeffs = map(float, coeffs.split())
        wlrange = map(float, wlrange.split())
        if self.x_data:
            x = self.x_data
        else:
            x = linspace(wlrange[0], wlrange[1],self.N)
        n = []
        for i in range(0, self.N):
            sum = 0
            for j in range(1, len(coeffs)-1,2):
                sum += (coeffs[j]*x[i]**2)/(x[i]**2 - coeffs[j+1]**2)
            sum += coeffs[0]
            n.append(sqrt(sum+1))
        return x, n

    def f2(self, coeffs, wlrange):
        coeffs = map(float, coeffs.split())
        wlrange = map(float, wlrange.split())
        if self.x_data:
            x = self.x_data
        else:
            x = linspace(wlrange[0], wlrange[1],self.N)
        n = []
        for i in range(0, self.N):
            sum = 0
            for j in range(1, len(coeffs)-1,2):
                sum += (coeffs[j]*x[i]**2)/(x[i]**2 - coeffs[j+1])
            sum += coeffs[0]
            n.append(sqrt(sum+1))
        return x, n
    
    def f3(self, coeffs, wlrange):
        coeffs = map(float, coeffs.split())
        wlrange = map(float, wlrange.split())
        x = linspace(wlrange[0], wlrange[1], self.N)
        n = []
        for i in range(0, self.N):
            sum = 0
            for j in range(1, len(coeffs)-1,2):
                sum += coeffs[j]*x[i]**coeffs[j+1]
            sum += coeffs[0]
            n.append(sqrt(sum))
        return x, n
    
    def f4(self, coeffs, wlrange):
        coeffs = map(float, coeffs.split())
        wlrange = map(float, wlrange.split())
        x = linspace(wlrange[0], wlrange[1], self.N)
        n = []
        
        for i in range(0, self.N):
            sum = coeffs[0]
            for j in range(1,8,4):
                sum += (coeffs[j]*x[i]**coeffs[j+1])/(x[i]**2 - coeffs[j+2]**coeffs[j+3])
            if len(coeffs)>9:
                for k in range(9, len(coeffs)-1,2):
                    sum += coeffs[k]*x[i]**coeffs[k+1]
            n.append(sqrt(sqrt(sum**2)))
        return x, n

    def f5(self, coeffs, wlrange):
        coeffs = map(float, coeffs.split())
        wlrange = map(float, wlrange.split())
        if self.x_data:
            x = self.x_data
        else:
            x = linspace(wlrange[0], wlrange[1],self.N)
        n = []
        for i in range(0, self.N):
            sum = 0
            for j in range(1, len(coeffs)-1,2):
                sum += coeffs[j]*x[i]**coeffs[j+1]
            sum += coeffs[0]
            n.append(sum)
        return x, n
    

    def tbnk(self, data):
        data = data.split('\n')
        data.pop()
        data = [row.split(' ') for row in data]
        x = [float(row[0]) for row in data]
        n = [float(row[1]) for row in data]
        k = [float(row[2]) for row in data]

        return x, n, k

    def tbk(self, data):
        data = data.split('\n')
        data.pop()
        data = [row.split(' ') for row in data]
        x = [float(row[0]) for row in data]
        k = [float(row[1]) for row in data]

        return x, k
        
        
