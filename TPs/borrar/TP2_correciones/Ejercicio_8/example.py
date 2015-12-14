from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('simple.ini')

print parser.get('nodo1', 'host')
print parser.get('nodo1', 'port')
print parser.get('nodo2', 'host')
print parser.get('nodo2', 'port')
