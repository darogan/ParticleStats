
     ____            _   _      _      ____  _        _                   
    |  _ \ __ _ _ __| |_(_) ___| | ___/ ___|| |_ __ _| |_ ___             
    | |_) / _` | '__| __| |/ __| |/ _ \___ \| __/ _` | __/ __|            
    |  __/ (_| | |  | |_| | (__| |  __/___) | || (_| | |_\__ \            
    |_|   \__,_|_|   \__|_|\___|_|\___|____/ \__\__,_|\__|___/            

# ParticleStats #
__Open source software for the analysis of particle motility and cytoskelteal polarity__

ParticleStats was originally created by Russell Hamilton ([Centre for Trophoblast Research, University of Cambridge](http://www.trophoblast.cam.ac.uk)) and Ilan Davis ([Department of Biochemistry, University of Oxford](http://www.bioch.ox.ac.uk/research/davis)) and in collaboration with the [Micron Advanced Imaging Facility](http://www.micron.ox.ac.uk).

ParticleStats2.0 is currently being developed by Russell Hamilton ([Dept Genetics, University of Cambridge](http://www.genetics.cam.ac.uk)) in collaboration with Anne Ferguson-Smith ([Dept Genetics, University of Cambridge](https://www.gen.cam.ac.uk/research-groups/research-groups/ferguson-smith)) and Ilan Davis ([Department of Biochemistry, University of Oxford](http://www.bioch.ox.ac.uk/research/davis)) with new features for comparing tracking data, cell migration and behavioural assays




##### Project Page #####

http://www.ParticleStats.com  

If you have ideas or request for new features please submit them as issues on the GitHub site.                              

##### Citation: #####

Hamilton, R.S., Parton, R.M., Oliveira, R.A., Ball, G., Vendra, G., Nasmyth, K. & Davis, I. (2010) ParticleStats: Open source software for the analysis of intracellular particle motility and cytoskeletal polarity. Nucleic Acids Research (Web Server Edition) [[DOI](http://dx.doi.org/10.1093/nar/gkq542)]

##### Abstract #####

The study of dynamic cellular processes in living cells is central to biology and is particularly powerful when the motility characteristics of individual objects within cells can be determined and analysed statistically. However, commercial programs only offer a very limited range of inflexible analysis modules and there are currently no open source programs for extensive analysis of particle motility. Here, we describe ParticleStats (www.ParticleStats.com), a web server and open source programs, which input the X,Y co-ordinate positions of objects in time, and outputs novel analyses, graphical plots and statistics for motile objects. ParticleStats comprises three separate analysis programs. Firstly ParticleStats:Directionality, for the global analysis of polarity, for example microtubule plus end growth in Drosophila oocytes. Secondly, ParticleStats:Compare for the analysis of saltatory movement in terms of runs and pauses. This can be applied to chromosome segregation and molecular motor based movements. Thirdly, ParticleStats:Kymographs for the analysis of kymograph images, for example as applied to separation of chromosomes in mitosis. These analyses have provided key insights into molecular mechanisms that are not possible from qualitative analysis alone and are widely applicable to many other cell biology problems.

##### ParticleStats::Modules #####

| Module | Availability | Description |  
| ------ | ------------ | ----------- |
| `ParticleStats::Compare` | Since 1.0 | The dynamics of particle movement, such as in the case of motor driven transport, can be explored through the calculation of runs and pauses in the movement |
| `ParticleStats::Directionality` | Since v1.0 | The directionality of a set of tracked particles is determined using directional statistics. The wind-maps are a novel way of visualising bias in the travel direction of particles. Further evidence is provided with rose diagrams and radial histograms |
| `ParticleStats::Kymographs` | Since v1.0 | Analysis of the dynamics of separating kinetochores as displayed in kymographs |
| `ParticleStats::TrackAlign` | New for v2.0 | Analysis and comparison of tracking data |
| `ParticleStats::Behavioural` | New for v2.0 | Analysis of the dynamics of zebrafish movement in behavioural tracking experiments |
| `ParticleStats::Cell` | Planned | Analysis of migrating cells |


##### Command Line Version #####
ParticleStats depends on several external packages to run, to simpify the installation there is a Docker version (see below).

The command line version has been tested on Linux and MacOSX

| Dependency | Source |
| ---------- | ------ |
| R          | https://cran.r-project.org       |
| inkscape   | https://inkscape.org |

| Python Modules | Source |
| -------------- | ------ |
| pillow, scipy, boot, xlwt, matplotlib, rpy2, xlrd | https://pypi.python.org |

| R libraries | Source |
| ----------- | ------ |
| CircStats   |  https://cran.r-project.org/src/contrib/CircStats_0.2-4.tar.gz |


For the command line version, once the dependencies are met, ParticleStats can be installed and run as follows.

    git clone https://github.com/darogan/ParticleStats

    cd ParticleStats

The three main tools, plus basic usage are:

    ParticleStats_Directionality.py --help

    ParticleStats_Compare.py --help

    ParticleStats_Kymographs.py --help

##### Docker Version #####
The Docker version of ParticleStats requires only Docker to be pre-installed. And the ParticleStats repository to be cloned - actually the only requirement from the ParticleStats repositoru is the `Dockerfile`. The Docker version compiles all the required packages automatically.
Download and install [Docker](https://docs.docker.com/engine/installation/) and then follow the steps below:

1. `git clone https://github.com/darogan/ParticleStats`

2. `cd ParticleStats`

3. `docker build -t particlestats_docker .`

4. `docker run -it particlestats_docker`

A Docker Hub version is planned to further similify the installation and usage of the Docker Version of ParticleStats.

##### Publications Citing ParticleStats #####

* Oliveira, R.A., Hamilton, R.S., Pauli, A., Davis, I., Nasmyth, K. (2010) Cohesin cleavage and Cdk inhibition trigger formation of daughter nuclei. Nature Cell Biology, 12, 185-192 [[DOI](http://dx.doi.org/10.1038/ncb2018)]

* Vendra, G., Hamilton, R.S. & Davis, I. (2007) Dynactin suppresses the retrograde movement of apically localized mRNA in Drosophila blastoderm embryos. RNA, 13, 1-8. [[DOI](http://dx.doi.org/10.1261/rna.509007)]

* Parton, R.M., Hamilton, R.S., Ball, G., Yang, L., Cullen, F., Lu, W., Ohkura, H. & Davis, I. (2011) A PAR-1 dependent orientation gradient of dynamic microtubules establishes cell polarity in the Drosophila oocyte. Journal of Cell Biology, 194, 121-135. [[DOI](http://dx.doi.org/10.1083/jcb.201103160)]

* Hartswood. E., Brodie, J., Vendra, G., Davis, I. and Finnegan. D.J. (2012) RNA:RNA interaction can enhance RNA localization in Drosophila oocytes. RNA, 18, 1-9. [[DOI](http://dx.doi.org/10.1261/rna.026674.111)]

##### GNU License #####

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or        (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.                                

You should have received a copy of the GNU General Public License along with this program.  If not, see http://www.gnu.org/licenses/

This software is still being developed so beware of bugs and feel free to suggest features
