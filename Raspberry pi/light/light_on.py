import subprocess

colors = {
	'BLUE': 'pigs p 18 255',
	'RED': 'pigs p 23 255',
	'GREEN': '\'pigs\', \'p\', \'24\', \'255\''
}

print(colors['BLUE'])
print(colors['RED'])
print(colors['GREEN'])
print('%s' % colors['GREEN'])

myVar='green'

if myVar == 'green':
	subprocess.call(['pigs', 'p', '24', '255'])

def turn_lights_off():
	subprocess.call(['pigs', 'p', '18', '0'])
	subprocess.call(['pigs', 'p', '23', '0'])
	subprocess.call(['pigs', 'p', '24', '0'])


if myVar == 'green':
	turn_lights_off()
