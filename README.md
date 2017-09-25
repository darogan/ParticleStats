# ParticleStats #
     ____            _   _      _      ____  _        _                   
    |  _ \ __ _ _ __| |_(_) ___| | ___/ ___|| |_ __ _| |_ ___             
    | |_) / _` | '__| __| |/ __| |/ _ \___ \| __/ _` | __/ __|            
    |  __/ (_| | |  | |_| | (__| |  __/___) | || (_| | |_\__ \            
    |_|   \__,_|_|   \__|_|\___|_|\___|____/ \__\__,_|\__|___/            

__Open source software for the analysis of particle motility and cytoskelteal polarity__

ParticleStats was created by Russell Hamilton ([Centre for Trophoblast Research, University of Cambridge](http://www.trophoblast.cam.ac.uk)) and Ilan Davis ([Department of Biochemistry, University of Oxford](http://www.bioch.ox.ac.uk/research/davis)) and in collaboration with the [Micron Advanced Imaging Facility](http://www.micron.ox.ac.uk).

##### Project Page #####

http://www.ParticleStats.com                                

##### Citation: #####

Hamilton, R.S. et al (2010) Nucl. Acids Res. Web Server Edition       
http://dx.doi.org/10.1093/nar/gkq542

##### Abstract #####

The study of dynamic cellular processes in living cells is central to biology and is particularly powerful when the motility characteristics of individual objects within cells can be determined and analysed statistically. However, commercial programs only offer a very limited range of inflexible analysis modules and there are currently no open source programs for extensive analysis of particle motility. Here, we describe ParticleStats (www.ParticleStats.com), a web server and open source programs, which input the X,Y co-ordinate positions of objects in time, and outputs novel analyses, graphical plots and statistics for motile objects. ParticleStats comprises three separate analysis programs. Firstly ParticleStats:Directionality, for the global analysis of polarity, for example microtubule plus end growth in Drosophila oocytes. Secondly, ParticleStats:Compare for the analysis of saltatory movement in terms of runs and pauses. This can be applied to chromosome segregation and molecular motor based movements. Thirdly, ParticleStats:Kymographs for the analysis of kymograph images, for example as applied to separation of chromosomes in mitosis. These analyses have provided key insights into molecular mechanisms that are not possible from qualitative analysis alone and are widely applicable to many other cell biology problems.

##### Command Line Version #####
ParticleStats depends on several external packages to run, to simpify the installation there is a Docker version requiring only Docker to be pre-installed, and the ParticleStats repository to be cloned. The Docker version compiles all the required packages automatically.

For the command line version, once the dependencies are met, ParticleStats can be installed and run as follows.

    git clone https://github.com/darogan/ParticleStats

    cd ParticleStats

The three main tools, plus basic usage are:

    ParticleStats_Directionality.py --help

    ParticleStats_Compare.py --help

    ParticleStats_Kymographs.py --help

##### Docker Version #####

Download and install [Docker](https://docs.docker.com/engine/installation/) and then follow the steps below:

1. `git clone https://github.com/darogan/ParticleStats`

2. `cd ParticleStats`

3. `docker build -t particlestats_docker .`

4. `docker run -it particlestats_docker`

A Docker Hub version is planned to further similify the installation and usage of the Docker Version of ParticleStats.


##### To Do #####
1. Shared directories for user data
2. Markdown version of documentation
3. Add functionality for zebra fish behavioral studies
4. Docker Hub Version

##### GNU License #####

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or        (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.                                

You should have received a copy of the GNU General Public License along with this program.  If not, see http://www.gnu.org/licenses/

This software is still being developed so beware of bugs and feel free to suggest features
