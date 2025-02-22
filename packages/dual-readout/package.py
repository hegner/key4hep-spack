# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkg.k4.key4hep_stack import Key4hepPackage


class DualReadout(CMakePackage, Key4hepPackage):
    """Repository for GEANT4 simulation & analysis of the dual-readout calorimeter """

    url      = "https://github.com/HEP-FCC/dual-readout/archive/v0.0.2.tar.gz"
    homepage = "https://github.com/HEP-FCC/dual-readout"
    git      = "https://github.com/HEP-FCC/dual-readout.git"

    maintainers = ['vvolkl', 'SanghyunKo']

    version('master', branch='master') 
    version("0.1.1", sha256="8d856b47b0b834ac0a53920434da210639c55a1ef375f7e0341731ad14a25318")
    version('0.1.0', sha256='f4b9387ccae0d4d364b1340eb116c5b4b93a6bc74c896fcd221619ddec31d5f6')

    # backport fix for build error with clang
    patch('https://github.com/HEP-FCC/dual-readout/commit/31c01d2f7867f6c44da63fdc7db69e30c4bb34bb.diff', when='@0.1.0',
          sha256='0fc3b0e77d52e1dec72a0dae73f15689720b28298deea1992301e8c41c80271c')


    depends_on('dd4hep')
    depends_on('edm4hep@0.4.1:')
    depends_on('podio@0.14.1:')
    depends_on('podio@0.15:', when='@0.1.1:')
    depends_on('py-jinja2', type=('build'))
    depends_on('py-pyyaml', type=('build'))
    depends_on('hepmc3+rootio')
    depends_on('fastjet')
    depends_on('root+fftw')
    depends_on('pythia8')
    depends_on('hsf-cmaketools')
    depends_on('k4fwcore')
    depends_on('k4fwcore@1.0pre14:')
    depends_on('simsipm')

    def cmake_args(self):
        args = []
        # C++ Standard
        args.append('-DCMAKE_CXX_STANDARD=%s' % self.spec['root'].variants['cxxstd'].value)
        if self.spec.satisfies('^gaudi@:34.99'):
          args.append('-DHOST_BINARY_TAG=x86_64-linux-gcc9-opt')
        return args

    def setup_build_environment(self, env):
        env.set('PYTHIA8_ROOT_DIR', self.spec["pythia8"].prefix)
        
    def setup_run_environment(self, env):
        env.set('DUALREADOUT', self.spec.prefix)
