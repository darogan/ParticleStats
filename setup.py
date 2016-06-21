###############################################################################
#        ____            _   _      _      ____  _        _                   #
#       |  _ \ __ _ _ __| |_(_) ___| | ___/ ___|| |_ __ _| |_ ___             #
#       | |_) / _` | '__| __| |/ __| |/ _ \___ \| __/ _` | __/ __|            #
#       |  __/ (_| | |  | |_| | (__| |  __/___) | || (_| | |_\__ \            #
#       |_|   \__,_|_|   \__|_|\___|_|\___|____/ \__\__,_|\__|___/            #
#                                                                             #
###############################################################################
#       ParticleStats: Open source software for the analysis of particle      #
#                      motility and cytoskelteal polarity                     #
#                                                                             #
#       Contact: Russell.Hamilton@bioch.ox.ac.uk                              #
#                http://www.ParticleStats.com                                 #
#                Department of Biochemistry, South Parks Road,                #
#                University of Oxford OX1 3QU                                 #
#       Copyright (C) 2009 Russell S. Hamilton                                #
###############################################################################
# GNU Licence Details:                                                        #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

from distutils.core import setup, Extension

module1 = Extension('ParticleStats_linRegressFit',
                    sources = ['ParticleStats_linRegressFit.c'])


setup(
	name = 'ParticleStats',
	version = '0.3',
	author = 'Russell Hamilton',
	author_email = 'Russell.Hamilton@bioch.ox.ac.uk',
	url = 'http://www.ParticleStats.com',
	description = 'ParticleStats: open source software for the analysis of particle motility',
	platforms = ["platform independent"],
	license = 'GPLv2',
	packages = ['ParticleStats'],
	#py_modules=[ "ParticleStats_Inputs.py", "ParticleStats_Maths.py", "ParticleStats_Outputs.py", "ParticleStats_Plots.py", "ParticleStats_RandomTrailGenerator.py", "ParticleStats_Vectors.py", "Test_Interactive_OSX_DivideUpLines.py", "Test_Interactive_OSX.py", "Test_Interactive.py" ],
	scripts=[ "scripts/ParticleStats_TrackCompare.py", "scripts/ParticleStats_Compare.py", "scripts/ParticleStats_Directionality.py", "scripts/ParticleStats_Kymographs.py", "scripts/ParticleStats_ROI.py" ],
	ext_modules = [module1],
	package_data={
		'ParticleStats': [
			 "data/*.xls",
			 "data/*.txt", ],
                     }
)
