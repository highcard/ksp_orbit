###### orbit.py - simple script that helped calculate distance & period values for 3 co-planar 
###### equidistant bodies orbiting a larger body in Kerbal Space program

import math
import datetime

"""

Global Constants

"""

pi = math.pi 					#mmmm... pi...

unit = {
	'name': '',					#Name of Body
	't': 's',						#Oribital Period in seconds (s)
	'mu': 'm^3 / s^2',	#Gravitational Parameter of body in a funky unit
	'm': 'kg',					#Mass in kilograms(kg)
	'r': 'm',						#Radius of body in meters (m)
	'a': 'm'						#Altitude of body's center of mass over parent (m)
}

kerbin = {
	'name': 'Kerbin',
	't': 6 * 3600.0,		# s
	'mu': 3.532e12, 		#m ** 3 / s ** 2
	'm': 5.292e22, 			#kg
	'r': 600000.0, 			#m
	'a': 1.3338240256e13, #m
	'children': ['Mun']
}

Mun = {
	'name': 'Mun',
	't': 6 * 3600.0,		# s
	'mu': 3.532e12, 		#m ** 3 / s ** 2
	'm': 5.292e22, 			#kg
	'r': 600000.0, 			#m
	'a': 1.3338240256e13, #m
	'parent': 'Kerbin'
}

kerbol = {
	'name': 'Kerbol',
	'r': 261600000
}

"""

Orbit & Utility Calculations given raw inputs

"""

def calc_period(alt, r, mu):
	"""Calculates the period of an orbiting body in seconds from altituide, radius of planet and mu"""
	t = 2 * pi * ((((alt + r) ** 3) / mu) ** (1/2.0))
	return t

def s_maj_axis(t, mu):
	"""Return the semi-major axis of an orbit given period & mu"""
	a = ((mu * (t ** 2))/(4 * pi ** 2)) ** (1/3.0)
	return a

def sat_dist(alt, r, ang):
	"""Returns distance between two orbiting bodies given altitude, radius of body, and angle betweens sats"""
	d = 2 * math.sin(math.radians(ang/2)) * (alt + r)
	return d

def los_alt(alt, r, ang):
	"""Calculates altitude of LOS between orbiting bodies over parent"""
	h = (math.cos(math.radians(ang/2)) * (alt + r)) - r
	return h

def polar_max_alt(alt, r, max_range):
	"""Calculates maximum alt above pole for signal range of equatorial satelite"""
	if max_range < alt + r:
		return False
	else:
		assert max_range >= (alt + r), \
			"Maximum Range must be greater than sum of altutitude and radius of body"
		h = (max_range ** 2 - (alt + r) ** 2) ** (1/2.0) - r
	return h

def calc_shadow_max_alt(r_body, alt_body, r_sun):
	"""Calculates max altitude shadow space caused by body blocking view of parent"""
	d = alt_body + r_sun
	ratio = r_body / r_sun
	dark_axis = (ratio * d) / (1.0 - ratio)
	dark_alt = dark_axis - r_body
	return dark_alt

def calc_angle_coverage(alt, body):
	"""calculates the angle that an object covers when viewed from distance."""
	th = math.degrees(math.atan(body['r'] / (body['r'] + alt)))
	return th

def calc_angle_ratio(alt, body, parent):
	"""compares ratio of body's apparent size to parent's apparent size when viewed from alt over body"""
	b_view = calc_angle_coverage(alt + body['r'], kerbin)
	p_view = calc_angle_coverage(alt + body['r'] + body['a'] + parent['r'], kerbol)
	return b_view / p_view

"""

Unit Calculations

"""

def m_to_km(n):
	"""Converts Meters to Kilometers"""
	return n / 1000.0


"""

Calculate values based on body

"""

def sync_axis(b):
	"""Returns the semi-major axis of the synchronous orbit of the given body"""
	return s_maj_axis(b['t'], b['mu'])

def sync_alt(b):
	"""Return the altitude of a geosynchronous orbit of a given body"""
	return sync_axis(b) - b['r']

"""

Display utility functions

"""

def dspValue(l, v, u):
	"""Returns a human-friendly string of the given label, value and unit"""
	print '\n%35s %10s %2s' % (l, v, u)

def print_body_stats(b):
	"""Prints stats of a body"""
	for i in b:
		print dspValue(i, b[i], unit[i])

def orbit_period(alt, body):
	"""Calculates the period of orbit around the body given the altitude of circular orbit over that body."""
	return datetime.timedelta(seconds=(calc_period(alt, body['r'], body['mu'])))


"""

Controller

"""

def iso_from_period():
	while True:
		try:
			period = float(raw_input("Enter Target Period around Kerbin:"))
			break
		except ValueError:
			print "Invalid entry. Try again..."
	orbit_alt = s_maj_axis(period * 3600.0, kerbin['mu']) - kerbin['r']

	dspValue('Orbital Period', orbit_period(orbit_alt, kerbin), "")

	dspValue('Target Orbit', m_to_km(orbit_alt), 'km')

	dspValue('Distance between bodies', m_to_km(sat_dist(orbit_alt, kerbin['r'], 60.0)), 'km')

	dspValue('Height of Direct LOS over Horizon', m_to_km(los_alt(orbit_alt, kerbin['r'], 60.0)), 'km')

	dspValue('Signal Range alt over poles', m_to_km(polar_max_alt(orbit_alt, kerbin['r'], 2.5e6)), 'km')



"""

Test Printing to Console

"""

iso_from_period()

# print m_to_km(calc_shadow_max_alt(kerbin['r'], kerbin['a'], kerbol['r']))